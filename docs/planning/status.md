# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 19 Nov 2026

## Stage

Design. The repository holds documents only; the FastAPI and Next.js template layers are added when the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

## Open pull requests

- #19 `docs/prompt-window-rule` (closes #18): rule 8 (decisions in a prompt window) and rules from homescout. Codex clean, checks green; owner-only merge (merge rules).
- `docs/journey-design` (closes #20): the main journey design, decision 0012 (a team of agents with a single-agent baseline), and the hotel and saved-trip answers. Waiting for the owner's approval of the design.

Merged on 19 Nov 2026: #1, #2, #3, #8, #12, #13, #15 and #17.

## Next steps

1. Owner reviews and approves the journey design ([spec](../superpowers/specs/2026-11-19-layover-journey-design.md)).
2. Write the build plan (Superpowers `writing-plans`): data contract first, the revised build order for the agent team and the baseline; then a Floorplan blueprint from the approved design.
3. Open questions from the design: Nuitee's terms for sandbox use, and how long a shareable trip link lasts.
4. Before switching commission on (it is built but off): choose a weather source that allows commercial use ([options](../references/data-sources.md#weather-options-for-a-site-that-earns-commission)), check the CAP Code and the other sources' commercial terms ([01 §5](../product/01-research-and-direction.md)).

## Blockers

None.

## Owner to-dos

- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). The partner links API needs its project ID (`trs`), so it is needed before commission is switched on (not before).
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Run `make repo-settings` if not done yet. Five OpenSSF Scorecard alerts are open on `main` (branch protection, code review, maintained, fuzzing, CII best practices); they are repository-level, not caused by any PR.
