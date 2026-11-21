from __future__ import annotations

from pathlib import Path

import httpx
import pytest
from asgi_lifespan import LifespanManager

from app.contract.widgets import WIDGET_KINDS
from app.main import create_app
from app.settings import Settings

pytestmark = pytest.mark.anyio


async def test_sample_trip_endpoint(client: httpx.AsyncClient) -> None:
    response = await client.get("/v1/sample/trip")
    assert response.status_code == 200
    assert response.json()["is_sample"] is True


async def test_sample_widgets_cover_all_kinds(client: httpx.AsyncClient) -> None:
    response = await client.get("/v1/sample/widgets")
    assert response.status_code == 200
    assert {item["kind"] for item in response.json()} == set(WIDGET_KINDS)
    assert len(WIDGET_KINDS) == 20


@pytest.mark.parametrize("route", ["/v1/sample/trip", "/v1/sample/widgets"])
async def test_missing_samples_folder_answers_503(route: str, tmp_path: Path) -> None:
    """Expected failure before the fix: the trip route gave a bare 500, the widgets route 200 []."""
    app = create_app(Settings(_env_file=None, app_env="test", samples_dir=tmp_path))
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get(route)
    assert response.status_code == 503
    assert response.headers["content-type"].startswith("application/problem+json")
    assert response.json()["detail"] == "Sample data is not available."
    assert response.headers["retry-after"] == "300"  # fastapi.md: Retry-After on a 503


async def test_routes_use_the_folder_from_the_apps_settings(tmp_path: Path) -> None:
    import shutil

    from app.settings import DEFAULT_SAMPLES_DIR

    shutil.copytree(DEFAULT_SAMPLES_DIR, tmp_path / "s")
    (tmp_path / "s" / "trip" / "sample-lisbon.json").unlink()
    app = create_app(Settings(_env_file=None, app_env="test", samples_dir=tmp_path / "s"))
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            assert (await client.get("/v1/sample/trip")).status_code == 503
            assert (await client.get("/v1/sample/widgets")).status_code == 200
