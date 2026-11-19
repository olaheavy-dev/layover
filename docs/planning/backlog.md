# Ordered backlog

Every open issue, in the order it is worked on (AGENTS.md, "How work flows"). Each issue's title starts with its order number (for example `[01]`) and the issue sits in its stage's milestone. When an issue's plan changes, update the issue, not this list; the list changes when an issue opens, closes or moves, in the PR that does it.

Each stage ends with a gate (`AGENTS.md`, "Review rounds and debt"): a whole-repository audit, its findings cleared in a tidy-up PR, `noticed` issues triaged, no open `review-followup` issue, a Floorplan map snapshot, and evaluations (a coverage table at the Design gate, a score report at build gates once evaluation cases exist).

## Stage: Design (milestone "Design")

The repository holds documents only until the design is approved ([0010](../decisions/0010-repository-and-stages.md)).

| # | Issue | Item | Notes |
|---|---|---|---|
| 05 | #9 | Create the `task` label used by the Task issue form | `noticed` issue, owner-only (repository settings) |

Done: `[01]` #4, `[02]` #5, `[03]` #6 and `[04]` #7, closed by the PR that adopted Vestagraph's practices; `[06]` #10, decision 0011 accepted; `[07]` #11, data sources and the earnings decision; `[08]` #14, free APIs chosen for integration; `[09]` #16, simple-english and Floorplan adopted; `[10]` #18, prompt-window rule and rules from homescout; `[11]` #20, the main journey design and decision 0012; `[12]` #22, evaluations at each stage gate.

Next design work (open design questions in [01 §5](../product/01-research-and-direction.md)) gets issues as it starts.

## Build steps

Milestones for the build steps are created when the build order in [01 §4](../product/01-research-and-direction.md) is approved; it is proposed today.
