"""Sample data for the website's widget gallery and for demos. Public and read only: nothing
here is real, and nothing is saved."""

from __future__ import annotations

from fastapi import APIRouter

from app.contract.samples import SampleWidget, load_sample_trip, load_sample_widgets
from app.contract.trip import Trip

router = APIRouter(prefix="/sample", tags=["sample"])


@router.get(
    "/trip",
    description="Returns the sample Lisbon trip. This is sample data, not a real trip.",
)
async def sample_trip() -> Trip:
    return load_sample_trip()


@router.get(
    "/widgets",
    description=(
        "Returns every sample widget, one per kind and state. This is sample data, not real "
        "fares, prices or advice."
    ),
)
async def sample_widgets() -> list[SampleWidget]:
    return load_sample_widgets()
