# Design gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the Design stage in one PR: evaluation cases with a coverage table, an approved build order with milestones, a Floorplan snapshot, a whole-repository audit with its fixes, and triage of the `noticed` issues.

**Architecture:** Documents plus two small Python checks in `tools/`, run by `mk/design.mk` in `make check`. The audit runs last, so it also reads the new content.

**Tech Stack:** Markdown, Python 3 standard library (`unittest`, `re`, `pathlib`), the Floorplan plugin, `gh`.

**Spec:** `docs/superpowers/specs/2026-11-20-design-gate-design.md` (issue #39, branch `docs/design-gate`).

## Global Constraints

- No product code, schemas or new dependencies (spec, Non-goals).
- Evaluation IDs are `AREA-NN`: zero-padded to at least two digits, never reused or renumbered, withdrawn rather than deleted (`AGENTS.md`).
- The existing 16 IDs in spec §7 keep their meaning.
- Owner decisions go in a prompt window and are recorded with the owner's words in the register (`AGENTS.md` rule 8).
- The Floorplan export never has Health ticked, and holds no local paths, secrets or personal data (`AGENTS.md`, "Floorplan snapshot").
- New docs follow `simple-english` with British spelling; existing docs keep their style.
- Checks use the Python standard library only, and are run with `PYTHONDONTWRITEBYTECODE=1` (as in `mk/design.mk`).
- No agent attribution in commits or the PR.

## Review Focus

- An ID cited in a doc but missing from `cases.md` (for example a typo `BRIEF-3`). Expected: `make check` fails and names the file. Tested in Task 1.
- An ID in a code block, or as an example in `AGENTS.md` (`PLAN-03`, `PLAN-100`). Expected: not flagged; only `docs/` is scanned, and only areas defined in `cases.md` count. Tested in Task 1.
- A withdrawn case. Expected: it stays defined and isn't reported as missing. Tested in Task 1.
- A Floorplan export with a Windows path (`C:\Users\`) or an SSH git remote (`git@github.com:`). Expected: the check fails. Tested in Task 3.
- A widget kind or rule added to the spec later with no case. Expected: the reviewer finds a missing row. Not automated: the coverage table is a reviewer check (register, 19 Nov 2026).

---

### Task 1: Evaluation cases, coverage table and the ID check

**Files:**
- Create: `docs/evaluations/cases.md`
- Create: `tools/check_eval_ids.py`
- Create: `tools/test_check_eval_ids.py`
- Modify: `mk/design.mk` (add the check, and add it to the target's `##` description)
- Modify: `docs/superpowers/specs/2026-11-19-layover-journey-design.md` §7 (one line pointing to `cases.md` as the master list)

**Interfaces:**
- Produces: `cases.md` with a `## Cases` table whose first column is the ID in backticks, and columns `ID | Area | What it checks | Passes when | Fails when | Scored by | Status` (Status: `planned` or `withdrawn`). It also has a `## Coverage` section with four tables (Intents, Journey steps, Widget kinds, 0011 rules), each row naming its case IDs.
- Produces: `check_eval_ids.main(root: Path) -> int` (0 = pass), `defined_ids(text: str) -> list[str]`, `cited_ids(text: str, areas: set[str]) -> set[str]`.

**Cases to add** (wording is the builder's; IDs and scope are fixed here):

| ID | Checks |
|---|---|
| `INTENT-06` | Low-confidence classification gets one clarifying question, not a guess |
| `INTENT-07` | A side question (`destination_facts`) during `plan_trip` keeps the trip state |
| `INTENT-08` | An entry or safety answer links the FCDO page and shows its update date (0011 rule 6) |
| `COMPARE-04` | The traveller swaps a destination for their own; the table re-ranks in code |
| `COMPARE-05` | A budget total shown to the traveller came from a tool call, not the model (0011 rule 3) |
| `TRIP-02` | Pick: the chosen place and the confirmed brief carry into the summary unchanged |
| `TRIP-03` | The summary shows each section with its source, or "not known" |
| `TRIP-04` | Every source cited in a trip's output is listed in `docs/references/data-sources.md` (0011 rule 5) |
| `ITIN-03` | The itinerary starts from the chosen hotel base |
| `ITIN-04` | The hotel list (OpenStreetMap) shows no prices |
| `BOOK-03` | Layover asks for exact dates before booking and never picks them |
| `BOOK-04` | A price change before the order asks for approval again |
| `BOOK-05` | If the hotel sandbox is unavailable, booking offers flights only and says why |
| `SHARE-01` | A shared link opens a frozen copy with "as of" dates and no chat |
| `SHARE-02` | With "Include my budget and who's travelling" off, the shared copy has no budget, traveller chips or budget lines |
| `WIDGET-01` to `WIDGET-20` | One per kind, in this order: the 16 in spec §5d, then `public_holidays`, `time_difference`, `fare_list`, `transport_route`. Each case: output valid against its schema, with a source label (Live, Cached with its age, Fallback or Unavailable), and the "Not known" and error states from the [brief's state table](../../design/brief.md#widget-states) shown, never as zero (0011 rules 2 and 4). `WIDGET-03` (`fare_card`) also checks that a fare with no data shows no price (0011 rule 1) |

Copy the 16 existing cases from spec §7 into the table unchanged.

- [ ] **Step 1: Write the failing tests** in `tools/test_check_eval_ids.py` (`unittest`, same style as `test_check_boards.py`, temporary folders):
  - `test_duplicate_id_fails`: two rows `` `BRIEF-01` `` → `main` returns 1, and the message names `BRIEF-01`.
  - `test_bad_form_fails`: rows `` `BRIEF-1` `` and `` `brief-01` `` → 1.
  - `test_cited_but_undefined_fails`: `docs/x.md` cites `BRIEF-09` while `BRIEF` is defined → 1, and the message names `docs/x.md`.
  - `test_unknown_area_ignored`: `docs/x.md` cites `PLAN-03` and `WCAG-22`, no `PLAN` area defined → 0.
  - `test_withdrawn_counts_as_defined`: a `withdrawn` row cited in `docs/` → 0.
  - `test_three_digit_ids`: `PLAN-100` is valid, `PLAN-007` is not (zero padding only up to two digits).
  - `test_real_repository_passes`: `main(repo_root)` → 0.
- [ ] **Step 2: Run the tests and confirm they fail.** Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tools/test_check_eval_ids.py`. Expected: ImportError (no module `check_eval_ids`).
- [ ] **Step 3: Implement `tools/check_eval_ids.py`.** ID form: `^[A-Z]{2,10}-(\d{2}|[1-9]\d{2,})$`. Defined IDs come from the first cell of table rows under `## Cases` in `docs/evaluations/cases.md`. Cited IDs come from `*.md` and `*.html` under `docs/`, with `cases.md` itself excluded, matching `\b(AREA)-\d+\b` only for defined areas. Print each problem as `path: message`. The docstring states what fails and the limits, like `check_boards.py`.
- [ ] **Step 4: Write `docs/evaluations/cases.md`** with the cases above and the coverage tables, then add the §7 pointer to the spec.
- [ ] **Step 5: Run the tests and confirm they pass.** Same command. Expected: OK, all tests.
- [ ] **Step 6: Add the check to `mk/design.mk`** (`PYTHONDONTWRITEBYTECODE=1 python3 tools/check_eval_ids.py`) and run `make check-design`. Expected: passes.
- [ ] **Step 7: Commit:** `git add docs/evaluations tools/check_eval_ids.py tools/test_check_eval_ids.py mk/design.mk docs/superpowers/specs/2026-11-19-layover-journey-design.md && git commit -m "docs: evaluation cases, coverage table and ID check (#39)"`

### Task 2: Build order (owner approval)

**Files:**
- Modify: `docs/product/01-research-and-direction.md` §4 (and remove "proposed")
- Modify: `docs/superpowers/specs/2026-11-19-layover-journey-design.md` §8 item 6 (answered, with a link)
- Modify: `docs/decisions/README.md` (register lines: this approval, and the two gate decisions from the spec)

- [ ] **Step 1: Draft the build order.** It starts with plan 1 (FastAPI layer, trip-state and widget schemas including the #26 kinds, money types, the commission switch, recorded-response tests, the holidays library, the Aspire app host). It ends with the earnings dashboard behind the switch. It places the agent team and the single-agent baseline ([0012](../decisions/0012-agent-team.md)), the MCP servers (0009, "from build step 2" in spec §6), retrieval (0008), Travelpayouts, booking, and the Next.js layer when frontend work starts (0010). Each step names the evaluation case IDs it adds (from Task 1).
- [ ] **Step 2: Post the draft in the chat in plain words, then ask in a prompt window:** approve, or change. The recommended option goes first.
- [ ] **Step 3: Write the approved order into 01 §4**, answer spec §8 item 6, and add the register lines with the owner's words.
- [ ] **Step 4: Create one milestone per build step:** `gh api repos/olaheavy-dev/layover/milestones -f title="Build 1: <name>"` and so on. Expected: `gh api repos/olaheavy-dev/layover/milestones --jq '.[].title'` lists them.
- [ ] **Step 5: Commit:** `docs: build order for the agent team, approved at the Design gate (#39)`

### Task 3: Floorplan blueprint and snapshot

**Files:**
- Create: `docs/floorplan/design.html`
- Create: `tools/check_floorplan.py`, `tools/test_check_floorplan.py`
- Modify: `mk/design.mk`, `docs/references/third-party.md`

**Interfaces:**
- Produces: `check_floorplan.main(root: Path) -> int`. It fails on `/Users/`, `/home/`, `C:\Users\` (any case), `file://` and `git@` in any file under `docs/floorplan/`.

- [ ] **Step 1: Review the installed plugin** (`~/.claude/plugins/cache/floorplan/`): its version, and every network call, command it runs and file it writes, and anything it sends. Report this to the owner in the chat. If it sends data anywhere, ask in a prompt window before running it.
- [ ] **Step 2: Write the failing tests:** `test_unix_path_fails`, `test_windows_path_fails`, `test_git_ssh_remote_fails`, `test_file_url_fails`, `test_clean_file_passes`, `test_no_folder_passes` (the check passes before the first snapshot).
- [ ] **Step 3: Run the tests.** Expected: ImportError.
- [ ] **Step 4: Implement `tools/check_floorplan.py`** and add it to `mk/design.mk`. Run the tests. Expected: OK.
- [ ] **Step 5: Draw the blueprint with the `floorplan:floorplan` skill** from the spec, the decisions (0005 to 0012) and the Task 2 build order. Export one HTML file to `docs/floorplan/design.html`, with Health not ticked.
- [ ] **Step 6: Check the export by hand** for personal data, private material, email addresses and file names that show private material. Then run `make check-design`. Expected: passes.
- [ ] **Step 7: Record in `third-party.md`** the plugin version, and the licence of each library and font bundled in the export.
- [ ] **Step 8: Commit:** `docs: Floorplan blueprint snapshot for the Design gate (#39)`

### Task 4: Whole-repository audit

- [ ] **Step 1: Dispatch a fresh-context Opus agent** with the "Code Review Rules" in `AGENTS.md`, `.claude/rules/`, and the gate checklist. It reads every tracked file except binary assets, and looks for contradictions, stale statements, broken links, unsourced figures and debt. Don't give it this plan's conclusions. Tell it: no attribution lines, report only, P0 to P3 with file, line, failure and fix.
- [ ] **Step 2: Weigh each finding:** right, partly right or wrong, with the cost of the change. Fix the right ones in the gate PR, or open an issue (`noticed`) for a fix outside the gate.
- [ ] **Step 3: Run `make check`.** Expected: passes. Commit: `docs: fixes from the Design gate audit (#39)`

### Task 5: Triage, backlog, status

- [ ] **Step 1: Comment on #9, #26, #27, #34 and #36** with where each goes (spec §5). Move #26 and #34 to the right build milestone. Fix #36 here only if it is under about an hour; otherwise move it to Build 1.
- [ ] **Step 2: Update `docs/planning/backlog.md`:** #39 (`[22]`), the build milestones and moved issues. Update `docs/planning/status.md`: the stage, next steps, and the evaluation report line "no evaluation set yet".
- [ ] **Step 3: Confirm there are no open `review-followup` issues:** `gh issue list --label review-followup --state open`. Expected: empty.
- [ ] **Step 4: Commit:** `docs: Design gate triage, backlog and status (#39)`

### Task 6: Verify, review, PR

- [ ] **Step 1: Run `make check`.** Expected: passes. Run a pre-flight search for every term and figure changed (`grep -rn "proposed" docs/product`, the case IDs, the milestone names).
- [ ] **Step 2: Run the pre-push review in a fresh context** (Opus, `superpowers:requesting-code-review`, plus `house-reviewers:code-security-reviewer` for the two scripts). Fix findings.
- [ ] **Step 3: Open the PR** with the `pr` skill: `docs: Design gate (#39)`, `Closes #39`, the criteria-to-test map (each acceptance criterion in #39 with its test or reviewer check), the status file update, and "Noticed, not changed". Then comment `@codex review`.
