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
- an image, font, video, audio file or PDF anywhere in the repository (found with `git ls-files`; generated .png test screenshots in frontend/e2e/screenshots/ are exempt) is not in a table row of
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

Pages are read with the standard library's html.parser (issue #36), not with regular expressions, so a tag
split ("<b>sa</b>fe"), an entity ("s&#97;fe", "saf&shy;e"), an upper-case or oddly spaced tag ("</SCRIPT\t\n x>")
and a comment cannot hide anything. Attribute values arrive decoded, the way a browser reads them, and CSS
escapes ("\\73 afe", "r\\65 d", "url(\\68 ttps://...)") are decoded before the CSS is checked. Web addresses are
read the way a browser reads them (tabs and line breaks dropped, "\\" taken as "/"). The "safe" check reads all
text outside <script> and <style>, hidden or not, and the "Sample data, not real" label must be in text a
visitor sees (not in a hidden element, <head>, <title>, <template>, an attribute or a script). Media files are
found with `git ls-files` across the whole repository, so a file outside docs/ is checked too.

Not covered: HTML strings inside inline scripts (their attributes are not scanned for "safe" or for colours);
hiding by class or opacity (text a stylesheet makes invisible still counts as visible for the label); and
anything a stylesheet does to a page the check cannot see. For hidden text, the check copies only the browser's
commonest optional-tag rules (an unclosed <head>, <p>, <li>, <dt>, <dd> and <option>), not its whole tree
builder: rarer cases, such as tables repairing bad nesting, may still read differently.

What a static check cannot do: it cannot prove that a script is self-contained. A script can build an address
from pieces (`import("https://" + host)`), read one from data, or load a file through code the check never
sees, and an iframe's `srcdoc` holds a second page that is not parsed. The check finds the plain mistakes (a
literal address in a tag, a style, a script or an event handler); the boards are also reviewed by eye, and
opening them offline shows a load that fails.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

BOARDS = Path("docs/design/boards")
REGISTER = Path("docs/assets/README.md")
SCREENSHOTS = Path("frontend/e2e/screenshots")
LABEL = "Sample data, not real"

PAGE_SUFFIXES = {".html", ".htm", ".xhtml"}
BOARD_SUFFIXES = PAGE_SUFFIXES | {".css", ".svg"}
SCRIPT_SUFFIXES = {".js", ".mjs"}
TEXT_SUFFIXES = BOARD_SUFFIXES | SCRIPT_SUFFIXES | {".md", ".json", ".txt"}
MEDIA_SUFFIXES = {".png", ".apng", ".jpg", ".jpeg", ".jpe", ".jfif", ".pjpeg", ".pjp", ".gif", ".webp", ".avif",
                  ".svg", ".svgz", ".ico", ".cur", ".bmp", ".tif", ".tiff", ".heic", ".heif", ".jxl", ".psd", ".ai",
                  ".eps", ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp4", ".m4v", ".webm", ".mov", ".mkv", ".avi",
                  ".3gp", ".mp3", ".ogg", ".oga", ".opus", ".wav", ".m4a", ".aac", ".flac", ".aiff", ".wma", ".pdf"}

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

COMMENT_CSS_OPEN = "/*"
COMMENT_CSS_CLOSE = "*/"
COLOUR_ATTRS = {"fill", "stroke", "stop-color", "flood-color", "lighting-color", "color", "bgcolor"}
BODY_COLOUR_ATTRS = {"text", "link", "vlink", "alink"}  # old HTML colour attributes, valid on <body>
TEXT_ATTRS = {"alt", "title", "aria-label", "aria-description", "aria-valuetext", "aria-roledescription",
              "placeholder", "value", "content", "label"}  # and every data-* attribute
URL_ATTRS = {"src", "href", "xlink:href", "srcset", "imagesrcset", "poster", "data", "background", "action",
             "formaction", "ping", "manifest"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source",
             "track", "wbr"}
BLOCK_TAGS = {"p", "div", "li", "ul", "ol", "td", "th", "tr", "table", "h1", "h2", "h3", "h4", "h5", "h6", "br",
              "hr", "section", "article", "header", "footer", "nav", "main", "aside", "figure", "figcaption",
              "blockquote", "option", "dt", "dd", "label", "button"}  # a line break between words, unlike <b>
