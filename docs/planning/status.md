# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 19 Nov 2026

## Stage

Design. The repository holds documents only; the FastAPI and Next.js template layers are added when the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

## Open pull requests

- #13 `docs/data-sources-and-earnings` (closes #11): candidate data sources, the earnings decision, and commission built but switched off. The owner merges it.
- `docs/free-api-candidates` (closes #14): the free APIs the owner chose to integrate, ideas for later, and sources considered and not used.

Merged on 19 Nov 2026: #1 (foundation decisions and docs), #2 and #3 (Dependabot), #8 (practices adopted from Vestagraph), #12 (decision 0011 accepted).

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
