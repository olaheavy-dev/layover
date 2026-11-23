# Build step 1 gate: design

Issue: #106 (`[61]`), in the Build 1 milestone. Date: 23 Nov 2026.

## Why

Build step 1 ("Foundation and data contract") has finished all 20 tasks of its plan. Every stage ends with a gate (`AGENTS.md`, "Review rounds and debt"). The gate shows that the repository is consistent and that the debt is known before build step 2 adds the first model calls. Step 2 starts from what this gate leaves behind: no stale or contradicting statements, a sorted backlog, a map of the real code and a first evaluation baseline.

## Goals

1. **Evaluation report.** Run `python -m app.evals.runner` and record its result as the first build-gate report: quality, speed and tokens, with the size of the trip set. This is the baseline that later gates compare against. A drop against it blocks a later gate.
2. **Floorplan map of the real code.** Turn the Design-gate blueprint into a map of the code that now exists. Export it as `docs/floorplan/build-1.html` and pass the export checks.
3. **Deferred ledger items.** The progress ledger (`.superpowers/sdd/2026-11-21-build-step-1/progress.md`, git-ignored) has about 44 "deferred" lines from PRs C, D and E, and some lines hold several points. Owner, 23 Nov 2026: "Fix small, file the rest (Recommended)". Small items are fixed in the gate PR. Bigger ones become `noticed` issues in the right milestone. None is left only in the ledger.
4. **Triage.** Each open `noticed` issue in the Build 1 milestone gets a comment: fixed in the gate, moved to a named later milestone, or closed with a reason. The issues are #9, #40, #56, #72, #73, #76, #79, #85, #86, #87, #89, #90, #91, #92, #96 and #97, plus #71 (major upgrades), which isn't labelled `noticed`. When this PR merges, the Build 1 milestone holds no open issue except ones waiting only on the owner, each named in the status file.
5. **Whole-repository review**, run last in a fresh context under the "Code Review Rules". Its findings are fixed in the same PR or opened as issues.
6. **Handover.** Status file, backlog and register updated. The Build 1 milestone closes when the PR merges.

## Non-goals

