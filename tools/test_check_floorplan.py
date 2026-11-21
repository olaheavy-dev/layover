"""Tests for tools/check_floorplan.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import base64
import contextlib
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_floorplan as cf  # noqa: E402


def csp_page(allowed: list[str], scripts: list[str]) -> str:
    hashes = " ".join(
        "'sha256-" + base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode() + "'" for body in allowed)
    tags = "".join(f"<script>{body}</script>" for body in scripts)
    return (f'<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src {hashes}">'
            f"{tags}")


class Floorplan(unittest.TestCase):
    def run_check(self, text: str | None, name: str = "design.html") -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            if text is not None:
                folder = root / "docs" / "floorplan"
                folder.mkdir(parents=True)
                (folder / name).write_text(text, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = cf.main(root)
            return code, out.getvalue()

    def test_unix_path_fails(self):
        code, out = self.run_check("<p>/Users/someone/source/app</p>")
        self.assertEqual(code, 1)
        self.assertIn("docs/floorplan/design.html", out)
        self.assertEqual(self.run_check("<p>/home/someone/app</p>")[0], 1)

    def test_windows_path_fails(self):
        self.assertEqual(self.run_check(r"<p>C:\Users\someone\app</p>")[0], 1)
        self.assertEqual(self.run_check(r"<p>c:\users\someone\app</p>")[0], 1)
        self.assertEqual(self.run_check(r'<p>"C:\\Users\\someone"</p>')[0], 1)

    def test_other_local_paths_fail(self):
        for text in ["/private/tmp/x", "/private/var/folders/ab/x", "/var/folders/ab/x", "/Volumes/Disk/x",
                     "/root/app", r"D:\Projects\layover", r'"C:\\\\Users\\\\bob"']:
            with self.subTest(text=text):
                self.assertEqual(self.run_check(f"<p>{text}</p>")[0], 1)

    def test_other_remotes_fail(self):
        for text in ["ssh://git@github.com/o/r.git", "git@github.com/o/r", "https://github.com/o/r.git",
                     "https://gitlab.com/o/r.git", "https://user:tok@github.com/o/r"]:
            with self.subTest(text=text):
                self.assertEqual(self.run_check(f"<p>{text}</p>")[0], 1)

    def test_git_ssh_remote_fails(self):
        self.assertEqual(self.run_check("<p>git@github.com:someone/app.git</p>")[0], 1)

    def test_file_url_fails(self):
        self.assertEqual(self.run_check('<a href="file:///tmp/x">x</a>')[0], 1)

    def test_other_file_types_checked(self):
        self.assertEqual(self.run_check("/Users/someone", name="data.json")[0], 1)

    def test_clean_file_passes(self):
        self.assertEqual(self.run_check("<p>backend/app/main.py and https://github.com/x/y</p>")[0], 0)

    def test_script_matching_csp_passes(self):
        self.assertEqual(self.run_check(csp_page(["var a = 1;  \n"], ["var a = 1;  \n"]))[0], 0)

    def test_script_not_in_csp_fails(self):
        # The pre-commit whitespace hook once trimmed a bundled script, so the browser blocked it (Codex, #42).
        code, out = self.run_check(csp_page(["var a = 1;  \n"], ["var a = 1;\n"]))
        self.assertEqual(code, 1)
        self.assertIn("Content-Security-Policy", out)

    def test_upper_case_and_odd_script_tags_are_checked(self):
        # Expected failure before the fix: the regex looked for a lower-case "<script>" and a plain "</script>"
        # only, so these scripts were never hashed (CodeQL alert 14, "py/bad-tag-filter").
        body = "var a = 1;\n"
        for opening, closing in (("<SCRIPT>", "</SCRIPT>"), ("<Script>", "</script >"), ("<script>", "</script\t\n bar>"),
                                 ("<script >", "</SCRIPT\n>"), ("<script type='text/javascript'>", "</script>")):
            with self.subTest(opening=opening, closing=closing):
                allowed = csp_page([body], [])
                self.assertEqual(self.run_check(allowed + f"{opening}{body}{closing}")[0], 0)
                code, out = self.run_check(allowed + f"{opening}{body}changed{closing}")
                self.assertEqual(code, 1, out)
                self.assertIn("Content-Security-Policy", out)

    def test_script_text_is_hashed_exactly_as_written(self):
        # Entities and line ends inside a script are not changed (a browser hashes the raw text).
        body = "var a = '&amp; &#97;'; // end\r\nvar b = '<b>';  \n"
        self.assertEqual(self.run_check(csp_page([body], [body]))[0], 0)

    def test_scripts_with_a_source_are_not_inline_and_a_comment_is_not_a_script(self):
        page = csp_page(["var a = 1;"], ["var a = 1;"]) + '<script src="x.js"></script><!-- <script>evil()</script> -->'
        self.assertEqual(self.run_check(page)[0], 0)

    def test_csp_meta_in_any_case_and_order_is_read(self):
        body = "var a = 1;"
        digest = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode()
        page = (f"<META CONTENT=\"script-src 'sha256-{digest}'\" HTTP-EQUIV='content-security-policy'>"
                f"<script>{body}</script><script>other()</script>")
        code, out = self.run_check(page)
        self.assertEqual(code, 1)
        self.assertIn("1 inline script(s)", out)

    def test_page_without_csp_skips_hash_check(self):
        self.assertEqual(self.run_check("<script>var a = 1;</script>")[0], 0)

    def test_no_folder_passes(self):
        self.assertEqual(self.run_check(None)[0], 0)


class RealRepository(unittest.TestCase):
    def test_real_repository_passes(self):
        root = Path(__file__).resolve().parent.parent
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = cf.main(root)
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
