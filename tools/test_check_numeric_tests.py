"""Tests for tools/check_numeric_tests.py. Run with: python3 -m unittest discover -s tools -p 'test_*.py'."""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_numeric_tests as cn  # noqa: E402

GOOD_TEST = '''
def test_a():
    """Adds.

    Working: 1 + 1 = 2.
    Source: arithmetic.
    """


def helper():
    pass
'''
GOOD_MONEY = "from decimal import Decimal\n\n\ndef f(x: Decimal) -> Decimal:\n    return x\n"
GOOD_CONTRACT = (
    "class MoneyValue:\n    amount_minor: int\n\n\n"
    "class Weather:\n    temperature_c: float\n"
)


class NumericTests(unittest.TestCase):
    def run_check(self, files: dict[str, str]) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = {
                "backend/tests/test_money.py": GOOD_TEST,
                "backend/src/app/money.py": GOOD_MONEY,
                "backend/src/app/contract/common.py": GOOD_CONTRACT,
            }
            base.update(files)
            for name, text in base.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = cn.main(root)
            return code, out.getvalue()

    def test_clean_files_pass(self):
        code, out = self.run_check({})
        self.assertEqual(code, 0, out)

    def test_test_without_docstring_fails(self):
        code, out = self.run_check({"backend/tests/test_money.py": "def test_a():\n    assert True\n"})
        self.assertEqual(code, 1)
        self.assertIn("test_a", out)

    def test_docstring_missing_source_fails(self):
        text = 'def test_a():\n    """Adds.\n\n    Working: 1 + 1 = 2.\n    """\n'
        code, out = self.run_check({"backend/tests/test_money.py": text})
        self.assertEqual(code, 1)
        self.assertIn("Source:", out)

    def test_docstring_missing_working_fails(self):
        text = 'def test_a():\n    """Adds.\n\n    Source: arithmetic.\n    """\n'
        code, out = self.run_check({"backend/tests/test_money.py": text})
        self.assertEqual(code, 1)
        self.assertIn("Working:", out)

    def test_method_in_test_class_is_checked(self):
        text = "class TestX:\n    def test_a(self):\n        pass\n"
        code, out = self.run_check({"backend/tests/test_money.py": text})
        self.assertEqual(code, 1)
        self.assertIn("test_a", out)

    def test_listed_extra_file_is_checked(self):
        original = cn.NUMERIC_TEST_FILES
        cn.NUMERIC_TEST_FILES = [*original, "backend/tests/test_budget.py"]
        try:
            code, out = self.run_check({"backend/tests/test_budget.py": "def test_b():\n    pass\n"})
        finally:
            cn.NUMERIC_TEST_FILES = original
        self.assertEqual(code, 1)
        self.assertIn("test_b", out)

    def test_unlisted_test_file_is_not_checked(self):
        code, out = self.run_check({"backend/tests/test_other.py": "def test_c():\n    pass\n"})
        self.assertEqual(code, 0, out)

    def test_missing_test_money_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = cn.main(Path(tmp))
        self.assertEqual(code, 1)
        self.assertIn("test_money.py", out.getvalue())

    def test_float_name_in_money_fails(self):
        code, out = self.run_check({"backend/src/app/money.py": "x = float('1.5')\n"})
        self.assertEqual(code, 1)
        self.assertIn("money.py", out)

    def test_float_literal_in_money_fails(self):
        code, out = self.run_check({"backend/src/app/money.py": "RATE = 0.84\n"})
        self.assertEqual(code, 1)
        self.assertIn("float", out)

    def test_float_annotation_in_money_fails(self):
        code, out = self.run_check({"backend/src/app/money.py": "def f(x: float) -> None:\n    pass\n"})
        self.assertEqual(code, 1)

    def test_float_minor_field_in_contract_fails(self):
        text = "class Foo:\n    price_minor: float\n"
        code, out = self.run_check({"backend/src/app/contract/foo.py": text})
        self.assertEqual(code, 1)
        self.assertIn("price_minor", out)

    def test_float_rate_field_in_contract_fails(self):
        text = "class Foo:\n    rate: float | None = None\n"
        code, out = self.run_check({"backend/src/app/contract/foo.py": text})
        self.assertEqual(code, 1)
        self.assertIn("rate", out)

    def test_float_inside_money_value_class_fails(self):
        text = "class MoneyValue:\n    amount: float\n"
        code, out = self.run_check({"backend/src/app/contract/common.py": text})
        self.assertEqual(code, 1)
        self.assertIn("MoneyValue", out)

    def test_float_in_other_contract_measure_passes(self):
        text = "class Sea:\n    temperature_c: float\n    lat: float = 0.5\n"
        code, out = self.run_check({"backend/src/app/contract/sea.py": text})
        self.assertEqual(code, 0, out)

    def test_contract_subfolder_is_scanned(self):
        text = "class Foo:\n    fee_minor: float\n"
        code, _ = self.run_check({"backend/src/app/contract/widgets/foo.py": text})
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
