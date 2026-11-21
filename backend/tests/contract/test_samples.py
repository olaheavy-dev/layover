"""Tests for the shared sample files (schemas/samples) and their loaders.

Expected failure before the files and loaders exist: `app.contract.samples` cannot be imported.
"""

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import pytest
from pydantic import TypeAdapter

from app.contract.samples import load_sample_trip, load_sample_widgets, samples_dir
from app.contract.widgets import WIDGET_KINDS, WIDGET_STATES, CostEstimate, Widget

REPO_ROOT = Path(__file__).resolve().parents[3]
PLACEHOLDER_STRINGS = {"", "N/A", "TBC", "-", "—"}


def _widget_files() -> list[Path]:
    return sorted((samples_dir() / "widgets").glob("*/*.json"))


def _walk(value: Any) -> list[Any]:
    """Every value inside a parsed JSON document, nested ones included."""
    found = [value]
    if isinstance(value, dict):
        for item in value.values():
            found.extend(_walk(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_walk(item))
    return found


def _strings(path: Path) -> list[str]:
    return [v for v in _walk(json.loads(path.read_text("utf-8"))) if isinstance(v, str)]


def test_every_kind_has_every_state() -> None:
    root = samples_dir() / "widgets"
    assert {p.name for p in root.iterdir() if p.is_dir()} == set(WIDGET_KINDS)
    for kind in WIDGET_KINDS:
        found = {p.stem for p in (root / kind).glob("*.json")}
        assert found == set(WIDGET_STATES[kind]), kind


def test_every_sample_validates() -> None:
    adapter: TypeAdapter[Widget] = TypeAdapter(Widget)
    files = _widget_files()
    assert files
    for path in files:
        widget = adapter.validate_json(path.read_bytes())
        assert widget.kind == path.parent.name, path


def test_sample_trip_is_marked() -> None:
    trip = load_sample_trip()
    assert trip.is_sample is True
    assert trip.trip_id == "sample-lisbon"
    assert len(load_sample_widgets()) == len(_widget_files())


def _missing_objects(document: Any) -> list[Any]:
    """Every object that says something is missing: a `missing` reason or the not_known state."""
    return [
        v
        for v in _walk(document)
        if isinstance(v, dict) and (v.get("missing") is not None or v.get("state") == "not_known")
    ]


def test_no_zero_for_missing() -> None:
    checked = 0
    paths = [*_widget_files(), *(samples_dir() / "trip").glob("*.json")]
    for path in paths:
        for obj in _missing_objects(json.loads(path.read_text("utf-8"))):
            checked += 1
            for value in _walk(obj):
                # bool is a kind of int in Python, so a flag set to false is not a zero.
                if isinstance(value, bool):
                    continue
                assert not (isinstance(value, int | float) and value == 0), path
                assert not (isinstance(value, str) and value.strip() in PLACEHOLDER_STRINGS), path
    assert checked > 0


def test_trip_matches_widget_samples() -> None:
    by_name = {(s.kind, s.state): s.widget for s in load_sample_widgets()}
    trip = load_sample_trip()
    assert trip.comparison == by_name[("comparison_table", "chosen")]
    assert trip.stay == by_name[("hotel_list", "chosen")]
    assert trip.booking == by_name[("booking_approval", "waiting")]
    assert [w.kind for w in trip.place_widgets] == [
        "fare_card",
        "cost_estimate",
        "advice_card",
        "climate_chart",
        "sea_conditions",
        "daylight",
        "money",
        "place_intro",
    ]
    for widget in trip.place_widgets:
        assert widget == by_name[(widget.kind, "filled")], widget.kind
    assert list(trip.days) == [
        by_name[("itinerary_day", "filled")],
        by_name[("itinerary_day", "not_known")],
        by_name[("itinerary_day", "empty")],
    ]
    # The brief is the confirmed sample, with the trip's own name.
    confirmed = by_name[("brief_summary", "confirmed")]
    assert trip.brief == confirmed.model_copy(update={"trip_name": trip.name})


def test_exact_flights_are_not_estimates() -> None:
    by_name = {(s.kind, s.state): s.widget for s in load_sample_widgets()}
    cost = by_name[("cost_estimate", "filled")]
    assert isinstance(cost, CostEstimate)
    assert cost.flights is not None
    assert cost.flights.amount is not None
    assert cost.flights.amount.is_estimate is False
    assert cost.stay is not None
    assert cost.stay.amount is not None
    assert cost.stay.amount.is_estimate is True


def test_no_invented_day_for_a_wikivoyage_month() -> None:
    for path in _widget_files():
        for value in _walk(json.loads(path.read_text("utf-8"))):
            if isinstance(value, dict) and "page_edited" in value:
                assert len(value["page_edited"]) == 7, path  # "2026-03": the boards give no day


def test_no_safe_wording(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "dont_write_bytecode", True)  # leave no tools/__pycache__ behind
    spec = importlib.util.spec_from_file_location(
        "check_boards", REPO_ROOT / "tools" / "check_boards.py"
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    safe = module.SAFE
    files = [*_widget_files(), *(samples_dir() / "trip").glob("*.json")]
    assert files
    for path in files:
        for text in _strings(path):
            assert not safe.search(text), (path, text)


def test_samples_dir_is_overridable(tmp_path: Path) -> None:
    from app.settings import Settings

    assert Settings(samples_dir=tmp_path).samples_dir == tmp_path