- No new features, widgets, endpoints or schema changes.
- No model calls. The template answer stays `llm: none` (step 2's first PR changes it).
- No dependency upgrades. The major upgrades stay in #71.
- No evaluation coverage table. That is a Design-gate rule; build gates run the evaluation set instead.

## Anti-goals

- A review that runs before the gate's own changes, so the map, the report and the ledger fixes go unchecked.
- Deferred items that vanish: an item dropped from the ledger without being fixed or opened as an issue.
- A "small fix" that grows into feature work. An item that needs a product choice, a new dependency or more than a short change becomes an issue instead.
- An evaluation report whose figures are typed by hand, or that shows a missing figure as zero. Step 1 makes no model calls, so tokens are "none: no model calls", never "0".
- A Floorplan export that holds local paths, secrets, personal data or Health.

## Constraints

- One issue, one branch (`chore/build-1-gate`), one PR. Branch and worktree: `../layover-gate-1`.
- The PR changes code, so it waits for Codex. The documentation-only fallback doesn't apply.
- Floorplan 0.11.0 is still the installed version, which is the version reviewed before the Design gate (`third-party.md`). If the installed version has changed by build time, stop and review it again before running it (owner, 20 Nov 2026: "Review, then run (Recommended)").
- The export checks apply: `tools/check_floorplan.py`, gitleaks, the 4 MB snapshot cap, a hand check for personal data, and the bundled licences in `third-party.md`.
- Numbers are test-first; fixes keep their tests and never weaken an assertion.

## Approaches

- **A. One gate PR, with the review last.** Chosen by the owner, 23 Nov 2026: "A: one PR, review last (Recommended)". It has the same shape as the Design gate and matches `AGENTS.md`, which puts the findings, the snapshot and the report in one tidy-up PR. The review checks the gate's own new work.
- **B. A code PR with the ledger fixes, then a documentation-only gate PR.** Smaller reviews and a fallback path for the second PR, but two review and merge cycles. Any code finding from the review would make the second PR a code PR anyway.
- **C. Review first, then fix everything.** Dropped: the review would never check the new map and report.

## Design

Order of work in the one PR:

### 1. Evaluation report

**(Agent's call)** The runner gets a `--report PATH` option that writes a Markdown report, so no figure is retyped (`AGENTS.md`, "Product figures are never typed by hand"). The report holds:

- the date, the commit and the command run;
- **quality:** the runner's totals line and the per-case table, exactly as printed;
- **speed:** the run's wall-clock time, measured by the runner;
- **tokens:** "none: build step 1 makes no model calls";
- **trip set:** how many traveller scripts and trips the run used, counted by the runner ("none yet" if zero). **(Agent's call)** "Used" means run, not present on disk. The runner loads no traveller scripts yet, so step 1 reports "none yet" and, on a separate line, "1 traveller script on disk, not run yet" (`evals/travellers/lisbon-may.json`). Counting files on disk would suggest a trip was evaluated when none was.

It is saved as `docs/evaluations/reports/build-1.md`. `docs/evaluations/cases.md` links to it, and its "Status" paragraph no longer says only that the Design gate reports no scores. The option is test-first: a test checks that the written report matches the runner's printed totals, and that tokens are never written as 0 when no calls were made.

Expected result, from the run on 23 Nov 2026: "total 53: 0 PASS, 20 SCHEMA PASS, 0 FAIL, 33 NOT RUN, 0 WITHDRAWN". Any FAIL blocks the gate until fixed or explained.

### 2. Floorplan map

1. Confirm the installed version is still 0.11.0.
2. Update the map from the working files in `floorplan/` (git-ignored) to the real code: backend, website, schemas, Aspire app host and tools.
3. Export without Health to `docs/floorplan/build-1.html`. Hand-check for personal data, private material and local paths.
4. **(Agent's call)** Keep `docs/floorplan/design.html` as the Design-gate snapshot. Each gate adds its own file, so the gates can be compared; `AGENTS.md` asks for `<stage>.html` at each gate. This isn't a replacement under the "clean up what you replace" rule.
5. Update `third-party.md` if the bundled code or fonts changed.

### 3. Deferred ledger items

The builder lists every point in the ledger's "deferred" lines (one row per point, not per line) in a table, in the PR's working files: item, PR, outcome, and the commit, issue or reason. Outcomes:

- **fixed here**, with the commit;
- **issue**, with its number;
- **already fixed**, with the commit or file that shows it;
- **no longer applies**, with the reason;
- **accepted earlier** **(agent's call)**: a review already accepted it with a reason (for example the PR C final review's "Triage: leave …" list, or the PR E review's "Accepted with reasons"). It isn't reopened; the row cites that review and its reason.

The files that recorded what each final fix round fixed were in the deleted `../layover-pr-*` worktrees. So the builder checks each item against the current code before choosing "already fixed". This is the largest part of the gate.

Rules for "small" **(agent's call)**: a change to one or two files, with its test, that needs no product choice and no new dependency.

**Traveller-facing text (owner, 23 Nov 2026: "Fix now, you review in PR (Recommended)").** Broken text on screen (for example "May: , typically.", "Compared 1 places", "Nothing is ordered until you press Approve" with no Approve button) is fixed as a bug in this PR. The PR description lists each before → after line. The PR doesn't merge until the owner has approved those lines. Approved product wording that isn't broken is never changed.

Items already tracked by an issue (for example the secret-check gaps in #83) get a comment on that issue instead of a new one. New issues are labelled `noticed`, put in the right milestone and added to `backlog.md` with an order number.

### 4. Triage

For each issue in Goal 4: fix it in the gate if it is small by the same rule, otherwise move it to a named milestone with a one-line reason. Owner-only items (#9, the task label; #79, the contract fields; #90, the privacy choice; #86, TfL terms) stay with the owner. **(Agent's call)** They move to the milestone where the answer is first needed, so Build 1 can close, and the status file lists them under "Owner to-dos". Template candidates (#56, #72, #73, #76, #91, #87, #40) stay labelled `template-candidate` and move to the Build 2 milestone, unless they are a one-line local fix. **(Agent's call)** No new milestone is created; that would be a repository change nobody asked for.

### 5. Whole-repository review

A fresh-context Opus agent reads the whole repository under the "Code Review Rules", after steps 1 to 4. It looks for contradictions, stale statements (for example the README's "design stage" status line, noted in the ledger) and debt. Findings are reported most serious first and fixed in the PR. Anything outside the gate becomes a `noticed` issue. Then the usual pre-push reviews: `requesting-code-review` and `code-security-reviewer`, plus `visual-reviewer` only if a ledger fix changes the website's look.

### 6. Handover

Update `backlog.md` (the new issue added, then closed by the PR; new issues added), the register for any easily reversible call, and `status.md`: the gate is done, the evaluation baseline, the next step (build plan 2). After merge, close the Build 1 milestone.

## Owner decisions in this gate (23 Nov 2026)

- Deferred ledger items: "Fix small, file the rest (Recommended)".
- How the gate is split: "A: one PR, review last (Recommended)".
- Broken traveller-facing text: "Fix now, you review in PR (Recommended)".

All three go in the [register](../../decisions/README.md#register).

## Left to the builder

- The exact Markdown layout of the evaluation report.
- The map's layout and grouping.
- Per-item ledger decisions, under the "small" rule above.
- Commit grouping (one commit per area is enough).
