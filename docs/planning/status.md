# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 19 Nov 2026

## Stage

Design. The repository holds documents only; the FastAPI and Next.js template layers are added when the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

## Open pull requests

- `docs/accept-0011` (closes #10): decision 0011 accepted by the owner ("Accept all six (Recommended)"); its rules are in `.claude/rules/product-integrity.md`.
- #8 `docs/adopt-vestagraph-practices` (closes #4 to #7): practices adopted from Vestagraph; waiting for Codex's review of its latest commit.

Merged on 19 Nov 2026: #1 (foundation decisions and docs), #2 and #3 (Dependabot).

## Next steps

1. Answer the first open design question: what the traveller has already decided when they open Layover ([01 §5](../product/01-research-and-direction.md)).
2. Continue the design (brainstorming), then write the design document and plan.

## Blockers

None.

## Owner to-dos

- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Travelpayouts project: create it once the repository or site exists.
- After the GitHub repository exists: run `make repo-settings`, and connect the repository to Codex review.
