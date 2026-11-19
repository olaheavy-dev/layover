# Status

Overwritten at the end of every session by the agent that ran it (AGENTS.md, "How work flows"); git history keeps the earlier ones.

Last updated: 19 Nov 2026, end of session.

## Stage

Design. The repository holds documents only. The main journey design is approved ([spec](../superpowers/specs/2026-11-19-layover-journey-design.md)). The design foundations are approved: the [design brief](../design/brief.md), the [information architecture](../design/information-architecture.md) and the [design tokens](../design/tokens.css) (issue #25). The boards for every screen and widget come next, still in the Design stage, then the Design gate. The FastAPI template layer comes with build plan 1, and the Next.js layer when frontend work starts ([0010](../decisions/0010-repository-and-stages.md), [spec §9](../superpowers/specs/2026-11-19-layover-journey-design.md)).

## Open pull requests

None.

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

What the journey design settled (owner answers in prompt windows; details in the [spec](../superpowers/specs/2026-11-19-layover-journey-design.md) and the [register](../decisions/README.md#register)):

- An undecided traveller describes a trip in chat; Layover confirms the brief, compares three places, and after the pick produces a summary, a day-by-day itinerary and a sandbox booking (Duffel flights; a hotel in the Nuitee sandbox, or flights only if Nuitee says no).
- Every message is classified into an intent first (`plan_trip`, `destination_facts`, `itinerary`, `fares_and_transport`); other travel questions get a Tavily web search with links, labelled "not checked by Layover"; non-travel questions are declined.
- Costs: real flight fares; stay and meal estimates from Wikivoyage listings where enough exist; other costs "not known"; Nuitee's price index planned behind a switch.
- Hotels from OpenStreetMap; shareable trip links, no accounts; public live trips with a limit per visitor and a cost cap.
- Every tool result is a typed widget; screens and widgets are designed to a world-class bar before the gate.
- Build: one plan per part, after the Design gate.

## Next steps

1. **Merge the design foundations PR** (issue #25): brief, information architecture, tokens and the contrast check in `make check`.
2. **Boards** (a new issue, PR 2 of the design work): static HTML boards for every screen in the [information architecture](../design/information-architecture.md) and every widget `kind` with its loading, empty, error and "not known" states, at 390 px and 1440 px, in light and dark, built on [tokens.css](../design/tokens.css). It includes the illustration side-by-side test on the welcome screen. Then the `design-reviewer` and `visual-reviewer` passes, tested against the 12 "bar for Layover" rules in the brief.
3. The Design gate: a Floorplan blueprint from the approved design, an evaluation coverage table, a whole-repository audit, a tidy-up PR, `noticed` triage, a map snapshot in `docs/floorplan/`.
4. Build plan 1: the foundation and the data contract (FastAPI template layer, trip-state and widget schemas, money types, the commission switch, recorded-response tests). Then one plan per part, written one at a time.

## Blockers

None. Owner decisions still open, needed later:

- Nuitee's terms for sandbox and price-index use (ask Nuitee before building the hotel demo), and approving the price-index spend before its switch is turned on.
- How long a working trip link and a shared trip link last (the working link keeps the chat, so it holds more personal data).
- The cost-cap figures, after build step 1 measures a trip's cost.
- The vector database (plan 3), and hosting and the database (plan 6).

## Owner to-dos

- Ask Nuitee whether a portfolio project may use its sandbox and price index.
- Pin Floorplan in agent-workflows ([agent-workflows#30](https://github.com/olaheavy-dev/agent-workflows/issues/30)); until then the installed plugin follows the author's latest version. Afterwards, uninstall `floorplan@floorplan` from the author's marketplace.
- Review the process issue [agent-workflows#31](https://github.com/olaheavy-dev/agent-workflows/issues/31) (brainstorming's open questions bypassed the prompt-window rule) in the weekly process review.
- Create the `task` label used by the Task issue form ([#9](https://github.com/olaheavy-dev/layover/issues/9)).
- Travelpayouts: join the Aviasales programme and find the API token (Profile → API token). Keep the token out of chat and out of git.
- Duffel: create a test-mode account and token (`duffel_test_...`).
- Tavily: create a free account and API key when the web-search step is built.
- Nuitee: create an account and sandbox key once Nuitee agrees to portfolio use.
- Before build step 4: read the Travelpayouts partner agreement (or ask the agent to read it in a browser) to confirm fares may link to Aviasales without a partner marker.
- Travelpayouts project: create it once Layover has a site (Travelpayouts asks for a link to a traffic source). It is needed before commission is switched on, not before.
- Travelpayouts payouts: set up the payout method yourself when earnings start (agents never enter payment details).
- Run `make repo-settings` if not done yet. Five OpenSSF Scorecard alerts are open on `main` (branch protection, code review, maintained, fuzzing, CII best practices). They are repository-health grades and don't block merges (owner: "Exempt Scorecard grades (Recommended)"); improve them when possible.
