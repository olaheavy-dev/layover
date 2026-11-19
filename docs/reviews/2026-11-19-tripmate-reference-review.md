# Review of a public tutorial project: TripMate AI (19 Nov 2026)

The owner shared a local copy of [TripMate AI Using MCP](https://github.com/entbappy/TripMate-AI-Using-MCP) (MIT licence), a tutorial travel planner built with LangGraph, FastAPI, PostgreSQL checkpoints and MCP. This review records what Layover can learn from it. The code was read, not run. No code is copied into Layover; ideas only.

## Worth learning from

| What | Why it helps |
|---|---|
| Connecting to several MCP servers at once (`MultiServerMCPClient`) | Shows a remote server over HTTP and local servers over stdio side by side |
| A small custom MCP server with `FastMCP` and `@mcp.tool()` | A template for wrapping weather, currency or FCDO tools ([decision 0009](../decisions/0009-tools-as-mcp-servers.md)) |
| LangGraph's PostgreSQL checkpointer with a `thread_id` | The durable version of the checkpoints the booking approval needs |
| FastAPI with a simple web page | A working shape for the API |

## Problems Layover must avoid

1. **Invented prices.** The flight agent fetches a generic list of airports and airlines (not the route asked about), cuts it to 3,000 characters, and asks the model for an "estimated airfare range". AviationStack gives schedules and status, not fares, so the prices are made up. Layover uses real cached fares with their age ([0004](../decisions/0004-flight-data-sources.md), [0011](../decisions/0011-product-integrity-rules.md)).
2. **A fixed chain, not agents.** Flight, hotel, weather, itinerary and final steps run one after another; none chooses a tool, and the three independent lookups don't run in parallel. Layover's Compare destinations runs truly parallel research agents ([0007](../decisions/0007-agent-design.md)).
3. **An API key in a URL.** The Tavily MCP endpoint is called with the key as a query parameter, where logs can record it. Layover sends keys in headers.
4. **Unpinned code run at startup.** `uvx aviationstack-mcp` downloads and runs a third-party package on each start with no version pin: a supply-chain risk.
5. **Hard-coded machine paths** (a Windows Python path and script path), so it only runs on the author's computer.
6. **Missing pieces:** no approval step, no retrieval or citations, no evaluations, and errors turned into text the model then writes around.

## Note

Tutorial clones are common in portfolios. The six points above are the contrast to show in Layover's README and in interviews.
