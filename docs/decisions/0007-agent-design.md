# 0007. Agent design: one planner agent, a fixed booking flow, and parallel research agents

Status: Accepted (19 Nov 2026). Superseded in part by [0012](0012-agent-team.md): points 1 and 4.

## Context

Layover’s planner needs a small set of tools (fares, weather, exchange rates, advice and guide retrieval, airport lookup). The working hypothesis, not yet measured, is that one agent can plan well with a set this small. Splitting it into several agents adds model calls, delay, cost and chances to lose context between agents, and makes evaluations harder. Anthropic’s guidance is to start with the simplest design that works and add complexity only when it improves results (Building effective agents). The planned evaluations (point 4 below) test this hypothesis. Booking with payment is a fixed sequence that should not be improvised by a model. The owner still wants to show multi-agent work: "I want a multi agent use case".

## Decision

1. **One planner agent** (Claude with tool calling) for the main traveller conversation.
2. **Booking is a fixed LangGraph subgraph, not an agent:** Duffel search, price check, approval (`interrupt()`), then order and test payment.
3. **Multi-agent feature: Compare destinations** (owner chose the recommended option). A supervisor plans the job and starts one research agent per destination in parallel with LangGraph's `Send` API; a final step ranks the results, checks the budget and cites sources. Example: "Lisbon, Marrakech, Malta or Tenerife for 5 days in March, under £700 from Manchester?"
4. Build the single agent first, so the multi-agent feature can be measured against it (speed, tokens, ranking quality), and to check the single planner's quality on its own tools.

## Consequences

- Each research agent sees only its own destination's data, which avoids mixing up figures between destinations.
- The number of research agents follows the request (two destinations or six).
- Results from parallel agents merge through a state reducer.
- Evaluations compare single-agent and multi-agent answers on the same questions.

## Alternatives considered

- **Multi-agent for everything** (flight agent, destination agent, booking agent and a supervisor): more cost and failure points, with no evidence yet of a quality gain at this tool count. Revisit if the evaluations show the single agent falling short.
- **Group-trip planner** (one agent per traveller plus a negotiating coordinator): memorable but hard to evaluate, token-heavy and prone to loops. Kept as a possible later idea.

## Sources

- LangGraph `Send` and map-reduce: https://docs.langchain.com/oss/python/langgraph/graph-api-send-command
- LangGraph orchestrator-worker pattern: https://docs.langchain.com/oss/python/langgraph/workflows-agents
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
