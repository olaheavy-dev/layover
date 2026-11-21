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
from app.contract.widgets import WIDGET_KINDS, WIDGET_STATES, Widget

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


def test_no_zero_for_missing() -> None:
    checked = 0
    for path in _widget_files():
        document = json.loads(path.read_text("utf-8"))
        if document.get("state") != "not_known":
            continue
        checked += 1
        for value in _walk(document):
            # bool is a kind of int in Python, so a flag set to false is not a zero.
            if isinstance(value, bool):
                continue
            assert not (isinstance(value, int | float) and value == 0), path
            assert not (isinstance(value, str) and value.strip() in PLACEHOLDER_STRINGS), path
    assert checked > 0


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
