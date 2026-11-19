# 0012. Agent design: a team of agents, measured against a single-agent baseline

Status: Accepted (19 Nov 2026). Supersedes points 1 and 4 of [0007](0007-agent-design.md); its points 2 and 3 stand.

## Context

Decision 0007 chose one planner agent for the traveller conversation and kept multi-agent work to one feature, Compare destinations. Its Context called "one agent is enough" a working hypothesis, not yet measured, and its alternatives said to revisit a fuller multi-agent design if evaluations showed a reason.

On 19 Nov 2026 the owner settled the main journey in prompt windows; the answers are recorded in the [journey design](../superpowers/specs/2026-11-19-layover-journey-design.md), and this decision rests on those answers: an undecided traveller describes a trip in chat, Layover compares three places, the traveller picks one, and Layover produces a trip summary, a day-by-day itinerary and a sandbox booking. Offered three ways to build it (one planner agent with a compare tool, recommended; a fixed sequence of steps; a team of agents), the owner chose the team of agents, then chose to keep a single-agent baseline for measurement. The owner's reason, from the prompt window: "Show multi-agent skills".

## Decision

1. **A team of agents under a supervisor** runs the journey: a brief agent holds the chat and confirms the brief; a compare step fans out one research agent per destination in parallel (LangGraph `Send`) and ranks the results; an itinerary agent builds the days from sourced places; booking runs as the fixed subgraph from 0007 point 2. The supervisor routes between them and owns the shared trip state.
2. **A single-agent baseline** with the same tools runs the same evaluation trips, so the team can be measured against it on speed, tokens and answer quality (owner: "Team + single-agent baseline (Recommended)").
3. 0007 point 2 (booking is a fixed subgraph with an approval step, not an agent) and point 3 (parallel research agents for Compare destinations) stand. The journey starts by comparing three places (owner: "let us start with three first"); the design proposes that the traveller can swap one for their own.

## Consequences

- More model calls and hand-offs than one agent; the evaluations report the cost difference against the baseline, and the README states it with its dataset (`AGENTS.md` rule 1).
- Each agent has a narrow job and its own small tool set, so prompts and tests are per agent.
- Shared trip state (the confirmed brief, the comparison, the chosen place, the itinerary) is the contract between agents and is fixed first in the plan (data contract first).
- If the baseline matches the team on quality at lower cost, that result is reported honestly; it doesn't reverse this decision on its own, since showing multi-agent work is the owner's stated aim.

## Alternatives considered

- **One planner agent with a compare tool** (0007, recommended by the agent): fewer moving parts and lower cost; the owner preferred a design that shows multi-agent orchestration across the whole journey.
- **A fixed sequence of steps** with chat only for the brief: most predictable, but less conversational than the owner chose (chat-only brief) and shows less agent judgement.
- **Team only, no baseline:** less to build, but no evidence for or against the team.

## Sources

- Owner's answers in prompt windows, 19 Nov 2026 (recorded in the journey design).
- LangGraph `Send` and map-reduce: https://docs.langchain.com/oss/python/langgraph/graph-api-send-command
- LangGraph workflows and agents (orchestrator-worker): https://docs.langchain.com/oss/python/langgraph/workflows-agents
- Anthropic, How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
