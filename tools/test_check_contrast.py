"""Tests for tools/check_contrast.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_contrast as cc  # noqa: E402


class ContrastRatio(unittest.TestCase):
    def test_black_on_white_is_21(self) -> None:
        # Working: relative luminance of white is 1, of black is 0, so (1 + 0.05) / (0 + 0.05) = 21.
        # Source: WCAG 2.2, definition of contrast ratio, https://www.w3.org/TR/WCAG22/#dfn-contrast-ratio
        self.assertAlmostEqual(cc.contrast("#000000", "#FFFFFF"), 21.0, places=2)

    def test_grey_767676_on_white_is_about_4_54(self) -> None:
        # Working: channel 0x76 = 118, 118 / 255 = 0.46275; it is above 0.04045, so
        # ((0.46275 + 0.055) / 1.055) ** 2.4 = 0.49076 ** 2.4 = 0.18116. All three channels are equal,
        # so luminance = 0.18116. Ratio = (1 + 0.05) / (0.18116 + 0.05) = 1.05 / 0.23116 = 4.542.
        # Source: WCAG 2.2 relative luminance, https://www.w3.org/TR/WCAG22/#dfn-relative-luminance
        self.assertAlmostEqual(cc.contrast("#767676", "#FFFFFF"), 4.54, places=2)

    def test_order_does_not_matter(self) -> None:
        self.assertEqual(cc.contrast("#12436E", "#FFFFFF"), cc.contrast("#FFFFFF", "#12436E"))


class Blend(unittest.TestCase):
    def test_half_black_over_white_is_mid_grey(self) -> None:
        # Working: 0.5 * 0 + 0.5 * 255 = 127.5, rounded to 128 = 0x80.
        self.assertEqual(cc.blend("#000000", "#FFFFFF", 0.5), "#808080")


SAMPLE = """
:root {
  --color-bg-primary: #FFFFFF;
  --color-bg-secondary: #FFFFFF;
  --color-bg-tertiary: #FFFFFF;
  --color-bg-inverse: #000000;
  --color-text-inverse: #FFFFFF;
  --color-text-primary: #000000;
  --color-text-secondary: #000000;
  --color-text-link: #000000;
  --color-text-on-accent: #FFFFFF;
  --color-accent-primary: #000000;
  --color-accent-primary-hover: #000000;
  --color-accent-primary-active: #000000;
  --color-border-control: #000000;
  --color-border-focus: #000000;
  --color-status-warning: #000000;
  --color-status-live: #000000;
  --color-status-cached: #000000;
  --color-status-not-known: #000000;
  --color-status-info: #000000;
  --color-scrim: #000000;
  --scrim-text-min-opacity: 0.6;
}
:root[data-theme="dark"] { DARK }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { DARK } }
"""
# Empty dark blocks: the dark theme inherits the passing light values.
DARK_OK = ""


class CheckFile(unittest.TestCase):
    def run_check(self, css: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            path.write_text(css)
            return cc.problems(path)

    def test_passing_file_has_no_problems(self) -> None:
        self.assertEqual(self.run_check(SAMPLE.replace("DARK", DARK_OK)), [])

    def test_low_contrast_text_fails(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK).replace("--color-text-secondary: #000000", "--color-text-secondary: #999999")
        found = self.run_check(css)
        self.assertTrue(any("color-text-secondary" in p and "light" in p for p in found), found)

    def test_dark_blocks_that_differ_fail(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK, 1).replace("DARK", "--color-text-primary: #111111;")
        found = self.run_check(css)
        self.assertTrue(any("differ" in p for p in found), found)


class FailurePaths(unittest.TestCase):
    def run_check(self, css: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            path.write_text(css)
            return cc.problems(path)

    def test_dark_only_failure_is_reported_as_dark(self) -> None:
        # Dark makes the card background black but leaves the black main text: 1:1.
        dark = "--color-bg-secondary: #000000;"
        found = self.run_check(SAMPLE.replace("DARK", dark))
        self.assertTrue(any(p.startswith("dark:") and "color-bg-secondary" in p for p in found), found)
        self.assertFalse(any(p.startswith("light:") for p in found), found)

    def test_missing_token_fails(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK).replace("  --color-text-link: #000000;\n", "")
        found = self.run_check(css)
        self.assertTrue(any("missing" in p and "color-text-link" in p for p in found), found)

    def test_non_hex_value_fails(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK).replace("--color-text-link: #000000", "--color-text-link: #000")
        found = self.run_check(css)
        self.assertTrue(any("six-digit hex" in p and "color-text-link" in p for p in found), found)

    def test_weak_scrim_fails(self) -> None:
        # Working: black at 0.2 over white = 0.8 * 255 = 204 = #CCCCCC; white on #CCCCCC is about 1.6:1.
        css = SAMPLE.replace("DARK", DARK_OK).replace("--scrim-text-min-opacity: 0.6", "--scrim-text-min-opacity: 0.2")
        found = self.run_check(css)
        self.assertTrue(any("scrim" in p for p in found), found)

    def test_missing_dark_block_fails(self) -> None:
        css = SAMPLE.replace(':root[data-theme="dark"] { DARK }', "").replace("DARK", DARK_OK)
        found = self.run_check(css)
        self.assertTrue(any("dark blocks" in p for p in found), found)

    def test_new_text_token_is_checked_without_a_list_change(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK).replace("--scrim-text-min-opacity: 0.6;", "--scrim-text-min-opacity: 0.6;\n  --color-status-success: #EEEEEE;")
        found = self.run_check(css)
        self.assertTrue(any("color-status-success" in p for p in found), found)

    def test_control_border_is_checked_on_the_page_background(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK).replace("--color-border-control: #000000", "--color-border-control: #F0F0F0")
        found = self.run_check(css)
        self.assertTrue(any("color-border-control" in p and "color-bg-primary" in p for p in found), found)

    def test_colour_in_a_later_root_block_fails(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK) + "\n:root { --color-text-primary: #EEEEEE; }\n"
        found = self.run_check(css)
        self.assertTrue(any("later :root" in p for p in found), found)


class RealTokens(unittest.TestCase):
    def test_layover_tokens_pass(self) -> None:
        path = Path(__file__).resolve().parent.parent / "docs" / "design" / "tokens.css"
        self.assertEqual(cc.problems(path), [])


if __name__ == "__main__":
    unittest.main()
