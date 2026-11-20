#!/usr/bin/env python3
"""Check Layover's evaluation case IDs (docs/evaluations/cases.md).

Evaluation cases have permanent IDs: an area code and a number, zero-padded to at least two digits
(BRIEF-03, then PLAN-100 after PLAN-99), never reused (AGENTS.md; register line of 19 Nov 2026, #6).

Fails when:
- docs/evaluations/cases.md is missing, or its "## Cases" table defines no IDs;
- an ID in the first column of the "## Cases" table is defined twice;
- an ID there is not in AREA-NN form (capital letters, a hyphen, two digits, or three or more with no
  leading zero);
- a row of the "## Cases" table (other than its header and divider) has no ID in backticks in its first cell;
- a .md or .html file under docs/, cases.md itself included (its coverage tables), cites an ID whose area is
  defined in cases.md but whose number is not. A withdrawn case stays in the table, so it still counts as
  defined.

Limits: only areas that cases.md defines are checked, so examples in other areas (PLAN-03 in AGENTS.md,
WCAG-22) are not flagged. Files outside docs/ are not scanned. An ID is found by a plain text match, so
an ID inside a code block counts as a citation. It reads only the current files, so it can't tell that a
row was deleted and its ID later reused: keeping withdrawn rows is a review rule (AGENTS.md).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CASES = Path("docs/evaluations/cases.md")
ID_FORM = re.compile(r"^[A-Z]{2,10}-(\d{2}|[1-9]\d{2,})$")
ROW_ID = re.compile(r"^\|\s*`([^`]+)`\s*\|")
DIVIDER = re.compile(r"^\|[\s:|-]+\|\s*$")


def defined_ids(text: str) -> list[str]:
    """IDs in the first column of table rows under the "## Cases" heading, in order, duplicates kept."""
    ids: list[str] = []
    in_cases = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_cases = line.strip() == "## Cases"
            continue
        if in_cases:
            match = ROW_ID.match(line)
            if match:
                ids.append(match.group(1))
    return ids


def unticked_rows(text: str) -> list[str]:
    """Table rows under "## Cases" whose first cell is not an ID in backticks (header and divider excepted)."""
    rows: list[str] = []
    in_cases = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_cases = line.strip() == "## Cases"
            continue
        if not in_cases or not line.startswith("|") or ROW_ID.match(line) or DIVIDER.match(line):
            continue
        if line.split("|")[1].strip() != "ID":
            rows.append(line.strip())
    return rows


def cited_ids(text: str, areas: set[str]) -> set[str]:
    """IDs in the given areas that the text mentions."""
    if not areas:
        return set()
    pattern = re.compile(r"\b(?:" + "|".join(sorted(map(re.escape, areas))) + r")-\d+\b")
    return set(pattern.findall(text))


def main(root: Path) -> int:
    problems: list[str] = []
    cases_path = root / CASES
    if not cases_path.is_file():
        print(f"{CASES}: missing")
        return 1
    cases_text = cases_path.read_text(encoding="utf-8")
    ids = defined_ids(cases_text)
    for line in unticked_rows(cases_text):
        problems.append(f"{CASES}: a Cases row has no ID in backticks: {line[:60]}")
    if not ids:
        problems.append(f"{CASES}: the '## Cases' table defines no IDs")
    seen: set[str] = set()
    for case_id in ids:
        if not ID_FORM.match(case_id):
            problems.append(f"{CASES}: {case_id} is not in AREA-NN form")
        if case_id in seen:
            problems.append(f"{CASES}: {case_id} is defined more than once")
        seen.add(case_id)
    valid = {i for i in seen if ID_FORM.match(i)}
    areas = {i.split("-")[0] for i in valid}
    docs = root / "docs"
    for path in sorted([*docs.rglob("*.md"), *docs.rglob("*.html")]):
        rel = path.relative_to(root).as_posix()
        for case_id in sorted(cited_ids(path.read_text(encoding="utf-8", errors="replace"), areas) - valid):
            problems.append(f"{rel}: cites {case_id}, which {CASES} does not define")
    for problem in problems:
        print(problem)
    if not problems:
        print(f"evaluation IDs: ok ({len(valid)} cases)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(Path(__file__).resolve().parent.parent))
