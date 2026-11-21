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
CAPTURED = datetime(2026, 11, 18, tzinfo=UTC)
CACHED = {"status": "cached", "source": "Travelpayouts", "captured_at": CAPTURED}
FARE = {
    "price": {"amount_minor": 9600, "currency": "GBP"},
    "captured_at": CAPTURED,
    "source": CACHED,
}

# The smallest valid payload per kind. Fields without a default are the required ones.
MINIMAL: dict[str, dict[str, Any]] = {
    "brief_summary": {},
    "comparison_table": {},
    "fare_card": {"origin": "MAN", "destination": "LIS", "month": "2027-05"},
    "climate_chart": {"place": "Lisbon"},
    "sea_conditions": {"place": "Lisbon"},
    "daylight": {"place": "Lisbon", "dates_set": True},
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
    "time_difference": {"place": "Lisbon", "dates_set": True},
    "fare_list": {"origin": "BRS", "month": "2027-03"},
    "transport_route": {"origin": "Paddington", "destination": "Heathrow", "dates_set": True},
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
    """A fare without `captured_at` fails on that field, not on some other rule."""
    no_time = {k: v for k, v in FARE.items() if k != "captured_at"}
    with pytest.raises(ValidationError) as exc:
        FareCard(
            kind="fare_card",
            state="filled",
            sources=[CACHED],
            origin="MAN",
            destination="LIS",
            month="2027-05",
            fare=no_time,
        )
    assert [e["loc"] for e in exc.value.errors()] == [("fare", "captured_at")]


def test_fare_time_matches_its_label() -> None:
    other = {**CACHED, "captured_at": datetime(2026, 11, 1, tzinfo=UTC)}
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python(
            {
                **_payload("fare_card"),
                "state": "filled",
                "sources": [CACHED],
                "fare": {**FARE, "source": other},
            }
        )


def test_filled_fare_card_validates_with_a_source() -> None:
    card = FareCard.model_validate(
        {
            "kind": "fare_card",
            "state": "filled",
            "sources": [CACHED],
            "origin": "MAN",
            "destination": "LIS",
            "month": "2027-05",
            "fare": FARE,
        }
    )
    assert card.fare is not None
    assert card.fare.price.amount_minor == 9600


def test_fare_list_must_be_sorted_lowest_first() -> None:
    """Fares sort lowest first.

    Working: 5900 (Faro, 59 pounds) < 6400 (Valencia, 64 pounds), so [5900, 6400] is in order.
    Source: sample-data.md, "Widget gallery: proposed widgets", `fare_list` (made-up fares).
    """

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
    """The difference is the place offset minus the UK offset.

    Working: Valletta is CEST, UTC+2 = 120 minutes; the UK is BST, UTC+1 = 60 minutes;
    120 - 60 = 60 minutes ahead.
    Source: sample-data.md, "Widget gallery: proposed widgets", `time_difference`, Valletta.
    """
    base = {
        "kind": "time_difference",
        "state": "filled",
        "sources": [SOURCE],
        "place": "Valletta",
        "dates_set": False,
    }
    ok = {**base, "uk_offset_minutes": 60, "place_offset_minutes": 120, "difference_minutes": 60}
    TypeAdapter(Widget).validate_python(ok)
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**ok, "difference_minutes": 120})


def test_transport_total_is_sum_of_legs() -> None:
    """The total is the sum of the legs.

    Working: 5 + 32 + 6 = 43 minutes.
    Source: sample-data.md, "Widget gallery: proposed widgets", `transport_route` (made-up times).
    """
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


def test_time_difference_accepts_a_place_behind_the_uk() -> None:
    """A place behind the UK has a negative difference.

    Working: constructed example, a zone at UTC-1 (-60 minutes) against BST UTC+1 (60):
    -60 - 60 = -120 minutes, two hours behind.
    Source: constructed example, not from sample-data.md.
    """
    widget = TypeAdapter(Widget).validate_python(
        {
            "kind": "time_difference",
            "state": "filled",
            "sources": [SOURCE],
            "place": "Sample place",
            "dates_set": True,
            "uk_offset_minutes": 60,
            "place_offset_minutes": -60,
            "difference_minutes": -120,
        }
    )
    assert widget.difference_minutes == -120  # type: ignore[union-attr]


@pytest.mark.parametrize("kind", ["daylight", "time_difference", "transport_route"])
def test_dates_set_is_required(kind: str) -> None:
    payload = {k: v for k, v in _payload(kind).items() if k != "dates_set"}
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python(payload)


def _advice(**over: Any) -> dict[str, Any]:
    return {
        "kind": "advice_card",
        "state": "filled",
        "sources": [CACHED],
        "place": "Portugal",
        "fcdo_url": "https://www.gov.uk/foreign-travel-advice/portugal",
        **over,
    }


def test_filled_advice_card_needs_its_update_date() -> None:
    TypeAdapter(Widget).validate_python(_advice(updated_on="2026-11-12"))
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python(_advice())
    # error and not_known states keep the link and need no date
    TypeAdapter(Widget).validate_python(_advice(state="error"))


