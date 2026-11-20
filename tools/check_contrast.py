#!/usr/bin/env python3
"""Check that Layover's design tokens meet WCAG 2.2 AA contrast in the light and dark themes.

Reads docs/design/tokens.css: the first `:root {` block holds the light values, and the two dark
blocks (`:root[data-theme="dark"]` and the `prefers-color-scheme: dark` block) override them. The
two dark blocks must hold the same values. Every --color-text-* and --color-status-* token is tested on
every page background and needs 4.5:1 (WCAG 1.4.3); control borders and the focus ring need 3:1
(WCAG 1.4.11). Every --color-chart-* token needs 3:1 on every page background (WCAG 1.4.11: chart marks).
The highlight colour is not tested: it is never text and never the only cue. --color-text-on-photo is
tested over a white photo under the scrim at its minimum opacity (the worst case), in both themes.
Formulas: https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio

Tinted surfaces: every --tint-surface-* token of the form `color-mix(in srgb, var(--X) N%, var(--Y))`
is worked out in each theme and --color-text-primary, --color-text-secondary and --color-text-link are
tested on it at 4.5:1. Other --tint-* tokens (glows, lines, borders, and a surface mixed with
`transparent`) are skipped and listed in the output: transparency can't be checked without the backdrop.
The --illus-* tokens are left out on purpose: illustrations are decorative and carry no information
(brief, "Accessibility requirements").
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TEXT = 4.5
NON_TEXT = 3.0

BACKGROUNDS = ("color-bg-primary", "color-bg-secondary", "color-bg-tertiary")

# Text tokens with their own background, or exempt (WCAG 1.4.3 exempts disabled controls).
SPECIAL_TEXT = {"color-text-on-accent", "color-text-inverse", "color-text-disabled", "color-text-on-photo"}

# Pairs that are not "text token on a page background": (foreground, background, minimum, what it is)
SPECIAL_PAIRS: list[tuple[str, str, float, str]] = [
    ("color-text-on-accent", "color-accent-primary", TEXT, "button text"),
    ("color-text-on-accent", "color-accent-primary-hover", TEXT, "button text, hover"),
    ("color-text-on-accent", "color-accent-primary-active", TEXT, "button text, pressed"),
    ("color-text-inverse", "color-bg-inverse", TEXT, "text on an inverse background"),
    *[("color-border-control", bg, NON_TEXT, "input and button borders") for bg in BACKGROUNDS],
    *[("color-border-focus", bg, NON_TEXT, "focus ring") for bg in BACKGROUNDS],
]

# Tokens every theme must define, so that deleting one fails the check.
REQUIRED = sorted({"color-text-primary", "color-text-secondary", "color-text-link", "color-status-warning",
                   "color-text-on-photo", "color-chart-1", "color-chart-2",
                   *BACKGROUNDS, *(t for pair in SPECIAL_PAIRS for t in pair[:2])})


def pairs_for(tokens: dict[str, str]) -> list[tuple[str, str, float, str]]:
    """Every text and status token on every page background, plus the special pairs.

    The list is built from the tokens themselves, so a colour token added later is checked
    without a change here.
    """
    text = sorted(t for t in tokens
                  if (t.startswith("color-text-") or t.startswith("color-status-")) and t not in SPECIAL_TEXT)
    built = [(t, bg, TEXT, "text") for t in text for bg in BACKGROUNDS]
    charts = [(t, bg, NON_TEXT, "chart mark") for t in sorted(tokens) if t.startswith("color-chart-")
              for bg in BACKGROUNDS]
    return built + charts + SPECIAL_PAIRS


TINT_TEXT = ("color-text-primary", "color-text-secondary", "color-text-link")
MIX = re.compile(r"^color-mix\(\s*in\s+srgb\s*,\s*var\(--([a-z0-9-]+)\)\s+(\d+(?:\.\d+)?)%\s*,"
                 r"\s*var\(--([a-z0-9-]+)\)\s*\)$")
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


def resolve_color_mix(value: str, tokens: dict[str, str]) -> str:
    """Work out `color-mix(in srgb, var(--X) N%, var(--Y))` as a hex colour. Raises ValueError otherwise.

    Each channel is X * N / 100 + Y * (1 - N / 100) on 0 to 255 values, then rounded half up to an 8-bit
    channel, as a browser stores it. Source: CSS Color 5, https://www.w3.org/TR/css-color-5/#color-mix
    (the sRGB mix without alpha is this weighted average).
    """
    m = MIX.match(value.strip())
    if not m:
        raise ValueError(f"cannot read {value!r}; expected color-mix(in srgb, var(--X) N%, var(--Y))")
    x, percent, y = m.group(1), float(m.group(2)), m.group(3)
    if percent > 100:
        raise ValueError(f"{value!r}: the percentage is over 100%")
    for name in (x, y):
        if name not in tokens or not HEX.match(tokens[name]):
            raise ValueError(f"{value!r}: --{name} is not a six-digit hex token")
    a, b = tokens[x].lstrip("#"), tokens[y].lstrip("#")
    out = [int(percent / 100 * int(a[i:i + 2], 16) + (1 - percent / 100) * int(b[i:i + 2], 16) + 0.5)
           for i in (0, 2, 4)]
    return "#" + "".join(f"{v:02X}" for v in out)


def split_tints(tokens: dict[str, str]) -> tuple[list[str], list[str]]:
    """(surfaces to check, other --tint-* tokens skipped). A surface mixed with transparent is skipped."""
    surfaces, skipped = [], []
    for name in sorted(t for t in tokens if t.startswith("tint-")):
        if name.startswith("tint-surface-") and "transparent" not in tokens[name]:
            surfaces.append(name)
        else:
            skipped.append(name)
    return surfaces, skipped


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
    for later in re.finditer(r":root\s*\{([^}]*)\}", css[css.index(":root {") + 1:]):
        if "--color-" in later.group(1):
            found.append(f"{path}: a later :root block sets colours; keep light colours in the first :root block")
    themes = {"light": light, "dark": {**light, **manual}}
    for theme, tokens in themes.items():
        for name in REQUIRED:
            if name not in tokens:
                found.append(f"{theme}: missing --{name}")
        for fg, bg, minimum, what in pairs_for(tokens):
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
        surfaces, _ = split_tints(tokens)
        for name in surfaces:
            try:
                surface = resolve_color_mix(tokens[name], tokens)
            except ValueError as error:
                found.append(f"{theme}: --{name}: {error}")
                continue
            for fg in TINT_TEXT:
                if fg in tokens and HEX.match(tokens[fg]):
                    ratio = contrast(tokens[fg], surface)
                    if ratio < TEXT:
                        found.append(f"{theme}: --{fg} on --{name} ({surface}) is {ratio:.2f}:1, "
                                     f"needs {TEXT}:1 (text on a tinted surface)")
        scrim, opacity = tokens.get("color-scrim"), tokens.get("scrim-text-min-opacity")
        on_photo = tokens.get("color-text-on-photo")
        if scrim and opacity and on_photo and HEX.match(scrim) and HEX.match(on_photo):
            under = blend(scrim, "#FFFFFF", float(opacity))
            ratio = contrast(on_photo, under)
            if ratio < TEXT:
                found.append(f"{theme}: --color-text-on-photo on the photo scrim is {ratio:.2f}:1, needs {TEXT}:1")
        else:
            found.append(f"{theme}: --color-scrim, --scrim-text-min-opacity and --color-text-on-photo "
                         "must be set, with six-digit hex colours")
    return found


def skipped_tints(path: Path) -> list[str]:
    """The --tint-* tokens that are not checked (glows, lines, borders, surfaces with transparency)."""
    css = re.sub(r"/\*.*?\*/", "", path.read_text(), flags=re.S)
    return split_tints(_block(css, ":root {") or {})[1]


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("docs/design/tokens.css")
    found = problems(path)
    for p in found:
        print(f"contrast: {p}", file=sys.stderr)
    skipped = skipped_tints(path)
    if skipped:
        print("contrast: not checked (transparency needs a backdrop): " + ", ".join(f"--{t}" for t in skipped))
    if not found:
        print(f"contrast: {path} meets WCAG 2.2 AA in both themes")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
