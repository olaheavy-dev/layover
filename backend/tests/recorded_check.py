"""Load recorded provider responses and check them for secrets.

A recording is one JSON file at tests/recorded/<provider>/<name>.json (format in
tests/recorded/README.md). The merge check reads these instead of calling a real service.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, HttpUrl

RECORDED_DIR = Path(__file__).parent / "recorded"

# A key name that holds a credential: one of these words standing alone or between "-" and "_"
# (so `access_token`, `x-api-key` and `Api-Key` match, but `tokens_used` does not). Case-insensitive.
SECRET_KEY = re.compile(
    r"(^|[-_])((access|refresh|auth)?[-_]?token|api[-_]?key|secret|password|authorization|cookie"
    r"|session|signature|client[-_]secret)($|[-_])",
    re.IGNORECASE,
)
# Values that look like a credential or personal data: a Duffel key, an email address, a Bearer or
# Basic header value, a JWT, or a key, token or signature in a URL's query string.
SECRET_VALUE = re.compile(
    r"duffel_(test|live)_"
    r"|[\w.+-]+@[\w-]+\.[\w.-]+"
    r"|\bBearer\s+\S+"
    r"|\bBasic\s+\S{8,}"
    r"|\beyJ[\w-]+\.[\w-]+\."
    r"|[?&](api[-_]?key|apikey|token|access[-_]?token|key|signature)=",
    re.IGNORECASE,
)


class Recording(BaseModel):
    """One captured exchange: what was asked, what came back, when, and from where."""

    model_config = ConfigDict(extra="forbid")

    provider: str
    captured_at: date
    source: HttpUrl
    request: dict[str, Any]
    response: dict[str, Any]


def load_recording(provider: str, name: str, root: Path = RECORDED_DIR) -> Recording:
    """Read tests/recorded/<provider>/<name>.json; raises if date or source is missing."""
    path = root / provider / f"{name}.json"
    return Recording.model_validate_json(path.read_text(encoding="utf-8"))


def recording_files(root: Path = RECORDED_DIR) -> list[Path]:
    """Every JSON file under the recorded folder."""
    return sorted(root.rglob("*.json"))


def find_secrets(data: object, where: str = "$") -> list[str]:
    """Paths of every secret-looking key or value, at any depth of dicts and lists."""
    found: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            here = f"{where}.{key}"
            if SECRET_KEY.search(str(key)) or SECRET_VALUE.search(str(key)):
                found.append(here)
            found.extend(find_secrets(value, here))
    elif isinstance(data, list):
        if (
            len(data) == 2 and isinstance(data[0], str) and SECRET_KEY.search(data[0])
        ):  # a [name, value] pair, such as a header
            found.append(where)
        for index, value in enumerate(data):
            found.extend(find_secrets(value, f"{where}[{index}]"))
    elif isinstance(data, str) and SECRET_VALUE.search(data):
        found.append(where)
    return found
