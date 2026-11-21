"""Loaders for the shared sample files in `schemas/samples`.

The files are samples: invented or copied from the design boards' sample data, never real
figures. They feed tests, the sample API endpoints and the website's widget gallery.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, TypeAdapter

from app.contract.trip import Trip
from app.contract.widgets import Widget

_WIDGET: TypeAdapter[Widget] = TypeAdapter(Widget)


class SamplesUnavailable(Exception):
    """The samples folder, or a file the loaders need, is not there."""


class SampleWidget(BaseModel):
    """One sample file: a widget kind, the state the file shows, and the parsed widget."""

    model_config = ConfigDict(frozen=True)

    is_sample: Literal[True] = True  # these are never real fares, prices or advice
    kind: str
    state: str  # the file name, for example "swapped"; the widget's own `state` may differ
    widget: Widget


@lru_cache
def load_sample_trip(root: Path) -> Trip:
    """The Lisbon sample trip (`trip/sample-lisbon.json` under `root`), marked `is_sample`.

    Read once per folder: the files do not change while the process runs.
    """
    path = root / "trip" / "sample-lisbon.json"
    if not path.is_file():
        raise SamplesUnavailable(f"missing sample trip file: {path.name}")
    return Trip.model_validate_json(path.read_bytes())


@lru_cache
def load_sample_widgets(root: Path) -> tuple[SampleWidget, ...]:
    """Every widget sample under `root`, sorted by kind then state. Read once per folder."""
    files = sorted((root / "widgets").glob("*/*.json"))
    if not files:
        raise SamplesUnavailable("no sample widget files found")
    return tuple(
        SampleWidget(
            kind=path.parent.name,
            state=path.stem,
            widget=_WIDGET.validate_json(path.read_bytes()),
        )
        for path in files
    )
