"""Query spans for the database, switched on only when traces are exported.

FastAPI's own telemetry (see main.telemetry_config) traces each request. This adds one span per
SQL statement, as a child of the request's span, through OpenTelemetry's psycopg instrumentation.
It works on the driver, so it covers SQLAlchemy's async engine (the SQLAlchemy instrumentation does
not support SQLAlchemy 2.1 yet). Nothing is hooked, and nothing imported, unless traces are
exported. Call it before the engine opens its first connection.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


def export_requested(env: Mapping[str, str]) -> bool:
    """True when FastAPI will export traces: its auto-configure is on and an OTLP endpoint is set
    (the two things FastAPI's own telemetry needs; app_env "test" is ruled out by the caller)."""
    endpoint = env.get("OTEL_EXPORTER_OTLP_ENDPOINT") or env.get(
        "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"
    )
    return env.get("FASTAPI_OTEL_AUTO_CONFIGURE", "").lower() == "true" and bool(endpoint)


def instrument_database(tracer_provider: Any | None = None) -> Callable[[], None]:
    """Trace the database queries; returns the function that switches the tracing off again."""
    from opentelemetry.instrumentation.psycopg import PsycopgInstrumentor

    instrumentor = PsycopgInstrumentor()
    instrumentor.instrument(tracer_provider=tracer_provider)

    def switch_off() -> None:
        instrumentor.uninstrument()

    return switch_off
