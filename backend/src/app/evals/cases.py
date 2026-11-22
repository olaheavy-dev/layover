"""Read the evaluation cases table (docs/evaluations/cases.md).

This mirrors `defined_ids` in tools/check_eval_ids.py, which sits outside the installed package.
A test checks that both read the same IDs from the same file.
"""

import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError

REPO_ROOT = Path(__file__).resolve().parents[4]
CASES_MD = REPO_ROOT / "docs" / "evaluations" / "cases.md"

_ROW_ID = re.compile(r"^\|\s*`([^`]+)`\s*\|")


class Case(BaseModel):
    """One row of the "## Cases" table."""

    model_config = ConfigDict(frozen=True)

    case_id: str
    area: str
    title: str  # the "What it checks" cell
    # The legend in cases.md defines `code` and `judge`, and the statuses `planned` and `withdrawn`.
    scored_by: Literal["code", "judge"]
    status: Literal["planned", "withdrawn"]


def parse_cases(path: Path = CASES_MD) -> list[Case]:
    """Every case in the "## Cases" table, in file order. Raises ValueError naming a bad row."""
    cases: list[Case] = []
    in_cases = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_cases = line.strip() == "## Cases"
            continue
        match = _ROW_ID.match(line) if in_cases else None
        if not match:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            raise ValueError(f"{match.group(1)}: expected 7 columns, found {len(cells)}")
        try:
            cases.append(
                Case(
                    case_id=match.group(1),
                    area=cells[1],
                    title=cells[2],
                    scored_by=cells[5],
                    status=cells[6],
                )
            )
        except ValidationError as error:
            raise ValueError(f"{match.group(1)}: {error}") from error
    return cases
