"""Sample data for the website's widget gallery and for demos. Public and read only: nothing
here is real, and nothing is saved."""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.contract.samples import (
    SamplesUnavailable,
    SampleWidget,
    load_sample_trip,
    load_sample_widgets,
)
from app.contract.trip import Trip
from app.problems import Problem

router = APIRouter(prefix="/sample", tags=["sample"])

UNAVAILABLE = "Sample data is not available."


# Plain `def`: FastAPI runs these in a worker thread, and the first call reads files.
@router.get(
    "/trip",
    description="Returns the sample Lisbon trip. This is sample data, not a real trip.",
)
def sample_trip(request: Request) -> Trip:
    try:
        return load_sample_trip(request.app.state.settings.samples_dir)
    except SamplesUnavailable as exc:
        raise Problem(503, detail=UNAVAILABLE) from exc


@router.get(
    "/widgets",
    description=(
        "Returns every sample widget, one per kind and state. This is sample data, not real "
        "fares, prices or advice."
    ),
)
def sample_widgets(request: Request) -> list[SampleWidget]:
    try:
        return list(load_sample_widgets(request.app.state.settings.samples_dir))
    except SamplesUnavailable as exc:
        raise Problem(503, detail=UNAVAILABLE) from exc
