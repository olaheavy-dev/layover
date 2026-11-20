#!/usr/bin/env python3
"""Check Layover's design boards (docs/design/boards/) and the media register.

Fails when:
- a board (.html, .css, .svg) uses a literal colour (hex, rgb(), hsl(), color-mix() and the other colour
  functions, or a named colour) instead of a token from docs/design/tokens.css (issue #28);
- a board page's text says "safe", "safer", "safest", "safely" or "unsafe" (decision 0011, rule 6).
  "Safety" is allowed, because it is part of the FCDO's own section name, "Safety and security";
- a file in the boards folder holds a local path (/Users/, /home/, C:\\Users\\);
- a board loads a script, stylesheet, font or image from another site. Boards are self-contained:
  fonts and images are committed and registered. Ordinary links (<a href>) to other sites are allowed;
- a board page has no "Sample data, not real" label (owner: "Marked samples, one file (Recommended)");
- an image, font, video or PDF anywhere under docs/ is not named in docs/assets/README.md
  (AGENTS.md: "Media is registered first").

Colours are checked only where they are colours: .css files, <style> blocks, style="" attributes and the
SVG colour attributes (fill, stroke and so on). So "#123" in board text, "#days" in a link and "&#169;"
are not colours.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOARDS = Path("docs/design/boards")
REGISTER = Path("docs/assets/README.md")
LABEL = "Sample data, not real"

BOARD_SUFFIXES = {".html", ".css", ".svg"}
TEXT_SUFFIXES = BOARD_SUFFIXES | {".md", ".json", ".txt", ".js"}
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico", ".woff", ".woff2",
                  ".ttf", ".otf", ".mp4", ".webm", ".mov", ".mp3", ".pdf"}

# CSS named colours (CSS Color Module Level 4, https://www.w3.org/TR/css-color-4/#named-colors) and the
# system colours (https://www.w3.org/TR/css-color-4/#css-system-colors). "transparent" and "currentColor"
# are allowed: they are not colours of their own.
NAMED = set("""
aliceblue antiquewhite aqua aquamarine azure beige bisque black blanchedalmond blue blueviolet brown burlywood
cadetblue chartreuse chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan darkgoldenrod
darkgray darkgreen darkgrey darkkhaki darkmagenta darkolivegreen darkorange darkorchid darkred darksalmon
darkseagreen darkslateblue darkslategray darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray
dimgrey dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold goldenrod gray green
greenyellow grey honeydew hotpink indianred indigo ivory khaki lavender lavenderblush lawngreen lemonchiffon
lightblue lightcoral lightcyan lightgoldenrodyellow lightgray lightgreen lightgrey lightpink lightsalmon
lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue lightyellow lime limegreen linen magenta
maroon mediumaquamarine mediumblue mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen
mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin navajowhite navy oldlace olive
olivedrab orange orangered orchid palegoldenrod palegreen paleturquoise palevioletred papayawhip peachpuff peru
pink plum powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon sandybrown seagreen
seashell sienna silver skyblue slateblue slategray slategrey snow springgreen steelblue tan teal thistle tomato
turquoise violet wheat white whitesmoke yellow yellowgreen
canvas canvastext linktext visitedtext activetext buttonface buttontext buttonborder field fieldtext highlight
highlighttext selecteditem selecteditemtext mark marktext graytext accentcolor accentcolortext
""".split())

COMMENT_CSS = re.compile(r"/\*.*?\*/", re.S)
COMMENT_HTML = re.compile(r"<!--.*?-->", re.S)
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
SCRIPT_BLOCK = re.compile(r"<script[^>]*>.*?</script>", re.S | re.I)
STYLE_ATTR = re.compile(r"""\sstyle\s*=\s*(["'])(.*?)\1""", re.S | re.I)
COLOUR_ATTR = re.compile(r"""\s(fill|stroke|stop-color|flood-color|lighting-color|color|bgcolor)\s*=\s*(["'])(.*?)\2""",
                         re.S | re.I)
HEX = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
FUNC = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix|light-dark)\s*\(", re.I)
URL_REF = re.compile(r"url\(\s*['\"]?#[^)]*\)", re.I)
VAR = re.compile(r"var\([^()]*(?:\([^()]*\)[^()]*)*\)")
DECL = re.compile(r"([a-zA-Z-]+)\s*:\s*([^;{}]+)")
COLOUR_PROP = re.compile(r"color|background|fill|stroke|border|outline|shadow|column-rule|text-decoration", re.I)

SAFE = re.compile(r"\b(safe|safer|safest|safely|unsafe)\b", re.I)
TEXT_ATTR = re.compile(r"""\s(?:alt|title|aria-label|placeholder)\s*=\s*(["'])(.*?)\1""", re.S | re.I)
TAG = re.compile(r"<[^>]+>")

LOCAL_PATH = re.compile(r"/Users/|/home/[A-Za-z]|[A-Za-z]:\\Users\\")

OUTSIDE = [
    re.compile(r"""<(?:script|img|source|video|audio|iframe|embed|image|use)\b[^>]*?\s(?:src|href|xlink:href)\s*=\s*["']((?:https?:)?//[^"']+)""",
               re.I | re.S),
    re.compile(r"""<link\b[^>]*?\shref\s*=\s*["']((?:https?:)?//[^"']+)""", re.I | re.S),
    re.compile(r"""url\(\s*["']?((?:https?:)?//[^"')]+)""", re.I),
    re.compile(r"""@import\s+(?:url\()?\s*["']?((?:https?:)?//[^"')\s;]+)""", re.I),
]


def _colour_contexts(path: Path, text: str) -> list[str]:
    """The parts of a file where a value is a colour: CSS and the SVG colour attributes."""
    if path.suffix == ".css":
        return [COMMENT_CSS.sub("", text)]
    text = COMMENT_HTML.sub("", text)
    parts = [COMMENT_CSS.sub("", block) for block in STYLE_BLOCK.findall(text)]
    parts += [value for _, value in STYLE_ATTR.findall(text)]
    parts += [f"{name}: {value}" for name, _, value in COLOUR_ATTR.findall(text)]
    return parts


def _literal_colours(css: str) -> list[str]:
    css = URL_REF.sub("url(#ref)", css)
    found = HEX.findall(css) + [m.group(0) for m in FUNC.finditer(css)]
    for prop, value in DECL.findall(css):
        if not COLOUR_PROP.search(prop):
            continue
        words = re.findall(r"[a-zA-Z]+", VAR.sub(" ", value))
        found += [w.lower() for w in words if w.lower() in NAMED]
    return found


def _visible_text(html: str) -> str:
    html = COMMENT_HTML.sub("", SCRIPT_BLOCK.sub("", STYLE_BLOCK.sub("", html)))
    attrs = " ".join(value for _, value in TEXT_ATTR.findall(html))
    return TAG.sub(" ", html) + " " + attrs


def _board_problems(root: Path, path: Path) -> list[str]:
    rel = path.relative_to(root)
    text = path.read_text(errors="replace")
    found: list[str] = []
    if LOCAL_PATH.search(text):
        found.append(f"{rel}: holds a local path; remove it")
    if path.suffix not in BOARD_SUFFIXES:
        return found
    literals = [c for part in _colour_contexts(path, text) for c in _literal_colours(part)]
    if literals:
        found.append(f"{rel}: literal colour {', '.join(sorted(set(literals)))}; use a token from tokens.css")
    no_comments = COMMENT_HTML.sub("", COMMENT_CSS.sub("", text)) if path.suffix != ".css" else COMMENT_CSS.sub("", text)
    for pattern in OUTSIDE:
        for url in pattern.findall(no_comments):
            found.append(f"{rel}: loads an outside file ({url}); commit and register it instead")
    if path.suffix == ".html":
        visible = _visible_text(text)
        for word in sorted({m.group(0).lower() for m in SAFE.finditer(visible)}):
            found.append(f'{rel}: says "{word}"; Layover never calls a place safe (decision 0011, rule 6)')
        if LABEL not in visible:
            found.append(f'{rel}: needs the label "{LABEL}"')
    return found


def _register_problems(root: Path) -> list[str]:
    docs = root / "docs"
    if not docs.is_dir():
        return []
    media = sorted(p for p in docs.rglob("*") if p.is_file() and p.suffix.lower() in MEDIA_SUFFIXES)
    if not media:
        return []
    register = root / REGISTER
    listed = register.read_text() if register.is_file() else ""
    return [f"{p.relative_to(root)}: not in {REGISTER}; register its source and terms before committing it"
            for p in media if p.name not in listed]


def problems(root: Path) -> list[str]:
    found: list[str] = []
    boards = root / BOARDS
    if boards.is_dir():
        for path in sorted(boards.rglob("*")):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                found += _board_problems(root, path)
    return found + _register_problems(root)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    found = problems(root)
    for p in found:
        print(f"boards: {p}", file=sys.stderr)
    if not found:
        print("boards: no literal colours, no \"safe\", no local paths or outside files, labels present, media registered")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
