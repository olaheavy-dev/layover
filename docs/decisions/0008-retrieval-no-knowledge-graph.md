# 0008. Retrieval over official advice and guides; no knowledge graph

Status: Accepted (19 Nov 2026)

## Context

Some travel knowledge changes by the minute (fares, weather, exchange rates); some is long text that changes slowly (entry rules, safety advice, destination guides). The owner asked whether a knowledge graph is needed or overkill.

## Decision

1. **Live data comes from API tools; slow-changing long text comes from retrieval (RAG).**
2. **RAG sources:**
   - FCDO foreign travel advice through the GOV.UK Content API (Open Government Licence). Each page's update date is stored with its chunks and shown to the traveller.
   - Wikivoyage destination guides (CC BY-SA; credit required).
   - Layover's own help and policy text.
3. **Retrieval features:** citations on every factual claim, freshness metadata, hybrid (keyword plus vector) search, and retrieval evaluations (right source fetched, answer faithful to it).
4. **No knowledge graph.** Reference facts (airports, cities, countries) live in plain tables, for example from OurAirports (public domain).

## Consequences

- Fares, weather, exchange rates and Duffel offer conditions stay as tools and are never put in the vector store.
- The README explains why a knowledge graph was not needed and when it would be (questions that hop across many relationships).

## Alternatives considered

- **Knowledge graph or GraphRAG** (for example Neo4j): an extra database, a modelling step and upkeep, with no feature that needs it yet.

## Sources

- GOV.UK Content API: https://content-api.publishing.service.gov.uk/
- Wikivoyage licence: https://en.wikivoyage.org/wiki/Wikivoyage:Copyleft
- OurAirports data: https://ourairports.com/data/
