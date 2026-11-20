#!/usr/bin/env python3
"""Check Layover's design boards (docs/design/boards/) and the media register.

Fails when:
- a board (.html, .htm, .xhtml, .css, .svg) uses a literal colour (hex, rgb(), hsl(), color-mix() and the
  other colour functions, or a named colour) instead of a token from docs/design/tokens.css (issue #28);
- a board's text says "safe", "safer", "safest", "safely" or "unsafe" (decision 0011, rule 6), in visible
  text, in alt, title, aria-label, placeholder, value or content attributes, in SVG text, or in a CSS
  `content` string. "Safety" is allowed, because it is part of the FCDO's own section name,
  "Safety and security";
- a file in the boards folder holds a local path (/Users/, /home/, C:\\Users\\);
- a board loads a script, stylesheet, font or image from another site (src, srcset, href, poster, data and
  background attributes, CSS url(), image-set() and @import, and addresses in scripts). Boards are
  self-contained: fonts and images are committed and registered. Links (<a href>) to other sites are allowed;
- a board page has no "Sample data, not real" label (owner: "Marked samples, one file (Recommended)");
- an image, font, video, audio file or PDF anywhere under docs/ is not in a table row of
  docs/assets/README.md, named by its path from the repository root in backticks
  (AGENTS.md: "Media is registered first").

Colours are checked only in declaration values and colour attributes: .css files, <style> blocks,
style="" attributes and the SVG colour attributes (fill, stroke and so on). So "#123" in board text,
"#days" in a link, a "#fade" selector and "&#169;" are not colours.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BOARDS = Path("docs/design/boards")
REGISTER = Path("docs/assets/README.md")
LABEL = "Sample data, not real"

PAGE_SUFFIXES = {".html", ".htm", ".xhtml"}
BOARD_SUFFIXES = PAGE_SUFFIXES | {".css", ".svg"}
SCRIPT_SUFFIXES = {".js", ".mjs"}
TEXT_SUFFIXES = BOARD_SUFFIXES | SCRIPT_SUFFIXES | {".md", ".json", ".txt"}
MEDIA_SUFFIXES = {".png", ".apng", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico", ".bmp", ".tif",
                  ".tiff", ".heic", ".jxl", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".webm", ".mov",
                  ".mp3", ".ogg", ".wav", ".m4a", ".pdf"}

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
SCRIPT_BLOCK = re.compile(r"<script[^>]*>(.*?)</script>", re.S | re.I)
TAG = re.compile(r"<([a-zA-Z][\w:-]*)((?:[^>\"']|\"[^\"]*\"|'[^']*')*)>", re.S)
ATTR = re.compile(r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>"']+))""", re.S)
COLOUR_ATTRS = {"fill", "stroke", "stop-color", "flood-color", "lighting-color", "color", "bgcolor"}
TEXT_ATTRS = {"alt", "title", "aria-label", "placeholder", "value", "content"}
URL_ATTRS = {"src", "href", "xlink:href", "srcset", "poster", "data", "background", "action", "formaction"}

