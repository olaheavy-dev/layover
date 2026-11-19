# 01: Research and direction (draft)

Status: draft, 19 Nov 2026. The product design is in progress; this document grows as it is agreed. Decisions in [`docs/decisions/`](../decisions/README.md) win where they differ.

## 1. What Layover is

An AI travel planner for a **UK-based traveller planning a holiday abroad**, built as a portfolio project for AI and agent engineering jobs, using real travel APIs, and built like a real product ([0003](../decisions/0003-purpose-and-traveller.md)).

## 2. What it should show a recruiter

- **Tool calling** against real APIs, with failures handled (timeouts, rate limits, expired offers) rather than covered up.
- **Retrieval with citations and freshness** over official FCDO advice and Wikivoyage ([0008](../decisions/0008-retrieval-no-knowledge-graph.md)).
- **A human approval step** before any booking or payment ([0007](../decisions/0007-agent-design.md)).
- **Parallel research agents**, measured against a single agent ([0007](../decisions/0007-agent-design.md)).
- **Tools as MCP servers** ([0009](../decisions/0009-tools-as-mcp-servers.md)).
- **Evaluations:** a set of test trips with checks such as "stayed under budget" and "cited FCDO advice", reported as a score.
- **Earnings attribution** (built behind the commission switch, off for now): which feature (chat, fare card, compare) drives clicks and bookings, from SubID-labelled partner links and Travelpayouts booking statistics (register line "Aviasales links are built by the backend…", [decisions](../decisions/README.md#register)).
- **Honesty about data:** every value labelled with its source and age ([0011](../decisions/0011-product-integrity-rules.md)).

## 3. What the traveller can see for real

Cached fares (Aviasales through Travelpayouts), weather, exchange rates, FCDO entry and safety advice, Wikivoyage guides, and possibly airport transfer prices, eSIM costs and attraction tickets. Booking runs in Duffel's sandbox. Hotels: real names and locations from OpenStreetMap, a sandbox booking in Nuitee Connect, and stay estimates from Wikivoyage listings ([journey design](../superpowers/specs/2026-11-19-layover-journey-design.md)). Details: [data sources](../references/data-sources.md).

## 4. Build order (proposed; to be revised by the plan for the agent team in [0012](../decisions/0012-agent-team.md))

1. A single LangGraph agent with plain-function tools: weather, exchange rates, FCDO advice.
2. Move those tools into Layover's own MCP servers.
3. Retrieval over FCDO and Wikivoyage, with citations, freshness dates and the first evaluations.
4. Browsing real cached fares from Travelpayouts, labelled with their age, each linking to Aviasales. With commission switched on, the link is a partner link with a SubID naming the feature that produced it; it is built now but switched off, so links are plain ([register](../decisions/README.md#register)).
5. The Duffel booking subgraph with the approval step.
6. Compare destinations: parallel research agents, measured against the single agent (to be revised: [0012](../decisions/0012-agent-team.md) makes the whole journey a team of agents, measured against a single-agent baseline).
7. A private earnings dashboard: clicks, bookings and earnings per feature from the booking statistics API, built behind the same switch.

The FastAPI and Next.js template layers are added before step 1 ([0010](../decisions/0010-repository-and-stages.md)).

## 5. Open design questions

In order of how much they change what gets built:

1. **What has the traveller already decided when they open Layover?** Answered: undecided, then plans ([journey design](../superpowers/specs/2026-11-19-layover-journey-design.md), [0012](../decisions/0012-agent-team.md)).
2. **Hotels:** answered: real hotel locations from OpenStreetMap and a sandbox hotel booking in Nuitee Connect; no real prices ([journey design](../superpowers/specs/2026-11-19-layover-journey-design.md)).
3. **Accounts and saved trips:** answered: shareable links, no accounts ([journey design](../superpowers/specs/2026-11-19-layover-journey-design.md)).
4. **Affiliate links and "non-commercial" data terms:** commission is switched off for now, so Layover is non-commercial and free tiers fit. Before switching it on, Layover would likely become commercial under Open-Meteo's terms (the free tier is non-commercial, and "promotional activities" count as commercial), and Nager.Date (sponsorship), REST Countries (paid plan) and Overpass (paid or self-hosted) would change too; weather options are compared in [data sources](../references/data-sources.md#weather-options-for-a-site-that-earns-commission).
5. **UK rules on labelling affiliate links (CAP Code)** to check before switching commission on.
6. **The public brand:** `layover` is the working name; a brand and domain check comes before launch.

## 6. Not doing

- Selling real tickets or taking real payments.
- Scraping any site.
- A knowledge graph ([0008](../decisions/0008-retrieval-no-knowledge-graph.md)).
- Multi-agent for its own sake ([0007](../decisions/0007-agent-design.md)).
