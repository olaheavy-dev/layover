# Ordered backlog

Every open issue, in the order it is worked on (AGENTS.md, "How work flows"). Each issue's title starts with its order number (for example `[01]`) and the issue sits in its stage's milestone. When an issue's plan changes, update the issue, not this list.

The [Layover build](https://github.com/orgs/olaheavy-dev/projects/5) board (To do, In progress, In review, Done) shows progress. This list stays the ordered list. Whoever opens, closes or moves an issue updates both: the list changes in the PR that does it. A card moves by its Status: set it to In progress when work starts, In review when the issue's PR opens, and Done when it merges.

Each stage ends with a gate (`AGENTS.md`, "Review rounds and debt"): a whole-repository audit, its findings cleared in a tidy-up PR, `noticed` issues triaged, no open `review-followup` issue, a Floorplan map snapshot, and evaluations (a coverage table at the Design gate, a score report at build gates once evaluation cases exist).

## Stage: Design (milestone "Design")

The repository holds documents and their checks only until the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

| # | Issue | Item | Notes |
|---|---|---|---|
| — | — | None open: the Design stage closed with the gate (#42) | |

## Build steps

The build order is approved ([01 §4](../product/01-research-and-direction.md#4-build-order), 20 Nov 2026). Each step is a milestone named "Build N: …" and ends with a gate. Issues for each step's own work are opened when its plan is written.

| # | Issue | Item | Milestone | Notes |
|---|---|---|---|---|
| 05 | #9 | Create the `task` label used by the Task issue form | Build 1 | `noticed` issue, owner-only (repository settings) |
| 23 | #40 | Move the Floorplan snapshot exemption into house-template-base | Build 1 | `noticed` in the Design gate audit |
| 38 | #70 | Update the website's minor and patch packages | Build 1 | Takes the parts of Dependabot's #59 that pass the peer check, before PRs C and D |
| 42 | #74 | Switch the agent framework from LangGraph to Microsoft Agent Framework | Build 1 | Owner's choice, 22 Nov 2026; decision 0013 replaces 0005 before PR C |
| 31 | #53 | Build 1 PR C: backend foundation | Build 1 | Build plan 1, PR C |
| 32 | #54 | Build 1 PR D: website, widgets and gallery | Build 1 | Build plan 1, PR D |
| 33 | #55 | Build 1 PR E: join the website to the API and add Aspire | Build 1 | Build plan 1, PR E |
| 34 | #56 | Remove the minimatch override once typescript-eslint uses minimatch 11 | Build 1 | `noticed` in PR A's final review |
| 39 | #71 | Website major upgrades: OpenTelemetry SDK 3, ESLint 10, TypeScript 7, jsdom 31 | Build 1 | Waits for `@vercel/otel`, the ESLint plugins and typescript-eslint to support them; replaces Dependabot's #60 |
| 40 | #72 | No check keeps `third-party.md` in step with the lock files | Build 1 | `noticed` while triaging the Dependabot PRs; template candidate |
| 41 | #73 | PR title check is cancelled when Dependabot rebases and renames a PR at once | Build 1 | `noticed` while triaging the Dependabot PRs; template candidate, owner-only (`.github/`) |
| 43 | #76 | `backend/pyproject.toml` says Dependabot groups the agent-framework packages for review, but no such group exists | Build 1 | `noticed` in the 0013 review; template candidate, owner-only (`.github/`) |
| 20 | #35 | Mood scenes for the welcome and How Layover works pages | Build 2 | Waits for the owner's images |
| 24 | #41 | How Layover works board leaves out Nuitee Connect | Build 2 | `noticed` in the Design gate audit |
| 19 | #34 | No chosen source for a place's currency | Build 3 | `noticed` in the boards PR; pick a source before the `money` widget shows a currency line |
| 35 | #64 | No contract state for the pounds-only money card | Build 3 | `noticed` in PR B |
| 36 | #65 | No contract state for the booking widget asking for dates | Build 6 | `noticed` in PR B |
| 27 | #48 | No privacy notice page in the site map | Build 7 | `noticed` in the build step 1 brainstorm |
| 37 | #66 | Rate limits for the public API routes | Build 7 | `noticed` in PR B's security review |

Milestones: Build 1: Foundation and data contract; Build 2: Chat, intents and the brief; Build 3: Facts about one place; Build 4: Fares and compare; Build 5: Itinerary and where to stay; Build 6: Sandbox booking; Build 7: Trip links and going public; Build 8: Earnings dashboard.

Done: `[01]` #4, `[02]` #5, `[03]` #6 and `[04]` #7, closed by the PR that adopted Vestagraph's practices; `[06]` #10, decision 0011 accepted; `[07]` #11, data sources and the earnings decision; `[08]` #14, free APIs chosen for integration; `[09]` #16, simple-english and Floorplan adopted; `[10]` #18, prompt-window rule and rules from homescout; `[11]` #20, the main journey design and decision 0012; `[12]` #22, evaluations at each stage gate; `[13]` #25, design foundations (brief, information architecture and tokens); `[14]` #31, boards readiness (widget state table, sample data, image rules, board checks); `[15]` #28, the design boards for every screen and widget state (#37); `[18]` #33, the owner's reason for decision 0004 recorded in the register; `[22]` #39, the Design gate (#42); `[25]` #45, widgets first: the website and all widgets in build step 1 (#44); `[26]` #46, Nuitee: the sandbox used without asking, the city price index dropped; `[28]` #49, build plan 1: the design and plan for build step 1; `[17]` #27, CodeQL scans Python (with the template layers); `[29]` #51, the template layers (PR A); `[21]` #36, the board checks read pages with `html.parser`, and the CodeQL warnings on `main` are cleared (#68); `[16]` #26, the four new widget kinds' schemas, and `[30]` #52, the data contract, samples and sample endpoints (PR B).
