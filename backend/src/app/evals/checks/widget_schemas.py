"""The schema part of WIDGET-01 to WIDGET-20: the samples for a widget kind match the contract."""

import re
from pathlib import Path

from app.contract.samples import SamplesUnavailable, load_sample_widgets
from app.contract.widgets import WIDGET_STATES
from app.settings import DEFAULT_SAMPLES_DIR

_KIND = re.compile(r"^`(\w+)`")


def widget_kind(title: str) -> str | None:
    """The widget `kind` a WIDGET case checks: the first backticked word of its "What it checks"."""
    match = _KIND.match(title)
    return match.group(1) if match else None


def check_widget_samples(kind: str, root: Path = DEFAULT_SAMPLES_DIR) -> tuple[bool, str]:
    """Pass when every sample of `kind` parses into the Pydantic widget models and every state the
    contract lists for the kind has a sample file. A file that fails to parse fails the check."""
    expected = WIDGET_STATES.get(kind)
    if expected is None:
        return False, f"{kind}: not a widget kind in the contract"
    try:
        samples = [s for s in load_sample_widgets(root) if s.kind == kind]
    except SamplesUnavailable as error:
        return False, f"{kind}: {error}"
    except ValueError as error:  # a sample that does not match its model
        return False, f"{kind}: a sample does not match the contract: {error}"
    found = {s.state for s in samples}
    missing = [state for state in expected if state not in found]
    if missing:
        return False, f"{kind}: no sample for state {', '.join(missing)}"
    return True, f"{kind}: {len(samples)} samples valid"
