"""Tests for tools/check_boards.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_boards as cb  # noqa: E402

LABEL = "Sample data, not real"

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
        self.write("docs/assets/README.md", "| `wave.svg` | drawn for Layover |")
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
        self.write("docs/assets/README.md", "| `lisbon.jpg` | Unsplash | Unsplash License |")
        self.write("docs/design/boards/img/lisbon.jpg", "x")
        self.assertEqual(cb.problems(self.root), [])

    def test_unregistered_font_anywhere_in_docs_fails(self) -> None:
        self.write("docs/assets/README.md", "| `lisbon.jpg` | Unsplash |")
        self.write("docs/assets/fonts/SourceSans3.woff2", "x")
        found = cb.problems(self.root)
        self.assertTrue(any("SourceSans3.woff2" in p for p in found), found)


class RealRepository(unittest.TestCase):
    def test_layover_passes(self) -> None:
        root = Path(__file__).resolve().parent.parent
        self.assertEqual(cb.problems(root), [])


if __name__ == "__main__":
    unittest.main()
