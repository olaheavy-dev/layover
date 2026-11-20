# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 20 Nov 2026, end of the session (the boards merged in #37).

## Stage

Design. The repository holds documents and their checks only. The main journey design (#21), the design foundations (#29), the boards readiness (#32) and the boards (#37) are merged: every screen and widget state is drawn in [docs/design/boards/](../design/boards/index.html). The Design gate comes next, then build plan 1. The FastAPI template layer comes with build plan 1, and the Next.js layer when frontend work starts ([0010](../decisions/0010-repository-and-stages.md), [spec §9](../superpowers/specs/2026-11-19-layover-journey-design.md)).

## Open pull requests

- This handover PR (end-of-session status and backlog).

## The boards (#37, merged 20 Nov 2026)

18 board pages and about 60 screens, listed with their states and two coverage tables in [index.html](../design/boards/index.html). The repository files are the master copy; a private claude.ai artifact shows the same boards (owner: "Repo + private artifact (Recommended)"). Its link is in the session chat, not here, because it is private.

Settled by the owner on 20 Nov 2026 (each answer is in the [register](../decisions/README.md#register)): the look (direction E, "harbour at night" dark theme), labels once per card with prices always labelled, long chats (grouped checks, "Jump to latest"), the phone trip strip, vague messages ("Which Valencia?", `BRIEF-03`), the logo (S3, the suitcase character, after five rounds), isometric illustrations matching the logo, the proposed widgets for #26, the side-answer and itinerary-only rules, and sharing ("Ask when sharing": a tick box for budget and travellers, off by default). Agent's calls: Layover asks for exact dates before booking and never picks them; the light warning colour is #964710 to keep 4.5:1 on tinted surfaces.

Reviews: design, visual, pre-push (Opus) and security reviews in fresh contexts, then Codex (one P2, fixed; the re-review found nothing). `make check` runs 105 tests; the contrast check covers text and status colours on the tinted surfaces, and the board check covers scripts, token overrides, register cells and the board index.

Follow-ups: #26 (schemas for the proposed widgets, build plan 1), #34 (no source for a place's currency), #35 (mood scenes, waiting for the owner's images), #36 (harden the board checks with a real HTML parser).

## Done on 19 Nov 2026

| Pull request | What merged |
|---|---|
| #1 | Foundation: decision records 0003 to 0011, the research and direction draft (01), data sources, the TripMate review |
| #2, #3 | Dependabot updates (pre-commit zizmor hook; six GitHub Actions) |
| #8 | Practices from Vestagraph: the `test-first` skill, hand-worked expected values, the criteria-to-test map, the step and skill table, live-service tests kept out of the merge check, permanent evaluation IDs, stage gates, the [ordered backlog](backlog.md), the review fallback |
| #12 | Decision 0011 (product integrity rules) accepted; its rules in `.claude/rules/product-integrity.md` |
| #13 | Candidate data sources, the earnings decision ("Labels and dashboard"), commission built but switched off |
| #15 | Free APIs chosen for integration, ideas for later, sources considered and not used |
| #17 | `simple-english` for docs and traveller copy; Floorplan blueprint after the design; a map snapshot at each gate |
| #19 | `AGENTS.md` rule 8 (decisions in a prompt window) and rules from homescout (figures and sources, docs and versions, teach as you build, merge safety; Scorecard grades exempt) |
| #21 | The main journey design (approved) and decision 0012 (a team of agents, measured against a single-agent baseline) |
| #23 | Evaluations at each stage gate (coverage table at the Design gate, scores at build gates) |
| #29 | Design foundations: the design brief with a benchmark of eight products, the information architecture, the design tokens, and a WCAG 2.2 AA contrast check in `make check` (`tools/check_contrast.py`) |
| #30 | End-of-session status (19 Nov 2026, evening) |

## Done on 20 Nov 2026

| Pull request | What merged |
|---|---|
| #32 | Boards readiness: the widget state table, sample data, image rules, new tokens and the board checks |
| #37 | The design boards for every screen and widget state, the asset register, the logo, the illustration guide, and stricter contrast and board checks |


A fresh-context readiness review (Fable) of everything the boards depend on. Verdict: ready after small fixes and owner decisions. The fixes and the owner's nine answers are in the boards-readiness PR (#31):

- **Widget states:** a table of every `kind` against Loading, Empty, Error and Not known, with the extra states, definitions of Empty and Fallback, and the label for each source ([brief](../design/brief.md#widget-states)). Owner: "Agent drafts, you approve (Recommended)".
- **Sample content:** every board says "Sample data, not real" and takes its figures from [sample-data.md](../design/boards/sample-data.md). Owner: "Marked samples, one file (Recommended)".
- **Images** ([brief](../design/brief.md#images)): real Unsplash photos for places ("Download and register (Recommended)"); AI mood scenes made by the owner, only where no named place shows ("AI for mood scenes only"); a three-way illustration test ("Two own styles + library (Recommended)", after comparing homescout); a drawn sample map.
- **Fonts:** WOFF2 files committed and registered ("Commit font files (Recommended)"). **Logo:** a mark designed in the boards PR ("Design a logo mark now").
- **Tokens and checks:** `--color-text-on-photo` and two chart colours; `tools/check_boards.py` in `make check` (literal colours, "safe", local paths, outside files, the sample label, the asset register).
- **Tidy-ups:** #28's screen checklist; the information architecture's itinerary-only order and pinned answers; stale lines in data sources and the register; backlog order (#28 is now `[15]`; #27 joined the Design milestone).

What the journey design settled (owner answers in prompt windows; details in the [spec](../superpowers/specs/2026-11-19-layover-journey-design.md) and the [register](../decisions/README.md#register)):

- An undecided traveller describes a trip in chat; Layover confirms the brief, compares three places, and after the pick produces a summary, a day-by-day itinerary and a sandbox booking (Duffel flights; a hotel in the Nuitee sandbox, or flights only if Nuitee says no).
- Every message is classified into an intent first (`plan_trip`, `destination_facts`, `itinerary`, `fares_and_transport`); other travel questions get a Tavily web search with links, labelled "not checked by Layover"; non-travel questions are declined.
- Costs: real flight fares; stay and meal estimates from Wikivoyage listings where enough exist; other costs "not known"; Nuitee's price index planned behind a switch.
- Hotels from OpenStreetMap; shareable trip links, no accounts; public live trips with a limit per visitor and a cost cap.
- Every tool result is a typed widget; screens and widgets are designed to a world-class bar before the gate.
- Build: one plan per part, after the Design gate.

What the design foundations settled (owner answers in prompt windows; details in the [brief](../design/brief.md), the [information architecture](../design/information-architecture.md) and the [register](../decisions/README.md#register)):

- Look: warm and inspiring tone, warm editorial style, chat plus trip canvas (phone: Chat and Trip tabs), Lucide icons, WCAG 2.2 AA.
- Colour and type: the Harbour palette in light and dark (one brand blue, one highlight, one warning colour); Source Serif 4 and Source Sans 3.
- Structure: one scrolling canvas with a section index (Brief, Compare, place, Stay, Days, Booking); side answers in the chat with "Add to trip"; a private working link that keeps the chat and a frozen shared link; a "How Layover works" page.
- Illustrations: chosen by a side-by-side test in the boards.
- Tooling: no project board until build plan 1; Aspire for local orchestration and tracing in build plan 1.

## Next steps

1. **The Design gate:** a Floorplan blueprint from the approved design, an evaluation coverage table (every intent, journey step, widget `kind` and decision 0011 rule mapped to an evaluation case ID), a whole-repository audit, a tidy-up PR, `noticed` triage (#9, #26, #27, #34, #36), and a map snapshot in `docs/floorplan/`. #35 (mood scenes) can land before or after the gate.
2. **Build plan 1:** the foundation and the data contract (FastAPI template layer, trip-state and widget schemas incl. the four kinds proposed for #26, money types, the commission switch, recorded-response tests, the holidays library as an approved dependency, and the Aspire app host). Then one plan per part, written one at a time. When build plan 1 starts, decide on a GitHub project board (owner: "Wait until build (Recommended)").

## Blockers

None. Owner decisions still open, needed later:

- Nuitee's terms for sandbox and price-index use (ask Nuitee before building the hotel demo), and approving the price-index spend before its switch is turned on.
- How long a working trip link and a shared trip link last (the working link keeps the chat, so it holds more personal data).
- The cost-cap figures, after build step 1 measures a trip's cost.
- The vector database (plan 3), and hosting and the database (plan 6).
- How the fonts are served in the app: the boards commit the font files (owner, 20 Nov 2026), and the frontend plan reuses them unless it records a reason not to.

## Owner to-dos

- Ask Nuitee whether a portfolio project may use its sandbox and price index.
- Make the mood scenes in ChatGPT from the prompts in [mood-scene-prompts.md](../design/boards/mood-scene-prompts.md) (welcome and "How Layover works" only), and send them to the agent to register before they are committed ([#35](https://github.com/olaheavy-dev/layover/issues/35)).
- Before Layover goes public: read OpenAI's sharing and publication policy again by hand, for the mood scenes' labelling.
- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Review the process issues in the weekly process review: [agent-workflows#31](https://github.com/olaheavy-dev/agent-workflows/issues/31) (brainstorming's open questions bypassed the prompt-window rule), [#32](https://github.com/olaheavy-dev/agent-workflows/issues/32) (research quotes reached docs unchecked), [#33](https://github.com/olaheavy-dev/agent-workflows/issues/33) (design options as whole screens; restrained palettes), [#35](https://github.com/olaheavy-dev/agent-workflows/issues/35) (a readiness review before a phase that builds from approved documents) and [#38](https://github.com/olaheavy-dev/agent-workflows/issues/38) (ask for the feel and reference logos before drawing logo options).
- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Tavily: create a free account and API key when the web-search step is built.
- Nuitee: create an account and sandbox key once Nuitee agrees to portfolio use.
- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). It is needed before commission is switched on, not before.
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Run `make repo-settings` if not done yet. Five OpenSSF Scorecard alerts are open on `main` (branch protection, code review, maintained, fuzzing, CII best practices). They are repository-health grades and don't block merges (owner: "Exempt Scorecard grades (Recommended)"); improve them when possible.
