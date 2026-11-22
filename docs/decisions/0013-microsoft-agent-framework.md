# 0013. Agent framework: Microsoft Agent Framework, in Python

Status: Accepted (22 Nov 2026). Supersedes point 2 of [0005](0005-python-and-langgraph.md); its point 1 (Python) stands. Changes how these are built, not what they chose: [0007](0007-agent-design.md) point 2 (booking) and point 3 (parallel research, kept by [0012](0012-agent-team.md) point 1), 0012 point 1 (the agent team), and how [0009](0009-tools-as-mcp-servers.md) connects tools.

## Context

Decision 0005 (19 Nov 2026) chose LangGraph after comparing it with Microsoft Agent Framework (MAF). On 22 Nov 2026 the owner changed the choice: "we will use maf please". In prompt windows the owner chose "Switch to MAF (Recommended)", "Python, as now (Recommended)", "Our own PostgreSQL store (Recommended)" for checkpoints, and "Keep LangSmith as well" for traces.

No code depended on the framework yet: build step 1 makes no model calls, and the backend's template answer is still `llm: none`.

MAF's official documentation was checked on 22 Nov 2026 for each thing Layover relies on (sources below):

| Layover needs | With LangGraph (0005, 0007, 0012) | With MAF |
| --- | --- | --- |
| Approval before booking | `interrupt()` and `Command(resume=...)` | A workflow step calls `ctx.request_info()` and the workflow pauses; the traveller's answer arrives in that step's `@response_handler`. Tools can also require approval with `@tool(approval_mode="always_require")`. |
| Saved, resumable state | PostgreSQL checkpointer | A checkpoint at the end of each superstep (one round in which every step that has work runs once), through a `CheckpointStorage`. Built-in stores: in memory, local files, Azure Cosmos DB. |
| Parallel research agents (Compare) | `Send` | Fan-out and fan-in in a graph workflow: one step sends work to several steps at once, and a later step collects their results. |
| Claude as the model | `langchain-anthropic` | `agent-framework-anthropic` (`AnthropicClient`) |
| Tools as MCP servers (0009) | `langchain-mcp-adapters` | `MCPStreamableHTTPTool` and `MCPStdioTool` |
| Traces | LangSmith | OpenTelemetry, the open standard for traces, which Aspire's dashboard shows and LangSmith can receive |

## Decision

