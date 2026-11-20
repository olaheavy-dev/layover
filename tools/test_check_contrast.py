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
  --color-text-on-photo: #FFFFFF;
  --color-chart-1: #000000;
  --color-chart-2: #000000;
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

    def test_text_on_photo_is_read_from_its_token(self) -> None:
        # Working: dark text on the scrim. Black at 0.6 over white = 0.4 * 255 = 102 = #666666.
        # Luminance of #10151B = 0.2126 * 0.00518 + 0.7152 * 0.00750 + 0.0722 * 0.01096 = 0.00726; of #666666
        # (102 / 255 = 0.4; (0.455 / 1.055) ** 2.4) = 0.1329. Ratio = 0.1829 / 0.05726 = 3.19, under 4.5:1. The old check tested a literal white,
        # so it could not catch a dark --color-text-on-photo.
        dark = "--color-text-on-photo: #10151B;"
        found = self.run_check(SAMPLE.replace("DARK", dark))
        self.assertTrue(any(p.startswith("dark:") and "photo" in p for p in found), found)

    def test_missing_text_on_photo_fails(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK).replace("  --color-text-on-photo: #FFFFFF;\n", "")
        found = self.run_check(css)
        self.assertTrue(any("missing" in p and "color-text-on-photo" in p for p in found), found)

    def test_text_on_photo_is_not_tested_on_page_backgrounds(self) -> None:
        # White on the white sample page is 1:1, but text on a photo never sits on a page background.
        found = self.run_check(SAMPLE.replace("DARK", DARK_OK))
        self.assertFalse(any("color-text-on-photo" in p and "color-bg-" in p for p in found), found)

    def test_faint_chart_colour_fails_at_3_to_1(self) -> None:
        # Working: #CCCCCC on white. Channel 204 / 255 = 0.8; ((0.8 + 0.055) / 1.055) ** 2.4 = 0.6038.
        # Ratio = 1.05 / (0.6038 + 0.05) = 1.61, under the 3:1 that WCAG 1.4.11 needs for chart marks.
        # Source: https://www.w3.org/TR/WCAG22/#non-text-contrast
        css = SAMPLE.replace("DARK", DARK_OK).replace("--color-chart-2: #000000", "--color-chart-2: #CCCCCC")
        found = self.run_check(css)
        self.assertTrue(any("color-chart-2" in p and "3.0:1" in p for p in found), found)

    def test_chart_colour_between_3_and_4_5_passes(self) -> None:
        # Working: #888888 on white. 136 / 255 = 0.5333; ((0.5333 + 0.055) / 1.055) ** 2.4 = 0.2462.
        # Ratio = 1.05 / (0.2462 + 0.05) = 3.54: enough for a chart mark (3:1), not for text (4.5:1).
        css = SAMPLE.replace("DARK", DARK_OK).replace("--color-chart-2: #000000", "--color-chart-2: #888888")
        self.assertEqual(self.run_check(css), [])

    def test_missing_chart_colour_fails(self) -> None:
        css = SAMPLE.replace("DARK", DARK_OK).replace("  --color-chart-1: #000000;\n", "")
        found = self.run_check(css)
        self.assertTrue(any("missing" in p and "color-chart-1" in p for p in found), found)


TINT_LINES = """  --color-highlight: #FFFFFF;
  --tint-surface-x: color-mix(in srgb, var(--color-highlight) 80%, var(--color-bg-secondary));
  --tint-glow: color-mix(in srgb, var(--color-highlight) 16%, transparent);
"""


