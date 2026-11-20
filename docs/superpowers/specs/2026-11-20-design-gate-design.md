# Design gate: design

Issue: [#39](https://github.com/olaheavy-dev/layover/issues/39). Date: 20 Nov 2026.

## Why

The Design stage ends with a gate (`AGENTS.md`, "Review rounds and debt"). The gate shows that the approved design is complete and consistent before any code is written. Build plan 1 starts from what the gate leaves behind: a settled build order, an evaluation case for every part of the journey, and a repository with no stale or contradicting statements.

## Goals

1. **Evaluation coverage.** Every intent, journey step, widget `kind` and decision 0011 rule maps to at least one evaluation case ID. A gap blocks the gate.
2. **Build order.** Section 4 of [01](../../product/01-research-and-direction.md) is rewritten for the agent team and the single-agent baseline ([0012](../../decisions/0012-agent-team.md)). The owner approves it in a prompt window. Then the build milestones are created.
3. **Floorplan snapshot.** A blueprint drawn from the approved design is saved as `docs/floorplan/design.html`.
4. **Audit.** A whole-repository audit in a fresh context. Its findings are fixed in the same PR, or opened as issues when they are outside the gate.
5. **Triage.** Each `noticed` issue (#9, #26, #27, #34, #36) gets a comment: fix in the gate, move to a build step, or close.
6. **Handover.** The status file, backlog and register are updated.

## Non-goals

- No product code, schemas or dependencies. Plan 1 fixes the JSON Schemas, including the four kinds proposed for #26.
- No evaluation harness or scores. The Design gate states "no evaluation set yet".
- No new screens. The boards are approved.

## Anti-goals

- Evaluation cases that only restate a rule without saying what passes and what fails.
- An audit that runs before the new content is written, so the new cases and build order go unchecked.
- A Floorplan export that holds local paths, secrets or personal data.

## Approaches

- **A. One gate PR, with the audit last.** Chosen by the owner ("continue", 20 Nov 2026, after the recommendation). It matches `AGENTS.md`, which puts the coverage table and the snapshot in the tidy-up PR, and the audit also checks the new content.
- **B. Two PRs** (content first, then audit and snapshot). Smaller reviews, but it bends the rule that puts the coverage table and the snapshot in the tidy-up PR.
- **C. Audit first, then add.** The new cases and build order would never be audited.

## Owner decisions in this gate (20 Nov 2026)

- Build order: "Revise it in the gate (Recommended)".
- Floorplan, not yet pinned (agent-workflows#30): "Review, then run (Recommended)". Check what the installed version fetches, runs or sends, then run it, and record the version.

Both go in the [register](../../decisions/README.md#register).

## Design

### 1. Evaluation cases

**(Agent's call)** A new file, `docs/evaluations/cases.md`, holds every case: its ID, what it checks, what passes and what fails, how it is scored (code or a model as judge, as spec §7 says), and its status (`planned` until the build step that adds it). Spec §7 keeps its first 16 cases by ID and links to the file as the master list. Existing IDs keep their meaning.

The coverage table has four parts, one row each:

- **Intents** (spec §5a): `plan_trip`, `destination_facts`, `itinerary`, `fares_and_transport`, `unsupported_travel`, `not_travel`.
- **Journey steps** (spec §5): brief, compare, pick, summary, itinerary, where to stay, try booking, keep it (share).
- **Widget kinds:** the 16 in spec §5d, and the four proposed for #26 that the owner chose in the boards PR.
- **0011 rules:** 1 to 6.

New cases use the existing area codes (`INTENT-`, `BRIEF-`, `COMPARE-`, `ITIN-`, `BOOK-`, `TRIP-`). **(Agent's call)** Two new areas: `WIDGET-` for checks on one widget kind (for example its "not known" state) and `SHARE-` for the shared link (for example the budget left out when the tick box is off).

**(Agent's call) Enforcement** (`AGENTS.md` rule 7): `tools/check_eval_ids.py`, run in `make check`, with tests. It fails when an ID is defined twice in `cases.md`, when an ID is not in `AREA-NN` form, or when an ID is cited anywhere in `docs/` but not defined in `cases.md`. The register line for permanent IDs said this check comes "once evaluation files exist".

### 2. Build order

A rewritten 01 §4 that starts from the foundation and the data contract (plan 1, as the status file says), keeps one plan per part (register, 19 Nov 2026), and keeps the earnings dashboard last. Spec §8 question 6 is then answered. The owner approves it in a prompt window before milestones are created, one per build step.

### 3. Floorplan

1. Read the installed plugin's skill and scripts: what it fetches, runs or sends. Report this to the owner before running it.
2. Draw the blueprint from the spec, the decisions and the build order.
3. Export one HTML file to `docs/floorplan/design.html`. Health is never ticked.
4. Check the export for personal data and private material by hand. Add a local-path check (`/Users/`, `/home/`) to `make check`, as the register line from 19 Nov 2026 asks.
5. Record the plugin version, and the licences of the code and fonts bundled in the export, in `docs/references/third-party.md`.

### 4. Audit

A fresh-context Opus agent reads the whole repository under the "Code Review Rules" in `AGENTS.md`. It looks for contradictions, stale statements and debt, after steps 1 to 3 are written. Its findings are reported, sorted and fixed in the gate PR. Larger findings become issues.

### 5. Triage

**(Agent's call), proposed:**

- #9 stays with the owner (creating a label is a repository setting).
- #26 moves to build plan 1.
- #27 stays open until `tools/` grows or the Python layer lands.
- #34 moves to the build step that shows the `money` widget.
- #36 is fixed in the gate if it is small, otherwise moved to plan 1.

Each issue gets a comment that names where it went.

### 6. Handover

Update the backlog (#39 added, then closed by the PR), the status file and the register.

## Left to the builder

- The exact wording of each new case and its pass and fail lines.
- How `check_eval_ids.py` parses `cases.md` (a Markdown table is enough).
- The layout of the blueprint.
