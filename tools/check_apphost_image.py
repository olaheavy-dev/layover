#!/usr/bin/env python3
"""Check that the Aspire app host runs the same PostgreSQL image as the backend's compose file.

backend/compose/db/compose.yaml pins `image: <name>:<tag>@sha256:<digest>`. apphost/apphost.mts must
name the same three parts (withImage, withImageTag, withImageSHA256), or `make dev-all` would run a
different database from `make db-up`. Dependabot updates the compose file only, so this check fails
until the app host is changed by hand.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

COMPOSE = Path("backend/compose/db/compose.yaml")
APPHOST = Path("apphost/apphost.mts")

COMPOSE_IMAGE = re.compile(r"^\s*image:\s*([^:\s]+):([^@\s]+)@sha256:([0-9a-f]{64})\s*$", re.M)
APPHOST_PARTS = {
    "name": re.compile(r'\.withImage\(\s*"([^"]+)"\s*\)'),
    "tag": re.compile(r'\.withImageTag\(\s*"([^"]+)"\s*\)'),
    "digest": re.compile(r'\.withImageSHA256\(\s*"([0-9a-f]{64})"\s*\)'),
}


def compose_image(text: str) -> dict[str, str] | None:
    match = COMPOSE_IMAGE.search(text)
    if not match:
        return None
    return dict(zip(("name", "tag", "digest"), match.groups(), strict=True))


def apphost_image(text: str) -> dict[str, str]:
    return {key: m.group(1) for key, rx in APPHOST_PARTS.items() if (m := rx.search(text))}


def problems(compose_text: str, apphost_text: str) -> list[str]:
    expected = compose_image(compose_text)
    if expected is None:
        return [f"{COMPOSE}: no image pinned as name:tag@sha256:digest"]
    found = apphost_image(apphost_text)
    out = []
    for key in ("name", "tag", "digest"):
        if found.get(key) != expected[key]:
            out.append(
                f"{APPHOST}: image {key} is {found.get(key)!r}, {COMPOSE} has {expected[key]!r}"
            )
    return out


def main() -> int:
    found = problems(COMPOSE.read_text(), APPHOST.read_text())
    for line in found:
        print(line)
    if not found:
        print("check_apphost_image: ok")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
