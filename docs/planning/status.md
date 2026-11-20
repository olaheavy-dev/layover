# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 20 Nov 2026, end of the Design gate session (#39).

## Stage

The Design gate is in review (issue #39); when it merges, the Design stage is closed and build step 1 starts. The repository still holds documents and their checks only. The build order is approved: eight steps in [01 §4](../product/01-research-and-direction.md#4-build-order), each a milestone ("Build 1: Foundation and data contract" to "Build 8: Earnings dashboard").

## Open pull requests

- The Design gate PR (closes issue #39): evaluation cases, build order, Floorplan snapshot, audit fixes and triage. Owner-merge (it changes a template-owned check).

## The Design gate (#39, 20 Nov 2026)

- **Evaluations:** [docs/evaluations/cases.md](../evaluations/cases.md) holds 53 cases (the first 16 from the spec, 37 new, including `WIDGET-01` to `WIDGET-20`) and a coverage table: every intent, journey step, widget `kind` and decision 0011 rule has at least one case. `tools/check_eval_ids.py` in `make check` fails on a duplicate, badly formed or undefined ID. Score report: **no evaluation set yet** (the first scores come at the build step 1 gate at the earliest).
- **Build order:** approved by the owner ("Approve, parallel per step (Recommended)"): each step is a vertical slice; its plan fixes the data contract, then backend and frontend are built in parallel and joined. The cost cap's figures now come after step 4, the first step that runs a whole trip ([register](../decisions/README.md#register)).
- **Floorplan:** version 0.11.0 reviewed (runs locally; its only outside call is an opt-in waitlist, turned off; files match the published checksums), then a blueprint drawn and exported to [docs/floorplan/design.html](../floorplan/design.html) after the owner checked the map ("Accurate enough"). The 2.2 MB file is exempt from the 1 MB large-file check (owner: "Allow it for snapshots (Recommended)"); `tools/check_floorplan.py` fails on common local-path, `file://` and git-remote forms (its docstring lists them). The blueprint's working files stay local in `floorplan/` (git-ignored), so build step 1 can turn it into a map of the real code.
- **Audit:** a fresh-context whole-repository audit found 20 items (4 P1, 7 P2, 9 P3). Fixed in the PR, except two `noticed` issues (#40, #41) and two left on purpose (accepted records 0003 and 0004 aren't rewritten; the model named in the snapshot comes from 0007 and is confirmed in the step 2 plan).
- **Triage:** #9, #26, #27, #36 and #40 in Build 1; #35 and #41 in Build 2; #34 in Build 3. No open `review-followup` issue.

## Next steps

1. **Merge the Design gate PR** once Codex has reviewed it (owner merge).
2. **Build plan 1** ([01 §4](../product/01-research-and-direction.md#4-build-order), step 1): brainstorm, then write the plan, fixing the data contract first. Decide on a GitHub project board when it starts (owner: "Wait until build (Recommended)").

## Blockers

None. Owner decisions still open, needed later:

- Nuitee's terms for sandbox and price-index use (ask Nuitee before step 6), and approving the price-index spend before its switch is turned on.
- How long a working trip link and a shared trip link last (before step 7).
- The cost-cap figures, after step 4 measures a whole trip's cost.
- The vector database (step 3), and hosting and the database (step 7).
- How the fonts are served in the app: the boards commit the font files (owner, 20 Nov 2026), and the frontend plan reuses them unless it records a reason not to.

## Owner to-dos

- Ask Nuitee whether a portfolio project may use its sandbox and price index.
- Make the mood scenes in ChatGPT from the prompts in [mood-scene-prompts.md](../design/boards/mood-scene-prompts.md) (welcome and "How Layover works" only), and send them to the agent to register before they are committed ([#35](https://github.com/olaheavy-dev/layover/issues/35)).
- Before Layover goes public: read OpenAI's sharing and publication policy again by hand, for the mood scenes' labelling.
- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Review the process issues in the weekly process review: [agent-workflows#31](https://github.com/olaheavy-dev/agent-workflows/issues/31) (brainstorming's open questions bypassed the prompt-window rule), [#32](https://github.com/olaheavy-dev/agent-workflows/issues/32) (research quotes reached docs unchecked), [#33](https://github.com/olaheavy-dev/agent-workflows/issues/33) (design options as whole screens; restrained palettes), [#35](https://github.com/olaheavy-dev/agent-workflows/issues/35) (a readiness review before a phase that builds from approved documents) and [#38](https://github.com/olaheavy-dev/agent-workflows/issues/38) (ask for the feel and reference logos before drawing logo options).
- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Merge the Design gate PR yourself: it changes `.pre-commit-config.yaml` (the large-file exemption for Floorplan snapshots), a template-owned check.
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Tavily: create a free account and API key when the web-search step is built.
- Nuitee: create an account and sandbox key once Nuitee agrees to portfolio use.
- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). It is needed before commission is switched on, not before.
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Run `make repo-settings` if not done yet. Five OpenSSF Scorecard alerts are open on `main` (branch protection, code review, maintained, fuzzing, CII best practices). They are repository-health grades and don't block merges (owner: "Exempt Scorecard grades (Recommended)"); improve them when possible.
