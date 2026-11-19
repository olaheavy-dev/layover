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
- **Earnings attribution:** which feature (chat, fare card, compare) drives clicks and bookings, from SubID-labelled partner links and Travelpayouts booking statistics (register line "Aviasales links are built by the backend…", [decisions](../decisions/README.md#register)).
- **Honesty about data:** every value labelled with its source and age ([0011](../decisions/0011-product-integrity-rules.md), proposed).

## 3. What the traveller can see for real

Cached fares (Aviasales through Travelpayouts), weather, exchange rates, FCDO entry and safety advice, Wikivoyage guides, and possibly airport transfer prices, eSIM costs and attraction tickets. Booking runs in Duffel's sandbox. Hotels have no data source yet. Details: [data sources](../references/data-sources.md).

## 4. Build order (proposed)

1. A single LangGraph agent with plain-function tools: weather, exchange rates, FCDO advice.
2. Move those tools into Layover's own MCP servers.
3. Retrieval over FCDO and Wikivoyage, with citations, freshness dates and the first evaluations.
4. Browsing real cached fares from Travelpayouts, labelled with their age, each linking to Aviasales through a partner link with a SubID naming the feature that produced it.
5. The Duffel booking subgraph with the approval step.
6. Compare destinations: parallel research agents, measured against the single agent.
7. A private earnings dashboard: clicks, bookings and earnings per feature from the booking statistics API.

The FastAPI and Next.js template layers are added before step 1 ([0010](../decisions/0010-repository-and-stages.md)).

## 5. Open design questions

In order of how much they change what gets built:

1. **What has the traveller already decided when they open Layover?** A fixed destination and dates needs a planner; "somewhere warm in May, under £800, from Manchester" needs inspiration and comparison, which would make Compare destinations the centrepiece.
2. **Hotels:** no hotel price data is available through Travelpayouts. Options include search links without prices, or another source.
3. **Accounts and saved trips:** does the traveller sign in and come back to a trip?
4. **Affiliate links and "non-commercial" data terms:** with affiliate earnings, Layover is likely commercial under Open-Meteo's terms (the free tier is non-commercial, and "promotional activities" count as commercial), so a paid plan or another weather source is needed before launch; options and their terms are compared in [data sources](../references/data-sources.md#weather-options-for-a-site-that-earns-commission). The same applies to Nager.Date (sponsorship) and REST Countries (paid plan).
5. **UK rules on labelling affiliate links (CAP Code)** to check before launch.
6. **The public brand:** `layover` is the working name; a brand and domain check comes before launch.
7. **Product integrity rules** ([0011](../decisions/0011-product-integrity-rules.md)): proposed, awaiting the owner.

## 6. Not doing

- Selling real tickets or taking real payments.
- Scraping any site.
- A knowledge graph ([0008](../decisions/0008-retrieval-no-knowledge-graph.md)).
- Multi-agent for its own sake ([0007](../decisions/0007-agent-design.md)).
