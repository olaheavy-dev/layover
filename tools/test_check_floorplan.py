"""Tests for tools/check_floorplan.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_floorplan as cf  # noqa: E402


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
