"""Run the evaluation cases: `python -m app.evals.runner [--case ID | --report PATH]`.

Prints one line per case (`PASS`, `SCHEMA PASS (full case needs step N)`, `FAIL` or
`NOT RUN (needs step N)`) and a total; exits 1 on any `FAIL`. In step 1 only the schema part of
WIDGET-01 to WIDGET-20 runs, and it reports `SCHEMA PASS`, never `PASS`: the case's other rules
(labels, "Not known", never "safe") are not checked yet. There are no model calls.

`--report PATH` also writes a Markdown baseline (quality, speed in milliseconds, tokens, trip set)
to PATH, for the build gates.

N is the build step that adds the case, read from the "Evaluation cases it adds" column of the
build-order table in docs/product/01-research-and-direction.md section 4. A case listed in more than
one step (a WIDGET case also appears in step 1 for its schema) takes the last step listed.
"""

import argparse
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path

from app.evals.cases import CASES_MD, REPO_ROOT, Case, parse_cases
from app.evals.checks.widget_schemas import check_widget_samples, widget_kind

DIRECTION_MD = REPO_ROOT / "docs" / "product" / "01-research-and-direction.md"

_STEP_ROW = re.compile(r"^\|\s*(\d+)\.\s[^|]*\|[^|]*\|([^|]*)\|")
_RANGE = re.compile(r"`([A-Z]+)-(\d+)`(?:\s+to\s+`([A-Z]+)-(\d+)`)?")


class Outcome(Enum):
    # S105: these are outcome names, not passwords
    SCHEMA_PASS = "SCHEMA PASS"  # noqa: S105
    PASS = "PASS"  # noqa: S105
    FAIL = "FAIL"
    NOT_RUN = "NOT RUN"
    WITHDRAWN = "WITHDRAWN"


@dataclass(frozen=True)
class Result:
    case: Case
    outcome: Outcome
    detail: str = ""
    step: int | None = None

    def line(self) -> str:
        if self.outcome is Outcome.NOT_RUN:
            return f"NOT RUN (needs step {self.step})"
        if self.outcome is Outcome.SCHEMA_PASS:
            return f"SCHEMA PASS (full case needs step {self.step})"
        return str(self.outcome.value)


def build_step_map(path: Path = DIRECTION_MD) -> dict[str, int]:
    """Case ID -> the build step that adds it, from the section 4 table. Later steps win."""
    steps: dict[str, int] = {}
    in_order = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_order = line.startswith("## 4.")
            continue
        row = _STEP_ROW.match(line) if in_order else None
        if not row:
            continue
        step = int(row.group(1))
        for area, first, area_end, last in _RANGE.findall(row.group(2)):
            end = last or first
            if area_end and area_end != area:
                raise ValueError(f"step {step}: range crosses areas: {area} to {area_end}")
            width = len(first)
            for n in range(int(first), int(end) + 1):
                steps[f"{area}-{n:0{width}d}"] = step
    return steps


def run_case(case: Case, steps: dict[str, int]) -> Result:
    if case.status == "withdrawn":
        return Result(case, Outcome.WITHDRAWN)
    step = steps.get(case.case_id)
    if step is None:
        return Result(case, Outcome.FAIL, "no build step lists this case in 01 section 4")
    if case.area == "Widget" and case.scored_by == "code":
        kind = widget_kind(case.title)
        if kind is None:
            return Result(case, Outcome.FAIL, "no widget kind in the case title")
        ok, detail = check_widget_samples(kind)
        if not ok:
            return Result(case, Outcome.FAIL, detail)
        return Result(case, Outcome.SCHEMA_PASS, detail, step)
    return Result(case, Outcome.NOT_RUN, "needs a later build step", step)


def run_cases(cases: list[Case], steps: dict[str, int]) -> list[Result]:
    return [run_case(case, steps) for case in cases]


