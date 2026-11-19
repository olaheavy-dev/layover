# Layover: the main journey and the agent team

Status: approved by the owner on 19 Nov 2026 ("Approve (Recommended)", prompt window). Issue #20.

Owner answers are quoted as chosen in prompt windows on 19 Nov 2026. Anything marked **(agent's call)** is a proposal the owner can change.

## 1. Intent

Layover is a portfolio project to win AI and agent engineering jobs, built like a real product ([0003](../../decisions/0003-purpose-and-traveller.md)). This design answers the first open design question: what the traveller has already decided when they open Layover. Owner: **"Undecided, then plans (Recommended)"**.

A UK-based traveller who hasn't chosen a destination describes the trip they want in chat. Layover compares three places with real data, the traveller picks one, and Layover produces a trip summary, a day-by-day itinerary and a sandbox booking.

Not every message is that journey. The owner: "users can ask any questions relating to travel as long as we support it, we need to be able to classify intention first". So every message is first classified into a supported intent and routed (§5a).

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
- Layover is non-commercial while commission is switched off, so free non-commercial tiers apply ([data sources](../../references/data-sources.md#chosen)).
- Free-tier limits shape caching: Open-Meteo counts a long history as many calls (a 10-year daily history for one place is about 260 calls), so monthly climate averages are computed once per place and month and cached ([data sources](../../references/data-sources.md#free-apis-chosen-for-integration-14)).
- Cached fares are 2 to 7 days old ([data sources](../../references/data-sources.md#chosen)); every fare shows its age and links to Aviasales to check the live price.
- Duffel test mode uses fictional flights and prices, so the booking demo is clearly labelled as a sandbox and never offers to book a Travelpayouts fare ([0004](../../decisions/0004-flight-data-sources.md)).

## 4. Approaches

Three ways to build the journey were offered:

| Approach | Trade-off |
|---|---|
| One planner agent with a "compare destinations" tool (recommended by the agent; [0007](../../decisions/0007-agent-design.md)) | Fewest moving parts and lowest cost; multi-agent work limited to Compare destinations |
| A fixed sequence of steps, chat only for the brief | Most predictable and easiest to evaluate; less conversational and less agent judgement |
| **A team of agents under a supervisor (chosen)** | Shows multi-agent orchestration across the journey; more calls and hand-offs |

Owner chose **"Team of agents"**, then **"Team + single-agent baseline (Recommended)"**, reason **"Show multi-agent skills"**. Recorded in [0012](../../decisions/0012-agent-team.md).

## 5a. Intents: classify first, then route

The supervisor's first step on every message is to classify it into one supported intent, as structured output (a label from a fixed list, so it can be tested), then route it. Owner chose all four intents and "Say so and suggest (Recommended)" for the rest; then, for unsupported travel questions only: "we can use for unsupported questioms that relates to travelling alone mot a ask about investment", and "Use it, don't ask" (accepting the risk in Tavily's terms, below):

| Intent | Example | Route |
|---|---|---|
| `plan_trip` | "Somewhere warm in May, about £800 for two, from Manchester" | The full journey below |
| `destination_facts` | "Do I need a visa for Turkey?", "What's Lisbon like in October?", "How much is £500 in euros?" | One research agent for one place: FCDO advice, climate, money, holidays, time difference, introduction |
| `itinerary` | "Three days in Porto" | Straight to the itinerary agent, skipping compare |
| `fares_and_transport` | "Cheapest flights from Bristol to anywhere in March", "How do I get to Gatwick?" | Cached fares (with their age) and TfL |
| `unsupported_travel` | A travel question none of the above covers | A Tavily web search: short quotes with their links and the retrieval date, labelled "from a web search, not checked by Layover", plus what Layover can do. Queries carry the travel question only, never traveller details. If the search finds nothing usable, an honest "I can't help with that yet". Logged without personal data to guide what to add next |
| `not_travel` | Anything else | Politely declined |

A conversation can move between intents (a `destination_facts` question in the middle of `plan_trip`); the supervisor keeps the trip state. **(Agent's call)** When the classifier isn't confident, the brief agent asks one clarifying question rather than guessing.

## 5. The journey (`plan_trip`)

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

## 5b. Budget and costs

Owner chose "Find cost estimates" for what "within budget" means. Offered the researched sources, the owner asked what free sources can cover, then chose "Free now, Nuitee later":

- **Flights:** real cached fares from Travelpayouts, with their age.
- **Stay and meals:** estimates from Wikivoyage listings ("typical double room" under Sleep, "a complete meal for one" under Eat), converted to pounds in tested code with Frankfurter. **(Agent's call)** An estimate is shown only when a city has a minimum number of priced listings (the figure is set in the plan), labelled with the listing count and the page's edit date. Otherwise "not known".
- **Local transport and activities:** "not known" (0011: missing costs are never shown as zero).
- **Later, switched off:** Nuitee Connect's city price index for stay (0.02 US dollars a request, cached per city and month), with a monthly cap, built behind a switch that stays off until the owner approves the spend.
- **Not from web search:** Tavily results are page snippets with estimated or missing dates, so no figure is taken from them (0011); Tavily serves unsupported travel questions only (§5a).

Example line: "Flights from £X, stay about £Y and meals about £Z (estimates from 6 Wikivoyage listings, page edited March 2026) of your £800; local transport and activities not known". The budget check is tested code.

## 5c. Public use and cost control

Owner: "Live trips but we will set limits or cap based on IP or something". Live trips are open to the public, with a limit per visitor and an overall cap on model spending. **(Agent's call)** As a precaution, Layover treats an IP address as personal data (the UK GDPR definition includes "an online identifier", [ICO](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/personal-information-what-is-it/what-is-personal-data/what-is-personal-data/)), so only a salted one-way hash is stored, for no longer than the limit window; the cap's figures are set by the owner once build step 1 measures a trip's cost (`AGENTS.md` rule 3).

## 5d. Widgets for tool results, and the design bar

Added by the owner after approval, 19 Nov 2026: "our tools will be attached to widgets so we can display our own custome ui for each tool calls not just free text", and "our designs have to be very thoutful, detailed, professional and worldclass". The owner chose "Now, in the Design stage (Recommended)" for designing the screens and widgets.

- **Widgets.** Every tool returns structured data tagged with a `kind`, and the interface draws each `kind` with its own component. The chat streams text and widget blocks together, and the shared trip page reuses the same widgets. **(Agent's call)** First kinds: `brief_summary`, `comparison_table`, `fare_card`, `climate_chart`, `sea_conditions`, `daylight`, `money`, `advice_card` (FCDO, with its update date), `place_intro`, `map`, `itinerary_day`, `hotel_list`, `cost_estimate`, `booking_approval`, `web_results` and `not_known`. Each widget shows its sources and their age, and each has loading, empty, error and "not known" states (0011). Plan 1 fixes one JSON Schema per `kind`.
- **Design bar.** Screens and widgets are designed in the Design stage, before the gate, with the design skills: a design brief, information architecture, design tokens with light and dark themes, boards for every screen and widget at phone and desktop widths, a benchmark against travel products, then the `design-reviewer` and `visual-reviewer` passes. Build starts from approved boards.

## 6. The agent team

| Part | Kind | Job | Tools and data |
|---|---|---|---|
| Supervisor | Agent | Classifies each message's intent (§5a), routes between the parts and owns the shared trip state | None directly |
| Web search | Tool step, not an agent | Answers `unsupported_travel` questions with quoted, linked results | Tavily search API |
| Brief agent | Agent | Chat with the traveller; produce the confirmed brief | OurAirports (airport lookup) |
| Compare | Fan-out of three research agents, then a ranking step | One agent per destination gathers its facts; ranking compares and checks the budget in code | Travelpayouts cached fares, Open-Meteo Historical/Climate and Marine, sunrise-sunset.org, Python `holidays`, Frankfurter, retrieval over FCDO advice and Wikivoyage ([0008](../../decisions/0008-retrieval-no-knowledge-graph.md)), Wikipedia |
| Itinerary agent | Agent | Days built from sourced places around the chosen base | Overpass (points of interest and OpenStreetMap hotels), retrieval over Wikivoyage, Open-Meteo, IANA time zones. **(Agent's call)** Foursquare Open Source Places waits unless Overpass proves too slow |
| Booking | Fixed subgraph, not an agent | Search, price check, approval, then order and test payment | Duffel test mode; Nuitee Connect sandbox |
| Single-agent baseline | Agent (evaluation only) | The same journey with all tools in one agent | All of the above |

**(Agent's call)** FCDO advice and Wikivoyage are retrieved from an index, as [0008](../../decisions/0008-retrieval-no-knowledge-graph.md) decided, not fetched live per question. A destination's pages are indexed the first time it is needed. The vector store is a new dependency, chosen with the owner's approval in the plan.

Each agent's tools sit behind Layover's own MCP servers from build step 2 ([0009](../../decisions/0009-tools-as-mcp-servers.md)). Totals, conversions and comparisons are tested code (`test-first` skill), never the model.

## 7. Evaluations

Permanent IDs per area (`AGENTS.md`): `INTENT-`, `BRIEF-`, `COMPARE-`, `ITIN-`, `BOOK-`, `TRIP-`. **(Agent's call)** First cases:

- `INTENT-01` each example in §5a is classified to its intent; `INTENT-02` a non-travel request is declined; `INTENT-03` an unsupported travel question gets web-search quotes with links and the "not checked by Layover" label, or "not yet", never an unsourced answer; `INTENT-04` a non-travel question (for example about investments) is declined without a web search; `INTENT-05` a web-search query never contains the traveller's details.
- `BRIEF-01` a vague request ends in a confirmed summary with every field set; `BRIEF-02` a budget or date misread is corrected before searching.
- `COMPARE-01` all three places stay within the budget in code, or say why not; `COMPARE-02` every figure carries its source and age; `COMPARE-03` no destination is called "safe".
- `ITIN-01` every stop exists in the source data; `ITIN-02` a gap in data is stated, not filled.
- `BOOK-01` no order is placed without the approval step; `BOOK-02` the booking is labelled as a sandbox and never uses a Travelpayouts fare.
- `TRIP-01` the team and the baseline run the same trips; speed, tokens and quality are reported side by side.

**(Agent's call)** Scoring: factual checks (sources, budget, approval, labels) are code; ranking and itinerary quality are scored by a model as judge against a written rubric, with the owner spot-checking a sample. Each evaluation trip has a scripted traveller that answers the brief questions, picks a place and approves or rejects booking. The README states the trip set's size with every score.

## 8. Open questions

For the owner or before building:

1. **Nuitee Connect terms:** its published terms (last updated January 2025) are booking conditions for travel agents and don't mention the sandbox, demo or portfolio use; whether its sandbox hotels are real or fake isn't stated. Ask Nuitee before building the hotel demo. If it says no or doesn't answer, "try booking" ships with Duffel flights only (owner: "Flights-only booking (Recommended)").
2. **Shareable link expiry:** how long a trip link lasts (a privacy and storage choice). **(Agent's call)** A link reopens a frozen copy of the trip (brief, comparison, summary, itinerary, booking state) with "as of" dates on every fare and advice date; the chat transcript isn't kept.
3. **Nuitee price index (later):** it is in beta ("may change in future versions"), its occupancy basis isn't stated, and its terms are unconfirmed (same question as item 1). The spend needs the owner's approval before the switch is turned on.
4. **Tavily terms:** they allow use "solely for Customer's internal business purposes", which may not cover a public site showing results; the owner chose to use it without asking and accepts that the account could be closed. Tavily keeps queries under a "perpetual, and irrevocable" licence and may use them for AI training, so queries never include traveller details.
5. **Spending cap figures and hosting:** set by the owner after build step 1 measures a trip's cost; hosting and the database are infrastructure decisions for the owner.
6. **Build order:** [01 §4](../../product/01-research-and-direction.md) starts with "a single LangGraph agent"; the plan revises it for the agent team and the baseline.

## 9. Left to the builder

The shared trip-state schema (fixed first in the plan), prompts, the ranking method within the budget rule, caching periods per source within each provider's terms, and how the three destinations are proposed within the brief. **(Agent's call)** The plan covers the backend, the agents and the API (including streamed tool calls and the approval pauses for "pick" and booking); screens are designed separately with the design skills before frontend tasks start.
