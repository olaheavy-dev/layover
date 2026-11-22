# 0013. Agent framework: Microsoft Agent Framework, in Python

Status: Accepted (22 Nov 2026). Supersedes point 2 of [0005](0005-python-and-langgraph.md); its point 1 (Python) stands. Amends how [0007](0007-agent-design.md) point 2 and [0012](0012-agent-team.md) point 1 are built, and how [0009](0009-tools-as-mcp-servers.md) connects tools; what those decisions chose stands.

## Context

Decision 0005 (19 Nov 2026) chose LangGraph after comparing it with Microsoft Agent Framework (MAF). On 22 Nov 2026 the owner changed the choice: "we will use maf please". Asked in a prompt window, the owner chose "Switch to MAF (Recommended)" and "Python, as now (Recommended)".

No code depended on the framework yet. Build step 1 makes no model calls, and the backend's template answer was still `llm: none`, so this was the cheapest point to change.

MAF's official documentation was checked on 22 Nov 2026 for each thing Layover relies on (sources below):

| Layover needs | With LangGraph (0005, 0007, 0012) | With MAF |
| --- | --- | --- |
| Approval before booking | `interrupt()` and `Command(resume=...)` | A workflow step calls `ctx.request_info()` and the workflow pauses; the answer arrives in that step's `@response_handler`. Tools can also require approval with `@tool(approval_mode="always_require")`. |
| Saved, resumable state | PostgreSQL checkpointer | Checkpoints at the end of each superstep, through a `CheckpointStorage`. Built-in stores: in memory, local files, Azure Cosmos DB. |
| Parallel research agents (Compare) | `Send` (map-reduce) | Fan-out and fan-in edges in a graph workflow (`WorkflowBuilder`) |
| Claude as the model | `langchain-anthropic` | `agent-framework-anthropic` (`AnthropicClient`) |
| Tools as MCP servers (0009) | `langchain-mcp-adapters` | `MCPStreamableHTTPTool` and `MCPStdioTool` |
| Traces | LangSmith | OpenTelemetry (GenAI semantic conventions), which Aspire's dashboard shows |

## Decision

1. **Agent framework: Microsoft Agent Framework, in Python.** The backend's template answer becomes `llm: maf` in PR C (#53).
2. **Workflows use the graph API (`WorkflowBuilder`).** MAF's documentation calls Python's functional workflow API (`@workflow`) experimental, so Layover doesn't build on it.
3. **Booking (0007 point 2) stays a fixed workflow with an approval step.** The order and the test payment are created only after the traveller approves: in the step's `@response_handler`, or in a later step. Nothing with a side effect runs before the pause.
4. **Checkpoints go in Layover's own PostgreSQL store**, written for MAF's `CheckpointStorage` protocol, saving JSON rather than pickle. It is built with booking in step 6, and it uses the PostgreSQL database already planned. Owner's choice in a prompt window: "Our own PostgreSQL store (Recommended)".
5. **Traces use MAF's OpenTelemetry output, shown in Aspire's dashboard.** LangSmith drops out. MAF's sensitive-data capture (`ENABLE_SENSITIVE_DATA`, which adds raw messages and tool arguments to traces) stays off.

## Consequences

- The plan's mapping of 0005, 0007 and 0012 to LangGraph APIs no longer applies. Those records keep their history, and each has a note pointing here.
- **The Anthropic connector is a pre-release.** MAF's documentation installs it with `pip install agent-framework-anthropic --pre`, and the locked version is `1.0.0b261112`. Each update to it is reviewed as a major update (AGENTS.md, "When merging").
- **Supply chain:** `agent-framework` 1.26.1 and 1.26.2 were malicious uploads on 17 Nov 2026 ([PYSEC-2026-4388](https://osv.dev/vulnerability/PYSEC-2026-4388)). Layover locks the `-core`, `-openai` and `-anthropic` packages, not that meta-package. The 7-day wait in `backend/pyproject.toml` (`exclude-newer`) and Dependabot's cooldown stay in place.
- **Release notes may be unavailable.** On 22 Nov 2026 MAF's GitHub repository (`microsoft/agent-framework`), which PyPI links to for release notes, returned 404. Until it is back, an update is reviewed by comparing the published packages (as on #62), and the official documentation on learn.microsoft.com is the reference.
- **Checkpoint safety:** MAF's documentation calls checkpoint storage a trust boundary. A JSON store avoids loading pickled data, and only the backend reads or writes it.
- **The LangSmith questions go away.** Its region, retention and terms were an open owner question before step 2. Traces stay in Aspire, on Layover's own machine or host. Any outside trace service added later is a new decision.
- **The evaluation runner** came with `llm: langchain` (LangSmith evaluations). Step 2's plan chooses one for MAF, and the evaluation case IDs don't change.
- More of the code is Layover's own: the PostgreSQL checkpoint store, and possibly glue that LangChain packages provided. Each piece is tested like any other code.

## Alternatives considered

- **Keep LangGraph (0005):** more examples and nothing to rewrite. The owner chose MAF.
- **Decide at build step 2:** no work now, but PR C's backend set-up would have started on an undecided framework.
- **MAF in .NET (C#):** fits the owner's .NET background, but the FastAPI backend from PR A, its template layer and build plan 1 would need redoing. The owner kept Python.
- **Checkpoints in MAF's built-in stores:** local files are lost when a host replaces its disk; Azure Cosmos DB adds a paid Azure service. Both use pickle.

## Sources

- Owner's answers in prompt windows, 22 Nov 2026 (issue [#74](https://github.com/olaheavy-dev/layover/issues/74)).
- MAF human-in-the-loop (Python): https://learn.microsoft.com/agent-framework/workflows/human-in-the-loop
- MAF checkpoints, including the built-in stores and the security notes: https://learn.microsoft.com/agent-framework/workflows/checkpoints
- MAF workflow APIs (graph and the experimental functional API): https://learn.microsoft.com/agent-framework/concepts/workflows/
- MAF functional workflow API, replay on resume: https://learn.microsoft.com/agent-framework/concepts/workflows/functional
- MAF Anthropic provider: https://learn.microsoft.com/agent-framework/integrations/by-component/model-providers/anthropic
- MAF MCP tools: https://learn.microsoft.com/agent-framework/agents/tools/local-mcp-tools
- MAF observability: https://learn.microsoft.com/agent-framework/agents/observability and https://learn.microsoft.com/agent-framework/workflows/observability
- MAF tool approval in handoff workflows: https://learn.microsoft.com/agent-framework/workflows/orchestrations/handoff
- PYSEC-2026-4388: https://osv.dev/vulnerability/PYSEC-2026-4388
