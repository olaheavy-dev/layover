#!/usr/bin/env python3
"""Check the frontend's copy and fonts.

Fails when:
- a .ts or .tsx file under frontend/src/ (test files, *.test.* and *.spec.*, are not scanned) says "safe",
  "safer", "safest", "safely" or "unsafe" (decision 0011, rule 6: Layover never says a destination is safe).
  It uses the SAFE pattern from tools/check_boards.py and lets `safe-area` through, as the boards check does, and the CSP keywords `unsafe-inline`, `unsafe-eval` and
  `unsafe-hashes` (frontend/src/lib/csp.ts), each only exactly, so `safe-inline` is still flagged.
  "Safety" is allowed: it is part of the FCDO's section name, "Safety and security". The check reads the
  whole file, so a comment or an identifier such as `safeMode` is flagged too (rename it);
- a file in frontend/src/fonts/ differs, by SHA-256 hash, from the file of the same name in
  docs/design/boards/fonts/, or has no copy there. The boards hold the registered originals
  (docs/assets/README.md); the frontend holds copies of the same files;
- frontend/src/styles/tokens.css differs, by SHA-256 hash, from docs/design/tokens.css (the original).
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from check_boards import SAFE  # noqa: E402

SRC = Path("frontend/src")
APP_FONTS = SRC / "fonts"
BOARD_FONTS = Path("docs/design/boards/fonts")
APP_TOKENS = SRC / "styles" / "tokens.css"
DESIGN_TOKENS = Path("docs/design/tokens.css")
SUFFIXES = {".ts", ".tsx"}
TEST_MARKERS = (".test.", ".spec.")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Let through the CSS `safe-area` and the exact Content-Security-Policy keywords `unsafe-inline`,
# `unsafe-eval` and `unsafe-hashes`. Each is allowed only after its own word, and only as a whole
# word, so "safe-inline" and "unsafe-evaluation" are still flagged.
ALLOWED_AFTER = {
    "safe": re.compile(r"-area\b"),
    "unsafe": re.compile(r"-(?:inline|eval|hashes)\b"),
}


def _safe_words(text: str) -> set[str]:
    found: set[str] = set()
    for m in SAFE.finditer(text):
        word = m.group(0).lower()
        allowed = ALLOWED_AFTER.get(word)
        if allowed and allowed.match(text, m.end()):
            continue
        found.add(word)
    return found


def problems(root: Path) -> list[str]:
    found: list[str] = []
    src = root / SRC
    for path in sorted(src.rglob("*")) if src.is_dir() else []:
        if path.suffix not in SUFFIXES or any(m in path.name for m in TEST_MARKERS):
            continue
        for word in sorted(_safe_words(path.read_text(encoding="utf-8"))):
            found.append(f"{path.relative_to(root)}: says \"{word}\"; Layover never says a destination is safe "
                         "(decision 0011, rule 6)")
    fonts = root / APP_FONTS
    for path in sorted(p for p in fonts.rglob("*") if p.is_file()) if fonts.is_dir() else []:
        rel = path.relative_to(fonts)
        original = root / BOARD_FONTS / rel
        if not original.is_file():
            found.append(f"{path.relative_to(root)}: no copy of it in {BOARD_FONTS}; "
                         "the boards hold the registered original")
        elif _sha256(path) != _sha256(original):
            found.append(f"{path.relative_to(root)}: differs from {BOARD_FONTS / rel}; copy the file again")
    tokens = root / APP_TOKENS
    if tokens.is_file():
        original = root / DESIGN_TOKENS
        if not original.is_file():
            found.append(f"{APP_TOKENS}: no copy of it in {DESIGN_TOKENS}; the design folder holds the original")
        elif _sha256(tokens) != _sha256(original):
            found.append(f"{APP_TOKENS}: differs from {DESIGN_TOKENS}; copy the file again")
    return found


def main() -> int:
    found = problems(Path("."))
    for p in found:
        print(f"copy: {p}", file=sys.stderr)
    if not found:
        print("copy: no \"safe\" wording in the frontend and the font and token copies match the originals")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
