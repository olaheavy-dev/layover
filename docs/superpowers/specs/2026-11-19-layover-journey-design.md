# Layover: the main journey and the agent team

Status: draft for the owner's approval, 19 Nov 2026. Issue #20.

Owner answers are quoted as chosen in prompt windows on 19 Nov 2026. Anything marked **(agent's call)** is a proposal the owner can change.

## 1. Intent

Layover is a portfolio project to win AI and agent engineering jobs, built like a real product ([0003](../../decisions/0003-purpose-and-traveller.md)). This design answers the first open design question: what the traveller has already decided when they open Layover. Owner: **"Undecided, then plans (Recommended)"**.

A UK-based traveller who hasn't chosen a destination describes the trip they want in chat. Layover compares three places with real data, the traveller picks one, and Layover produces a trip summary, a day-by-day itinerary and a sandbox booking.

## 2. Goals, non-goals and anti-goals

**Goals.** A recruiter who tries Layover comes away convinced of all four (owner chose all four):

1. **Honest, grounded answers:** every fact cited with its age; no invented prices or places; clear "not known" states ([0011](../../decisions/0011-product-integrity-rules.md)).
2. **Real agent engineering:** visible tool calls, a team of agents, parallel research agents, an approval step before booking, and an evaluation score in the README with its dataset.
3. **Feels like a real product:** fast, works on a phone, good empty and error states, shareable trip links.
4. **Useful for real trips:** sensible places for the budget, real fares to check, practical notes a UK holidaymaker would act on.

**Non-goals (for this design):** real bookings or payments (sandboxes only, [0004](../../decisions/0004-flight-data-sources.md)); accounts and sign-in; real hotel prices; commission switched on (register: "Commission is built but switched off…"); live flight positions (OpenSky is an idea for later).

**Anti-goals (failure even if it works):** an invented fare, place, opening time or rule; a destination called "safe"; the model doing arithmetic; scraping; a missing value shown as zero ([0011](../../decisions/0011-product-integrity-rules.md)).

## 3. Constraints

- Decisions [0004](../../decisions/0004-flight-data-sources.md) (cached real fares to browse, Duffel sandbox to book), [0008](../../decisions/0008-retrieval-no-knowledge-graph.md) (retrieval over FCDO and Wikivoyage), [0009](../../decisions/0009-tools-as-mcp-servers.md) (tools become MCP servers), [0011](../../decisions/0011-product-integrity-rules.md) and [0012](../../decisions/0012-agent-team.md).
- Layover is non-commercial while commission is switched off, so free non-commercial tiers apply ([data sources](../../references/data-sources.md)).
- Free-tier limits shape caching: Open-Meteo counts a long history as many calls (a 10-year daily history for one place is about 260 calls), so monthly climate averages are computed once per place and month and cached ([data sources](../../references/data-sources.md#free-apis-chosen-for-integration-14)).
- Cached fares are 2 to 7 days old ([data sources](../../references/data-sources.md)); every fare shows its age and links to Aviasales to check the live price.
- Duffel test mode uses fictional flights and prices, so the booking demo is clearly labelled as a sandbox and never offers to book a Travelpayouts fare ([0004](../../decisions/0004-flight-data-sources.md)).

## 4. Approaches

Three ways to build the journey were offered:

| Approach | Trade-off |
|---|---|
| One planner agent with a "compare destinations" tool (recommended by the agent; [0007](../../decisions/0007-agent-design.md)) | Fewest moving parts and lowest cost; multi-agent work limited to Compare destinations |
| A fixed sequence of steps, chat only for the brief | Most predictable and easiest to evaluate; less conversational and less agent judgement |
| **A team of agents under a supervisor (chosen)** | Shows multi-agent orchestration across the journey; more calls and hand-offs |

Owner chose **"Team of agents"**, then **"Team + single-agent baseline (Recommended)"**, reason **"Show multi-agent skills"**. Recorded in [0012](../../decisions/0012-agent-team.md).

## 5. The journey

1. **Brief (chat).** Owner: **"Chat only"**. The traveller types; the brief agent asks for whatever is missing: departure airport, when (month or dates), length, how many people, total budget in pounds, and the feel ("warm, beach, good food"). **(Agent's call)** Before searching, it restates the brief as one confirmed summary ("Manchester, 5 nights in May, 2 people, £800 total, warm and relaxed") for the traveller to confirm or correct. The confirmed brief is the fixed input the rest of the journey and the evaluations use.
2. **Compare three places.** Owner: **"let us start with three first"**. The supervisor proposes three destinations that fit the brief; one research agent per destination runs in parallel; a ranking step compares them side by side and checks the budget in code. **(Agent's call)** The traveller can swap a destination for one of their own.
3. **Pick.** The traveller chooses one place.
4. **Trip summary.** Fare range from their airport with its age and an Aviasales link (plain while commission is off), typical weather for the month, sea temperature where relevant, daylight, local holidays, money (exchange rate), FCDO advice link with its update date, a short introduction, photos and a map.
5. **Itinerary.** A day-by-day plan. **(Agent's call)** Built only from places in Layover's data (OpenStreetMap and Foursquare points of interest, Wikivoyage, Wikipedia), each stop linked to its source; the agent arranges days by distance, known opening times and the weather, and says when it lacks data rather than guessing. It starts from where the traveller stays (below).
6. **Where to stay.** Owner: **"Look for a hotel data source"**, then **"Nuitee sandbox + OSM hotels (Recommended)"**. Real hotel names and locations come from OpenStreetMap (no prices); the traveller can pick one as the itinerary's base.
7. **Try booking (sandbox).** Owner: **"Summary + itinerary + booking"**. A clearly labelled "try booking" flow: flights in Duffel test mode and a hotel in the Nuitee Connect sandbox, each pausing for the traveller's approval before any order ([0007](../../decisions/0007-agent-design.md) point 2).
8. **Keep it.** Owner: **"Shareable link, no accounts (Recommended)"**. Each trip gets a private link the traveller can reopen or share; no sign-in.

```
Chat brief ─▶ confirm summary ─▶ compare 3 (parallel) ─▶ pick ─▶ summary ─▶ itinerary ─▶ try booking (approve) ─▶ share link
```

## 6. The agent team

| Part | Kind | Job | Tools and data |
|---|---|---|---|
| Supervisor | Agent | Routes between the parts and owns the shared trip state | None directly |
| Brief agent | Agent | Chat with the traveller; produce the confirmed brief | OurAirports (airport lookup) |
| Compare | Fan-out of three research agents, then a ranking step | One agent per destination gathers its facts; ranking compares and checks the budget in code | Travelpayouts cached fares, Open-Meteo Historical/Climate and Marine, sunrise-sunset.org, Python `holidays`, Frankfurter, FCDO Content API, Wikipedia |
| Itinerary agent | Agent | Days built from sourced places around the chosen base | Overpass, Foursquare Open Source Places, Wikivoyage (MediaWiki API), OpenStreetMap hotels, Open-Meteo, IANA time zones |
| Booking | Fixed subgraph, not an agent | Search, price check, approval, then order and test payment | Duffel test mode; Nuitee Connect sandbox |
| Single-agent baseline | Agent (evaluation only) | The same journey with all tools in one agent | All of the above |

Each agent's tools sit behind Layover's own MCP servers from build step 2 ([0009](../../decisions/0009-tools-as-mcp-servers.md)). Totals, conversions and comparisons are tested code (`test-first` skill), never the model.

## 7. Evaluations

Permanent IDs per area (`AGENTS.md`): `BRIEF-`, `COMPARE-`, `ITIN-`, `BOOK-`, `TRIP-`. **(Agent's call)** First cases:

- `BRIEF-01` a vague request ends in a confirmed summary with every field set; `BRIEF-02` a budget or date misread is corrected before searching.
- `COMPARE-01` all three places stay within the budget in code, or say why not; `COMPARE-02` every figure carries its source and age; `COMPARE-03` no destination is called "safe".
- `ITIN-01` every stop exists in the source data; `ITIN-02` a gap in data is stated, not filled.
- `BOOK-01` no order is placed without the approval step; `BOOK-02` the booking is labelled as a sandbox and never uses a Travelpayouts fare.
- `TRIP-01` the team and the baseline run the same trips; speed, tokens and quality are reported side by side.

## 8. Open questions

For the owner or before building:

1. **Nuitee Connect terms:** its published terms (last updated January 2025) are booking conditions for travel agents and don't mention the sandbox, demo or portfolio use; whether its sandbox hotels are real or fake isn't stated. Ask Nuitee before building the hotel demo.
2. **Shareable link expiry:** how long a trip link lasts (a privacy and storage choice).
3. **Build order:** [01 §4](../../product/01-research-and-direction.md) starts with "a single LangGraph agent"; the plan revises it for the agent team and the baseline.

## 9. Left to the builder

The shared trip-state schema (fixed first in the plan), prompts, the ranking method within the budget rule, caching periods per source within each provider's terms, screen layouts (designed separately), and how the three destinations are proposed within the brief.