def totals_line(results: list[Result]) -> str:
    count = {o: sum(r.outcome is o for r in results) for o in Outcome}
    return (
        f"total {len(results)}: {count[Outcome.PASS]} PASS, "
        f"{count[Outcome.SCHEMA_PASS]} SCHEMA PASS, {count[Outcome.FAIL]} FAIL, "
        f"{count[Outcome.NOT_RUN]} NOT RUN, {count[Outcome.WITHDRAWN]} WITHDRAWN"
    )


@dataclass(frozen=True)
class ReportInfo:
    date: str
    commit: str
    command: str
    seconds: float
    model_calls: int
    trips_run: int
    scripts_on_disk: int


def current_commit() -> str:
    """`git describe --always --dirty` for HEAD: a short hash, plus "-dirty" when the tree has
    uncommitted changes. "not known" when git is missing or fails."""
    try:
        done = subprocess.run(
            ["git", "describe", "--always", "--dirty"],  # noqa: S607
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return "not known"
    return done.stdout.strip() or "not known"


def report_command(report: Path) -> str:
    """The command line for the report, with the path relative to the repository. A path outside
    the repository is cut to its file name, so a committed report never holds a local folder."""
    try:
        shown = report.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        shown = report.name
    return f"python -m app.evals.runner --report {shown}"


def render_report(results: list[Result], info: ReportInfo) -> str:
    if info.model_calls == 0:
        tokens = "none: this run made no model calls"
    else:
        tokens = f"not counted yet ({info.model_calls} model calls)"
    trip_set = "none yet" if info.trips_run == 0 else f"{info.trips_run} trips run"
    lines = [
        "# Evaluation report",
        "",
        f"Date: {info.date}",
        f"HEAD when run: {info.commit}",
        f"Command: `{info.command}`",
        "",
        f"Quality: {totals_line(results)}",
        f"Speed: {round(info.seconds * 1000)} ms for the whole run",
        f"Tokens: {tokens}",
        f"Trip set: {trip_set}",
    ]
    if info.scripts_on_disk > info.trips_run:
        noun = "script" if info.scripts_on_disk == 1 else "scripts"
        lines.append(f"{info.scripts_on_disk} traveller {noun} on disk, not run yet")
    lines += ["", "| Case | Outcome | Detail |", "|---|---|---|"]
    for r in results:
        detail = ""
        if r.outcome is Outcome.FAIL:
            # Keep the detail on one table row: escape pipes, turn line breaks into spaces.
            detail = " ".join(r.detail.replace("|", "\\|").split())
        lines.append(f"| `{r.case.case_id}` | {r.line()} | {detail} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m app.evals.runner")
    parser.add_argument("--case", help="run one case by ID, for example WIDGET-03")
    parser.add_argument("--report", type=Path, help="also write a Markdown report to this path")
    args = parser.parse_args(argv)
    if args.report and args.case:
        parser.error("--report writes a whole-set baseline; it can't be used with --case")
    started = time.perf_counter()
    cases = parse_cases(CASES_MD)
    if args.case:
        cases = [c for c in cases if c.case_id == args.case]
        if not cases:
            print(f"unknown case: {args.case}")
            return 1
    results = run_cases(cases, build_step_map())
    seconds = time.perf_counter() - started
    for r in results:
        extra = f"  {r.detail}" if r.outcome is Outcome.FAIL and r.detail else ""
        print(f"{r.case.case_id:<12} {r.line()}{extra}")
    print(totals_line(results))
    if args.report:
        info = ReportInfo(
            date=date.today().isoformat(),
            commit=current_commit(),
            command=report_command(args.report),
            seconds=seconds,
            # No case runs a trip or a model until build step 2.
            model_calls=0,
            trips_run=0,
            scripts_on_disk=len(list((REPO_ROOT / "evals" / "travellers").glob("*.json"))),
        )
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_report(results, info), encoding="utf-8")
    return 1 if any(r.outcome is Outcome.FAIL for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
