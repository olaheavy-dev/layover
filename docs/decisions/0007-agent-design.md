# 0007. Agent design: one planner agent, a fixed booking flow, and parallel research agents

Status: Accepted (19 Nov 2026)

## Context

With fewer than ten tools, one agent can handle planning well. Splitting it into several agents adds model calls, delay, cost and lost context between agents, and makes evaluations harder. Booking with payment is a fixed sequence that should not be improvised by a model. The owner still wants to show multi-agent work: "I want a multi agent use case".

## Decision

1. **One planner agent** (Claude with tool calling) for the main traveller conversation.
2. **Booking is a fixed LangGraph subgraph, not an agent:** Duffel search, price check, approval (`interrupt()`), then order and test payment.
3. **Multi-agent feature: Compare destinations** (owner chose the recommended option). A supervisor plans the job and starts one research agent per destination in parallel with LangGraph's `Send` API; a final step ranks the results, checks the budget and cites sources. Example: "Lisbon, Marrakech, Malta or Tenerife for 5 days in March, under £700 from Manchester?"
4. Build the single agent first, so the multi-agent feature can be measured against it (speed, tokens, ranking quality).

## Consequences

- Each research agent sees only its own destination's data, which avoids mixing up figures between destinations.
- The number of research agents follows the request (two destinations or six).
- Results from parallel agents merge through a state reducer.
- Evaluations compare single-agent and multi-agent answers on the same questions.

## Alternatives considered

- **Multi-agent for everything** (flight agent, destination agent, booking agent and a supervisor): more cost and failure points for no quality gain at this tool count.
- **Group-trip planner** (one agent per traveller plus a negotiating coordinator): memorable but hard to evaluate, token-heavy and prone to loops. Kept as a possible later idea.

## Sources

- LangGraph `Send` and map-reduce: https://docs.langchain.com/oss/python/langgraph/graph-api-send-command
- LangGraph orchestrator-worker pattern: https://docs.langchain.com/oss/python/langgraph/workflows-agents
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
