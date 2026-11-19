# Decisions

Hard-to-reverse decisions get a numbered record in this folder (template: [0001](0001-record-decisions.md)). Easily reversible ones get a line in the register below. Accepted records aren't rewritten: a new record supersedes an old one.

## Records

| No. | Decision | Status |
| --- | --- | --- |
| [0001](0001-record-decisions.md) | Record decisions in this folder | Accepted |
| [0002](0002-start-from-house-template.md) | Start from the house template layers | Accepted |
| [0003](0003-purpose-and-traveller.md) | Purpose, audience and the traveller | Accepted |
| [0004](0004-flight-data-sources.md) | Flight data: cached real fares to browse, a sandbox to book | Accepted |
| [0005](0005-python-and-langgraph.md) | Python backend with LangGraph | Accepted |
| [0006](0006-nextjs-frontend.md) | Next.js frontend | Accepted |
| [0007](0007-agent-design.md) | Agent design: one planner agent, a fixed booking flow, and parallel research agents | Accepted |
| [0008](0008-retrieval-no-knowledge-graph.md) | Retrieval over official advice and guides; no knowledge graph | Accepted |
| [0009](0009-tools-as-mcp-servers.md) | Tools become MCP servers from build step 2 | Accepted |
| [0010](0010-repository-and-stages.md) | Repository: code name Layover, public, design before code | Accepted |
| [0011](0011-product-integrity-rules.md) | Product integrity rules | Accepted |

## Register

| Date | Choice | Why |
| --- | --- | --- |
| 2026-11-19 | Join only the Aviasales programme on Travelpayouts for now | It is the only brand that gives flight data; the others give affiliate links or feeds Layover doesn't use yet |
| 2026-11-19 | Send the Travelpayouts token in the `X-Access-Token` header, never as a URL parameter | Keys in URLs end up in logs |
| 2026-11-19 | Create the Travelpayouts "project" after the repository or site exists | It asks for a link to a traffic source; owner: "We can defer this creation" |
