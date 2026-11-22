#!/usr/bin/env python3
"""Check Layover's numeric code against the test-first skill (.claude/skills/test-first/).

Fails when:
- a test function (name starting `test_`) in backend/tests/test_money.py, or in any file listed in
  NUMERIC_TEST_FILES, has no docstring with both "Working:" and "Source:" (a hand-worked expected
  value with its source, AGENTS.md);
- backend/src/app/money.py uses `float`: the name, a float literal, or a `float` annotation;
- a money field in backend/src/app/contract/ uses `float`: a field named `*_minor` or `rate`, or
  anything inside the MoneyValue or MoneyEstimate classes. Other measures (temperatures,
  coordinates) may be floats.

Limits: it reads the syntax tree only, so it can't tell that a docstring's working is right, and a
float reached through an alias (`F = float`) is caught at the alias only. Money fields with other
names are not found: add a numeric test file or extend MONEY_CLASSES.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

NUMERIC_TEST_FILES = ["backend/tests/test_money.py"]
MONEY_MODULE = "backend/src/app/money.py"
CONTRACT_DIR = "backend/src/app/contract"
MONEY_CLASSES = {"MoneyValue", "MoneyEstimate"}


def has_float(node: ast.AST) -> bool:
    """True when the node holds the name `float` or a float literal."""
    return any(
        (isinstance(n, ast.Name) and n.id == "float")
        or (isinstance(n, ast.Constant) and isinstance(n.value, float))
        for n in ast.walk(node)
    )


def is_money_field(name: str) -> bool:
    return name == "rate" or name.endswith("_minor")


def parse(path: Path, problems: list[str]) -> ast.Module | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError) as err:
        problems.append(f"{path}: cannot read or parse ({err})")
        return None


def check_tests(path: Path, problems: list[str]) -> None:
    tree = parse(path, problems)
    if tree is None:
        return
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
            doc = ast.get_docstring(node) or ""
            for label in ("Working:", "Source:"):
                if label not in doc:
                    problems.append(f"{path}:{node.lineno}: {node.name} has no '{label}' in its docstring")


def check_no_float_in_money_module(path: Path, problems: list[str]) -> None:
    tree = parse(path, problems)
    if tree is None:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "float":
            problems.append(f"{path}:{node.lineno}: uses float (money is Decimal or integer minor units)")
        elif isinstance(node, ast.Constant) and isinstance(node.value, float):
            problems.append(f"{path}:{node.lineno}: float literal {node.value!r} (use Decimal)")


def check_contract(path: Path, problems: list[str]) -> None:
    tree = parse(path, problems)
    if tree is None:
        return
    for cls in (n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)):
        if cls.name in MONEY_CLASSES and has_float(cls):
            problems.append(f"{path}:{cls.lineno}: {cls.name} uses float")
            continue
        for stmt in cls.body:
            if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                if is_money_field(stmt.target.id) and has_float(stmt):
                    problems.append(
                        f"{path}:{stmt.lineno}: money field {stmt.target.id} uses float"
                    )


def main(root: Path = Path(".")) -> int:
    problems: list[str] = []
    for name in NUMERIC_TEST_FILES:
        path = root / name
        if path.is_file():
            check_tests(path, problems)
        else:
            problems.append(f"{name}: missing (numeric tests must exist)")
    money = root / MONEY_MODULE
    if money.is_file():
        check_no_float_in_money_module(money, problems)
    else:
        problems.append(f"{MONEY_MODULE}: missing")
    for path in sorted((root / CONTRACT_DIR).rglob("*.py")):
        check_contract(path, problems)
    for line in problems:
        print(line)
    if problems:
        print(f"check_numeric_tests: {len(problems)} problem(s)")
        return 1
    print("check_numeric_tests: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