1. **Agent framework: Microsoft Agent Framework, in Python** (owner). The backend's template answer stays `llm: none` in build step 1, as the owner chose for step 1 on 21 Nov 2026 ("Database only (Recommended)": the model gateway stays off until the Anthropic terms and prices are checked). Step 2's first PR changes it to `llm: maf`.
2. **Workflows use the graph API (`WorkflowBuilder`)** (agent's call: MAF's documentation calls Python's functional workflow API, `@workflow`, experimental).
3. **Booking (0007 point 2) stays a fixed workflow with an approval step** (agent's call, from MAF's documented request-and-response pattern). The order and the test payment are created only after the traveller approves: in the step's `@response_handler`, or in a later step.
4. **Checkpoints go in Layover's own PostgreSQL store** (owner), written for MAF's `CheckpointStorage` protocol, saving JSON rather than pickle (Python's built-in format for saving objects as bytes, which can run code when it is loaded). It is built with booking in step 6, in the PostgreSQL database already planned.
5. **Traces use MAF's OpenTelemetry output.** Locally they go to Aspire's dashboard, as in the 19 Nov 2026 register line. They also go to LangSmith, through its OpenTelemetry endpoint (owner: "Keep LangSmith as well"). MAF's sensitive-data setting (`ENABLE_SENSITIVE_DATA`, which adds raw messages, tool arguments and tool results to traces) stays off until LangSmith's region, retention and terms are checked and approved before step 2's first model call. Turning it on is part of that check.

## Consequences

- The LangGraph APIs named in 0005, 0007 and 0012 no longer apply. Those records keep their text, and each has a note pointing here.
- **Booking must be safe to run twice.** MAF saves a checkpoint when the traveller's answer is delivered, then runs the order step. If the backend stops after Duffel creates the order but before the next checkpoint, resuming runs the order step again. So the order and payment calls are idempotent (running them twice has the same effect as once): each is keyed on the approval's `request_id`, the key is recorded in PostgreSQL before the call, and step 6 has a test that stops and resumes the workflow at that point.
- **The JSON store owns all conversion.** MAF's checkpoint holds live objects and leaves conversion to the store. Layover's store converts every type a checkpoint can hold (MAF's message and content types, pending approval requests, Layover's own state and `Decimal` money) to JSON and back. On loading, it accepts only a listed set of types, and it has a round-trip test for each one.
- **Checkpoint safety:** MAF's documentation calls checkpoint storage a trust boundary: whatever reads a checkpoint trusts its contents. Only the backend reads or writes the store.
- **The Anthropic connector is a pre-release** (a version published before the stable release): MAF's documentation installs it with `pip install agent-framework-anthropic --pre`, and the locked version is `1.0.0b261112`. This record adds a rule: every update to an `agent-framework-*` pre-release is reviewed as a major update (a Codex review and its release notes or a package comparison), never merged as a small dependency update. Reviewers enforce it until the owner adds it to the merge rules in `AGENTS.md`, which are owner-only. The template comment in `backend/pyproject.toml` says `.github/dependabot.yml` groups these packages for review, but no such group exists ([#76](https://github.com/olaheavy-dev/layover/issues/76)).
- **Supply chain:** the `agent-framework` package (a meta-package, which only pulls in the others) had malicious releases 1.26.1 and 1.26.2 on 17 Nov 2026 ([PYSEC-2026-4388](https://osv.dev/vulnerability/PYSEC-2026-4388)). Layover locks the `-core`, `-openai` and `-anthropic` packages, not that meta-package. The 7-day wait in `backend/pyproject.toml` (`exclude-newer`) and Dependabot's cooldown stay.
- **Release notes may be unavailable.** On 22 Nov 2026 MAF's GitHub repository (`microsoft/agent-framework`), which PyPI links to for release notes, returned 404. Until it is back, an update is reviewed by comparing the published packages (as on [#62](https://github.com/olaheavy-dev/layover/pull/62#discussion_r4658085468)), and learn.microsoft.com is the reference.
- **Evaluations don't read tool results from traces.** With sensitive data off, MAF's tool spans hold no arguments or results, so cases that check a figure against a tool result (for example `COMPARE-05`) read MAF's run events and responses instead. The evaluation runner came with `llm: langchain` (LangSmith evaluations); step 2's plan chooses one for MAF. Evaluation case IDs don't change.
- **Where traces go once Layover is hosted** is decided with hosting (step 7).
- **New dependency in step 2:** MAF's MCP tools need the `mcp` package (`mcp>=2.2.0,<3`), which isn't in `uv.lock`. Step 2 asks the owner to approve it with the other packages `llm: maf` brings.
- More of the code is Layover's own: the PostgreSQL checkpoint store, and possibly glue that LangChain packages provided. Each piece is tested like any other code.

## Alternatives considered

- **Keep LangGraph (0005):** more examples and nothing to rewrite. The owner chose MAF.
- **Decide at build step 2:** no work now, but step 1's plan would have described a framework that might change.
- **MAF in .NET (C#):** fits the owner's .NET background, but the FastAPI backend from PR A, its template layer and build plan 1 would need redoing. The owner kept Python.
- **Checkpoints in MAF's built-in stores:** the file store depends on the host keeping its disk, and Azure Cosmos DB adds a paid Azure service. Both use pickle, loaded through a restricted reader that accepts a set list of types by default.
- **Traces in Aspire only:** no outside service, but no hosted trace views. The owner chose to keep LangSmith as well.

## Sources

- Owner's answers in prompt windows, 22 Nov 2026 (issue [#74](https://github.com/olaheavy-dev/layover/issues/74)); the step 1 answer in the [build step 1 design](../superpowers/specs/2026-11-21-build-step-1-design.md).
- MAF human-in-the-loop (Python): https://learn.microsoft.com/agent-framework/workflows/human-in-the-loop
- MAF checkpoints, including the built-in stores and the security notes: https://learn.microsoft.com/agent-framework/workflows/checkpoints
- MAF workflow APIs (graph, and the experimental functional API): https://learn.microsoft.com/agent-framework/concepts/workflows/
- MAF Python 1.13.0 checkpoint upgrade guide (a checkpoint is saved when responses are delivered): https://learn.microsoft.com/agent-framework/support/upgrade/python-1-13-0-workflow-checkpoint-upgrade-guide
- MAF Python 2026 significant changes (checkpoints hold live objects; the store converts them): https://learn.microsoft.com/agent-framework/support/upgrade/python-2026-significant-changes
- MAF Anthropic provider: https://learn.microsoft.com/agent-framework/integrations/by-component/model-providers/anthropic
- MAF MCP tools: https://learn.microsoft.com/agent-framework/agents/tools/local-mcp-tools
- MAF observability: https://learn.microsoft.com/agent-framework/agents/observability and https://learn.microsoft.com/agent-framework/workflows/observability
- MAF tool approval in handoff workflows: https://learn.microsoft.com/agent-framework/workflows/orchestrations/handoff
- LangSmith, Trace with OpenTelemetry: https://docs.langchain.com/langsmith/trace-with-opentelemetry
- PYSEC-2026-4388: https://osv.dev/vulnerability/PYSEC-2026-4388