class TintMix(unittest.TestCase):
    """color-mix(in srgb, A p%, B): each channel is A * p / 100 + B * (1 - p / 100), on 0 to 255 values.

    Source: CSS Color 5, https://www.w3.org/TR/css-color-5/#color-mix (premultiplied sRGB mix; with no
    alpha it is the plain weighted average above).
    """

    TOKENS = {"a": "#FF0000", "b": "#FFFFFF", "k": "#000000"}

    def test_resolve_red_20_percent_over_white(self) -> None:
        # Working: red = (255, 0, 0), white = (255, 255, 255), p = 20%.
        # R = 255 * 0.2 + 255 * 0.8 = 255; G = 0 * 0.2 + 255 * 0.8 = 204; B = 204. 204 = 0xCC, so #FFCCCC.
        self.assertEqual(cc.resolve_color_mix("color-mix(in srgb, var(--a) 20%, var(--b))", self.TOKENS), "#FFCCCC")

    def test_resolve_exact_half_rounds_up(self) -> None:
        # Working: black 50% over white: 0 * 0.5 + 255 * 0.5 = 127.5 per channel. A browser stores 8-bit
        # channels, so 127.5 rounds half up to 128 = 0x80: #808080.
        self.assertEqual(cc.resolve_color_mix("color-mix(in srgb, var(--k) 50%, var(--b))", self.TOKENS), "#808080")

    def test_resolve_malformed_mix_fails_loudly(self) -> None:
        for bad in ("color-mix(in oklab, var(--a) 20%, var(--b))",   # not the sRGB space
                    "color-mix(in srgb, var(--a), var(--b))",         # no percentage
                    "color-mix(in srgb, var(--a) 120%, var(--b))",    # over 100%
                    "color-mix(in srgb, var(--zzz) 20%, var(--b))",   # unknown token
                    "color-mix(in srgb, var(--a) 20%, transparent)",  # transparency has no backdrop here
                    "color-mix(in srgb, #FF0000 20%, var(--b))"):     # not a token
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    cc.resolve_color_mix(bad, self.TOKENS)

    def test_surfaces_are_split_from_glows_and_lines(self) -> None:
        tokens = {"tint-surface-chip": "x", "tint-surface-index": "color-mix(in srgb, var(--a) 92%, transparent)",
                  "tint-glow": "color-mix(in srgb, var(--a) 16%, transparent)", "tint-border-lift": "x",
                  "illus-water": "x", "color-text-primary": "#000000"}
        surfaces, skipped = cc.split_tints(tokens)
        self.assertEqual(surfaces, ["tint-surface-chip"])
        self.assertEqual(skipped, ["tint-border-lift", "tint-glow", "tint-surface-index"])  # no --illus-*


