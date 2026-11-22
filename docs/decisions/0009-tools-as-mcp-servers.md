# 0009. Tools become MCP servers from build step 2

Status: Accepted (19 Nov 2026). Agents connect to the MCP servers through Microsoft Agent Framework's MCP tools, not `langchain-mcp-adapters` ([0013](0013-microsoft-agent-framework.md)); the decision itself stands.

## Context

The Model Context Protocol (MCP) is a standard way to expose tools to any AI application. A public tutorial project the owner shared (TripMate AI, reviewed in [the TripMate review](../reviews/2026-11-19-tripmate-reference-review.md)) shows the pattern: tools in separate MCP servers, connected to a LangGraph agent with `langchain-mcp-adapters`.

## Decision

Build the first tools as plain Python functions, then move them into Layover's own MCP servers (FastMCP) once they work, in build step 2 (owner chose the recommended option).

## Consequences

- Layover's tools can also be used from Claude Desktop and other MCP clients.
- Lessons from the review apply: API keys go in environment variables or headers, never in URLs; package versions are pinned; no hard-coded machine paths; no third-party MCP server downloaded and run unpinned at startup.

## Alternatives considered

- **MCP from the start:** cleanest end state, but MCP and the API integrations would be debugged at the same time.
- **No MCP:** simplest, but loses a skill employers look for.

## Sources

- Model Context Protocol: https://modelcontextprotocol.io/
- LangChain MCP adapters: https://github.com/langchain-ai/langchain-mcp-adapters