NOT_SHOWN_TAGS = {"head", "title", "template", "script", "style"}
# Tags that may sit in <head>. Any other tag, or visible text, ends the head even without </head>
# (WHATWG HTML, "Optional tags" and the "in head" insertion mode).
HEAD_TAGS = {"html", "head", "title", "meta", "link", "style", "script", "base", "noscript", "template"}
# Start tags that end an open <p> (WHATWG HTML, "Optional tags": "A p element's end tag may be omitted if
# ... immediately followed by" one of these), and tags that end an open element of the same kind.
P_CLOSERS = {"address", "article", "aside", "blockquote", "details", "dialog", "div", "dl", "fieldset",
             "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header",
             "hgroup", "hr", "main", "menu", "nav", "ol", "p", "pre", "search", "section", "table", "ul"}
SELF_CLOSERS = {"li": {"li"}, "dt": {"dt", "dd"}, "dd": {"dt", "dd"}, "option": {"option"}}
# Elements a search for an open element stops at (WHATWG HTML, "has an element in scope"). A <template> is
# one, so nothing inside a template can close an element outside it.
SCOPE_LIMITS = {"html", "template", "table", "td", "th", "caption", "marquee", "object", "applet"}

HEX = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b")
FUNC = re.compile(r"\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix)\s*\(", re.I)
URL_FUNC = re.compile(r"url\([^()]*\)", re.I)
STRING = re.compile(r"\"[^\"]*\"|'[^']*'")
VAR = re.compile(r"var\([^()]*(?:\([^()]*\)[^()]*)*\)")
BODY = re.compile(r"\{([^{}]*)\}")
COLOUR_PROP = re.compile(r"color|background|fill|stroke|border|outline|shadow|column-rule|text-decoration|filter"
                         r"|emphasis|caret|accent|scrollbar",
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
OUTSIDE_URL = re.compile(r"^(?:(?:https?|wss?|ftp):)?//", re.I)
CSS_OUTSIDE = re.compile(r"""(?:url\(\s*["']?|["'])\s*((?:(?:https?|wss?|ftp):)?[/\\]{2}[^"')\s,]+)""", re.I)
CSS_ESCAPE = re.compile(r"\\([0-9a-fA-F]{1,6})[ \t\n\r\f]?|\\(?:\r\n|[\n\r\f])|\\([^0-9a-fA-F\n\r\f\"'\\])")
URL_JUNK = re.compile(r"[\t\n\r]")
SPACE = re.compile(r"\s+")
SCRIPT_OUTSIDE = re.compile(r"""https?://[^\s"'`)]+|["'`]//[^\s"'`)]+""", re.I)


def _strip_css_comments(css: str) -> str:
    """Remove /* */ comments in one pass (an unclosed comment runs to the end, as in a browser)."""
    out: list[str] = []
    pos = 0
    while True:
        start = css.find(COMMENT_CSS_OPEN, pos)
        if start < 0:
            out.append(css[pos:])
            return "".join(out)
        out.append(css[pos:start])
        end = css.find(COMMENT_CSS_CLOSE, start + 2)
        if end < 0:
            return "".join(out)
        pos = end + 2


def _css_unescape_one(match: re.Match[str]) -> str:
    if match.group(1):
        code = int(match.group(1), 16)
        return chr(code) if 0 < code <= 0x10FFFF and not 0xD800 <= code <= 0xDFFF else "\ufffd"
    return match.group(2) or ""  # a backslash and a line break joins the lines; "\x" is "x"


def _css_unescape(css: str) -> str:
    """Decode CSS escapes ("\\73 afe" is "safe"). Escaped quotes and backslashes stay as they are."""
    return CSS_ESCAPE.sub(_css_unescape_one, css)


def _clean_css(css: str) -> str:
    return _css_unescape(_strip_css_comments(css))


def _normal_url(value: str) -> str:
    """An address as a browser reads it: tabs and line breaks dropped, outer spaces trimmed, "\\" as "/"."""
    return URL_JUNK.sub("", value).strip("\x00\x01\x02\x03\x04\x05\x06\x07\x08\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f ").replace("\\", "/")


def _is_outside(value: str) -> bool:
    return bool(OUTSIDE_URL.match(_normal_url(value)))


class _Page(HTMLParser):
    """What the checks need from a page, read the way a browser reads it (entities decoded, comments ignored)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, list[tuple[str, str]]]] = []
        self.styles: list[str] = []
        self.scripts: list[str] = []
        self.text: list[str] = []  # all text outside <script> and <style>
        self.visible: list[str] = []  # the part of it a visitor sees
        self._raw: str | None = None
        self._raw_text: list[str] = []
        self._stack: list[tuple[str, bool]] = []
        self._open: dict[str, int] = {}
        self._hidden = 0

    def _in_scope(self, tag: str) -> bool:
        """True if `tag` is open and no scope limit (such as a <template>) sits above it."""
        for name, _hidden in reversed(self._stack):
            if name == tag:
                return True
            if name in SCOPE_LIMITS:
                return False
        return False

    def _end_head(self) -> None:
        """Close an open <head> the way a browser does when body content starts. Inside a <template>
        nothing closes the head: the template's content is never shown."""
        if self._in_scope("head"):
            self.handle_endtag("head")

    def _close_optional(self, tag: str) -> None:
        """End an open <p>, <li>, <dt>, <dd> or <option> that this start tag ends in a browser."""
        if tag in P_CLOSERS and self._in_scope("p"):
            self.handle_endtag("p")
        for open_tag in SELF_CLOSERS.get(tag, ()):
            if self._stack and self._stack[-1][0] == open_tag:
                self.handle_endtag(open_tag)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in HEAD_TAGS:
            self._end_head()
        self._close_optional(tag)
        pairs = [(name.lower(), value or "") for name, value in attrs]
        self.tags.append((tag, pairs))
        self._break(tag)
        if tag in VOID_TAGS:
            return
        hidden = tag in NOT_SHOWN_TAGS or any(_hides(name, value) for name, value in pairs)
        self._stack.append((tag, hidden))
        self._open[tag] = self._open.get(tag, 0) + 1
        self._hidden += hidden
        if tag in ("script", "style"):
            self._raw, self._raw_text = tag, []

    def _break(self, tag: str) -> None:
        if tag in BLOCK_TAGS and not self._raw:
            self.text.append("\n")
            if not self._hidden:
                self.visible.append("\n")

    def handle_endtag(self, tag: str) -> None:
        self._break(tag)
        if tag == self._raw:
            (self.styles if tag == "style" else self.scripts).append("".join(self._raw_text))
            self._raw = None
        # A browser ignores an end tag whose element is not in scope (for example, one inside a <template>
        # whose element is outside it), so it never pops the template.
        if self._in_scope(tag) or tag in SCOPE_LIMITS and self._open.get(tag):
            while self._stack:
                name, hidden = self._stack.pop()
                self._open[name] -= 1
                self._hidden -= hidden
                if name == tag:
                    break

    def handle_data(self, data: str) -> None:
        if self._raw:
            self._raw_text.append(data)
            return
        if data.strip() and self._in_scope("head") and not self._open.get("title"):
            self._end_head()
        self.text.append(data)
        if not self._hidden:
            self.visible.append(data)

    def close(self) -> None:
        super().close()
        if self._raw:  # an unclosed <script> or <style> runs to the end of the file
            (self.styles if self._raw == "style" else self.scripts).append("".join(self._raw_text))
            self._raw = None


def _hides(name: str, value: str) -> bool:
    if name == "hidden":
        return True
    if name == "style":
        for prop, val in _declarations(value, is_body=True):
            val = val.lower().replace("!important", "").strip()
            if (prop.lower() == "display" and val == "none") or (prop.lower() == "visibility" and val == "hidden"):
                return True
    return False


def _parse(text: str) -> _Page:
    page = _Page()
    page.feed(text)
    page.close()
    return page


def _words(bits: list[str]) -> str:
    """Text with format characters (soft hyphen, zero-width space) removed and look-alike forms folded."""
    return "".join(c for c in unicodedata.normalize("NFKC", "".join(bits)) if unicodedata.category(c) != "Cf")


def _says(bits: list[str]) -> set[str]:
    """The forbidden words in some text, also when tags or entities split a word ("sa</b>fe")."""
    clean = [_words([b]) for b in bits]
    found = {m.group(0).lower() for m in SAFE.finditer(" ".join(clean))}
    return found | {m.group(0).lower() for m in SAFE.finditer("".join(clean))}


def _declarations(css: str, is_body: bool) -> list[tuple[str, str]]:
    """(property, value) pairs from rule bodies, or from one body (a style attribute)."""
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


def _refresh_target(content: str) -> str:
    """The address in a <meta http-equiv="refresh" content="0; url=..."> value, or an empty string."""
    _, _, rest = content.partition(";") if ";" in content else content.partition(",")
    rest = rest.strip()
    rest = re.sub(r"^url\s*=\s*", "", rest, flags=re.I)
    return rest.strip("\"' \t\n\r")


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

    page = _parse(text) if suffix != ".css" else _Page()
    css_parts = [text] if suffix == ".css" else list(page.styles)
    scripts = list(page.scripts)
    text_bits: list[str] = []
    style_attrs: list[str] = []
    decls: list[tuple[str, str]] = []
    for tag, attrs in page.tags:
        for name, value in attrs:
            if name == "style":
                style_attrs.append(value)
            elif name in COLOUR_ATTRS or (tag == "body" and name in BODY_COLOUR_ATTRS):
                decls.append((name if name in COLOUR_ATTRS else "color", value))
            if name in TEXT_ATTRS or name.startswith("data-"):
                text_bits.append(value)
            if name.startswith("on") or (name in ("href", "src", "action", "formaction")
                                         and _normal_url(value).lower().startswith("javascript:")):
                scripts.append(value)
            if name in URL_ATTRS and not (tag == "a" and name == "href"):
                if name in ("srcset", "imagesrcset"):
                    candidates = [c.strip().split(" ")[0] for c in value.split(",")]
                elif name == "ping":
                    candidates = value.split()
                else:
                    candidates = [value]
                outside += [_normal_url(c) for c in candidates if _is_outside(c)]
        if tag == "meta" and dict(attrs).get("http-equiv", "").strip().lower() == "refresh":
            target = _refresh_target(dict(attrs).get("content", ""))
            if _is_outside(target):
                outside.append(_normal_url(target))
    css_parts += style_attrs
    cleaned = [_clean_css(part) for part in css_parts]
    for part in cleaned[: len(cleaned) - len(style_attrs)]:
        decls += _declarations(part, is_body=False)
    for part in cleaned[len(cleaned) - len(style_attrs):]:
        decls += _declarations(part, is_body=True)
    for part in cleaned:
        outside += [_normal_url(u) for u in CSS_OUTSIDE.findall(part)]
        text_bits += [s[1:-1] for s in CSS_CONTENT.findall(part)]
    for script in scripts:
        outside += SCRIPT_OUTSIDE.findall(script)

    for name in sorted({prop for prop, _ in decls if TOKEN_DEF.match(prop)}):
        found.append(f"{rel}: defines {name}; token values live only in docs/design/tokens.css")
    literals = _literal_colours(decls)
    if literals:
        found.append(f"{rel}: literal colour {', '.join(sorted(set(literals)))}; use a token from tokens.css")
    found += [f"{rel}: loads an outside file ({u}); commit and register it instead" for u in sorted(set(outside))]

    for word in sorted(_says(text_bits + page.text)):
        found.append(f'{rel}: says "{word}"; Layover never calls a place safe (decision 0011, rule 6)')
    if suffix in PAGE_SUFFIXES and LABEL not in SPACE.sub(" ", _words(page.visible)):
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


def _repo_files(root: Path) -> list[Path]:
    """Every file git tracks or would add (not ignored). Outside a git repository: the files under docs/."""
    # Drop GIT_DIR and the other GIT_* variables a git hook sets: with them, git ignores `root` and
    # lists the repository the hook runs in.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True,
                             check=True, timeout=30, text=True, env=env).stdout.strip()
        if Path(top).resolve() == root.resolve():
            listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others",
                                     "--exclude-standard"], capture_output=True, check=True, timeout=60, env=env).stdout
            return [root / name for name in listed.decode("utf-8", errors="replace").split("\0") if name]
    except (OSError, subprocess.SubprocessError):
        pass
    print(f"boards: {root} is not a git repository (or git failed); media checked under docs/ only", file=sys.stderr)
    docs = root / "docs"
    return list(docs.rglob("*")) if docs.is_dir() else []


def _register_problems(root: Path) -> list[str]:
    # Generated test screenshots of Layover's own pages are exempt from the register (owner's decision of
    # 21 Nov 2026: register line in docs/decisions/README.md; AGENTS.md, "Media is registered first").
    exempt = root / SCREENSHOTS
    media = sorted({p for p in _repo_files(root) if p.suffix.lower() in MEDIA_SUFFIXES and p.is_file()
                    and not (p.suffix.lower() == ".png" and exempt in p.parents)})
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
    linked = set()
    for tag, attrs in _parse(index.read_text(errors="replace")).tags:
        if tag == "a":
            for name, value in attrs:
                target = value.split("#")[0].split("?")[0].strip()
                if name == "href" and target and not _is_outside(target):
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
