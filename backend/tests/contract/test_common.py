"""Tests for the source labels and the widget base."""

from datetime import UTC, date, datetime

import pytest
from pydantic import ValidationError

from app.contract.common import (
    NO_OUTSIDE_SOURCE,
    MoneyEstimate,
    MoneyValue,
    SourceLabel,
    WidgetBase,
)


class _Widget(WidgetBase):
    """Test-only widget that adds the `kind` field later widgets carry."""

    kind: str


def _label() -> SourceLabel:
    return SourceLabel(status="live", source="Open-Meteo")


def test_cached_label_needs_a_date() -> None:
    with pytest.raises(ValidationError):
        SourceLabel(status="cached", source="Open-Meteo")


def test_cached_label_with_release_date_only() -> None:
    label = SourceLabel(status="cached", source="FCDO", data_date=date(2026, 11, 4))
    assert label.captured_at is None


def test_cached_label_with_captured_at_only() -> None:
    label = SourceLabel(
        status="cached", source="Open-Meteo", captured_at=datetime(2026, 11, 1, tzinfo=UTC)
    )
    assert label.data_date is None


def test_unavailable_label_needs_no_time() -> None:
    label = SourceLabel(status="unavailable", source="Duffel")
    assert label.captured_at is None
    assert label.data_date is None


def test_source_name_is_never_empty() -> None:
    with pytest.raises(ValidationError):
        SourceLabel(status="live", source="")


def test_naive_captured_at_is_rejected() -> None:
    with pytest.raises(ValidationError):
        SourceLabel(status="live", source="Duffel", captured_at=datetime(2026, 11, 1))


def test_not_known_needs_missing_reason() -> None:
    with pytest.raises(ValidationError):
        _Widget(kind="visa", state="not_known", sources=[], missing=None)
    ok = _Widget(kind="visa", state="not_known", sources=[], missing="No source covers it.")
    assert ok.missing == "No source covers it."


def test_filled_widget_needs_a_source() -> None:
    with pytest.raises(ValidationError):
        _Widget(kind="weather", state="filled", sources=[])
    assert _Widget(kind="weather", state="filled", sources=[_label()]).state == "filled"


def test_filled_widget_without_source_allowed_for_own_content_kinds() -> None:
    assert frozenset({"brief_summary", "not_known"}) == NO_OUTSIDE_SOURCE
    for kind in NO_OUTSIDE_SOURCE:
        assert _Widget(kind=kind, state="filled", sources=[]).sources == []


def test_widget_base_is_frozen_and_forbids_extra() -> None:
    widget = _Widget(kind="weather", state="empty", sources=[])
    with pytest.raises(ValidationError):
        widget.state = "error"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        _Widget(kind="weather", state="empty", sources=[], surprise=1)  # type: ignore[call-arg]


def test_money_rejects_float() -> None:
    with pytest.raises(ValidationError):
        MoneyValue(amount_minor=19.5, currency="GBP")


def test_money_rejects_numeric_string() -> None:
    with pytest.raises(ValidationError):
        MoneyValue(amount_minor="1950", currency="GBP")


@pytest.mark.parametrize("code", ["gbp", "GBPX", "GB", "G1P"])
def test_currency_code_shape(code: str) -> None:
    with pytest.raises(ValidationError):
        MoneyValue(amount_minor=1, currency=code)


def test_estimate_is_marked() -> None:
    exact = MoneyValue(amount_minor=12345, currency="GBP")
    shown = MoneyValue(amount_minor=12000, currency="GBP")
    with pytest.raises(ValidationError):
        MoneyEstimate(exact=exact, shown=shown)  # type: ignore[call-arg]
    with pytest.raises(ValidationError):
        MoneyEstimate(exact=exact, shown=shown, is_estimate=False)
    assert MoneyEstimate(exact=exact, shown=shown, is_estimate=True).is_estimate is True


def test_estimate_currencies_must_match() -> None:
    with pytest.raises(ValidationError):
        MoneyEstimate(
            exact=MoneyValue(amount_minor=100, currency="GBP"),
            shown=MoneyValue(amount_minor=100, currency="EUR"),
            is_estimate=True,
        )
