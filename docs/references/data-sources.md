# Data sources

What each outside source gives Layover, its access terms and limits, and when that was last checked. Re-check a source's terms before building with it, and update this page in the same pull request.

Checked on 19 Nov 2026 unless a row says otherwise.

## Chosen

| Source | What it gives | Access | Real or sandbox | Used for | Decision |
|---|---|---|---|---|---|
| [Travelpayouts: Aviasales Data API](https://support.travelpayouts.com/hc/en-us/articles/203956163) | Cheapest fares, price calendars, popular destinations | Travelpayouts account, API token (Profile → API token), sent in the `X-Access-Token` header. Join the Aviasales programme ([FAQ](https://support.travelpayouts.com/hc/en-us/articles/204529267-FAQ-about-Aviasales-API)). No brand approval ([requirements](https://support.travelpayouts.com/hc/en-us/articles/203956083-Requirements-for-Aviasales-data-API-access)) | **Real, cached** from users' searches, kept 2 to 7 days | Browsing fares | [0004](../decisions/0004-flight-data-sources.md) |
| [Duffel (test mode)](https://duffel.com/docs/api/overview/test-mode) | Search, offers, orders, payments (balance, or card through [Payment Intents](https://duffel.com/docs/api/payment-intents) and the [card form with 3D Secure](https://duffel.com/docs/guides/card-form-component-with-3dsecure)) | Free sandbox; `duffel_test_` token; [test cards](https://duffel.com/docs/api/overview/test-mode); unlimited balance in test mode ([Payments](https://duffel.com/docs/api/v2/payments)) | **Sandbox:** fake prices; "Duffel Airways" is a fictional test airline ([help](https://help.duffel.com/hc/en-gb/articles/4410085835282-Are-the-flight-prices-in-test-mode-sandbox-real)) | The booking demo | [0004](../decisions/0004-flight-data-sources.md) |
| [GOV.UK Content API](https://content-api.publishing.service.gov.uk/) (FCDO travel advice, e.g. `/api/content/foreign-travel-advice/france`) | Entry requirements, safety and travel advice per country, with update dates | Free, no key; Open Government Licence | Real | Retrieval (RAG) and citations | [0008](../decisions/0008-retrieval-no-knowledge-graph.md) |
| [Wikivoyage](https://en.wikivoyage.org/) | Destination guides | Free; CC BY-SA, credit required | Real (community-written) | Retrieval (RAG) | [0008](../decisions/0008-retrieval-no-knowledge-graph.md) |
| [Open-Meteo](https://open-meteo.com/en/docs) | Weather forecasts and history | Free API for non-commercial use only, no key; CC BY 4.0, credit required; under 10,000 calls a day, 5,000 an hour, 600 a minute ([terms](https://open-meteo.com/en/terms)). The terms count sites with subscriptions or advertising, and promotional activities, as commercial | Real | Weather tool | Open question: do Aviasales affiliate links make Layover commercial under these terms? |
| [Frankfurter](https://frankfurter.dev/) | European Central Bank exchange rates | Free, no key | Real (daily reference rates) | Currency tool | — |
| [OurAirports](https://ourairports.com/data/) | Airports, countries, regions | Public domain download | Real | Reference tables | [0008](../decisions/0008-retrieval-no-knowledge-graph.md) |

## Possible extras through Travelpayouts (no brand approval)

From [Brands that provide access to APIs and data feeds](https://support.travelpayouts.com/hc/en-us/articles/20384016664594-Brands-that-provide-access-to-APIs-and-data-feeds-for-Travelpayouts-partners). Each brand has its own terms in its documentation; read them before use.

| Brand | What it gives | Possible use for a UK holidaymaker |
|---|---|---|
| Omio | Feed of popular destinations by country (trains, buses) | Rail options, e.g. Eurostar trips |
| intui.travel | Transfer search with prices, airport route lists, booking links | Airport-to-hotel transfer cost |
| Airalo | eSIM prices by country and region, validity, operator | Mobile data cost abroad |
| Tiqets | Cities and offers (for widgets) | Attraction tickets |
| Viator | Feed of discounted tours (deals only, not a full catalogue) | Tour deals |
| WeGoTrip | Self-guided quest tours, cities, reviews | Niche activities |

**No hotel data:** no hotel brand (Booking.com or others) appears on that list, so Travelpayouts gives no hotel prices. How Layover handles hotels is an open design question.

## Not available or rejected

| Source | Why not |
|---|---|
| Amadeus Self-Service APIs | Shut down on 17 July 2026; only enterprise access remains ([PhocusWire](https://www.phocuswire.com/amadeus-shut-down-self-service-apis-portal-developers), [Skift](https://skift.com/2026/09/03/amadeus-brings-travel-tech-into-claude/)) |
| Aviasales Flight Search API (live) | Needs at least 50,000 monthly active users ([Travelpayouts](https://support.travelpayouts.com/hc/en-us/articles/203956173)) |
| Kiwi.com API (through Travelpayouts) | Needs at least 50,000 monthly active users ([Travelpayouts](https://support.travelpayouts.com/hc/en-us/articles/360019237899-Kiwi-com-affiliate-program-API)) |
| GetTransfer | Needs brand approval ([Travelpayouts brands list](https://support.travelpayouts.com/hc/en-us/articles/20384016664594-Brands-that-provide-access-to-APIs-and-data-feeds-for-Travelpayouts-partners)) |
| Skyscanner partner API | Not checked; assumed to need a partnership. Check before relying on this row |
| Google Flights | No public flight-price API found as of 19 Nov 2026 |
| Scraper APIs (Google Flights, Skyscanner scrapers) | They scrape sites; Layover doesn't scrape ([0011](../decisions/0011-product-integrity-rules.md), proposed) |
| Duffel live mode | Means selling real tickets with real money; not needed for a portfolio |

## Duffel coverage (for reference)

Duffel says it reaches 300+ airlines through one API ([Duffel](https://duffel.com/flights/airlines/swiss)), and that its airlines' partner networks reach 380+ ([Duffel blog](https://duffel.com/blog/access-routes-from-more-than-380-airlines-on-duffel)). Test mode does not show real coverage.
