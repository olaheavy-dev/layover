# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 21 Nov 2026, end-of-session overwrite (after PR A #57, the CodeQL fix #68 and PR B #67 merged).

## Stage

Build step 1 is under way ("Build 1: Foundation and data contract"). Done today:

- **PR A (#57):** the FastAPI backend and the Next.js website from the house templates.
- **#68:** the board checks read pages with `html.parser` (#36), and the CodeQL warnings on `main` are cleared.
- **PR B (#67):** the data contract, the shared samples and the sample endpoints.

`make repo-settings` was run on 21 Nov 2026, so CodeQL for Python and TypeScript is now a required check. The build order is in [01 §4](../product/01-research-and-direction.md#4-build-order): eight steps, each a milestone.

## Open pull requests

- **Six Dependabot updates (#58 to #63)**, opened when PR A added the backend and frontend:
  - small updates, which merge on green checks: #58 (pnpm action), #59 (frontend minor and patch), #61 (backend minor and patch) and #63 (types-pyyaml);
  - #60, a major frontend update, which needs its migration notes read;
  - #62 (`agent-framework-anthropic`, a `0.`-style beta), where a minor bump counts as major.
- No other PR is open.

## The Design gate (#42, merged 20 Nov 2026)

- **Evaluations:** [docs/evaluations/cases.md](../evaluations/cases.md) holds 53 cases (the first 16 from the spec, 37 new, including `WIDGET-01` to `WIDGET-20`) and a coverage table: every intent, journey step, widget `kind` and decision 0011 rule has at least one case. `tools/check_eval_ids.py` in `make check` fails on a duplicate, badly formed or undefined ID. Score report: **no evaluation set yet** (the first scores come at the build step 1 gate at the earliest).
- **Build order:** approved by the owner ("Approve, parallel per step (Recommended)"): each step is a vertical slice; its plan fixes the data contract, then backend and frontend are built in parallel and joined. The cost cap's figures now come after step 4, the first step that runs a whole trip ([register](../decisions/README.md#register)).
- **Floorplan:** version 0.11.0 reviewed (runs locally; its only outside call is an opt-in waitlist, turned off; files match the published checksums), then a blueprint drawn and exported to [docs/floorplan/design.html](../floorplan/design.html) after the owner checked the map ("Accurate enough"). The 2.2 MB file is exempt from the 1 MB large-file check (owner: "Allow it for snapshots (Recommended)") and from the whitespace hooks, so it stays byte-for-byte as exported (Codex found that a trimmed script broke the map; fixed and checked in headless Chrome). `tools/check_floorplan.py` fails on common local-path, `file://` and git-remote forms, and on any inline script that no longer matches the page's Content-Security-Policy. The blueprint's working files stay local in `floorplan/` (git-ignored), so build step 1 can turn it into a map of the real code.
- **Audit:** a fresh-context whole-repository audit found 20 items (4 P1, 7 P2, 9 P3). Fixed in the PR, except two `noticed` issues (#40, #41) and two left on purpose (accepted records 0003 and 0004 aren't rewritten; the model named in the snapshot comes from 0007 and is confirmed in the step 2 plan).
- **Triage:** #9, #26, #27, #36 (done in #68) and #40 in Build 1; #35 and #41 in Build 2; #34 in Build 3. No open `review-followup` issue.
- **Reviews:** the audit, a pre-push review and a security review (Opus, fresh contexts), then Codex: one P1 (the snapshot's blocked script), fixed; the re-review found nothing.

## Next steps

1. **Dependabot:** triage #58 to #63 (above) before starting new work, so PRs C and D begin from current packages.
2. **PRs C (#53, backend foundation) and D (#54, website) in parallel**, then **E (#55, join and Aspire)**, then the step 1 gate. Issues #53 to #55 are on the [project board](https://github.com/orgs/olaheavy-dev/projects/5).
3. **Carry into PR C (#53):** the `round_estimate` tests need a case that lands exactly on £5 (half up); PR B's samples never do, and they are worked by hand in `schemas/samples/README.md`.
4. **Carry into PR E (#55):** the backend's Docker image holds no `schemas/` folder, so the sample endpoints answer 503 there until the image ships the samples or `SAMPLES_DIR` points at them (`backend/Dockerfile` belongs to the template).

## Blockers

None. Owner decisions still open, needed later:

- How long a working trip link and a shared trip link last (before step 7).
- The cost-cap figures, after step 4 measures a whole trip's cost.
- The vector database (step 3), and hosting and the database (step 7).
- Before build step 2 (the first model calls): Anthropic's terms for a public app, its data retention and its prices (spending needs the owner's approval; the prices also feed the cost cap); and LangSmith's region (US or EU), retention and terms, because its traces would hold travellers' messages (UK GDPR). Build step 1 makes no model calls, so neither blocks it.
- Build step 4: Layover's own token figures for the agent team against the single-agent baseline (`TRIP-01`); any outside figure quoted before then cites its source.
- Build step 7: how to stop scripts from starting trips. ALTCHA (a free, open-source bot check that doesn't track visitors) is one option to weigh alongside the hashed-address limit (spec §5c).

## Owner to-dos

- Make the mood scenes in ChatGPT from the prompts in [mood-scene-prompts.md](../design/boards/mood-scene-prompts.md) (welcome and "How Layover works" only), and send them to the agent to register before they are committed ([#35](https://github.com/olaheavy-dev/layover/issues/35)).
- Before Layover goes public: read OpenAI's sharing and publication policy again by hand, for the mood scenes' labelling.
- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Review the process issues in the weekly process review: [agent-workflows#31](https://github.com/olaheavy-dev/agent-workflows/issues/31) (brainstorming's open questions bypassed the prompt-window rule), [#32](https://github.com/olaheavy-dev/agent-workflows/issues/32) (research quotes reached docs unchecked), [#33](https://github.com/olaheavy-dev/agent-workflows/issues/33) (design options as whole screens; restrained palettes), [#35](https://github.com/olaheavy-dev/agent-workflows/issues/35) (a readiness review before a phase that builds from approved documents) [#38](https://github.com/olaheavy-dev/agent-workflows/issues/38) (ask for the feel and reference logos before drawing logo options) and [#39](https://github.com/olaheavy-dev/agent-workflows/issues/39) (generated files changed by commit hooks; check them in a browser) and [#41](https://github.com/olaheavy-dev/agent-workflows/issues/41) (the alert check before merging missed alerts that a newly turned-on CodeQL language brings in).
- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Tavily: create a free account and API key when the web-search step is built.
- Nuitee: create an account and sandbox key before build step 6 (owner's call, 21 Nov 2026: use the sandbox without asking Nuitee, #46).
- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). It is needed before commission is switched on, not before.
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Six OpenSSF Scorecard alerts are open on `main`: branch protection, code review, maintained, fuzzing, CII best practices, and pinned dependencies (in the template's `frontend/Dockerfile`). They are repository-health grades and don't block merges (owner: "Exempt Scorecard grades (Recommended)"); improve them when possible.
- Template updates: add `TEMPLATE_UPDATE_TOKEN` to the `template-update` environment in the repository settings (a fine-grained token with contents and pull-requests write on this repository). Without it, template updates arrive as an issue instead of a pull request.
