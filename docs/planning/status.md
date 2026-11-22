# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 22 Nov 2026, end-of-session overwrite (after #75, #77, #84 and #94 merged).

## Stage

Build step 1 is under way ("Build 1: Foundation and data contract"). Done:

- **PR A (#57):** the FastAPI backend and the Next.js website from the house templates.
- **#68:** the board checks read pages with `html.parser` (#36), and the CodeQL warnings on `main` are cleared.
- **PR B (#67):** the data contract, the shared samples and the sample endpoints.
- **22 Nov 2026:**
  - the Dependabot updates (#58, #61, #62, #63) and the website's minor and patch updates (#75); the major upgrades wait in #71;
  - decision 0013, Microsoft Agent Framework in Python (#77);
  - **PR C (#84):** the backend foundation: money, recordings, holidays and the evaluation runner. The runner's total is "53: 0 PASS, 20 SCHEMA PASS, 0 FAIL, 33 NOT RUN, 0 WITHDRAWN";
  - the owner's map choice: MapLibre GL JS with OpenFreeMap's free tiles, recorded in the [register](../decisions/README.md#register); the map is drawn in #93 (Build 3), and the widget lists its places with links until then;
  - #62 (`agent-framework-anthropic`, a pre-release) was reviewed as a major update: Codex, then [a comparison of the two published wheels](https://github.com/olaheavy-dev/layover/pull/62#discussion_r4658085468), because MAF's GitHub repository returned 404;
  - **PR D (#94):** the website (home, trip, shared trip, How Layover works, link not found), the 20 widgets in every state and the development gallery, with axe, page titles, fonts, a 390 px phone width and screenshots in Playwright's Linux image.

`make repo-settings` was run on 21 Nov 2026, so CodeQL for Python and TypeScript is now a required check. The build order is in [01 §4](../product/01-research-and-direction.md#4-build-order): eight steps, each a milestone.

## Open pull requests

None apart from this handover PR.

## The Design gate (#42, merged 20 Nov 2026)

- **Evaluations:** [docs/evaluations/cases.md](../evaluations/cases.md) holds 53 cases (the first 16 from the spec, 37 new, including `WIDGET-01` to `WIDGET-20`) and a coverage table: every intent, journey step, widget `kind` and decision 0011 rule has at least one case. `tools/check_eval_ids.py` in `make check` fails on a duplicate, badly formed or undefined ID. Score report: **no evaluation set yet** (the first scores come at the build step 1 gate at the earliest).
- **Build order:** approved by the owner ("Approve, parallel per step (Recommended)"): each step is a vertical slice; its plan fixes the data contract, then backend and frontend are built in parallel and joined. The cost cap's figures now come after step 4, the first step that runs a whole trip ([register](../decisions/README.md#register)).
- **Floorplan:** version 0.11.0 reviewed (runs locally; its only outside call is an opt-in waitlist, turned off; files match the published checksums), then a blueprint drawn and exported to [docs/floorplan/design.html](../floorplan/design.html) after the owner checked the map ("Accurate enough"). The 2.2 MB file is exempt from the 1 MB large-file check (owner: "Allow it for snapshots (Recommended)") and from the whitespace hooks, so it stays byte-for-byte as exported (Codex found that a trimmed script broke the map; fixed and checked in headless Chrome). `tools/check_floorplan.py` fails on common local-path, `file://` and git-remote forms, and on any inline script that no longer matches the page's Content-Security-Policy. The blueprint's working files stay local in `floorplan/` (git-ignored), so build step 1 can turn it into a map of the real code.
- **Audit:** a fresh-context whole-repository audit found 20 items (4 P1, 7 P2, 9 P3). Fixed in the PR, except two `noticed` issues (#40, #41) and two left on purpose (accepted records 0003 and 0004 aren't rewritten; the model named in the snapshot comes from 0007 and is confirmed in the step 2 plan).
- **Triage:** #9, #26, #27, #36 (done in #68) and #40 in Build 1; #35 and #41 in Build 2; #34 in Build 3. No open `review-followup` issue.
- **Reviews:** the audit, a pre-push review and a security review (Opus, fresh contexts), then Codex: one P1 (the snapshot's blocked script), fixed; the re-review found nothing.

## Next steps

1. **PR E (#55): join the website to the API and add Aspire** (plan Tasks 19 and 20), then the **step 1 gate** (a whole-repository review, a tidy-up PR, `noticed` issues triaged, a Floorplan snapshot, and the first evaluation report). Issues are on the [project board](https://github.com/orgs/olaheavy-dev/projects/5).
2. **The progress ledger** for build plan 1 is in `.superpowers/sdd/2026-11-21-build-step-1/progress.md` (git-ignored, on the owner's machine): Tasks 8 to 20 are done (PR E is waiting for review). It lists every ruling made and every deferred review item.
3. **Keep the template answer `llm: none` in step 1:** step 2's first PR changes it to `llm: maf` (0013 point 1). (The £5 half-up case that PR B's samples never hit is now covered by `test_estimate_nearest_ten` and `test_round_estimate_ten_pound_boundaries`.)
4. **Done in PR E (#55), tasks 19 and 20:** `make dev-all` runs the Aspire app host (`apphost/`): PostgreSQL, the migrations, the backend and the website, with traces from the website through the backend in the Aspire dashboard. Task 19: the website reads the samples through the API (`GET /v1/sample/trip` and `/v1/sample/widgets`) and renders those pages on each request, so `make image-frontend` builds without the sample files. The backend image gets the samples through a named extra build context (`additional_contexts` in `backend/compose.yaml`, `COPY --from=samples` in `backend/Dockerfile`), and `make image` builds. Both are template-owned files, so the PR is labelled template-candidate. The API checks the samples against the schema; the website no longer reads them from disk.
5. **Step 2: check the full trace.** The first step with a database route checks that one Aspire trace runs from the website through the backend to PostgreSQL (register, 22 Nov 2026). Step 1 shows website to backend by hand, and `test_database_queries_create_spans` proves queries create spans.
6. **Watch for upstream support (#71):** OpenTelemetry SDK 3 (waits for `@vercel/otel`), ESLint 10 (waits for the plugins in `eslint-config-next`) and TypeScript 7 (waits for typescript-eslint and openapi-typescript). jsdom 31 isn't blocked; it moves with that batch for one review.

## Blockers

None. Owner decisions still open, needed later:

- How long a working trip link and a shared trip link last (before step 7).
- The cost-cap figures, after step 4 measures a whole trip's cost.
- The vector database (step 3), and hosting and the database (step 7).
- Before build step 2 (the first model calls): Anthropic's terms for a public app, its data retention and its prices (spending needs the owner's approval; the prices also feed the cost cap); and LangSmith's region (US or EU), retention and terms, before MAF's sensitive-data setting is turned on, because traces would then hold travellers' messages (UK GDPR; [0013](../decisions/0013-microsoft-agent-framework.md) point 5). Build step 1 makes no model calls, so neither blocks it.
- Build step 4: Layover's own token figures for the agent team against the single-agent baseline (`TRIP-01`); any outside figure quoted before then cites its source.
- Build step 7: how to stop scripts from starting trips. ALTCHA (a free, open-source bot check that doesn't track visitors) is one option to weigh alongside the hashed-address limit (spec §5c).

## Owner to-dos

- Make the mood scenes in ChatGPT from the prompts in [mood-scene-prompts.md](../design/boards/mood-scene-prompts.md) (welcome and "How Layover works" only), and send them to the agent to register before they are committed ([#35](https://github.com/olaheavy-dev/layover/issues/35)).
- Before Layover goes public: read OpenAI's sharing and publication policy again by hand, for the mood scenes' labelling.
- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Review the process issues in the weekly process review: [agent-workflows#31](https://github.com/olaheavy-dev/agent-workflows/issues/31) (brainstorming's open questions bypassed the prompt-window rule), [#32](https://github.com/olaheavy-dev/agent-workflows/issues/32) (research quotes reached docs unchecked), [#33](https://github.com/olaheavy-dev/agent-workflows/issues/33) (design options as whole screens; restrained palettes), [#35](https://github.com/olaheavy-dev/agent-workflows/issues/35) (a readiness review before a phase that builds from approved documents) [#38](https://github.com/olaheavy-dev/agent-workflows/issues/38) (ask for the feel and reference logos before drawing logo options) and [#39](https://github.com/olaheavy-dev/agent-workflows/issues/39) (generated files changed by commit hooks; check them in a browser) and [#41](https://github.com/olaheavy-dev/agent-workflows/issues/41) (the alert check before merging missed alerts that a newly turned-on CodeQL language brings in); from 22 Nov 2026, [#43](https://github.com/olaheavy-dev/agent-workflows/issues/43) (confirm each required check reported on the head commit) and [#45](https://github.com/olaheavy-dev/agent-workflows/issues/45) (the pre-flight check should search recorded owner answers for the settings a change touches).
- Review the copy in [PR #94's description](https://github.com/olaheavy-dev/layover/pull/94) (the list of new fixed wording, including the page titles and "This link does not work").
- Confirm the fixed TfL Journey Planner link in the transport widget, and check TfL's terms for the "Geomni UK Map data" credit ([#86](https://github.com/olaheavy-dev/layover/issues/86)).
- Decide which contract fields the boards show but the contract lacks ([#79](https://github.com/olaheavy-dev/layover/issues/79)).
- Follow-ups opened from PR D's reviews: [#89](https://github.com/olaheavy-dev/layover/issues/89) (widget consistency), [#90](https://github.com/olaheavy-dev/layover/issues/90) (a shared trip reveals the party size: your privacy decision), [#91](https://github.com/olaheavy-dev/layover/issues/91) (template drift) and [#92](https://github.com/olaheavy-dev/layover/issues/92) (layout drift from the boards).
- Copy review of the holiday names' American spelling ("Labor Day", [#80](https://github.com/olaheavy-dev/layover/issues/80)).
- Watch Portugal's Proposta de Lei 77/XVII/1 (labour reform) in case it changes article 234 of the Labour Code, the list the holidays test relies on.
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