HEX = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
FUNC = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\s*\(", re.I)
URL_FUNC = re.compile(r"url\([^)]*\)", re.I)
STRING = re.compile(r"\"[^\"]*\"|'[^']*'")
VAR = re.compile(r"var\([^()]*(?:\([^()]*\)[^()]*)*\)")
BODY = re.compile(r"\{([^{}]*)\}")
COLOUR_PROP = re.compile(r"color|background|fill|stroke|border|outline|shadow|column-rule|text-decoration|filter",
                         re.I)
CSS_CONTENT = re.compile(r"content\s*:\s*(\"[^\"]*\"|'[^']*')", re.I)

SAFE = re.compile(r"\b(safe|safer|safest|safely|unsafe)\b", re.I)
LOCAL_PATH = re.compile(r"(?<![\w.%-])(?:/Users/|/home/[A-Za-z])|[A-Za-z]:\\Users\\")
OUTSIDE_URL = re.compile(r"^\s*(?:https?:)?//", re.I)
CSS_OUTSIDE = re.compile(r"""(?:url\(\s*["']?|["'])\s*((?:https?:)?//[^"')\s,]+)""", re.I)
SCRIPT_OUTSIDE = re.compile(r"""https?://[^\s"'`)]+|["'`]//[^\s"'`)]+""", re.I)


def _attrs(tag_body: str) -> list[tuple[str, str]]:
    """(name, value) for each attribute, quoted or not."""
    return [(name.lower(), dq or sq or bare) for name, dq, sq, bare in ATTR.findall(tag_body)]


def _declarations(css: str, is_body: bool) -> list[tuple[str, str]]:
    """(property, value) pairs from rule bodies, or from one body (a style attribute)."""
    css = COMMENT_CSS.sub("", css)
    bodies = [css] if is_body else BODY.findall(css)
    out = []
    for body in bodies:
        for decl in body.split(";"):
            if ":" in decl:
                prop, value = decl.split(":", 1)
                out.append((prop.strip(), value.strip()))
    return out


def _literal_colours(decls: list[tuple[str, str]]) -> list[str]:
    found: list[str] = []
    for prop, value in decls:
        plain = STRING.sub(" ", URL_FUNC.sub(" ", value))
        found += HEX.findall(plain) + [m.group(0) for m in FUNC.finditer(plain)]
        if prop.startswith("--") or COLOUR_PROP.search(prop):
            words = re.findall(r"[a-zA-Z]+", VAR.sub(" ", plain))
            found += [w.lower() for w in words if w.lower() in NAMED]
    return found


def _css_parts(text: str, suffix: str) -> list[str]:
    if suffix == ".css":
        return [text]
    return STYLE_BLOCK.findall(COMMENT_HTML.sub("", text))


def _board_problems(root: Path, path: Path) -> list[str]:
    rel = path.relative_to(root)
    suffix = path.suffix.lower()
    text = path.read_text(errors="replace")
    found: list[str] = []
    if LOCAL_PATH.search(text):
        found.append(f"{rel}: holds a local path; remove it")
    outside: list[str] = []
    if suffix in SCRIPT_SUFFIXES:
        outside += SCRIPT_OUTSIDE.findall(COMMENT_CSS.sub("", text))
    if suffix not in BOARD_SUFFIXES:
        return found + [f"{rel}: loads an outside file ({u}); commit and register it instead" for u in outside]

    markup = COMMENT_HTML.sub("", text) if suffix != ".css" else ""
    css_parts = _css_parts(text, suffix)
    decls = [d for part in css_parts for d in _declarations(part, is_body=False)]
    text_bits: list[str] = []
    for tag, body in TAG.findall(markup):
        for name, value in _attrs(body):
            if name == "style":
                decls += _declarations(value, is_body=True)
                css_parts.append(value)
            elif name in COLOUR_ATTRS:
                decls.append((name, value))
            if name in TEXT_ATTRS:
                text_bits.append(value)
            if name in URL_ATTRS and not (tag.lower() == "a" and name == "href"):
                candidates = [c.strip().split(" ")[0] for c in value.split(",")] if name == "srcset" else [value]
                outside += [c.strip() for c in candidates if OUTSIDE_URL.match(c)]
    for part in css_parts:
        outside += CSS_OUTSIDE.findall(COMMENT_CSS.sub("", part))
        text_bits += [s[1:-1] for s in CSS_CONTENT.findall(part)]
    for script in SCRIPT_BLOCK.findall(markup):
        outside += SCRIPT_OUTSIDE.findall(script)

    literals = _literal_colours(decls)
    if literals:
        found.append(f"{rel}: literal colour {', '.join(sorted(set(literals)))}; use a token from tokens.css")
    found += [f"{rel}: loads an outside file ({u}); commit and register it instead" for u in sorted(set(outside))]

    if suffix != ".css":
        visible = TAG.sub(" ", STYLE_BLOCK.sub(" ", SCRIPT_BLOCK.sub(" ", markup)))
        text_bits.append(visible)
    else:
        visible = ""
    for word in sorted({m.group(0).lower() for m in SAFE.finditer(" ".join(text_bits))}):
        found.append(f'{rel}: says "{word}"; Layover never calls a place safe (decision 0011, rule 6)')
    if suffix in PAGE_SUFFIXES and LABEL not in visible:
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
    rows = [line for line in register.read_text().splitlines() if line.lstrip().startswith("|")] \
        if register.is_file() else []
    named = {m for row in rows for m in re.findall(r"`([^`]+)`", row)}
    return [f"{p.relative_to(root).as_posix()}: not in a table row of {REGISTER} as "
            f"`{p.relative_to(root).as_posix()}`; register its source and terms before committing it"
            for p in media if p.relative_to(root).as_posix() not in named]


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
