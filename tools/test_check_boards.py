"""Tests for tools/check_boards.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import sys
import tempfile
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

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

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
        self.assertTrue(any("outside" in p and "fonts.googleapis.com" in p for p in found), found)

    def test_outside_script_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("</body>", '<script src="//unpkg.com/x.js"></script></body>'))
        self.assertTrue(any("outside" in p and "unpkg.com" in p for p in found), found)

    def test_hot_linked_image_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("<svg>", '<img alt="" src="https://images.unsplash.com/photo-1"><svg>'))
        self.assertTrue(any("outside" in p and "images.unsplash.com" in p for p in found), found)

    def test_outside_font_in_css_fails(self) -> None:
        page = GOOD_PAGE.replace("<style>", "<style>\n  @font-face { src: url(https://example.com/f.woff2); }")
        found = self.page(page)
        self.assertTrue(any("outside" in p and "example.com" in p for p in found), found)

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
        self.assertTrue(any("outside" in p and "images.unsplash.com" in p for p in found), found)

    def test_outside_poster_and_object_data_fail(self) -> None:
        page = GOOD_PAGE.replace("<svg>", '<video poster="https://x.test/p.jpg"></video><object data="https://y.test/o"></object><svg>')
        found = self.page(page)
        self.assertTrue(any("x.test" in p for p in found) and any("y.test" in p for p in found), found)

    def test_unquoted_and_spaced_outside_src_fail(self) -> None:
        page = GOOD_PAGE.replace("</body>", '<script src=https://unpkg.com/x.js></script><img alt="" src=" https://z.test/i.jpg"></body>')
        found = self.page(page)
        self.assertTrue(any("unpkg.com" in p for p in found) and any("z.test" in p for p in found), found)

    def test_outside_import_in_inline_script_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace("</body>", '<script type="module">import x from "https://esm.sh/x";</script></body>'))
        self.assertTrue(any("esm.sh" in p for p in found), found)

    def test_outside_image_set_fails(self) -> None:
        found = self.page(GOOD_PAGE.replace(".clear {", '.hero { background-image: image-set("https://cdn.test/a.jpg" 1x); }\n  .clear {'))
        self.assertTrue(any("cdn.test" in p for p in found), found)

    def test_outside_address_in_js_file_fails(self) -> None:
        self.write("docs/design/boards/switch.js", 'const u = "https://cdn.test/lib.js"; // a comment // is fine')
        found = cb.problems(self.root)
        self.assertTrue(any("switch.js" in p and "cdn.test" in p for p in found), found)

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
        self.assertTrue(any("switch.js" in p and "cdn.test" in p for p in found), found)

    def test_inline_script_outside_address_after_slash_star_string_fails(self) -> None:
        page = GOOD_PAGE.replace("</body>", '<script>const a = "/*"; fetch("https://cdn.test/x"); const b = "*/";</script></body>')
        found = self.page(page)
        self.assertTrue(any("cdn.test" in p for p in found), found)

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
        self.assertTrue(any("esm.sh" in p for p in found), found)
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
