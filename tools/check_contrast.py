#!/usr/bin/env python3
"""Check that Layover's design tokens meet WCAG 2.2 AA contrast in the light and dark themes.

Reads docs/design/tokens.css: the first `:root {` block holds the light values, and the two dark
blocks (`:root[data-theme="dark"]` and the `prefers-color-scheme: dark` block) override them. The
two dark blocks must hold the same values. Text pairs need 4.5:1 (WCAG 1.4.3) and control and focus
pairs need 3:1 (WCAG 1.4.11). White text on a photo is tested over a white photo under the scrim at
its minimum opacity. Formulas: https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TEXT = 4.5
NON_TEXT = 3.0

# (foreground token, background token, minimum ratio, what it is)
PAIRS: list[tuple[str, str, float, str]] = [
    ("color-text-primary", "color-bg-primary", TEXT, "main text on the page"),
    ("color-text-primary", "color-bg-secondary", TEXT, "main text on cards"),
    ("color-text-primary", "color-bg-tertiary", TEXT, "text on chips"),
    ("color-text-secondary", "color-bg-primary", TEXT, "quiet text on the page"),
    ("color-text-secondary", "color-bg-secondary", TEXT, "quiet text on cards"),
    ("color-text-link", "color-bg-primary", TEXT, "links on the page"),
    ("color-text-link", "color-bg-secondary", TEXT, "links on cards"),
    ("color-text-on-accent", "color-accent-primary", TEXT, "button text"),
    ("color-text-on-accent", "color-accent-primary-hover", TEXT, "button text, hover"),
    ("color-text-on-accent", "color-accent-primary-active", TEXT, "button text, pressed"),
    ("color-status-warning", "color-bg-primary", TEXT, "warning text on the page"),
    ("color-status-warning", "color-bg-secondary", TEXT, "warning text on cards"),
    ("color-status-live", "color-bg-secondary", TEXT, "Live label"),
    ("color-status-cached", "color-bg-secondary", TEXT, "Cached label"),
    ("color-status-not-known", "color-bg-secondary", TEXT, "Not known label"),
    ("color-status-info", "color-bg-secondary", TEXT, "information text"),
    ("color-border-control", "color-bg-secondary", NON_TEXT, "input and button borders"),
    ("color-border-focus", "color-bg-primary", NON_TEXT, "focus ring on the page"),
    ("color-border-focus", "color-bg-secondary", NON_TEXT, "focus ring on cards"),
]

DECL = re.compile(r"--([a-z0-9-]+)\s*:\s*([^;]+);")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def _channel(value: int) -> float:
    c = value / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (_channel(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def blend(top: str, bottom: str, opacity: float) -> str:
    """The colour of `top` at `opacity` laid over an opaque `bottom`."""
    t, b = top.lstrip("#"), bottom.lstrip("#")
    out = [round(opacity * int(t[i:i + 2], 16) + (1 - opacity) * int(b[i:i + 2], 16)) for i in (0, 2, 4)]
    return "#" + "".join(f"{v:02X}" for v in out)


def _block(css: str, opener: str) -> dict[str, str] | None:
    start = css.find(opener)
    if start == -1:
        return None
    body_start = css.index("{", start) + 1
    body_end = css.index("}", body_start)
    return {name: value.strip() for name, value in DECL.findall(css[body_start:body_end])}


def problems(path: Path) -> list[str]:
    css = re.sub(r"/\*.*?\*/", "", path.read_text(), flags=re.S)
    light = _block(css, ":root {")
    manual = _block(css, ':root[data-theme="dark"]')
    system = _block(css, ':root:not([data-theme="light"])')
    if light is None or manual is None or system is None:
        return [f"{path}: needs a light :root block and both dark blocks"]
    found: list[str] = []
    if manual != system:
        found.append(f"{path}: the two dark blocks differ; keep them identical")
    themes = {"light": light, "dark": {**light, **manual}}
    for theme, tokens in themes.items():
        for fg, bg, minimum, what in PAIRS:
            if fg not in tokens or bg not in tokens:
                found.append(f"{theme}: missing --{fg} or --{bg} ({what})")
                continue
            a, b = tokens[fg], tokens[bg]
            if not (HEX.match(a) and HEX.match(b)):
                found.append(f"{theme}: --{fg} and --{bg} must be six-digit hex values ({what})")
                continue
            ratio = contrast(a, b)
            if ratio < minimum:
                found.append(f"{theme}: --{fg} on --{bg} is {ratio:.2f}:1, needs {minimum}:1 ({what})")
        scrim, opacity = tokens.get("color-scrim"), tokens.get("scrim-text-min-opacity")
        if scrim and opacity and HEX.match(scrim):
            under = blend(scrim, "#FFFFFF", float(opacity))
            ratio = contrast("#FFFFFF", under)
            if ratio < TEXT:
                found.append(f"{theme}: white text on the photo scrim is {ratio:.2f}:1, needs {TEXT}:1")
        else:
            found.append(f"{theme}: missing --color-scrim or --scrim-text-min-opacity")
    return found


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/design/tokens.css")
    found = problems(path)
    for p in found:
        print(f"contrast: {p}", file=sys.stderr)
    if not found:
        print(f"contrast: {path} meets WCAG 2.2 AA in both themes")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
