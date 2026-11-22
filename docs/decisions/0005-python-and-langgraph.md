# 0005. Python backend with LangGraph

Status: Accepted (19 Nov 2026). Point 2 (LangGraph) superseded by [0013](0013-microsoft-agent-framework.md) on 22 Nov 2026: Layover uses Microsoft Agent Framework. Point 1 (Python) stands.

## Context

The project's purpose is AI and agent jobs (decision 0003). The owner's earlier projects are on .NET and Python. Two agent frameworks were compared: LangGraph and Microsoft Agent Framework (MAF, the successor to Semantic Kernel and AutoGen). Both support what Layover needs: a graph of steps, a human approval step, saved and resumable state (checkpoints), and parallel agents.

## Decision

1. **Language: Python** (owner chose the recommended option). The recommendation's reasoning, not a measured claim: Python is the language most associated with AI and agent roles, and agent, MCP and evaluation examples tend to appear there first.
2. **Agent framework: LangGraph.** The owner raised it ("I am looking to use Langgraph") and kept it after the comparison with MAF.

## Consequences

- The backend comes from `house-template-fastapi` with `llm: langchain` (LangChain, LangGraph, LangSmith, PostgreSQL checkpoints, evals), applied when building starts (decision 0010).
- Booking approval uses LangGraph's `interrupt()` and `Command(resume=...)`, which needs a checkpointer and a `thread_id`. On resume, the paused node runs again from the top, so nothing with a side effect (creating an order) may run before the `interrupt()` in the same node.
- MAF stays a reasonable choice for Azure and .NET employers; reconsider only through a new record.

## Alternatives considered

- **Microsoft Agent Framework:** ready-made concurrent orchestration and one-line tool approval (`approval_mode="always_require"`), Python and .NET. Fewer examples, newer API, Azure-first defaults.
- **C# / .NET:** fits the owner's background and UK enterprise roles; fewer agent examples.
- **TypeScript:** Duffel's official JavaScript SDK and card form fit well; less common in AI-specific roles.

## Sources

- LangGraph interrupts: https://docs.langchain.com/oss/python/langgraph/interrupts
- Microsoft Agent Framework overview: https://learn.microsoft.com/agent-framework/overview/
- MAF human-in-the-loop: https://learn.microsoft.com/agent-framework/workflows/human-in-the-loop
- MAF tool approval (`approval_mode="always_require"`), in the handoff orchestration guide: https://learn.microsoft.com/agent-framework/workflows/orchestrations/handoff
