# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 19 Nov 2026

## Stage

Design. The repository holds documents only; the FastAPI and Next.js template layers are added when the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

## Open pull requests

- `docs/project-foundations`: decision records 0003 to 0011, the research and direction draft, data sources, the TripMate review and this file.
- #2 and #3: Dependabot updates (zizmor pre-commit hook v1.31.1 to 1.32.0; six GitHub Actions updates). Small dependency updates merge on green checks unless one is a major bump.
- `docs/adopt-vestagraph-practices` (stacked on the PR above; closes #4 to #7): practices adopted from Vestagraph: the `test-first` skill, hand-worked expected values, the criteria-to-test map, the step and skill table, live-service tests kept out of the merge check, permanent evaluation IDs, stage gates, the [ordered backlog](backlog.md) and a one-hour review fallback. The owner merges it (it changes the merge rules).

## Next steps

1. Answer the first open design question: what the traveller has already decided when they open Layover ([01 §5](../product/01-research-and-direction.md)).
2. Continue the design (brainstorming), then write the design document and plan.
3. Decide on the proposed product integrity rules ([0011](../decisions/0011-product-integrity-rules.md)).

## Blockers

None.

## Owner to-dos

- Merge `docs/project-foundations`, then `docs/adopt-vestagraph-practices` (owner-only: merge rules). After `docs/project-foundations` merges, the agent merges `main` into `docs/adopt-vestagraph-practices` and requests a fresh `@codex review` before it can merge.
- Create the `task` label (the Task issue form applies it, but the repository doesn't have it).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Travelpayouts project: create it once the repository or site exists.
- Run `make repo-settings`, and connect the repository to Codex review, if not done yet.
