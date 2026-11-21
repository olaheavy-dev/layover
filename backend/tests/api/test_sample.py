from __future__ import annotations

import httpx
import pytest

from app.contract.widgets import WIDGET_KINDS

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