class TintFile(unittest.TestCase):
    def run_check(self, css: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            path.write_text(css)
            return cc.problems(path)

    def sample(self, dark: str = "", tint: str = TINT_LINES) -> str:
        return SAMPLE.replace("DARK", dark).replace("  --color-chart-2: #000000;\n", "  --color-chart-2: #000000;\n" + tint)

    def test_tint_that_keeps_contrast_passes(self) -> None:
        # Working: highlight white 80% over white = white. Black text on white is 21:1.
        self.assertEqual(self.run_check(self.sample()), [])

    def test_quiet_text_on_a_mid_grey_tint_fails_with_token_theme_and_ratio(self) -> None:
        # Working: tint = black 50% over white = #808080 (127.5 rounds to 128). Text is #999999.
        # Luminance of #808080: 128 / 255 = 0.50196; ((0.50196 + 0.055) / 1.055) ** 2.4 = 0.52796 ** 2.4 = 0.2159.
        # Luminance of #999999: 153 / 255 = 0.6; (0.655 / 1.055) ** 2.4 = 0.62085 ** 2.4 = 0.3185.
        # Ratio = (0.3185 + 0.05) / (0.2159 + 0.05) = 0.3685 / 0.2659 = 1.39, under 4.5:1.
        # Source: https://www.w3.org/TR/WCAG22/#dfn-relative-luminance and #dfn-contrast-ratio
        tint = ("  --color-highlight: #000000;\n"
                "  --tint-surface-x: color-mix(in srgb, var(--color-highlight) 50%, var(--color-bg-secondary));\n")
        css = self.sample(tint=tint).replace("--color-text-secondary: #000000", "--color-text-secondary: #999999")
        found = self.run_check(css)
        self.assertTrue(any("tint-surface-x" in p and "light" in p and "color-text-secondary" in p
                            and "1.39:1" in p for p in found), found)
        # Its own page-background checks fail too, so look for the tint line, not only for any line.

    def test_tint_failure_in_dark_only_is_reported_as_dark(self) -> None:
        # Working: dark highlight is black. Tint = black 80% over white = 255 * 0.2 = 51 = #333333.
        # Luminance of #333333: 51 / 255 = 0.2; (0.255 / 1.055) ** 2.4 = 0.24171 ** 2.4 = 0.0331.
        # Black text on it: (0.0331 + 0.05) / (0 + 0.05) = 1.66, under 4.5:1. In light the tint is white: 21:1.
        found = self.run_check(self.sample(dark="--color-highlight: #000000;"))
        tint_lines = [p for p in found if "tint-surface-x" in p]
        self.assertTrue(tint_lines and all(p.startswith("dark:") for p in tint_lines), found)
        self.assertTrue(any("1.66:1" in p for p in tint_lines), found)

    def test_malformed_tint_surface_fails_loudly(self) -> None:
        css = self.sample().replace(" 80%", "")
        found = self.run_check(css)
        self.assertTrue(any("tint-surface-x" in p and "color-mix" in p for p in found), found)

    def test_glow_with_transparency_is_not_a_failure(self) -> None:
        # --tint-glow in TINT_LINES mixes with transparent: it is skipped, not parsed or failed.
        self.assertEqual(self.run_check(self.sample()), [])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            path.write_text(self.sample())
            self.assertEqual(cc.skipped_tints(path), ["tint-glow"])


class TokenBlocks(unittest.TestCase):
    """A --color-* token may be defined once, in one of the three known blocks (gap 4)."""

    def run_check(self, css: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            path.write_text(css)
            return cc.problems(path)

    def base(self) -> str:
        return SAMPLE.replace("DARK", DARK_OK)

    def test_colour_defined_in_another_rule_fails_and_names_the_token(self) -> None:
        # Expected failure before the fix: only a later :root block is looked at, so a class rule is not.
        found = self.run_check(self.base() + "\n.card { --color-text-primary: #FFFFFF; }\n")
        self.assertTrue(any("--color-text-primary" in p and ".card" in p and "outside" in p for p in found), found)

    def test_colour_defined_inside_a_media_query_rule_fails(self) -> None:
        found = self.run_check(self.base() + "\n@media (min-width: 40rem) { body { --color-bg-primary: #000000; } }\n")
        self.assertTrue(any("--color-bg-primary" in p and "outside" in p for p in found), found)

    def test_token_defined_twice_in_one_block_fails(self) -> None:
        css = self.base().replace("  --color-chart-1: #000000;\n", "  --color-chart-1: #000000;\n  --color-chart-1: #111111;\n")
        found = self.run_check(css)
        self.assertTrue(any("--color-chart-1" in p and "twice" in p and ":root" in p for p in found), found)

    def test_token_defined_twice_in_the_dark_block_fails(self) -> None:
        dark = "--color-chart-1: #000000; --color-chart-1: #111111;"
        found = self.run_check(SAMPLE.replace("DARK", dark))
        self.assertTrue(any("--color-chart-1" in p and "twice" in p and "dark" in p for p in found), found)

    def test_later_block_overriding_a_token_fails_and_names_it(self) -> None:
        # Each block already sets the token once; a second copy of the block sets it again.
        base = SAMPLE.replace("DARK", "--color-text-primary: #000000;")
        for later in (':root { --color-text-primary: #EEEEEE; }',
                      ':root[data-theme="dark"] { --color-text-primary: #EEEEEE; }',
                      '@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --color-text-primary: #EEEEEE; } }'):
            with self.subTest(later=later):
                found = self.run_check(base + "\n" + later + "\n")
                self.assertTrue(any("--color-text-primary" in p and "later" in p for p in found), found)

    def test_non_colour_custom_properties_elsewhere_are_not_colour_tokens(self) -> None:
        self.assertEqual(self.run_check(self.base() + "\n.card { --card-pad: 8px; --tint-x: red; }\n"), [])

    def test_each_token_once_per_block_passes(self) -> None:
        dark = "--color-chart-1: #000000;"
        self.assertEqual(self.run_check(SAMPLE.replace("DARK", dark)), [])


class StatusTextOnTints(unittest.TestCase):
    """The status text tokens are tested on tinted surfaces like the other text tokens (gap 4)."""

    STATUS = ("color-status-info", "color-status-warning", "color-status-live", "color-status-cached",
              "color-status-not-known")
    TINT = ("  --color-highlight: #000000;\n"
            "  --tint-surface-x: color-mix(in srgb, var(--color-highlight) 50%, var(--color-bg-secondary));\n")

    def run_check(self, css: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tokens.css"
            path.write_text(css)
            return cc.problems(path)

    def sample(self, dark: str = "") -> str:
        return SAMPLE.replace("DARK", dark).replace("  --color-chart-2: #000000;\n", "  --color-chart-2: #000000;\n" + self.TINT)

    def test_the_tint_text_list_holds_the_five_status_tokens(self) -> None:
        for token in self.STATUS:
            self.assertIn(token, cc.TINT_TEXT)

    def test_status_text_too_faint_on_a_tint_fails_with_token_theme_and_ratio(self) -> None:
        # Working: tint = black 50% over white = 127.5 per channel, rounded half up to 128 = #808080.
        # Luminance of #808080: 128 / 255 = 0.50196; ((0.50196 + 0.055) / 1.055) ** 2.4 = 0.2159.
        # Status text #333333: 51 / 255 = 0.2; ((0.2 + 0.055) / 1.055) ** 2.4 = 0.24171 ** 2.4 = 0.03311.
        # Ratio = (0.2159 + 0.05) / (0.03311 + 0.05) = 0.2659 / 0.08311 = 3.20, under 4.5:1.
        # On white it is 1.05 / 0.08311 = 12.6:1, so only the tint check catches it.
        # Source: https://www.w3.org/TR/WCAG22/#dfn-relative-luminance and #dfn-contrast-ratio
        css = self.sample().replace("--color-status-info: #000000", "--color-status-info: #333333")
        found = self.run_check(css)
        self.assertTrue(any("tint-surface-x" in p and "light" in p and "color-status-info" in p and "3.20:1" in p
                            for p in found), found)

    def test_every_status_token_is_checked_on_the_tint(self) -> None:
        # Same working as above, each token set to #333333 in turn.
        for token in self.STATUS:
            with self.subTest(token=token):
                css = self.sample().replace(f"--{token}: #000000", f"--{token}: #333333")
                found = self.run_check(css)
                self.assertTrue(any("tint-surface-x" in p and f"--{token} " in p and "3.20:1" in p for p in found), found)

    def test_missing_status_token_fails_loudly_with_a_tint_present(self) -> None:
        css = self.sample().replace("  --color-status-cached: #000000;\n", "")
        found = self.run_check(css)
        self.assertTrue(any("color-status-cached" in p and "tinted surface" in p and "missing" in p for p in found), found)

    def test_non_hex_status_token_fails_loudly_with_a_tint_present(self) -> None:
        css = self.sample().replace("--color-status-live: #000000", "--color-status-live: #000")
        found = self.run_check(css)
        self.assertTrue(any("color-status-live" in p and "tinted surface" in p and "six-digit hex" in p for p in found), found)

    def test_status_tokens_on_a_tint_that_keeps_contrast_pass(self) -> None:
        # Black on #808080: (0.2159 + 0.05) / 0.05 = 5.32, over 4.5:1.
        self.assertEqual(self.run_check(self.sample()), [])


class RealTokens(unittest.TestCase):
    def test_layover_tokens_pass(self) -> None:
        path = Path(__file__).resolve().parent.parent / "docs" / "design" / "tokens.css"
        self.assertEqual(cc.problems(path), [])


class RealTintTokens(unittest.TestCase):
    PATH = Path(__file__).resolve().parent.parent / "docs" / "design" / "tokens.css"

    def test_every_tint_surface_is_checked_and_the_rest_listed(self) -> None:
        # Eight surfaces carry text (top bar, chat, pill, verdict box, chart band, chip, traveller bubble, and
        # the top of a lifted card).
        # The index bar (92% over transparent), the glows and the lines are skipped and listed.
        surfaces, skipped = cc.split_tints(cc._block(self.PATH.read_text(), ":root {"))
        self.assertEqual(surfaces, ["tint-surface-chart-band", "tint-surface-chat", "tint-surface-chip",
                                    "tint-surface-lift", "tint-surface-pill", "tint-surface-topbar", "tint-surface-traveller",
                                    "tint-surface-verdict"])
        self.assertIn("tint-surface-index", skipped)
        self.assertIn("tint-glow", skipped)
        self.assertFalse(any(name.startswith("illus-") for name in skipped))


if __name__ == "__main__":
    unittest.main()
