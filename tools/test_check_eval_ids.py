"""Tests for tools/check_eval_ids.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_eval_ids as ce  # noqa: E402

HEAD = ("# Evaluation cases\n\n## Cases\n\n"
        "| ID | Area | What it checks | Passes when | Fails when | Scored by | Status |\n"
        "|---|---|---|---|---|---|---|\n")


def row(case_id: str, status: str = "planned") -> str:
    return f"| `{case_id}` | Area | something | yes | no | code | {status} |\n"


class EvalIds(unittest.TestCase):
    def run_check(self, rows: str, docs: dict[str, str] | None = None) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = root / "docs" / "evaluations" / "cases.md"
            cases.parent.mkdir(parents=True)
            cases.write_text(HEAD + rows + "\n## Coverage\n\nCites `BRIEF-01` here.\n", encoding="utf-8")
            for name, text in (docs or {}).items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = ce.main(root)
            return code, out.getvalue()

    def test_duplicate_id_fails(self):
        code, out = self.run_check(row("BRIEF-01") + row("BRIEF-01"))
        self.assertEqual(code, 1)
        self.assertIn("BRIEF-01", out)

    def test_bad_form_fails(self):
        self.assertEqual(self.run_check(row("BRIEF-01") + row("BRIEF-1"))[0], 1)
        self.assertEqual(self.run_check(row("BRIEF-01") + row("brief-02"))[0], 1)

    def test_cited_but_undefined_fails(self):
        code, out = self.run_check(row("BRIEF-01"), {"docs/x.md": "See BRIEF-09."})
        self.assertEqual(code, 1)
        self.assertIn("docs/x.md", out)
        self.assertIn("BRIEF-09", out)

    def test_cited_in_html_checked(self):
        code, out = self.run_check(row("BRIEF-01"), {"docs/b/x.html": "<p>BRIEF-07</p>"})
        self.assertEqual(code, 1)
        self.assertIn("BRIEF-07", out)

    def test_unknown_area_ignored(self):
        code, _ = self.run_check(row("BRIEF-01"), {"docs/x.md": "PLAN-03, WCAG-22 and BRIEF-01."})
        self.assertEqual(code, 0)

    def test_withdrawn_counts_as_defined(self):
        code, _ = self.run_check(row("BRIEF-01") + row("BRIEF-02", "withdrawn"), {"docs/x.md": "BRIEF-02"})
        self.assertEqual(code, 0)

    def test_three_digit_ids(self):
        self.assertEqual(self.run_check(row("BRIEF-01") + row("PLAN-100"))[0], 0)
        self.assertEqual(self.run_check(row("BRIEF-01") + row("PLAN-007"))[0], 1)

    def test_missing_cases_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(ce.main(Path(tmp)), 1)

    def test_empty_cases_table_fails(self):
        self.assertEqual(self.run_check("")[0], 1)

    def test_undefined_id_in_coverage_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = root / "docs" / "evaluations" / "cases.md"
            cases.parent.mkdir(parents=True)
            cases.write_text(HEAD + row("BRIEF-01") + "\n## Coverage\n\n| `plan_trip` | `BRIEF-61` |\n", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = ce.main(root)
        self.assertEqual(code, 1)
        self.assertIn("BRIEF-61", out.getvalue())

    def test_row_without_backticks_fails(self):
        code, out = self.run_check(row("BRIEF-01") + "| BRIEF-01 | Area | x | y | n | code | planned |\n")
        self.assertEqual(code, 1)
        self.assertIn("backticks", out)

    def test_defined_ids_reads_only_cases_section(self):
        text = HEAD + row("BRIEF-01") + "\n## Coverage\n\n| Intent | Cases |\n|---|---|\n| `plan_trip` | `BRIEF-01` |\n"
        self.assertEqual(ce.defined_ids(text), ["BRIEF-01"])


class RealRepository(unittest.TestCase):
    def test_real_repository_passes(self):
        root = Path(__file__).resolve().parent.parent
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = ce.main(root)
        self.assertEqual(code, 0, out.getvalue())


if __name__ == "__main__":
    unittest.main()
