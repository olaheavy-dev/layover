"""OpenTelemetry request spans from FastAPI's native telemetry: requests are traced, health probes
are not."""

from __future__ import annotations

import httpx
import pytest
from asgi_lifespan import LifespanManager
from opentelemetry import trace
from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from pydantic import SecretStr

from app import db
from app.main import create_app
from app.settings import Settings
from app.tracing import export_requested

pytestmark = pytest.mark.anyio


async def test_requests_are_traced_but_health_probes_are_not() -> None:
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    app = create_app(
        Settings(_env_file=None, app_env="test"), telemetry={"tracer_provider": provider}
    )

    @app.get("/ping")
    async def ping() -> str:
        return "pong"

    async with LifespanManager(app) as manager:
        transport = httpx.ASGITransport(app=manager.app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            await client.get("/health/live")
            await client.get("/ping")
    names = {span.name for span in exporter.get_finished_spans()}
    assert "GET /ping" in names
    assert not any("/health" in name for name in names)


async def test_no_export_without_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    """With no OTLP endpoint, startup sets up no exporter and traces no database queries."""
    monkeypatch.delenv("OTEL_EXPORTER_OTLP_ENDPOINT", raising=False)
    monkeypatch.delenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", raising=False)
    monkeypatch.setenv("FASTAPI_OTEL_AUTO_CONFIGURE", "true")
    before = trace.get_tracer_provider()
    app = create_app(Settings(_env_file=None, app_env="local"))
    async with LifespanManager(app):
        assert app.state.database_traced is False
        assert trace.get_tracer_provider() is before
        assert not PsycopgInstrumentor().is_instrumented_by_opentelemetry


def test_export_requested_only_with_an_endpoint() -> None:
    assert export_requested({}) is False
    assert export_requested({"OTEL_EXPORTER_OTLP_ENDPOINT": ""}) is False
    assert export_requested({"OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4318"}) is True
    assert export_requested({"OTEL_EXPORTER_OTLP_TRACES_ENDPOINT": "http://x/v1/traces"}) is True
    # Switching auto-configure on without an endpoint exports nothing, so nothing is traced.
    assert export_requested({"FASTAPI_OTEL_AUTO_CONFIGURE": "true"}) is False


async def test_database_queries_create_spans(database_url: str) -> None:
    """Once the instrumentation is on (a tracer provider is passed), a query through the app's
    engine is a span of its own, with the PostgreSQL system name."""
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    settings = Settings(_env_file=None, app_env="test", database_url=SecretStr(database_url))
    app = create_app(settings, telemetry={"tracer_provider": provider})
    async with LifespanManager(app):
        assert app.state.database_traced is True
        await db.ping(app.state.engine)
    spans = [s for s in exporter.get_finished_spans() if s.attributes]
    selects = [s for s in spans if s.attributes and s.attributes.get("db.system") == "postgresql"]
    assert any(s.name == "SELECT" for s in selects)
    assert not PsycopgInstrumentor().is_instrumented_by_opentelemetry
