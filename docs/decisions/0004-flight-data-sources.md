# 0004. Flight data: cached real fares to browse, a sandbox to book

Status: Accepted (19 Nov 2026)

## Context

The owner wants visitors to see real flights: "we do not need to accept payments just display the flights to visitors". The owner also wants the agent to show a full booking flow. Checked on 19 Nov 2026 (details and sources in [data sources](../references/data-sources.md)):

- **Amadeus Self-Service APIs were shut down on 17 July 2026.** Most "AI travel agent" tutorials depend on them.
- **Live flight search is gated:** Aviasales' Flight Search API and Kiwi.com's API (through Travelpayouts) both require at least 50,000 monthly active users. Google Flights has no public API. Scraper APIs break sites' terms.
- **Travelpayouts' Aviasales Data API** gives real fares cached from real users' searches (kept 2 to 7 days), needs no brand approval, and is used with the account's API token.
- **Duffel test mode** is a free sandbox for the whole booking flow: search, price check, order and test payment (balance or card through Duffel's card form with 3D Secure). Its flights and prices are not real. Duffel covers 300+ airlines in live mode, but going live means selling real tickets.

## Decision

Use both, kept clearly apart:

1. **Browse (real data):** Travelpayouts Aviasales Data API. Every fare shows its age ("from £89, found 2 days ago") and links to Aviasales to check the live price.
2. **Book (sandbox demo):** Duffel test mode, in a separate, clearly labelled "try booking" flow with an approval step before any order or payment.
3. The agent never offers to book a Travelpayouts fare through Duffel: those flights are not bookable there.

The owner chose this over "Duffel only" and "Travelpayouts only" (reason not stated; the recommendation had been Duffel only, for simplicity).

## Consequences

- Two integrations. Fares on screen will not match the bookable sandbox flights; the interface must make the two modes obvious.
- Cached fares can be stale; showing their age is required, and that staleness rule is a test case.
- Route coverage of Aviasales' cache must be checked for the routes the traveller cares about.
- The Travelpayouts token goes in the `X-Access-Token` header, never in a URL.

## Alternatives considered

- **Duffel only:** simplest, full flow, but every flight is fake.
- **Travelpayouts only:** real fares, but no booking or payment flow to show agent actions.
- **Amadeus:** closed to new self-service users.
- **Live search APIs (Aviasales Search, Kiwi.com, Skyscanner):** gated by traffic or partnership.
- **Scraping (e.g. Google Flights scrapers):** against sites' terms; rejected.

## Sources

- See [data sources](../references/data-sources.md), checked 19 Nov 2026.
