# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 23 Nov 2026, end-of-session overwrite (after the gate, #112, and the owner's to-dos: #9, #79 split, #107 copy review).

## Stage

Build step 1 ("Build 1: Foundation and data contract") is finished: all 20 tasks of build plan 1 merged in PRs A to E (#57, #67, #84, #94, #98). Its gate (#106) merged in #112 on 23 Nov 2026, and the Build 1 milestone is closed. Build step 2 ("Chat, intents and the brief") is next.

The build order is in [01 §4](../product/01-research-and-direction.md#4-build-order): eight steps, each a milestone. `make repo-settings` was run on 21 Nov 2026, so CodeQL for Python and TypeScript is a required check.

## Open pull requests

None apart from this handover PR.

## The build step 1 gate (#106, merged in #112)

One PR, with the whole-repository review run last (owner: "A: one PR, review last (Recommended)").

- **Evaluation baseline:** the runner now writes its own report (`--report`), so no figure is retyped: [reports/build-1.md](../evaluations/reports/build-1.md). Later gates compare against it, and a drop blocks a gate.
- **Floorplan:** a map of the real code, [docs/floorplan/build-1.html](../floorplan/build-1.html), from Floorplan 0.11.0 (the reviewed version), exported without Health. The owner looked at it and answered "Accurate enough (Recommended)"; it was exported again afterwards to correct labels and wording (gate review G2 and G3). `design.html` stays as the Design-gate snapshot.
- **Deferred review points:** the 90 points that the build step 1 reviews put off were sorted against the code (owner: "Fix small, file the rest (Recommended)"): 36 already fixed, 27 tracked in issues, 13 accepted earlier with a reason, 9 fixed in the gate, 5 no longer apply. The table is in the PR description.
- **Traveller text:** three broken lines fixed, four strings in all (owner: "Fix now, you review in PR (Recommended)"); the owner approved them before the merge ("Approve and merge (Recommended)").
- **Triage:** #85 fixed; the other 16 Build 1 issues moved, each with a reason comment (14 to Build 2, #86 to Build 4, #90 to Build 7). New issues: #107 to #111.
- **Whole-repository review:** 18 findings (1 P1, 6 P2, 11 P3), 15 fixed in the gate and 3 opened as issues (#109, #110, #111). The P1 was a missing data-sources row for SIX Group's ISO 4217 list; the owner chose "Cite SIX, record the risk (Recommended)" (register, 23 Nov 2026).
- **CodeQL alert #19** (`js/missing-origin-check` in `build-1.html`, the elkjs message handler that Floorplan bundles) blocked the merge. The owner dismissed it as "won't fix", the same decision as #16 for `design.html` (owner: "Dismiss it like #16 (Recommended)"); the reason is recorded on #112. Each gate's new snapshot can raise it again.
- Codex found no issues; every check passed. No `review-followup` issue is open.

The Design gate (#42, 20 Nov 2026) is recorded in its PR and in [its design](../superpowers/specs/2026-11-20-design-gate-design.md).

## Next steps

1. **Build plan 2** ("Chat, intents and the brief"): brainstorm, then the plan, which fixes the data contract first. Its first PR changes the template answer `llm: none` to `llm: maf` (0013 point 1).
2. **Step 2: check the full trace.** The first step with a database route checks that one Aspire trace runs from the website through the backend to PostgreSQL (register, 22 Nov 2026).
3. **Step 7 (hosting):** an image-publishing workflow must pass `--build-context samples=schemas/samples` to the backend build. A failed trip page answers HTTP 200, so uptime checks should watch the backend's `/health/ready`.
4. **Template candidates** (labelled `template-candidate`, Build 2): offer them to house-template-base in one batch.
5. **Watch for upstream support (#71):** OpenTelemetry SDK 3, ESLint 10, TypeScript 7; jsdom 31 moves with that batch.

## Blockers

None. Owner decisions still open, needed later:

- How long a working trip link and a shared trip link last (before step 7).
- The cost-cap figures, after step 4 measures a whole trip's cost.
- The vector database (step 3), and hosting and the database (step 7).
- Before build step 2 (the first model calls): Anthropic's terms for a public app, its data retention and its prices (spending needs the owner's approval; the prices also feed the cost cap); and LangSmith's region (US or EU), retention and terms, before MAF's sensitive-data setting is turned on, because traces would then hold travellers' messages (UK GDPR; [0013](../decisions/0013-microsoft-agent-framework.md) point 5). Build step 1 makes no model calls, so neither blocks it.
- Build step 4: Layover's own token figures for the agent team against the single-agent baseline (`TRIP-01`); any outside figure quoted before then cites its source.
- Build step 7: how to stop scripts from starting trips. ALTCHA (a free, open-source bot check that doesn't track visitors) is one option to weigh alongside the hashed-address limit (spec §5c).

## Owner to-dos

- **In build step 2's plan:** settle #79 (the brief's `filled` state). The other missing contract fields are in #114, #115 and #116, one per later step.
- **Confirm SIX Group's terms in a browser:** the [data sources](../references/data-sources.md) row for the ISO 4217 list summarises an automated read of SIX's [terms of use](https://www.six-group.com/en/services/legal/terms-of-use.html); check the wording matches.
- Make the mood scenes in ChatGPT from the prompts in [mood-scene-prompts.md](../design/boards/mood-scene-prompts.md) (welcome and "How Layover works" only), and send them to the agent to register before they are committed ([#35](https://github.com/olaheavy-dev/layover/issues/35)).
- Before Layover goes public: read OpenAI's sharing and publication policy again by hand, for the mood scenes' labelling.
- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Review the process issues in the weekly process review: [agent-workflows#31](https://github.com/olaheavy-dev/agent-workflows/issues/31) (brainstorming's open questions bypassed the prompt-window rule), [#32](https://github.com/olaheavy-dev/agent-workflows/issues/32) (research quotes reached docs unchecked), [#33](https://github.com/olaheavy-dev/agent-workflows/issues/33) (design options as whole screens; restrained palettes), [#35](https://github.com/olaheavy-dev/agent-workflows/issues/35) (a readiness review before a phase that builds from approved documents) [#38](https://github.com/olaheavy-dev/agent-workflows/issues/38) (ask for the feel and reference logos before drawing logo options) and [#39](https://github.com/olaheavy-dev/agent-workflows/issues/39) (generated files changed by commit hooks; check them in a browser) and [#41](https://github.com/olaheavy-dev/agent-workflows/issues/41) (the alert check before merging missed alerts that a newly turned-on CodeQL language brings in); from 22 Nov 2026, [#43](https://github.com/olaheavy-dev/agent-workflows/issues/43) (confirm each required check reported on the head commit), [#45](https://github.com/olaheavy-dev/agent-workflows/issues/45) (the pre-flight check should search recorded owner answers for the settings a change touches), [#51](https://github.com/olaheavy-dev/agent-workflows/issues/51) (test a plan's end-to-end checks against what the code can do by then) and [#52](https://github.com/olaheavy-dev/agent-workflows/issues/52) (parallel reviewers in one worktree collide on test server ports); from 23 Nov 2026, [#54](https://github.com/olaheavy-dev/agent-workflows/issues/54) (the push hook's two messages contradict each other), [#55](https://github.com/olaheavy-dev/agent-workflows/issues/55) (register lines put the agent's reasons in the owner's mouth), and a new case on [#41](https://github.com/olaheavy-dev/agent-workflows/issues/41) (the alert check looked at the PR's head, not its merge ref).
- Review the copy in [PR #94's description](https://github.com/olaheavy-dev/layover/pull/94) (the list of new fixed wording, including the page titles and "This link does not work").
- Confirm the fixed TfL Journey Planner link in the transport widget, and check TfL's terms for the "Geomni UK Map data" credit ([#86](https://github.com/olaheavy-dev/layover/issues/86)).
- Follow-ups opened from PR D's reviews: [#89](https://github.com/olaheavy-dev/layover/issues/89) (widget consistency), [#90](https://github.com/olaheavy-dev/layover/issues/90) (a shared trip reveals the party size: your privacy decision), [#91](https://github.com/olaheavy-dev/layover/issues/91) (template drift) and [#92](https://github.com/olaheavy-dev/layover/issues/92) (layout drift from the boards).
- Review the new fixed wording from PR E: the error page title "Something went wrong · Layover" ([#98](https://github.com/olaheavy-dev/layover/pull/98)).
- Copy review of the holiday names' American spelling ("Labor Day", [#80](https://github.com/olaheavy-dev/layover/issues/80)).
- Watch Portugal's Proposta de Lei 77/XVII/1 (labour reform) in case it changes article 234 of the Labour Code, the list the holidays test relies on.
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Tavily: create a free account and API key when the web-search step is built.
- Nuitee: create an account and sandbox key before build step 6 (owner's call, 21 Nov 2026: use the sandbox without asking Nuitee, #46).
- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). It is needed before commission is switched on, not before.
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Six OpenSSF Scorecard alerts are open on `main`: branch protection, code review, maintained, fuzzing, CII best practices, and pinned dependencies (in the template's `frontend/Dockerfile`). They are repository-health grades and don't block merges (owner: "Exempt Scorecard grades (Recommended)"); improve them when possible.
- Template updates: add `TEMPLATE_UPDATE_TOKEN` to the `template-update` environment in the repository settings (a fine-grained token with contents and pull-requests write on this repository). Without it, template updates arrive as an issue instead of a pull request.
