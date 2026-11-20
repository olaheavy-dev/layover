#!/usr/bin/env python3
"""Check Layover's design boards (docs/design/boards/) and the media register.

Fails when:
- a board (.html, .htm, .xhtml, .css, .svg) uses a literal colour (hex, rgb(), hsl(), color-mix() and the
  other colour functions, or a named colour) instead of a token from docs/design/tokens.css (issue #28);
- a board's text says "safe", "safer", "safest", "safely" or "unsafe" (decision 0011, rule 6), in visible
  text, in alt, title, aria-label, placeholder, value or content attributes, in SVG text, or in a CSS
  `content` string, and anywhere in a .js or .mjs file (strings and comments). "Safety" is allowed, because
  it is part of the FCDO's own section name, "Safety and security";
- a board defines a --color-*, --tint-*, --illus-* or --logo-* custom property (token values live only in
  docs/design/tokens.css, so the contrast check covers them); using var(--x) is fine;
- a file in the boards folder holds a local path (/Users/, /home/, C:\\Users\\);
- a board loads a script, stylesheet, font or image from another site (src, srcset, href, poster, data and
  background attributes, CSS url(), image-set() and @import, and addresses in scripts). Boards are
  self-contained: fonts and images are committed and registered. Links (<a href>) to other sites are allowed;
- a board page has no "Sample data, not real" label (owner: "Marked samples, one file (Recommended)");
- a board page in docs/design/boards/ (not index.html, not the screens/ sub-folder) is not linked from
  docs/design/boards/index.html, once index.html exists (the index is how the reviewers check coverage);
- an image, font, video, audio file or PDF anywhere under docs/ is not in a table row of
  docs/assets/README.md, named by its path from the repository root in backticks, with a non-empty Source
  and Licence cell (columns found by the header row of that table; empty, whitespace and a dash do not
  count) (AGENTS.md: "Media is registered first").

Scripts (.js, .mjs) get a pragmatic text scan, not a parser. Limits: the "safe" check reads the whole file, so
a comment or an identifier such as `safeMode` is flagged too (rename it); only `safe-area` is let through. Hex colours are flagged only when
quoted whole ("#12436E") or after a colon in a string ("color:#fff"), so a "#fade" id selector is not
flagged. rgb(, hsl( and the other colour functions are flagged anywhere. A named colour is flagged only
when assigned straight to a colour property (`.style.color = "red"`, `style.setProperty("color", "red")`,
`setAttribute("fill", "red")`); a colour built by joining strings or read from data is not seen. Outside
addresses are found in the raw text, comments included.

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
STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style\s*>", re.S | re.I)
SCRIPT_BLOCK = re.compile(r"<script[^>]*>(.*?)</script\s*>", re.S | re.I)
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

TOKEN_DEF = re.compile(r"^--(?:color|tint|illus|logo)-")
JS_HEX = re.compile(r"""(?:["'`]|:\s*)(#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4}))(?=["'`;\s)])""")
JS_PROP_COLOUR = r"(?:[\w-]*(?:color|colour|background|fill|stroke|border|outline|shadow)[\w-]*)"
JS_NAMED_ASSIGN = re.compile(
    r"""(?:\.style\.""" + JS_PROP_COLOUR + r"""\s*=|(?:setProperty|setAttribute)\(\s*["']""" + JS_PROP_COLOUR +
    r"""["']\s*,)\s*["'`]\s*([A-Za-z]+)\s*["'`]""", re.I)
JS_TOKEN_SET = re.compile(r"""setProperty\(\s*["'](--(?:color|tint|illus|logo)-[\w-]*)["']""")

SAFE = re.compile(r"\b(safe|safer|safest|safely|unsafe)\b", re.I)
JS_SAFE = re.compile(r"\b(safe|safer|safest|safely|unsafe)\b(?!-area)", re.I)  # env(safe-area-inset-*) is CSS
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


def _script_problems(rel: Path, text: str) -> list[str]:
    """The colour, token and "safe" checks for a .js or .mjs file. See the module docstring for its limits."""
    found: list[str] = []
    literals = JS_HEX.findall(text) + [m.group(0) for m in FUNC.finditer(text)]
    literals += [m.group(1).lower() for m in JS_NAMED_ASSIGN.finditer(text) if m.group(1).lower() in NAMED]
    if literals:
        found.append(f"{rel}: literal colour {', '.join(sorted(set(literals)))}; use a token from tokens.css")
    for name in sorted(set(JS_TOKEN_SET.findall(text))):
        found.append(f"{rel}: defines {name}; token values live only in docs/design/tokens.css")
    for word in sorted({m.group(0).lower() for m in JS_SAFE.finditer(text)}):
        found.append(f'{rel}: says "{word}"; Layover never calls a place safe (decision 0011, rule 6)')
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
        # Raw text: stripping /* */ would also strip a string that looks like a comment (a false pass).
        outside += SCRIPT_OUTSIDE.findall(text)
    if suffix not in BOARD_SUFFIXES:
        if suffix in SCRIPT_SUFFIXES:
            found += _script_problems(rel, text)
        return found + [f"{rel}: loads an outside file ({u}); commit and register it instead" for u in sorted(set(outside))]

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

    for name in sorted({prop for prop, _ in decls if TOKEN_DEF.match(prop)}):
        found.append(f"{rel}: defines {name}; token values live only in docs/design/tokens.css")
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


EMPTY_CELLS = {"", "-", "\u2013", "\u2014"}


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _registered(register: Path) -> tuple[set[str], set[str]]:
    """(paths with a complete row, paths whose row lacks a Source or a Licence).

    Each table's header row names its columns: "Source" and "Licence..." (or "License...") must be non-empty.
    A row under no header, or under a header without those columns, counts as incomplete.
    """
    complete: set[str] = set()
    incomplete: set[str] = set()
    if not register.is_file():
        return complete, incomplete
    lines = register.read_text().splitlines()
    source_col = licence_col = None
    header = True  # the next table line starts a table
    for n, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            header = True
            continue
        cells = _cells(line)
        if header:
            following = lines[n + 1] if n + 1 < len(lines) else ""
            is_header = bool(re.fullmatch(r"\|?[\s:|-]+\|?", following.strip())) and following.strip().startswith(("|", "-", ":"))
            source_col = licence_col = None
            if is_header:
                names = [c.lower() for c in cells]
                source_col = next((i for i, c in enumerate(names) if c == "source"), None)
                licence_col = next((i for i, c in enumerate(names) if c.startswith(("licence", "license"))), None)
                header = False
                continue
            header = False
        if re.fullmatch(r"\|?[\s:|-]+\|?", line.strip()):
            continue
        ok = (source_col is not None and licence_col is not None and max(source_col, licence_col) < len(cells)
              and cells[source_col] not in EMPTY_CELLS and cells[licence_col] not in EMPTY_CELLS)
        for path in re.findall(r"`([^`]+)`", line):
            (complete if ok else incomplete).add(path)
    return complete, incomplete


def _register_problems(root: Path) -> list[str]:
    docs = root / "docs"
    if not docs.is_dir():
        return []
    media = sorted(p for p in docs.rglob("*") if p.is_file() and p.suffix.lower() in MEDIA_SUFFIXES)
    if not media:
        return []
    complete, incomplete = _registered(root / REGISTER)
    found = []
    for p in media:
        rel = p.relative_to(root).as_posix()
        if rel in complete:
            continue
        if rel in incomplete:
            found.append(f"{rel}: its row in {REGISTER} needs a Source cell and a Licence cell that are not "
                         f"empty (under a table header that names them); register its source and terms")
        else:
            found.append(f"{rel}: not in a table row of {REGISTER} as `{rel}`; "
                         f"register its source and terms before committing it")
    return found


def _index_problems(root: Path) -> list[str]:
    boards = root / BOARDS
    index = boards / "index.html"
    if not index.is_file():
        return []
    markup = COMMENT_HTML.sub("", index.read_text(errors="replace"))
    linked = set()
    for tag, body in TAG.findall(markup):
        if tag.lower() == "a":
            for name, value in _attrs(body):
                target = value.split("#")[0].split("?")[0].strip()
                if name == "href" and target and not OUTSIDE_URL.match(target):
                    linked.add(Path(target).as_posix().removeprefix("./"))
    pages = sorted(p.name for p in boards.glob("*") if p.is_file() and p.suffix.lower() in PAGE_SUFFIXES
                   and p.name != "index.html")
    return [f"{(BOARDS / name).as_posix()}: not linked from index.html; add it to the board index"
            for name in pages if name not in linked]


def problems(root: Path) -> list[str]:
    found: list[str] = []
    boards = root / BOARDS
    if boards.is_dir():
        for path in sorted(boards.rglob("*")):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                found += _board_problems(root, path)
    return found + _index_problems(root) + _register_problems(root)


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
