# Ordered backlog

Every open issue, in the order it is worked on (AGENTS.md, "How work flows"). Each issue's title starts with its order number (for example `[01]`) and the issue sits in its stage's milestone. When an issue's plan changes, update the issue, not this list; the list changes when an issue opens, closes or moves, in the PR that does it.

Each stage ends with a gate (`AGENTS.md`, "Review rounds and debt"): a whole-repository audit, its findings cleared in a tidy-up PR, `noticed` issues triaged, no open `review-followup` issue, a Floorplan map snapshot, and evaluations (a coverage table at the Design gate, a score report at build gates once evaluation cases exist).

## Stage: Design (milestone "Design")

The repository holds documents and their checks only until the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

| # | Issue | Item | Notes |
|---|---|---|---|
| 22 | #39 | Design gate: evaluation coverage, build order, Floorplan snapshot and audit | Closed by the gate PR |

## Build steps

The build order is approved ([01 §4](../product/01-research-and-direction.md#4-build-order), 20 Nov 2026). Each step is a milestone named "Build N: …" and ends with a gate. Issues for each step's own work are opened when its plan is written.

| # | Issue | Item | Milestone | Notes |
|---|---|---|---|---|
| 05 | #9 | Create the `task` label used by the Task issue form | Build 1 | `noticed` issue, owner-only (repository settings) |
| 16 | #26 | Widget kinds for holidays, time difference, fares to anywhere and TfL | Build 1 | `noticed`; proposals drawn and chosen in #37; cases `WIDGET-17` to `WIDGET-20`; step 1 fixes the schemas |
| 17 | #27 | CodeQL scans Actions only; Python in `tools/` is not scanned | Build 1 | `noticed`; template-owned workflow; fix when the FastAPI layer adds Python |
| 21 | #36 | Harden the board checks with a real HTML parser | Build 1 | `noticed` in the boards PR's security review |
| 23 | #40 | Move the Floorplan snapshot exemption into house-template-base | Build 1 | `noticed` in the Design gate audit |
| 20 | #35 | Mood scenes for the welcome and How Layover works pages | Build 2 | Waits for the owner's images |
| 24 | #41 | How Layover works board leaves out Nuitee Connect | Build 2 | `noticed` in the Design gate audit |
| 19 | #34 | No chosen source for a place's currency | Build 3 | `noticed` in the boards PR; pick a source before the `money` widget shows a currency line |

Milestones: Build 1: Foundation and data contract; Build 2: Chat, intents and the brief; Build 3: Facts about one place; Build 4: Fares and compare; Build 5: Itinerary and where to stay; Build 6: Sandbox booking; Build 7: Trip links and going public; Build 8: Earnings dashboard.

Done: `[01]` #4, `[02]` #5, `[03]` #6 and `[04]` #7, closed by the PR that adopted Vestagraph's practices; `[06]` #10, decision 0011 accepted; `[07]` #11, data sources and the earnings decision; `[08]` #14, free APIs chosen for integration; `[09]` #16, simple-english and Floorplan adopted; `[10]` #18, prompt-window rule and rules from homescout; `[11]` #20, the main journey design and decision 0012; `[12]` #22, evaluations at each stage gate; `[13]` #25, design foundations (brief, information architecture and tokens); `[14]` #31, boards readiness (widget state table, sample data, image rules, board checks); `[15]` #28, the design boards for every screen and widget state (#37); `[18]` #33, the owner's reason for decision 0004 recorded in the register.
