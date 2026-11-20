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
  or a GitHub, GitLab or Bitbucket address ending in .git;
- an inline <script> whose SHA-256 hash is not allowed by the page's Content-Security-Policy. The export
  only runs scripts whose exact bytes match a hash, so a changed byte (for example a whitespace hook
  trimming line ends) blocks the map in the browser (Codex review of #42).

Limits: this is a text search. It doesn't find personal data or private material in names and
descriptions; that check is done by hand before the snapshot is committed. Secrets are caught by gitleaks
in `make check`. No folder means no snapshot yet, which passes.
"""

from __future__ import annotations

import base64
import hashlib
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

CSP = re.compile(r'<meta\s+http-equiv="Content-Security-Policy"[^>]*\scontent="([^"]*)"', re.IGNORECASE)
INLINE_SCRIPT = re.compile(r"<script>(.*?)</script>", re.DOTALL)


def blocked_scripts(text: str) -> int:
    """How many inline scripts the page's Content-Security-Policy would block (0 when it has no policy)."""
    policy = CSP.search(text)
    if not policy:
        return 0
    allowed = set(re.findall(r"'sha256-([A-Za-z0-9+/=]+)'", policy.group(1)))
    return sum(
        base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode() not in allowed
        for body in INLINE_SCRIPT.findall(text))


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
            blocked = blocked_scripts(text)
            if blocked:
                problems.append(f"{rel}: {blocked} inline script(s) not allowed by its Content-Security-Policy "
                                "(the file changed after export; export it again)")
    for problem in problems:
        print(problem)
    if not problems:
        print("floorplan snapshots: no local paths, file addresses or git remotes; scripts match their CSP")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(Path(__file__).resolve().parent.parent))
