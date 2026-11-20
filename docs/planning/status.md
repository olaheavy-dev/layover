# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 20 Nov 2026, end of the session (written in the boards-readiness PR, for #31).

## Stage

Design. The repository holds documents and their checks only. The main journey design is approved ([spec](../superpowers/specs/2026-11-19-layover-journey-design.md)). The design foundations are approved and merged (#29): the [design brief](../design/brief.md), the [information architecture](../design/information-architecture.md) and the [design tokens](../design/tokens.css). A readiness review on 20 Nov 2026 found what the boards still needed; #31 settles it (the widget state table, sample data, image rules, new tokens and the board checks). The boards for every screen and widget come next (#28), still in the Design stage, then the Design gate. The FastAPI template layer comes with build plan 1, and the Next.js layer when frontend work starts ([0010](../decisions/0010-repository-and-stages.md), [spec §9](../superpowers/specs/2026-11-19-layover-journey-design.md)).

## Open pull requests

- [#32](https://github.com/olaheavy-dev/layover/pull/32) boards readiness (closes #31 and #33). CI passes. Codex found one P1, now fixed: Python cache files with local paths had been committed. Next session: check Codex's re-review of the latest commit and merge if it's clean (owner: "Move merge to next session"). The cache files stay in the branch's earlier commits until the branch is deleted after the merge; the squash merge keeps them out of `main`.

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

A fresh-context readiness review (Fable) of everything the boards depend on. Verdict: ready after small fixes and owner decisions. The fixes and the owner's nine answers are in the boards-readiness PR (#31):

- **Widget states:** a table of every `kind` against Loading, Empty, Error and Not known, with the extra states, definitions of Empty and Fallback, and the label for each source ([brief](../design/brief.md#widget-states)). Owner: "Agent drafts, you approve (Recommended)".
- **Sample content:** every board says "Sample data, not real" and takes its figures from [sample-data.md](../design/boards/sample-data.md). Owner: "Marked samples, one file (Recommended)".
- **Images** ([brief](../design/brief.md#images)): real Unsplash photos for places ("Download and register (Recommended)"); AI mood scenes made by the owner, only where no named place shows ("AI for mood scenes only"); a three-way illustration test ("Two own styles + library (Recommended)", after comparing homescout); a drawn sample map.
- **Fonts:** WOFF2 files committed and registered ("Commit font files (Recommended)"). **Logo:** a mark designed in the boards PR ("Design a logo mark now").
- **Tokens and checks:** `--color-text-on-photo` and two chart colours; `tools/check_boards.py` in `make check` (literal colours, "safe", local paths, outside files, the sample label, the asset register).
- **Logo:** the owner chose S3, the suitcase character. Final drawing in `docs/design/boards/logo/` (four one-colour SVG masters), shown on the logo board and in every screen's top bar; tokens `--logo-ink` and `--logo-sun` added. The "Logo marks" task in the boards task list is ticked.
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

1. **Merge #32** once Codex's re-review is clean (see above).
2. **Fresh session: the boards** (issue #28, PR 2 of the design work), with the design-flow phases 5 and 6 (`brief-to-tasks`, then `frontend-design`). Follow #28's screen checklist and the [state table](../design/brief.md#widget-states). Start by creating `docs/assets/README.md`, then commit the fonts, read the Unsplash licence again and register the photos. The boards include the three-way illustration test, two or three logo marks in the real top bar, and the mood-scene prompts for the owner. Then the `design-reviewer` and `visual-reviewer` passes, tested against the 12 "bar for Layover" rules in the brief. Show every option inside a real screen, and ask every question in a prompt window.
3. The Design gate: a Floorplan blueprint from the approved design, an evaluation coverage table, a whole-repository audit, a tidy-up PR, `noticed` triage, a map snapshot in `docs/floorplan/`.
4. Build plan 1: the foundation and the data contract (FastAPI template layer, trip-state and widget schemas, money types, the commission switch, recorded-response tests, and the Aspire app host for local orchestration and tracing). Then one plan per part, written one at a time. When build plan 1 starts, decide on a GitHub project board (owner: "Wait until build (Recommended)").

## Blockers

None. Owner decisions still open, needed later:

- Nuitee's terms for sandbox and price-index use (ask Nuitee before building the hotel demo), and approving the price-index spend before its switch is turned on.
- How long a working trip link and a shared trip link last (the working link keeps the chat, so it holds more personal data).
- The cost-cap figures, after build step 1 measures a trip's cost.
- The vector database (plan 3), and hosting and the database (plan 6).
- How the fonts are served in the app: the boards commit the font files (owner, 20 Nov 2026), and the frontend plan reuses them unless it records a reason not to.

## Owner to-dos

- Ask Nuitee whether a portfolio project may use its sandbox and price index.
- During the boards: make the mood scenes in ChatGPT from the prompts the agent writes (welcome and "How Layover works" only), and pick the illustration style, the free library and the logo mark.
- Before Layover goes public: read OpenAI's sharing and publication policy again by hand, for the mood scenes' labelling.
- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Review the process issues in the weekly process review: [agent-workflows#31](https://github.com/olaheavy-dev/agent-workflows/issues/31) (brainstorming's open questions bypassed the prompt-window rule), [#32](https://github.com/olaheavy-dev/agent-workflows/issues/32) (research quotes reached docs unchecked) [#33](https://github.com/olaheavy-dev/agent-workflows/issues/33) (design options as whole screens; restrained palettes) and [#35](https://github.com/olaheavy-dev/agent-workflows/issues/35) (a readiness review before a phase that builds from approved documents).
- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Tavily: create a free account and API key when the web-search step is built.
- Nuitee: create an account and sandbox key once Nuitee agrees to portfolio use.
- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). It is needed before commission is switched on, not before.
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Run `make repo-settings` if not done yet. Five OpenSSF Scorecard alerts are open on `main` (branch protection, code review, maintained, fuzzing, CII best practices). They are repository-health grades and don't block merges (owner: "Exempt Scorecard grades (Recommended)"); improve them when possible.