def test_comparison_weather_has_its_own_label_and_period() -> None:
    """Each card's weather carries a source label and its averages period."""
    weather = {
        "high_c": 22.0,
        "low_c": 14.0,
        "rainy_days": 5,
        "averages_period": "1991-2020",
        "source": SOURCE,
    }
    card = {"place": "Lisbon", "card_state": "ready"}
    base = {**_payload("comparison_table"), "state": "filled", "sources": [SOURCE]}
    TypeAdapter(Widget).validate_python({**base, "cards": [{**card, "weather": weather}]})
    no_period = {k: v for k, v in weather.items() if k != "averages_period"}
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**base, "cards": [{**card, "weather": no_period}]})
    no_label = {k: v for k, v in weather.items() if k != "source"}
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**base, "cards": [{**card, "weather": no_label}]})


def test_fare_list_search_links() -> None:
    url = "https://www.aviasales.com/search"
    base = {
        "kind": "fare_list",
        "state": "empty",
        "sources": [],
        "origin": "BRS",
        "month": "2027-03",
    }
    widget = TypeAdapter(Widget).validate_python(
        {
            **base,
            "search_url": url,
            "rows": [{"destination": "NAP", "missing": "no cached fare", "search_url": url}],
        }
    )
    assert str(widget.search_url) == url  # type: ignore[union-attr]


def _money(minor: int) -> dict[str, Any]:
    return {"amount_minor": minor, "currency": "GBP"}


def _estimate(exact: int, shown: int) -> dict[str, Any]:
    return {"exact": _money(exact), "shown": _money(shown), "is_estimate": True}


def _line(**over: Any) -> dict[str, Any]:
    return {"amount": _estimate(19200, 19000), "source": CACHED, **over}


def _cost(**over: Any) -> dict[str, Any]:
    return {**_payload("cost_estimate"), "state": "filled", "sources": [SOURCE], **over}


def test_cost_estimate_with_a_missing_line_must_be_partial() -> None:
    missing = {"missing": "no source has local bus fares"}
    TypeAdapter(Widget).validate_python(_cost(local_transport=missing, is_partial=True))
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python(_cost(local_transport=missing, is_partial=False))
    TypeAdapter(Widget).validate_python(_cost(flights=_line(), is_partial=False))


def test_comparison_card_with_a_missing_line_must_be_partial() -> None:
    base = {**_payload("comparison_table"), "state": "filled", "sources": [SOURCE]}
    card = {
        "place": "Valencia",
        "card_state": "ready",
        "stay": {"missing": "too few priced listings"},
    }
    TypeAdapter(Widget).validate_python({**base, "cards": [{**card, "is_partial": True}]})
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python({**base, "cards": [{**card, "is_partial": False}]})


def test_budget_gap_is_never_negative_and_pairs_with_a_position() -> None:
    """Lisbon: budget 800 pounds, complete known costs 782 pounds.

    Working: 800 - 782 = 18 pounds under, so exact 1800 minor units, shown about 20 pounds (2000).
    Source: sample-data.md, "The three places", Lisbon (the sample is partial there; this
    test uses a complete total to test the rule).
    """
    under = {"budget_gap": _estimate(1800, 2000), "budget_position": "under", "is_partial": False}
    TypeAdapter(Widget).validate_python(_cost(**under))
    with pytest.raises(ValidationError):  # negative gap
        TypeAdapter(Widget).validate_python(
            _cost(**{**under, "budget_gap": _estimate(-1800, -2000)})
        )
    with pytest.raises(ValidationError):  # gap without position
        TypeAdapter(Widget).validate_python(
            _cost(budget_gap=_estimate(1800, 2000), is_partial=False)
        )
    with pytest.raises(ValidationError):  # position without gap
        TypeAdapter(Widget).validate_python(_cost(budget_position="under", is_partial=False))
    with pytest.raises(ValidationError):  # "on" needs a gap of exactly zero
        TypeAdapter(Widget).validate_python(_cost(**{**under, "budget_position": "on"}))
    TypeAdapter(Widget).validate_python(
        _cost(budget_gap=_estimate(0, 0), budget_position="on", is_partial=False)
    )


def test_partial_total_is_only_compared_when_already_over() -> None:
    """Valletta: known costs 902 pounds against 800 pounds, 102 over (exact 10200, about 100).

    Working: 902 - 800 = 102. Source: sample-data.md, "The three places", Valletta.
    A partial total cannot be called under or on budget, because a missing line could change it.
    """
    missing = {"missing": "no source has activities"}
    over = {"activities": missing, "is_partial": True}
    TypeAdapter(Widget).validate_python(
        _cost(**over, budget_gap=_estimate(10200, 10000), budget_position="over")
    )
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python(
            _cost(**over, budget_gap=_estimate(1800, 2000), budget_position="under")
        )


def test_comparison_card_budget_gap_rules() -> None:
    base = {**_payload("comparison_table"), "state": "filled", "sources": [SOURCE]}
    card = {"place": "Lisbon", "card_state": "ready", "is_partial": False}
    TypeAdapter(Widget).validate_python(
        {
            **base,
            "cards": [{**card, "budget_gap": _estimate(1800, 2000), "budget_position": "under"}],
        }
    )
    with pytest.raises(ValidationError):
        TypeAdapter(Widget).validate_python(
            {**base, "cards": [{**card, "budget_gap": _estimate(1800, 2000)}]}
        )


def test_fare_list_has_a_slug_for_one_place_not_known() -> None:
    assert "one_place_not_known" in WIDGET_STATES["fare_list"]
