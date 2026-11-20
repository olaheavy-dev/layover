#!/usr/bin/env python3
"""Check the Floorplan map snapshots in docs/floorplan/ (AGENTS.md, "Floorplan snapshot at each gate").

A snapshot is an exported Floorplan map, committed at each stage gate. The export should hold no folder
paths or git remotes, but it is generated, so this check makes sure (register line of 19 Nov 2026, #16).

Fails when any file under docs/floorplan/ holds:
- a local path: /Users/, /home/, /root/, /Volumes/, /private/tmp/, /private/var/, /var/folders/, or a
  Windows drive path such as C:\\Users or D:\\Projects (one to four backslashes, as JSON inside a script
  doubles them);
- a file:// address;
- a git remote: ssh://, git@host: or git@host/, an http(s) address with a user name or token before an @,
  or a GitHub, GitLab or Bitbucket address ending in .git.

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
    ("a local path", re.compile(
        r"/Users/|/home/|/root/|/Volumes/|/private/(?:tmp|var)/|/var/folders/|\b[A-Za-z]:\\{1,4}[A-Za-z0-9_.$ -]",
        re.IGNORECASE)),
    ("a file:// address", re.compile(r"file://", re.IGNORECASE)),
    ("a git remote", re.compile(
        r"ssh://|\bgit@[A-Za-z0-9.-]+[:/]|https?://[^/\s\"'@<>]+@"
        r"|https?://(?:www\.)?(?:github\.com|gitlab\.com|bitbucket\.org)/[^\s\"'<>]*\.git\b",
        re.IGNORECASE)),
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
