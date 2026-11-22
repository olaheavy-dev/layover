"""Tests for tools/check_copy.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_copy as cc  # noqa: E402

BOARD_FONTS = Path("docs/design/boards/fonts")
APP_FONTS = Path("frontend/src/fonts")


class CheckCopy(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name)

    def write(self, rel: str, content: str | bytes) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content)

    def test_safe_in_a_tsx_file_fails(self) -> None:
        self.write("frontend/src/app/card.tsx", "export const A = () => <p>Lisbon is safe</p>;\n")
        found = cc.problems(self.root)
        self.assertTrue(any("card.tsx" in p and "safe" in p for p in found), found)

    def test_unsafe_and_safely_in_a_ts_file_fail(self) -> None:
        self.write("frontend/src/lib/copy.ts", 'export const a = "unsafe"; export const b = "travel safely";\n')
        found = cc.problems(self.root)
        self.assertTrue(any("unsafe" in p for p in found), found)
        self.assertTrue(any("safely" in p for p in found), found)

    def test_fcdo_wording_passes(self) -> None:
        self.write("frontend/src/app/card.tsx",
                   "export const A = () => <p>FCDO travel advice, updated 3 May 2027</p>;\n")
        self.assertEqual(cc.problems(self.root), [])

    def test_safe_area_is_allowed(self) -> None:
        self.write("frontend/src/app/bar.tsx",
                   'export const A = () => <div className="pb-[env(safe-area-inset-bottom)]" />;\n')
        self.assertEqual(cc.problems(self.root), [])

    def test_csp_keywords_are_allowed(self) -> None:
        self.write("frontend/src/lib/csp.ts", "export const s = \"script-src 'unsafe-inline' 'unsafe-eval'\";\n")
        self.assertEqual(cc.problems(self.root), [])

    def test_unsafe_on_its_own_still_fails(self) -> None:
        self.write("frontend/src/lib/csp.ts", 'export const s = "unsafe to visit";\n')
        self.assertTrue(cc.problems(self.root))

    def test_safety_is_allowed(self) -> None:
        # "Safety and security" is the FCDO's own section name (tools/check_boards.py).
        self.write("frontend/src/app/s.tsx", "export const A = () => <h2>Safety and security</h2>;\n")
        self.assertEqual(cc.problems(self.root), [])

    def test_test_files_are_not_scanned(self) -> None:
        self.write("frontend/src/app/card.test.tsx", 'it("never says safe", () => {});\n')
        self.write("frontend/src/lib/copy.spec.ts", 'it("never says safe", () => {});\n')
        self.assertEqual(cc.problems(self.root), [])

    def test_files_outside_src_are_not_scanned(self) -> None:
        self.write("frontend/e2e/home.spec.ts", 'expect(text).not.toContain("safe");\n')
        self.assertEqual(cc.problems(self.root), [])

    def test_identical_font_copies_pass(self) -> None:
        self.write(f"{BOARD_FONTS}/A.woff2", b"font-bytes")
        self.write(f"{APP_FONTS}/A.woff2", b"font-bytes")
        self.assertEqual(cc.problems(self.root), [])

    def test_a_font_that_differs_from_its_board_copy_fails(self) -> None:
        self.write(f"{BOARD_FONTS}/A.woff2", b"font-bytes")
        self.write(f"{APP_FONTS}/A.woff2", b"changed-bytes")
        found = cc.problems(self.root)
        self.assertTrue(any("A.woff2" in p and "differs" in p for p in found), found)

    def test_a_font_with_no_board_copy_fails(self) -> None:
        self.write(f"{APP_FONTS}/B.woff2", b"font-bytes")
        found = cc.problems(self.root)
        self.assertTrue(any("B.woff2" in p and "no copy" in p for p in found), found)

    def test_a_licence_text_is_compared_too(self) -> None:
        self.write(f"{BOARD_FONTS}/OFL-X.txt", "licence one")
        self.write(f"{APP_FONTS}/OFL-X.txt", "licence two")
        found = cc.problems(self.root)
        self.assertTrue(any("OFL-X.txt" in p and "differs" in p for p in found), found)

    def test_the_real_repository_passes(self) -> None:
        self.assertEqual(cc.problems(Path(__file__).resolve().parent.parent), [])


if __name__ == "__main__":
    unittest.main()
