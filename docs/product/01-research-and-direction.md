# 01: Research and direction (draft)

Status: draft, 19 Nov 2026; the build order (§4) was approved at the Design gate on 20 Nov 2026. This document grows as it is agreed. Decisions in [`docs/decisions/`](../decisions/README.md) win where they differ.

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

## 4. Build order

Approved by the owner at the Design gate, 20 Nov 2026 ([#39](https://github.com/olaheavy-dev/layover/issues/39)): "Approve, parallel per step (Recommended)". It replaces the earlier proposal, which started with "a single LangGraph agent", to fit the agent team and the single-agent baseline in [0012](../decisions/0012-agent-team.md). Each step has one plan, so "build plan N" means the plan for step N. Each step is a GitHub milestone and ends with a gate (`AGENTS.md`, "Review rounds and debt").

**How each step is built.** Each step is a vertical slice: the backend, its widgets on screen and its evaluation cases together. The step's plan fixes the data contract first (the JSON Schema of each widget `kind` and any API shape). Then a backend agent and a frontend agent build at the same time against that contract, the frontend with sample data in the schema's shape, and a final task joins them. Owner, asking: "My arrangements would be to pair ui and backend that could be in parallel at the same time, will this make us faster?" Parallel work within a step shortens waiting time at about the same total agent cost. Work is not run in parallel across steps, because two steps would change the same schemas and files. **Widgets first (owner, 20 Nov 2026):** the website and all 20 widget components are built in step 1, in parallel with the backend foundation, as soon as the schemas are fixed, from the boards and their sample data. Later steps connect real data to finished widgets, and build independent tools (such as weather, money and holidays) in parallel. Owner, asking: "what is the plan, can we parallelise frontend and backend work that are related,more pace?"; chose "Widgets in Build 1 (Recommended)". If a real source shows that a widget's schema must change, the step that finds it changes the schema and the widget together.

| Step | What it builds | Evaluation cases it adds ([cases](../evaluations/cases.md)) |
|---|---|---|
| 1. Foundation and data contract | The FastAPI template layer; trip-state and widget JSON Schemas for all 20 kinds (including the four proposed for [#26](https://github.com/olaheavy-dev/layover/issues/26)); money types; the commission switch, off; recorded-response tests; the Python `holidays` library as an approved dependency; the Aspire app host; the evaluation runner with a scripted traveller. In parallel, once the schemas are fixed: the Next.js template layer, the website's pages and chat shell, and all 20 widget components with their states from the [boards](../design/boards/index.html), shown with the boards' sample data | The schema part of `WIDGET-01` to `WIDGET-20` (each full case joins the evaluation set in the step that builds its widget, listed below); a test that the commission switch is off by default |
| 2. Chat, intents and the brief | The chat connected to the server, streaming text and widgets; the supervisor and intent classifier; the brief agent; Tavily web search; the single-agent baseline starts. The first tools are written as plain functions and moved into Layover's own MCP servers in this step ([0009](../decisions/0009-tools-as-mcp-servers.md)) | `INTENT-01` to `INTENT-06`, `BRIEF-01` to `BRIEF-03`, `WIDGET-01`, `WIDGET-15`, `WIDGET-16` |
| 3. Facts about one place | A research agent for one place: weather, sea, daylight, holidays, time difference, exchange rates, Wikipedia; retrieval over FCDO advice and Wikivoyage ([0008](../decisions/0008-retrieval-no-knowledge-graph.md)); the vector database, chosen with the owner; the `tzdata` package for time zones, if the system has no time-zone data, as a dependency for the owner to approve ([data sources](../references/data-sources.md)) | `INTENT-08`, `WIDGET-04` to `WIDGET-09`, `WIDGET-17`, `WIDGET-18`, `TRIP-04` |
| 4. Fares and compare | Travelpayouts cached fares, each linking to Aviasales (a partner link with a SubID only when commission is switched on, [register](../decisions/README.md#register)), and TfL routes; cost estimates; three research agents in parallel, then ranking and the budget check in tested code; the first whole trip, measured against the baseline | `INTENT-07`, `COMPARE-01` to `COMPARE-06`, `TRIP-01`, `TRIP-02`, `WIDGET-02`, `WIDGET-03`, `WIDGET-13`, `WIDGET-19`, `WIDGET-20` |
| 5. Itinerary and where to stay | The itinerary agent; OpenStreetMap hotels and stops through Overpass; the map | `TRIP-03` (the summary is complete once the map exists), `ITIN-01` to `ITIN-05`, `WIDGET-10` to `WIDGET-12` |
| 6. Sandbox booking | Duffel flights in test mode with the approval step; a Nuitee sandbox hotel if Nuitee agrees, otherwise flights only | `BOOK-01` to `BOOK-05`, `WIDGET-14` |
| 7. Trip links and going public | Working and shared trip links; limits per visitor and the cost cap; hosting and the database (the owner's decisions) | `SHARE-01`, `SHARE-02` |
| 8. Earnings dashboard | Clicks, bookings and earnings per feature from the booking statistics API, behind the commission switch, which stays off | None |

Both the FastAPI and the Next.js template layers are added in step 1 ([0010](../decisions/0010-repository-and-stages.md): the layers come when building starts).

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
