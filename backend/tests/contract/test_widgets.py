"""Tests for the 20 widget models."""

from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

from app.contract.widgets import (
    WIDGET_KINDS,
    WIDGET_STATES,
    AdviceCard,
    BookingApproval,
    BriefSummary,
    FareCard,
    Widget,
)

EXPECTED_KINDS = (
    "brief_summary",
    "comparison_table",
    "fare_card",
    "climate_chart",
    "sea_conditions",
    "daylight",
    "money",
    "advice_card",
    "place_intro",
    "map",
    "itinerary_day",
    "hotel_list",
    "cost_estimate",
    "booking_approval",
    "web_results",
    "not_known",
    "public_holidays",
    "time_difference",
    "fare_list",
    "transport_route",
)

SOURCE = {"status": "live", "source": "Open-Meteo"}
FARE = {
    "price": {"amount_minor": 9600, "currency": "GBP"},
    "captured_at": datetime(2026, 11, 18, tzinfo=UTC),
    "source": {"status": "live", "source": "Travelpayouts"},
}

# The smallest valid payload per kind. Fields without a default are the required ones.
MINIMAL: dict[str, dict[str, Any]] = {
    "brief_summary": {},
    "comparison_table": {},
    "fare_card": {"origin": "MAN", "destination": "LIS", "month": "2027-05"},
    "climate_chart": {"place": "Lisbon"},
    "sea_conditions": {"place": "Lisbon"},
    "daylight": {"place": "Lisbon"},
    "money": {},
    "advice_card": {
        "place": "Portugal",
        "fcdo_url": "https://www.gov.uk/foreign-travel-advice/portugal",
    },
    "place_intro": {"place": "Lisbon"},
    "map": {},
    "itinerary_day": {"day_number": 1},
    "hotel_list": {"place": "Lisbon"},
    "cost_estimate": {"place": "Lisbon"},
    "booking_approval": {"sandbox": True},
    "web_results": {},
    "not_known": {},
    "public_holidays": {"place": "Lisbon"},
    "time_difference": {"place": "Lisbon"},
    "fare_list": {"origin": "BRS", "month": "2027-03"},
    "transport_route": {"origin": "Paddington", "destination": "Heathrow"},
}


def _payload(kind: str) -> dict[str, Any]:
    state = "not_known" if kind == "not_known" else "loading"
    extra = {"missing": "no source has it"} if kind == "not_known" else {}
    return {"kind": kind, "state": state, "sources": [], **extra, **MINIMAL[kind]}


def test_twenty_kinds() -> None:
    assert len(WIDGET_KINDS) == 20
    assert WIDGET_KINDS == EXPECTED_KINDS


@pytest.mark.parametrize("kind", EXPECTED_KINDS)
def test_discriminator_routes_each_kind(kind: str) -> None:
    widget = TypeAdapter(Widget).validate_python(_payload(kind))
    assert widget.kind == kind
    assert type(widget).__name__ == "".join(p.capitalize() for p in kind.split("_"))


def test_advice_card_has_no_safety_field() -> None:
    assert not [name for name in AdviceCard.model_fields if "safe" in name.lower()]


def test_no_widget_field_names_safety() -> None:
    adapter = TypeAdapter(Widget)
    for kind in WIDGET_KINDS:
        cls = type(adapter.validate_python(_payload(kind)))
        assert not [n for n in cls.model_fields if "safe" in n.lower()], kind


def test_booking_approval_is_always_sandbox() -> None:
    with pytest.raises(ValidationError):
        BookingApproval(kind="booking_approval", state="loading", sources=[], sandbox=False)


def test_no_source_kinds() -> None:
    BriefSummary(kind="brief_summary", state="filled", sources=[])
    with pytest.raises(ValidationError):
        FareCard(
            kind="fare_card",
            state="filled",
            sources=[],
            origin="MAN",
            destination="LIS",
            month="2027-05",
        )


def test_states_cover_brief() -> None:
    """Every kind has states; all but `not_known` include `loading`.

    The brief's "Widget states" table says `not_known` has no Loading state (Layover writes it
    without an outside call), so it is the one kind without `loading`.
    """
    assert set(WIDGET_STATES) == set(WIDGET_KINDS)
    for kind, states in WIDGET_STATES.items():
        assert len(states) == len(set(states)), kind
        if kind == "not_known":
            assert "loading" not in states
        else:
            assert "loading" in states, kind
            assert "filled" in states, kind


def test_fare_has_capture_time() -> None:
    no_time = {k: v for k, v in FARE.items() if k != "captured_at"}
    with pytest.raises(ValidationError):
        FareCard(
            kind="fare_card",
            state="filled",
            sources=[],
            origin="MAN",
            destination="LIS",
            month="2027-05",
            fare=no_time,
        )


def test_filled_fare_card_validates_with_a_source() -> None:
    card = FareCard.model_validate(
        {
            "kind": "fare_card",
            "state": "filled",
            "sources": [SOURCE],
            "origin": "MAN",
            "destination": "LIS",
            "month": "2027-05",
            "fare": FARE,
        }
    )
    assert card.fare is not None
    assert card.fare.price.amount_minor == 9600


def test_fare_list_must_be_sorted_lowest_first() -> None:
    def row(dest: str, minor: int) -> dict[str, Any]:
        return {
            "destination": dest,
            "fare": {**FARE, "price": {"amount_minor": minor, "currency": "GBP"}},
        }

    base = {
        "kind": "fare_list",
        "state": "filled",
        "sources": [SOURCE],
        "origin": "BRS",
        "month": "2027-03",
    }
    TypeAdapter(Widget).validate_python({**base, "rows": [row("FAO", 5900), row("VLC", 6400)]})
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**base, "rows": [row("VLC", 6400), row("FAO", 5900)]})


def test_time_difference_works_out_by_hand() -> None:
    # Valletta: CEST is UTC+2 (120 min), UK BST is UTC+1 (60 min); 120 - 60 = 60 (sample-data.md).
    base = {"kind": "time_difference", "state": "filled", "sources": [SOURCE], "place": "Valletta"}
    ok = {**base, "uk_offset_minutes": 60, "place_offset_minutes": 120, "difference_minutes": 60}
    TypeAdapter(Widget).validate_python(ok)
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**ok, "difference_minutes": 120})


def test_transport_total_is_sum_of_legs() -> None:
    # 5 + 32 + 6 = 43 minutes (sample-data.md).
    legs = [
        {"mode": "walk", "minutes": 5},
        {"mode": "Elizabeth line", "minutes": 32},
        {"mode": "walk", "minutes": 6},
    ]
    base = {**_payload("transport_route"), "state": "filled", "sources": [SOURCE], "legs": legs}
    TypeAdapter(Widget).validate_python({**base, "total_minutes": 43})
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**base, "total_minutes": 44})


def test_cost_line_without_amount_needs_a_reason() -> None:
    base = {**_payload("cost_estimate"), "state": "filled", "sources": [SOURCE]}
    TypeAdapter(Widget).validate_python({**base, "stay": {"missing": "too few priced listings"}})
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**base, "stay": {}})


def test_not_known_kind_is_always_not_known() -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python(
            {"kind": "not_known", "state": "filled", "sources": [], "missing": "local bus fares"}
        )
