#!/usr/bin/env python3
"""Check the Floorplan map snapshots in docs/floorplan/ (AGENTS.md, "Floorplan snapshot at each gate").

A snapshot is an exported Floorplan map, committed at each stage gate. The export should hold no folder
paths or git remotes, but it is generated, so this check makes sure (register line of 19 Nov 2026, #16).

Fails when any file under docs/floorplan/ holds:
- a local path: /Users/, /home/, or C:\\Users\\ (any case, with single or doubled backslashes);
- a file:// address;
- an SSH git remote (git@host:...).

Limits: this is a text search. It doesn't find personal data or private material in names and
descriptions; that check is done by hand before the snapshot is committed. Secrets are caught by gitleaks
in `make check`. No folder means no snapshot yet, which passes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FOLDER = Path("docs/floorplan")
PATTERNS = [
    ("a local path", re.compile(r"/Users/|/home/|[A-Za-z]:\\{1,2}Users\\", re.IGNORECASE)),
    ("a file:// address", re.compile(r"file://", re.IGNORECASE)),
    ("an SSH git remote", re.compile(r"\bgit@[A-Za-z0-9.-]+:")),
]


def main(root: Path) -> int:
    folder = root / FOLDER
    problems: list[str] = []
    if folder.is_dir():
        for path in sorted(p for p in folder.rglob("*") if p.is_file()):
            text = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(root).as_posix()
            for what, pattern in PATTERNS:
                match = pattern.search(text)
                if match:
                    line = text.count("\n", 0, match.start()) + 1
                    problems.append(f"{rel}:{line}: holds {what}")
    for problem in problems:
        print(problem)
    if not problems:
        print("floorplan snapshots: no local paths, file addresses or git remotes")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(Path(__file__).resolve().parent.parent))
