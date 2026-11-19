# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 19 Nov 2026

## Stage

Design. The repository holds documents only; the FastAPI and Next.js template layers are added when the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

## Open pull requests

- `docs/free-api-candidates` (#15, closes #14): the free APIs the owner chose to integrate, ideas for later, and sources considered and not used. The owner authorised the agent to merge it once Codex and the checks are clean.

Merged on 19 Nov 2026: #1 (foundation decisions and docs), #2 and #3 (Dependabot), #8 (practices adopted from Vestagraph), #12 (decision 0011 accepted; its rules in `.claude/rules/product-integrity.md`), #13 (candidate data sources, the earnings decision, commission built but switched off).

## Next steps

1. Answer the first open design question: what the traveller has already decided when they open Layover ([01 §5](../product/01-research-and-direction.md)).
2. Continue the design (brainstorming), then write the design document and plan.
3. Research free APIs that add value (#14): trip timing, places and maps, getting there and around, practical and safety context; the owner then picks which to integrate.
4. Before switching commission on (it is built but off): choose a weather source that allows commercial use ([options](../references/data-sources.md#weather-options-for-a-site-that-earns-commission)), check the CAP Code and the other sources' commercial terms ([01 §5](../product/01-research-and-direction.md)).

## Blockers

None.

## Owner to-dos

- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). The partner links API needs its project ID (`trs`), so it is needed before commission is switched on (not before).
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Run `make repo-settings` if not done yet. Five OpenSSF Scorecard alerts are open on `main` (branch protection, code review, maintained, fuzzing, CII best practices); they are repository-level, not caused by any PR.
