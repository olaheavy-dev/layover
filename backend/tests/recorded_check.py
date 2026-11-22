"""Load recorded provider responses and check them for secrets.

A recording is one JSON file at tests/recorded/<provider>/<name>.json (format in
tests/recorded/README.md). The merge check reads these instead of calling a real service.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path
from typing import Any

from pydantic import BaseModel, HttpUrl

RECORDED_DIR = Path(__file__).parent / "recorded"

# Key names that hold a credential, compared in lower case.
SECRET_KEYS = frozenset({"token", "api_key", "authorization", "x-access-token", "password"})
# Values that look like a Duffel key or an email address (personal data).
SECRET_VALUE = re.compile(r"duffel_(test|live)_|[\w.+-]+@[\w-]+\.[\w.-]+", re.IGNORECASE)


class Recording(BaseModel):
    """One captured exchange: what was asked, what came back, when, and from where."""

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
            if str(key).lower() in SECRET_KEYS:
                found.append(here)
            found.extend(find_secrets(value, here))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            found.extend(find_secrets(value, f"{where}[{index}]"))
    elif isinstance(data, str) and SECRET_VALUE.search(data):
        found.append(where)
    return found
