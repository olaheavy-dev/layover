# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 19 Nov 2026

## Stage

Design. The repository holds documents only; the FastAPI and Next.js template layers are added when the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

## Open pull requests

- `docs/accept-0011` (closes #10): decision 0011 accepted by the owner ("Accept all six (Recommended)"); its rules are in `.claude/rules/product-integrity.md` and named in `AGENTS.md`.
- `docs/data-sources-and-earnings` (closes #11): candidate data sources and the earnings decision; in progress.

Merged on 19 Nov 2026: #1 (foundation decisions and docs), #2 and #3 (Dependabot), #8 (practices adopted from Vestagraph: test-first, live-test, IDs, stage gates, backlog, review fallback).

## Next steps

1. Answer the first open design question: what the traveller has already decided when they open Layover ([01 §5](../product/01-research-and-direction.md)).
2. Continue the design (brainstorming), then write the design document and plan.

## Blockers

None.

## Owner to-dos

- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Travelpayouts project: create it once the repository or site exists.
- Run `make repo-settings` if not done yet. Five OpenSSF Scorecard alerts are open on `main` (branch protection, code review, maintained, fuzzing, CII best practices); they are repository-level, not caused by any PR.
