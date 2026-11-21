"""Tests for tools/check_boards.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import contextlib
import io
import re
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_boards as cb  # noqa: E402

LABEL = "Sample data, not real"
REG_HEAD = ("| File | What it is | Source | Author or owner | Licence and terms | Date checked |\n"
            "|---|---|---|---|---|---|\n")


def reg_row(path: str, source: str = "Unsplash", licence: str = "Unsplash License") -> str:
    return f"| `{path}` | a file | {source} | someone | {licence} | 20 Nov 2026 |\n"

GOOD_PAGE = f"""<!doctype html>
<html lang="en-GB">
<head>
<link rel="stylesheet" href="../tokens.css">
<style>
  /* A comment may name #FFFFFF or red without failing. */
  body {{ background: var(--color-bg-primary); color: var(--color-text-primary); }}
  .card {{ border: 1px solid var(--color-border-primary); box-shadow: var(--shadow-md); }}
  .clear {{ background: transparent; color: currentColor; }}
</style>
</head>
<body>
<p class="sample">{LABEL}</p>
<a href="#days">Days</a> <a href="#fade">Fade</a>
<a href="https://www.gov.uk/foreign-travel-advice/portugal">FCDO travel advice</a>
<p>FCDO safety and security advice, updated 1 May. Issue #123 is fine in text.</p>
<svg><circle fill="var(--color-chart-1)" stroke="currentColor"/><use href="#abc"/>
<rect fill="url(#bead)"/></svg>
<p>&#x2014; &#169;</p>
</body>
</html>
"""


class Boards(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.boards = self.root / "docs" / "design" / "boards"
        self.boards.mkdir(parents=True)
        quiet = contextlib.redirect_stderr(io.StringIO())  # the "not a git repository" note, in every test
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def assertOutside(self, found: list[str], url: str, name: str = "welcome.html") -> None:
        """The exact message for one outside address, so a host name is never matched as a substring."""
        folder = "docs/design/boards/"
        self.assertIn(f"{folder}{name}: loads an outside file ({url}); commit and register it instead", found)

    def page(self, text: str, name: str = "welcome.html") -> list[str]:
        self.write(f"docs/design/boards/{name}", text)
        return cb.problems(self.root)

    # Passing cases

    def test_no_boards_folder_passes(self) -> None:
        self.boards.rmdir()
        self.assertEqual(cb.problems(self.root), [])

    def test_good_page_passes(self) -> None:
        self.assertEqual(self.page(GOOD_PAGE), [])

    # Literal colours

    def test_hex_colour_in_style_block_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("var(--color-bg-primary)", "#F7F6F3"))
        self.assertTrue(any("literal colour" in p and "#F7F6F3" in p for p in found), found)

    def test_short_hex_in_style_attribute_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace('<p class="sample">', '<p class="sample" style="color: #fff">'))
        self.assertTrue(any("literal colour" in p and "#fff" in p for p in found), found)

    def test_rgb_function_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("var(--shadow-md)", "0 1px 2px rgba(0, 0, 0, 0.2)"))
        self.assertTrue(any("literal colour" in p and "rgba(" in p for p in found), found)

    def test_color_mix_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("transparent;", "color-mix(in srgb, var(--color-accent-primary) 50%, white);"))
        self.assertTrue(any("literal colour" in p and "color-mix(" in p for p in found), found)

    def test_named_colour_in_css_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("color: var(--color-text-primary)", "color: Navy"))
        self.assertTrue(any("literal colour" in p and "navy" in p for p in found), found)

    def test_named_colour_in_svg_attribute_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace('stroke="currentColor"', 'stroke="white"'))
        self.assertTrue(any("literal colour" in p and "white" in p for p in found), found)

    def test_hex_in_svg_file_fails(self) -> None:
        self.write("docs/assets/README.md", "| `docs/design/boards/wave.svg` | drawn for Layover |")
        self.write("docs/design/boards/wave.svg", '<svg><path fill="#12436E"/></svg>')
        found = cb.problems(self.root)
        self.assertTrue(any("wave.svg" in p and "literal colour" in p for p in found), found)

    def test_hex_in_css_file_fails(self) -> None:
        self.write("docs/design/boards/boards.css", ".x { background-color: #000000; }")
        found = cb.problems(self.root)
        self.assertTrue(any("boards.css" in p and "#000000" in p for p in found), found)

    # The word "safe" (decision 0011, rule 6)

    def test_safe_in_text_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("Issue #123", "Lisbon is safe for families. Issue #123"))
        self.assertTrue(any('"safe"' in p for p in found), found)

    def test_safest_in_alt_text_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("<svg>", '<img alt="The safest beach" src="beach.jpg"><svg>'))
        self.assertTrue(any('"safest"' in p for p in found), found)

    def test_safe_in_a_class_name_or_style_passes(self) -> None:
        page = GOOD_PAGE.replace('<p class="sample">', '<p class="sample safe-area">').replace(
            ".clear {", ".pad { padding: env(safe-area-inset-top); }\n  .clear {")
        self.assertEqual(self.page(page), [])

    # Local paths

    def test_local_path_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("Issue #123", "Saved from /Users/someone/Desktop"))
        self.assertTrue(any("local path" in p for p in found), found)

    def test_local_path_in_sample_data_fails(self) -> None:
        self.write("docs/design/boards/sample-data.md", "Exported from /home/someone/trip.json")
        found = cb.problems(self.root)
        self.assertTrue(any("sample-data.md" in p and "local path" in p for p in found), found)

    # Outside resources: boards load nothing from other sites

    def test_outside_stylesheet_fails(self) -> None:
        page = GOOD_PAGE.replace('href="../tokens.css"', 'href="https://fonts.googleapis.com/css2?family=Source+Serif+4"')
        found = self.page(page)
        self.assertOutside(found, "https://fonts.googleapis.com/css2?family=Source+Serif+4")

    def test_outside_script_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("</body>", '<script src="//unpkg.com/x.js"></script></body>'))
        self.assertOutside(found, "//unpkg.com/x.js")

    def test_hot_linked_image_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("<svg>", '<img alt="" src="https://images.unsplash.com/photo-1"><svg>'))
        self.assertOutside(found, "https://images.unsplash.com/photo-1")

    def test_outside_font_in_css_fails(self) -> None:
        page = GOOD_PAGE.replace("<style>", "<style>\n  @font-face { src: url(https://example.com/f.woff2); }")
        found = self.page(page)
        self.assertOutside(found, "https://example.com/f.woff2")

    def test_outside_link_to_a_page_passes(self) -> None:
        self.assertEqual(self.page(GOOD_PAGE.replace("FCDO travel advice", "FCDO travel advice (opens GOV.UK)")), [])

    # Sample label (owner: "Marked samples, one file (Recommended)")

    def test_page_without_sample_label_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace(LABEL, "Welcome"))
        self.assertTrue(any("welcome.html" in p and LABEL in p for p in found), found)

    # Asset register (AGENTS.md: media is registered first)

    def test_unregistered_image_fails(self) -> None:
        self.write("docs/design/boards/img/lisbon.jpg", "x")
        found = cb.problems(self.root)
        self.assertTrue(any("lisbon.jpg" in p and "docs/assets/README.md" in p for p in found), found)

    def test_registered_image_passes(self) -> None:
        self.write("docs/assets/README.md", REG_HEAD + reg_row("docs/design/boards/img/lisbon.jpg"))
        self.write("docs/design/boards/img/lisbon.jpg", "x")
        self.assertEqual(cb.problems(self.root), [])

    def test_unregistered_font_anywhere_in_docs_fails(self) -> None:
        self.write("docs/assets/README.md", "| `docs/design/boards/img/lisbon.jpg` | Unsplash |")
        self.write("docs/assets/fonts/SourceSans3.woff2", "x")
        found = cb.problems(self.root)
        self.assertTrue(any("SourceSans3.woff2" in p for p in found), found)

    # Regression tests from the pre-push review of #31

    def test_outside_srcset_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("<svg>", '<img alt="" src="a.jpg" srcset="b.jpg 1x, https://images.unsplash.com/p 2x"><svg>'))
        self.assertOutside(found, "https://images.unsplash.com/p")

    def test_outside_poster_and_object_data_fail(self) -> None:
        page = GOOD_PAGE.replace("<svg>", '<video poster="https://x.test/p.jpg"></video><object data="https://y.test/o"></object><svg>')
        found = self.page(page)
        self.assertOutside(found, "https://x.test/p.jpg")
        self.assertOutside(found, "https://y.test/o")

    def test_unquoted_and_spaced_outside_src_fail(self) -> None:
        page = GOOD_PAGE.replace("</body>", '<script src=https://unpkg.com/x.js></script><img alt="" src=" https://z.test/i.jpg"></body>')
        found = self.page(page)
        self.assertOutside(found, "https://unpkg.com/x.js")
        self.assertOutside(found, "https://z.test/i.jpg")

    def test_outside_import_in_inline_script_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("</body>", '<script type="module">import x from "https://esm.sh/x";</script></body>'))
        self.assertOutside(found, "https://esm.sh/x")

    def test_outside_image_set_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace(".clear {", '.hero { background-image: image-set("https://cdn.test/a.jpg" 1x); }\n  .clear {'))
        self.assertOutside(found, "https://cdn.test/a.jpg")

    def test_outside_address_in_js_file_fails(self) -> None:
        self.write("docs/design/boards/switch.js", 'const u = "https://cdn.test/lib.js"; // a comment // is fine')
        found = cb.problems(self.root)
        self.assertOutside(found, "https://cdn.test/lib.js", "switch.js")

    def test_upper_case_and_htm_pages_are_checked(self) -> None:
        bad = GOOD_PAGE.replace('<p class="sample">', '<p class="sample" style="color: #fff">')
        found = self.page(bad, name="A.HTML") + self.page(bad, name="b.htm")
        self.assertTrue(any("A.HTML" in p for p in found) and any("b.htm" in p for p in found), found)

    def test_safe_in_svg_text_fails(self) -> None:
        self.write("docs/assets/README.md", "| `docs/design/boards/poster.svg` | drawn for Layover |")
        self.write("docs/design/boards/poster.svg", "<svg><text>Safe travels</text></svg>")
        found = cb.problems(self.root)
        self.assertTrue(any("poster.svg" in p and '"safe"' in p for p in found), found)

    def test_safe_in_value_attribute_and_css_content_fail(self) -> None:
        page = GOOD_PAGE.replace("<svg>", '<input value="Safe trip"><svg>').replace(".clear {", '.x::after { content: "unsafe"; }\n  .clear {')
        found = self.page(page)
        self.assertTrue(any('"safe"' in p for p in found) and any('"unsafe"' in p for p in found), found)

    def test_named_colour_in_custom_property_and_filter_fails(self) -> None:
        page = GOOD_PAGE.replace(".clear {", ":root { --brand: navy; }\n  .glow { filter: drop-shadow(0 0 2px red); }\n  .clear {")
        found = self.page(page)
        self.assertTrue(any("navy" in p and "red" in p for p in found), found)

    def test_register_needs_the_full_path_in_a_table_row(self) -> None:
        # "lisbon.jpg" in prose, and "data.png" containing "a.png", must not count as registered.
        self.write("docs/assets/README.md", "Removed: `docs/design/boards/lisbon.jpg` (licence unclear)\n| `docs/x/data.png` | x |")
        self.write("docs/design/boards/lisbon.jpg", "x")
        self.write("docs/design/boards/a.png", "x")
        found = cb.problems(self.root)
        self.assertTrue(any("lisbon.jpg" in p for p in found) and any("boards/a.png" in p for p in found), found)

    def test_more_media_types_are_registered(self) -> None:
        self.write("docs/design/boards/scan.tiff", "x")
        found = cb.problems(self.root)
        self.assertTrue(any("scan.tiff" in p for p in found), found)

    def test_no_false_positives(self) -> None:
        # Colour words in file names, a "#fade" selector, a "#123" string, light-dark() with tokens,
        # and "/home/" inside a web address are all fine.
        self.write("docs/assets/README.md", REG_HEAD + reg_row("docs/design/boards/img/red-door.jpg"))
        self.write("docs/design/boards/img/red-door.jpg", "x")
        page = GOOD_PAGE.replace(".clear {", """.door { background: url(img/red-door.jpg); }
  #fade { opacity: 0; }
  .tag::before { content: "#123"; }
  .t { color: light-dark(var(--color-text-primary), var(--color-text-secondary)); }
  .clear {""").replace("Issue #123", 'See <a href="https://example.org/en/home/about">this page</a>.')
        self.assertEqual(self.page(page), [])

    # Gap 1: .js files get the same "safe" and literal-colour checks

    def js(self, text: str) -> list[str]:
        self.write("docs/design/boards/switch.js", text)
        return cb.problems(self.root)

    def test_safe_in_js_string_and_comment_fails(self) -> None:
        # Expected failure before the fix: .js files are only scanned for local paths and outside addresses.
        found = self.js('el.textContent = "Lisbon is safe";\n// the safest option\n')
        self.assertTrue(any("switch.js" in p and '"safe"' in p for p in found), found)
        self.assertTrue(any("switch.js" in p and '"safest"' in p for p in found), found)

    def test_safety_and_safe_area_in_js_pass(self) -> None:
        self.assertEqual(self.js('el.textContent = "Safety and security"; el.style.padding = "env(safe-area-inset-top)";'), [])

    def test_hex_and_functions_in_js_fail(self) -> None:
        for code, needle in (('el.style.color = "#12436E";', "#12436E"),
                             ("ctx.fillStyle = '#fff';", "#fff"),
                             ('el.style.background = `rgba(0, 0, 0, 0.5)`;', "rgba("),
                             ('const c = "hsl(200 50% 40%)";', "hsl(")):
            with self.subTest(code=code):
                found = self.js(code)
                self.assertTrue(any("switch.js" in p and "literal colour" in p and needle in p for p in found), found)

    def test_named_colour_assigned_to_a_colour_property_in_js_fails(self) -> None:
        for code in ('el.style.color = "red";',
                     "el.style.backgroundColor = 'Navy';",
                     "el.style.setProperty('color', 'red');",
                     "el.setAttribute('fill', \"white\");"):
            with self.subTest(code=code):
                found = self.js(code)
                self.assertTrue(any("switch.js" in p and "literal colour" in p for p in found), found)

    def test_js_with_tokens_and_colour_words_elsewhere_passes(self) -> None:
        code = ('el.style.color = "var(--color-text-primary)"; el.style.setProperty("background", "var(--color-bg-secondary)");\n'
                'const label = "red"; const w = "white"; el.className = "red-door";\n'
                'el.style.color = "currentColor";')
        self.assertEqual(self.js(code), [])

    def test_js_comment_looking_text_in_a_string_does_not_hide_an_outside_address(self) -> None:
        # The string below contains "/*" and then "*/" later, so stripping /* */ would remove the address.
        found = self.js('const a = "/*"; const u = "https://cdn.test/lib.js"; const b = "*/";')
        self.assertOutside(found, "https://cdn.test/lib.js", "switch.js")

    def test_inline_script_outside_address_after_slash_star_string_fails(self) -> None:
        page = GOOD_PAGE.replace("</body>", '<script>const a = "/*"; fetch("https://cdn.test/x"); const b = "*/";</script></body>')
        found = self.page(page)
        self.assertOutside(found, "https://cdn.test/x")

    # Gap 2: token values live only in tokens.css

    def test_defining_a_token_in_a_style_block_fails(self) -> None:
        for prop in ("--color-text-primary", "--tint-glow", "--illus-water", "--logo-ink"):
            with self.subTest(prop=prop):
                found = self.page(GOOD_PAGE.replace(".clear {", ".x { %s: var(--color-accent-primary); }\n  .clear {" % prop))
                self.assertTrue(any("welcome.html" in p and prop in p and "tokens.css" in p for p in found), found)

    def test_defining_a_token_in_a_style_attribute_or_css_file_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace('<p class="sample">', '<p class="sample" style="--color-bg-primary: var(--color-bg-tertiary)">'))
        self.assertTrue(any("--color-bg-primary" in p for p in found), found)
        self.write("docs/design/boards/boards.css", ":root { --color-accent-primary: var(--color-chart-1); }")
        found = cb.problems(self.root)
        self.assertTrue(any("boards.css" in p and "--color-accent-primary" in p for p in found), found)

    def test_defining_a_token_from_js_fails(self) -> None:
        found = self.js("document.documentElement.style.setProperty('--color-bg-primary', 'var(--color-bg-tertiary)');")
        self.assertTrue(any("switch.js" in p and "--color-bg-primary" in p for p in found), found)

    def test_using_tokens_and_defining_other_properties_passes(self) -> None:
        page = GOOD_PAGE.replace(".clear {", ".x { --gap: 8px; --card-pad: 12px; color: var(--color-text-primary); }\n  .clear {")
        self.assertEqual(self.page(page), [])

    # Gap 3: a register row needs a Source and a Licence

    def registered(self, row: str) -> list[str]:
        self.write("docs/assets/README.md", REG_HEAD + row)
        self.write("docs/design/boards/img/lisbon.jpg", "x")
        return cb.problems(self.root)

    def test_row_with_empty_or_dash_source_or_licence_fails(self) -> None:
        # Expected failure before the fix: any table row naming the path counts as registered.
        for source, licence in (("", "Unsplash License"), ("   ", "Unsplash License"), ("\u2014", "Unsplash License"),
                                ("Unsplash", ""), ("Unsplash", "  "), ("Unsplash", "\u2014"), ("Unsplash", "-")):
            with self.subTest(source=source, licence=licence):
                found = self.registered(reg_row("docs/design/boards/img/lisbon.jpg", source, licence))
                self.assertTrue(any("lisbon.jpg" in p and "Source" in p and "Licence" in p for p in found), found)

    def test_row_with_source_and_licence_passes(self) -> None:
        self.assertEqual(self.registered(reg_row("docs/design/boards/img/lisbon.jpg")), [])

    def test_row_under_no_header_is_not_registered(self) -> None:
        self.write("docs/assets/README.md", "| `docs/design/boards/img/lisbon.jpg` | Unsplash | Unsplash License |")
        self.write("docs/design/boards/img/lisbon.jpg", "x")
        found = cb.problems(self.root)
        self.assertTrue(any("lisbon.jpg" in p for p in found), found)

    def test_columns_are_found_by_each_tables_own_header(self) -> None:
        # Second table lists the columns in another order; the licence is empty there.
        self.write("docs/assets/README.md", REG_HEAD + reg_row("docs/design/boards/img/a.jpg") +
                   "\n| Licence | File | Source |\n|---|---|---|\n| MIT | `docs/design/boards/img/b.jpg` | Lucide |\n"
                   "|  | `docs/design/boards/img/c.jpg` | Lucide |\n")
        for n in "abc":
            self.write(f"docs/design/boards/img/{n}.jpg", "x")
        found = cb.problems(self.root)
        self.assertEqual([p.split(":")[0] for p in found], ["docs/design/boards/img/c.jpg"], found)

    # Gap 5: closing tags may hold whitespace

    def test_style_closer_with_whitespace_is_still_scanned(self) -> None:
        # "</style >" is a valid closer; without the fix the block is not found and its colour is missed.
        page = GOOD_PAGE.replace("</style>", "</style >").replace("var(--color-bg-primary)", "#F7F6F3", 1)
        found = self.page(page)
        self.assertTrue(any("literal colour" in p and "#F7F6F3" in p for p in found), found)

    def test_script_closer_with_whitespace_is_still_scanned(self) -> None:
        page = GOOD_PAGE.replace("</body>", '<script>import x from "https://esm.sh/x";</script ></body>')
        found = self.page(page)
        self.assertOutside(found, "https://esm.sh/x")
        # the script is not read as visible text either
        page = GOOD_PAGE.replace("</body>", "<script>var s = 'safe';</script\t\n></body>")
        self.assertEqual(self.page(page), [])

    # The board index (docs/design/boards/index.html) links every board page

    def index(self, *hrefs: str) -> None:
        links = " ".join(f'<a href="{h}">board</a>' for h in hrefs)
        self.write("docs/design/boards/index.html", GOOD_PAGE.replace("<a href=\"#days\">", links + " <a href=\"#days\">"))

    def test_board_page_missing_from_the_index_fails(self) -> None:
        # Expected failure before the check exists: nothing looks at index.html, so no problem is reported.
        self.write("docs/design/boards/welcome.html", GOOD_PAGE)
        self.write("docs/design/boards/booking.html", GOOD_PAGE)
        self.index("welcome.html")
        found = cb.problems(self.root)
        self.assertEqual([p for p in found if "not linked" in p],
                         ["docs/design/boards/booking.html: not linked from index.html; add it to the board index"], found)

    def test_index_that_links_every_board_page_passes(self) -> None:
        self.write("docs/design/boards/welcome.html", GOOD_PAGE)
        self.write("docs/design/boards/booking.html", GOOD_PAGE)
        self.index("welcome.html", "booking.html#top")  # a fragment still counts as a link
        self.assertEqual(cb.problems(self.root), [])

    def test_screens_in_the_sub_folder_need_no_index_link(self) -> None:
        self.write("docs/design/boards/screens/welcome.html", GOOD_PAGE)
        self.index()
        self.assertEqual(cb.problems(self.root), [])

    def test_a_link_to_another_site_does_not_count(self) -> None:
        self.write("docs/design/boards/welcome.html", GOOD_PAGE)
        self.index("https://example.org/welcome.html")
        found = cb.problems(self.root)
        self.assertTrue(any("welcome.html" in p and "not linked" in p for p in found), found)

    # Issue #36: the checks read the page with html.parser, so tags, entities and escapes cannot hide anything

    def safe_found(self, found: list[str]) -> bool:
        return any('says "safe"' in p for p in found)

    def test_safe_split_by_tags_or_entities_fails(self) -> None:
        # Expected failure before the fix: the visible text is found by stripping tags with a regex and
        # entities are never decoded, so "sa</b>fe", "s&#97;fe" and "saf&shy;e" do not read as "safe".
        for text in ("Lisbon is <b>sa</b>fe", "Lisbon is s&#97;fe", "Lisbon is saf&shy;e", "Lisbon is s&#x61;fe",
                     "Lisbon is sa<span>f</span><i>e</i>", "Lisbon is sa&#8203;fe", "Lisbon is <b>sa</b><!-- x -->fe"):
            with self.subTest(text=text):
                self.assertTrue(self.safe_found(self.page(GOOD_PAGE.replace("Issue #123", text + ". Issue #123"))))

    def test_safe_in_more_attributes_fails(self) -> None:
        for attr in ("aria-description", "aria-valuetext", "label", "data-note", "aria-roledescription"):
            with self.subTest(attr=attr):
                found = self.page(GOOD_PAGE.replace("<svg>", f'<option {attr}="A safe choice"></option><svg>'))
                self.assertTrue(self.safe_found(found), found)

    def test_safe_in_title_and_svg_title_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("<svg>", "<svg><title>Safe place</title>"))
        self.assertTrue(self.safe_found(found), found)

    def test_safe_with_a_css_escape_in_content_fails(self) -> None:
        for content in (r"\73 afe", r"\000073afe", r"s\61 fe", "sa\\\nfe"):
            with self.subTest(content=content):
                found = self.page(GOOD_PAGE.replace(".clear {", '.x::after { content: "%s"; }\n  .clear {' % content))
                self.assertTrue(self.safe_found(found), found)

    def test_words_that_only_touch_the_word_safe_pass(self) -> None:
        # "Safety", "unsafely"-like split words across separate sentences are judged on whole words only.
        page = GOOD_PAGE.replace("Issue #123", "<b>Safety</b> and security. The <i>sa</i> <i>fe</i> are separate words")
        self.assertEqual(self.page(page), [])

    def test_entity_and_escaped_colours_fail(self) -> None:
        cases = (('<p class="sample" style="color:&#35;ff0000">', "#ff0000"),
                 ('<p class="sample" style="color:&num;ff0000">', "#ff0000"),
                 ('<p class="sample" style="color:r&#101;d">', "red"),
                 ('<p class="sample" style="background:&#x23;fff">', "#fff"))
        for opening, needle in cases:
            with self.subTest(opening=opening):
                found = self.page(GOOD_PAGE.replace('<p class="sample">', opening))
                self.assertTrue(any("literal colour" in p and needle in p for p in found), found)
        for css, needle in ((r"color: r\65 d;", "red"), (r"color: \23 ff0000;", "#ff0000"), (r"color: \72 gb(1 2 3);", "rgb(")):
            with self.subTest(css=css):
                found = self.page(GOOD_PAGE.replace("transparent;", css))
                self.assertTrue(any("literal colour" in p and needle in p for p in found), found)

    def test_entity_in_a_style_block_is_not_a_colour(self) -> None:
        # A browser does not decode entities inside <style>, so "&#35;fff" there is not a colour.
        self.assertEqual(self.page(GOOD_PAGE.replace(".clear {", '.x::before { content: "&#35;fff"; }\n  .clear {')), [])

    def test_more_colour_properties_and_old_colour_attributes_fail(self) -> None:
        found = self.page(GOOD_PAGE.replace(".clear {", ".x { text-emphasis: red; caret-color: blue; accent-color: green; }\n  .clear {"))
        self.assertTrue(any("literal colour" in p and "red" in p and "blue" in p and "green" in p for p in found), found)
        for attr in ("text", "link", "vlink", "alink", "bgcolor"):
            with self.subTest(attr=attr):
                found = self.page(GOOD_PAGE.replace("<body>", f'<body {attr}="#ff0000">'))
                self.assertTrue(any("literal colour" in p and "#ff0000" in p for p in found), found)

    def test_outside_loads_hidden_by_entities_or_slashes_fail(self) -> None:
        cases = (('<link rel="stylesheet" href="&#104;ttps://x.test/a.css">', "https://x.test/a.css"),
                 ('<script src="&#x2f;&#x2f;x.test/a.js"></script>', "//x.test/a.js"),
                 ('<script src="\\\\x.test/a.js"></script>', "//x.test/a.js"),
                 ('<img alt="" src="ht\ntps://x.test/a.jpg">', "https://x.test/a.jpg"),
                 ('<img alt="" src="\thttps://x.test/a.jpg">', "https://x.test/a.jpg"),
                 ('<img alt="" src="HTTPS://x.test/a.jpg">', "HTTPS://x.test/a.jpg"))
        for tag, url in cases:
            with self.subTest(tag=tag):
                self.assertOutside(self.page(GOOD_PAGE.replace("<svg>", tag + "<svg>")), url)

    def test_outside_url_with_a_css_escape_fails(self) -> None:
        page = GOOD_PAGE.replace(".clear {", ".x { background: url(\\68 ttps://x.test/a.png); }\n  .clear {")
        self.assertOutside(self.page(page), "https://x.test/a.png")

    def test_meta_refresh_and_ping_fail(self) -> None:
        for head, url in (('<meta http-equiv="refresh" content="0; url=https://x.test/go">', "https://x.test/go"),
                          ('<meta http-equiv="Refresh" content="5;URL=\'//x.test/go\'">', "//x.test/go")):
            with self.subTest(head=head):
                self.assertOutside(self.page(GOOD_PAGE.replace("</head>", head + "</head>")), url)
        found = self.page(GOOD_PAGE.replace("<svg>", '<a href="#x" ping="https://x.test/p https://y.test/q">x</a><svg>'))
        self.assertOutside(found, "https://x.test/p")
        self.assertOutside(found, "https://y.test/q")

    def test_meta_refresh_to_a_board_page_passes(self) -> None:
        self.assertEqual(self.page(GOOD_PAGE.replace("</head>", '<meta http-equiv="refresh" content="0; url=index.html"></head>')), [])

    def test_outside_address_in_an_event_handler_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("<svg>", """<button onclick="fetch('https://x.test/hit')">go</button><svg>"""))
        self.assertOutside(found, "https://x.test/hit")

    def test_label_must_be_visible(self) -> None:
        # Expected failure before the fix: the label is looked for in the text left after stripping tags,
        # so a hidden element, a <title> or a <template> still counts.
        label_p = f'<p class="sample">{LABEL}</p>'
        cases = {
            "hidden attribute": GOOD_PAGE.replace(label_p, f'<p class="sample" hidden>{LABEL}</p>'),
            "hidden parent": GOOD_PAGE.replace(label_p, f'<div hidden><p class="sample">{LABEL}</p></div>'),
            "display none": GOOD_PAGE.replace(label_p, f'<p style="display: none">{LABEL}</p>'),
            "visibility hidden": GOOD_PAGE.replace(label_p, f'<p style="visibility:hidden">{LABEL}</p>'),
            "title only": GOOD_PAGE.replace(label_p, "").replace("<head>", f"<head><title>{LABEL}</title>"),
            "template": GOOD_PAGE.replace(label_p, f"<template><p>{LABEL}</p></template>"),
            "attribute only": GOOD_PAGE.replace(label_p, f'<img alt="{LABEL}" src="a.jpg">'),
            "script string": GOOD_PAGE.replace(label_p, f'<script>var s = "{LABEL}";</script>'),
        }
        for name, page in cases.items():
            with self.subTest(name=name):
                found = self.page(page)
                self.assertTrue(any("welcome.html" in p and f'needs the label "{LABEL}"' in p for p in found), found)

    def test_head_closes_without_its_end_tag(self) -> None:
        # Codex P1 on #68: </head> is optional (WHATWG HTML, "Optional tags"), and a browser shows the body.
        # Expected failure before the fix: the open <head> kept everything after it hidden.
        self.assertIn("</head>", GOOD_PAGE)
        for name, page in {
            "body start tag": GOOD_PAGE.replace("</head>", ""),
            "no body tag": GOOD_PAGE.replace("</head>", "").replace("<body>", ""),
        }.items():
            with self.subTest(name=name):
                self.assertEqual(self.page(page), [])

    def test_label_split_by_inline_markup_or_entities_passes(self) -> None:
        page = GOOD_PAGE.replace(LABEL, "Sample <b>data</b>,&nbsp;not   real")
        self.assertEqual(self.page(page), [])

    def test_tricky_but_valid_tags_are_still_scanned(self) -> None:
        # A closing tag may carry attributes and odd spacing and any case (the old regex missed these).
        page = GOOD_PAGE.replace("</body>", "<SCRIPT>import x from 'https://esm.sh/x';</SCRIPT\t\n bar></body>")
        self.assertOutside(self.page(page), "https://esm.sh/x")
        page = GOOD_PAGE.replace("</style>", "</STYLE\n>").replace("var(--color-bg-primary)", "#F7F6F3", 1)
        found = self.page(page)
        self.assertTrue(any("literal colour" in p and "#F7F6F3" in p for p in found), found)

    def test_a_comment_hides_nothing_and_shows_nothing(self) -> None:
        # Text inside an HTML comment is not on the page: it can say "safe" and cannot supply the label.
        self.assertEqual(self.page(GOOD_PAGE.replace("Issue #123", "<!-- safe, #ffffff, https://x.test/a.js --> Issue #123")), [])
        found = self.page(GOOD_PAGE.replace(LABEL, "<!-- %s -->" % LABEL))
        self.assertTrue(any(f'needs the label "{LABEL}"' in p for p in found), found)

    def test_checks_finish_fast_on_pathological_input(self) -> None:
        # Expected failure before the fix: the tag regex took about 26 s on "<a " * 20000 (issue #36).
        for name, junk in (("open tags", "<a " * 20000), ("open comments", "<!--" * 20000),
                           ("open css comments", "<style>" + "/*" * 20000 + "</style>"),
                           ("open url functions", "<style>" + "url(" * 20000 + "</style>"),
                           ("open quotes", '<p title="' + "'" * 20000), ("open braces", "<style>" + "{" * 20000 + "</style>"),
                           ("unclosed script", "<script>" + "'" * 20000)):
            with self.subTest(name=name):
                start = time.monotonic()
                self.page(GOOD_PAGE.replace("</body>", junk + "</body>"))
                self.assertLess(time.monotonic() - start, 3.0)

    # Issue #36: media anywhere in the repository, found with git ls-files

    def git_repo(self) -> None:
        # Without GIT_* variables: inside a git hook, GIT_DIR would point this at the real repository.
        clean_env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True, env=clean_env)

    def test_unusual_media_extensions_anywhere_in_the_repository_fail(self) -> None:
        self.git_repo()
        names = ("a.jfif", "b.svgz", "c.m4v", "d.flac", "e.opus", "f.psd", "G.PNG")
        for name in names:
            self.write(f"frontend/public/{name}", "x")
        found = cb.problems(self.root)
        for name in names:
            with self.subTest(name=name):
                self.assertTrue(any(p.startswith(f"frontend/public/{name}:") and "docs/assets/README.md" in p for p in found), found)

    def test_registered_media_outside_docs_passes(self) -> None:
        self.git_repo()
        self.write("docs/assets/README.md", REG_HEAD + reg_row("frontend/public/a.jfif"))
        self.write("frontend/public/a.jfif", "x")
        self.assertEqual(cb.problems(self.root), [])

    def test_generated_test_screenshots_are_exempt_but_other_media_is_not(self) -> None:
        # Register line of 21 Nov 2026 (docs/decisions/README.md) and AGENTS.md: test screenshots are exempt.
        self.git_repo()
        self.write("frontend/e2e/screenshots/pages.spec.ts/home-dark.png", "x")
        self.write("frontend/public/home.png", "x")
        found = cb.problems(self.root)
        self.assertEqual([p.split(":")[0] for p in found], ["frontend/public/home.png"], found)

    def test_safe_split_by_tags_after_a_block_is_found(self) -> None:
        # Expected failure before the fix: all text is joined with nothing between blocks, so "Lisbon" and
        # "sa<b>fe" read as "Lisbonsafe" and there is no word boundary before "safe".
        for body in ("<p>Sample data, not real</p><p>Lisbon</p><p>sa<b>fe</b></p>", "<li>A</li><li>sa<i>fe</i></li>",
                     "<p>Sample data, not real</p><p>sa<!-- x -->fe</p>", "<td>Lisbon</td><td>s<b>a</b>fe</td>",
                     "<h2>Lisbon</h2>sa<b>fe</b>", "Lisbon<br>sa<b>fe</b>"):
            with self.subTest(body=body):
                found = self.page(GOOD_PAGE.replace("<svg>", body + "<svg>"))
                self.assertTrue(self.safe_found(found), found)

    def test_inline_tags_still_join_words(self) -> None:
        self.assertEqual(self.page(GOOD_PAGE.replace("Issue #123", "<b>Safety</b> and <i>sa</i><b>vings</b>")), [])

    def test_screenshot_exemption_is_png_only(self) -> None:
        self.git_repo()
        self.write("frontend/e2e/screenshots/pages.spec.ts/photo.jpg", "x")
        self.write("frontend/e2e/screenshots/pages.spec.ts/home.png", "x")
        found = cb.problems(self.root)
        self.assertEqual([p.split(":")[0] for p in found], ["frontend/e2e/screenshots/pages.spec.ts/photo.jpg"], found)

    def test_a_fallback_to_docs_only_is_said_on_stderr(self) -> None:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            cb.problems(self.root)  # not a git repository
        self.assertIn("not a git repository", err.getvalue())

    def test_ignored_and_dependency_files_are_not_media(self) -> None:
        self.git_repo()
        self.write(".gitignore", "node_modules/\n")
        self.write("frontend/node_modules/pkg/logo.png", "x")
        self.assertEqual(cb.problems(self.root), [])


class BoardScript(unittest.TestCase):
    """docs/design/boards/board.js sets a frame's address only from a board screen path (CodeQL alert 15)."""

    root = Path(__file__).resolve().parent.parent
    boards = root / "docs" / "design" / "boards"

    def pattern(self) -> re.Pattern[str]:
        source = (self.boards / "board.js").read_text()
        match = re.search(r"var SCREEN = /(.+)/;", source)
        self.assertIsNotNone(match, "board.js needs a SCREEN pattern for data-screen")
        return re.compile(match.group(1).replace("\\/", "/"))

    def test_every_data_screen_on_the_boards_is_accepted(self) -> None:
        pattern = self.pattern()
        screens = [value for page in self.boards.glob("*.html")
                   for tag, attrs in cb._parse(page.read_text()).tags for name, value in attrs if name == "data-screen"]
        self.assertGreater(len(screens), 50)
        self.assertEqual([s for s in screens if not pattern.fullmatch(s)], [])

    def test_other_addresses_are_refused(self) -> None:
        pattern = self.pattern()
        for bad in ("javascript:alert(1)", "https://example.org/x.html", "//example.org/x.html", "/screens/a.html",
                    "../screens/a.html", "screens/../a.html", "screens/a.html#x", "screens/a.html?x=<b>",
                    "screens/A.html", "screens/a.js", "data:text/html,x", "screens/a.html\n", ""):
            with self.subTest(bad=bad):
                self.assertIsNone(pattern.fullmatch(bad))

    def test_the_theme_comes_from_a_fixed_list(self) -> None:
        source = (self.boards / "board.js").read_text()
        self.assertIn('var THEMES = ["light", "dark"];', source)
        self.assertIn("THEMES.indexOf(theme) === -1", source)


class RealRepository(unittest.TestCase):
    def test_layover_passes(self) -> None:
        root = Path(__file__).resolve().parent.parent
        self.assertEqual(cb.problems(root), [])

    def test_layover_has_a_board_index(self) -> None:
        # Without index.html the "not linked" check would never run.
        root = Path(__file__).resolve().parent.parent
        self.assertTrue((root / "docs" / "design" / "boards" / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()
