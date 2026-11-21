"""Tests for the trip model."""

import pytest
from pydantic import ValidationError

from app.contract.trip import ShareSettings, Trip
from app.contract.widgets import FareCard


def test_share_hides_budget_by_default() -> None:
    assert ShareSettings().include_budget_and_travellers is False


def test_trip_sections_optional() -> None:
    trip = Trip(trip_id="t1", is_sample=True, name="Empty trip", share=ShareSettings())
    assert trip.brief is None
    assert trip.days == []


def test_days_are_itinerary_days() -> None:
    card = FareCard(
        kind="fare_card",
        state="not_known",
        sources=[],
        missing="no fare data",
        origin="LON",
        destination="LIS",
        month="2027-05",
    )
    with pytest.raises(ValidationError):
        Trip(trip_id="t1", is_sample=True, name="Bad", share=ShareSettings(), days=[card])
