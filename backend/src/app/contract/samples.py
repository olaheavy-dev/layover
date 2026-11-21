"""Loaders for the shared sample files in `schemas/samples`.

The files are samples: invented or copied from the design boards' sample data, never real
figures. They feed tests, the sample API endpoints (still to come) and the website's widget gallery.
"""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, TypeAdapter

from app.contract.trip import Trip
from app.contract.widgets import Widget
from app.settings import get_settings

_WIDGET: TypeAdapter[Widget] = TypeAdapter(Widget)


class SampleWidget(BaseModel):
    """One sample file: a widget kind, the state the file shows, and the parsed widget."""

    model_config = ConfigDict(frozen=True)

    kind: str
    state: str  # the file name, for example "swapped"; the widget's own `state` may differ
    widget: Widget


def samples_dir() -> Path:
    """The sample files' folder: the SAMPLES_DIR setting, else the repository's schemas/samples."""
    return get_settings().samples_dir


def load_sample_trip() -> Trip:
    """The Lisbon sample trip (`trip/sample-lisbon.json`), marked `is_sample`."""
    return Trip.model_validate_json((samples_dir() / "trip" / "sample-lisbon.json").read_bytes())


def load_sample_widgets() -> list[SampleWidget]:
    """Every widget sample, sorted by kind then state."""
    root = samples_dir() / "widgets"
    return [
        SampleWidget(
            kind=path.parent.name,
            state=path.stem,
            widget=_WIDGET.validate_json(path.read_bytes()),
        )
        for path in sorted(root.glob("*/*.json"))
    ]
