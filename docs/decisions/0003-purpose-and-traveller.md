# 0003. Purpose, audience and the traveller

Status: Accepted (19 Nov 2026)

## Context

Layover started as a question: is a travel assistant worth building as a startup or as a portfolio project? Travel is a hard startup market (people buy rarely, margins are thin affiliate commissions, live supplier data is gated, and Google, Booking.com, Expedia and general AI assistants already plan trips). It is a strong portfolio domain because everyone understands it and it naturally exercises tool calling, retrieval, constraints and evaluation.

## Decision

1. **Purpose:** a portfolio project to win AI and agent engineering jobs. The owner's words: "AI/agent skills for job hunting INTERACTING WITH REAL APIS".
2. **Standard:** built like a real product, not a demo. The owner's words: "a traveller experience that would convince a recruiter, we have to build it like the real thing."
3. **The traveller:** a UK-based traveller planning a holiday abroad. The owner's words: "UK-based traveller planning a holiday abroad". So: departures from UK airports, prices in pounds, and the UK Foreign, Commonwealth & Development Office (FCDO) travel advice, which is written for British nationals.
4. **Not a startup for now.** A startup would need a narrow niche and a better business model than affiliate commission; that is out of scope.

## Consequences

- The agent work (tools, retrieval, approval step, parallel agents, evaluations) must show *through* a traveller experience, not replace it.
- Content and data choices are judged by whether they serve a UK holidaymaker (pounds, UK airports, FCDO advice).
- Still open: what the traveller has already decided when they open the app (a fixed destination and dates, or "somewhere warm in May under £800"). This shapes the main journey and is the next design question.

## Alternatives considered

- **Startup:** rejected for now, for the market reasons above.
- **A narrow startup niche** (visa-heavy travel, small-business travel, tools for travel agents): kept as ideas only.
- **A generic "AI plans your trip" chatbot:** no edge over general assistants and weak portfolio evidence.

## Sources

- Conversation with the owner, 19 Nov 2026.
- FCDO foreign travel advice: https://www.gov.uk/foreign-travel-advice
