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


class RealTokens(unittest.TestCase):
    def test_layover_tokens_pass(self) -> None:
        path = Path(__file__).resolve().parent.parent / "docs" / "design" / "tokens.css"
        self.assertEqual(cc.problems(path), [])


if __name__ == "__main__":
    unittest.main()
