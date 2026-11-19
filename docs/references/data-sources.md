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
| Scraper APIs (Google Flights, Skyscanner scrapers) | They scrape sites; Layover doesn't scrape ([0011](../decisions/0011-product-integrity-rules.md)) |
| Duffel live mode | Means selling real tickets with real money; not needed for a portfolio |

## Free APIs chosen for integration (#14)

Chosen by the owner on 19 Nov 2026 in prompt windows, from research on the providers' own pages that day (register line "Free APIs chosen…"). Layover is non-commercial while commission is switched off, so free non-commercial tiers fit; the last column says what changes if commission is switched on. Nothing is built until the build stage, and each source's terms are re-read before building with it.

| Source | What it gives | Value for a UK holidaymaker | Access | Licence and credit | Limits | If commission is switched on |
|---|---|---|---|---|---|---|
| [Open-Meteo Historical Weather](https://open-meteo.com/en/docs/historical-weather-api) and [Climate](https://open-meteo.com/en/docs/climate-api) APIs | Past daily weather from 1940 (ERA5) and modelled daily climate 1950 to 2050 ("should not be mistaken for actual measurements") | Monthly averages: how warm, wet and sunny a place is in May | No key for non-commercial use ([features](https://open-meteo.com/en/features)) | CC BY 4.0; credit Open-Meteo, plus Copernicus (historical) or the CMIP6 programme (climate) | Free tier: 600 calls a minute, 5,000 an hour, 10,000 a day, 300,000 a month, applied by IP address and application. A request covering more than 2 weeks for one location, or more than 10 variables, counts as several calls ([pricing](https://open-meteo.com/en/pricing)): a 10-year daily history for one place is about 260 calls (3,650 days ÷ 14), so averages should be computed once and cached. Whether these limits are shared with the forecast API is not confirmed | Paid plan needed ([terms](https://open-meteo.com/en/terms)) |
| [Open-Meteo Marine](https://open-meteo.com/en/docs/marine-weather-api) | Sea surface temperature, waves, swell; forecast and history from 1940; "accuracy at coastal areas is limited" | Sea temperature and conditions for beach trips | As above | CC BY 4.0; credit the model providers, for Copernicus Marine "generated using E.U. Copernicus Marine Service Information" | As above, including the weighting of long or many-variable requests | Paid plan needed |
| [sunrise-sunset.org](https://sunrise-sunset.org/api) | Sunrise, sunset, twilight and golden hour for any date and place, in local time | Daylight hours for planning days out | "No sign up or API key required" | A visible link to sunrise-sunset.org where the data is shown | No figure; free "for reasonable request volumes", with HTTP 429 when too fast | Commercial use isn't mentioned on the page: re-check |
| [IANA time zone database](https://data.iana.org/time-zones/tz-link.html) (offline) | The history of local time for places worldwide, released "every few months" | Local time and time difference from the UK, with no API call | Offline: Python's [`zoneinfo`](https://docs.python.org/3/library/zoneinfo.html) reads it from the system, or from the `tzdata` package, which needs approval as a dependency | Public domain | None | No change. Included by the agent as a default (offline, public domain); the owner can remove it |
| [OpenFreeMap](https://openfreemap.org/) | Vector map tiles and styles | The base map for destinations, places and routes | "No API keys", "no registration" | "Attribution is required"; MapLibre adds it automatically ([home page](https://openfreemap.org/)). The exact credit names are not confirmed on the pages read | "No limits on the number of map views or requests" | Its FAQ says commercial use is fine; the terms page is silent: re-check |
| [Wikipedia](https://www.mediawiki.org/wiki/Wikimedia_APIs) and [Wikidata](https://www.wikidata.org/wiki/Wikidata:Licensing) | Article summaries; structured facts such as population and languages | Short destination introductions and country facts | No key; an informative User-Agent with contact details ([policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy)) | Wikipedia text CC BY-SA, crediting authors with a link to the page; Wikidata CC0, no credit required ([terms of use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use)) | 10 requests a minute with no identifying User-Agent; 200 a minute for a compliant one ([rate limits](https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits)). The summary endpoint's own limits are not confirmed | Allowed: the licences "do allow commercial uses" |
| [Unsplash API](https://unsplash.com/documentation) | Photos | Destination photos | Key and app registration | Credit "Unsplash" and the photographer, with a link to their profile; use the returned image URLs directly; call the download endpoint for each download ([API terms](https://unsplash.com/api-terms)) | Demo 50 requests an hour; production 1,000 an hour after approval | Allowed for "commercial and non-commercial purposes" ([licence](https://unsplash.com/license)) |
| [Foursquare Open Source Places](https://docs.foursquare.com/data-products/docs/access-fsq-os-places) | A bulk download of points of interest (not a live API) | Places near a hotel, if Overpass is too slow | Account on the Places Portal and an access token | Apache 2.0 | None (bulk data); update frequency not stated | Apache 2.0 allows it |
| [TfL Unified API](https://api-portal.tfl.gov.uk/) | London transport data | Getting to Heathrow, Gatwick, Stansted or London City from London | Free key (`app_key`) after registering | Credit "Powered by TfL Open Data" and "Contains OS data © Crown copyright and database rights 2016" with Geomni UK Map data; TfL branding guidelines apply ([licence](https://tfl.gov.uk/corporate/terms-and-conditions/transport-data-service), read in a browser) | At most 500 calls a minute per data feed | Allowed: "Exploit the Information commercially and non-commercially" |
| [Python `holidays`](https://github.com/vacanza/holidays) (offline) | Public holidays for 250 country codes | Local holidays at the destination, with no API call or terms of service | Offline library | MIT | None | MIT allows it. An offline alternative to Nager.Date for destination holidays |

## Ideas for later

Researched on 19 Nov 2026 and kept for later; the owner chose not to integrate these now.

| Source | What it gives | Why later | If commission is switched on |
|---|---|---|---|
| [Google Travel Impact Model](https://developers.google.com/travel/impact-model) | Flight CO2 estimates per flight or route (next 11 months); free with a Google Cloud key; CC BY-SA 4.0 | Owner's choice; quotas and API terms not confirmed | Data CC BY-SA 4.0 allows it; API terms not confirmed |
| [Mobility Database](https://github.com/MobilityData/mobility-database-catalogs) | A CC0 catalogue of public transport timetables (GTFS) worldwide | Each city's feed has its own licence to check | Catalogue CC0; each feed's own terms decide |
| [OpenSky Network](https://openskynetwork.github.io/opensky-api/rest.html) | Live aircraft positions | Its terms limit use to "non-profit research and non-profit education", and operational use "in any live product, service, or automated system" needs a written licence; data can't be shared outside the user's institute ([terms](https://opensky-network.org/about/terms-of-use), read in a browser). Owner chose "Move to ideas" | Needs a written licence |
| [USGS earthquake feeds](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) | Recent earthquakes, updated every minute, no key | Licence and credit wording not confirmed | Not confirmed |
| [GDACS](https://www.gdacs.org/Knowledge/overview.aspx) | UN and European Commission alerts for earthquakes, cyclones, floods and volcanoes; "purely indicative" | Licence, credit and limits not confirmed | Not confirmed |
| [NASA EONET](https://eonet.gsfc.nasa.gov/docs/v3) | Wildfires, storms and landslides; "for visualization and general information purposes only" | Data licence not confirmed | Not confirmed |
| [Open-Meteo Air Quality](https://open-meteo.com/en/docs/air-quality-api) | UV index, air pollution and pollen (Europe, in season), a few days ahead | Not chosen now; useful during a trip rather than when choosing one | Paid plan needed |
| [OpenAQ](https://docs.openaq.org/about/about) | Measured air quality from stations; free sign-up; 60 requests a minute, 2,000 an hour | Patchy coverage; licence and commercial use not confirmed | Not confirmed |
| [Pexels API](https://www.pexels.com/api/documentation/) | Photos and videos; key; 200 requests an hour, 20,000 a month | An alternative to Unsplash | The licence lists free use, including marketing; "commercial" isn't named |
| [MapTiler](https://www.maptiler.com/cloud/pricing/), [Stadia Maps](https://stadiamaps.com/pricing/), [OpenStreetMap tiles](https://operations.osmfoundation.org/policies/tiles/) | Map tiles | Alternatives to OpenFreeMap; MapTiler's and Stadia's free plans are non-commercial | MapTiler and Stadia free plans: no; OpenStreetMap tiles: no separate rule, access "may be withdrawn at any point" |
| [pycountry](https://pypi.org/project/pycountry/) | ISO countries, currencies and languages offline; LGPL-2.1 | Alternative to REST Countries for codes | LGPL-2.1 allows it, with its linking conditions |
| [TravelHealthPro](https://travelhealthpro.org.uk/widget.php) | The UK's travel health advice (UKHSA) | No free API (the API has a set-up cost and annual fee); link out instead | Linking out is unaffected |

## Considered and not used

| Source | Why not |
|---|---|
| [OpenFlights data](https://openflights.org/data.php) | Stale: airports "as of January 2017", routes not updated since June 2014 |
| [OSRM demo server](https://github.com/Project-OSRM/osrm-backend/wiki/Api-usage-policy) | "Excessive use is not allowed" and access may be withdrawn at any time; not for production |
| Transitland, Navitia, OpenRouteService, OpenTripMap, Rail Data Marketplace, IEC World Plugs | Their pages blocked automated reading or showed no terms on 19 Nov 2026; not checked |

## Duffel coverage (for reference)

Duffel says it reaches 300+ airlines through one API ([Duffel](https://duffel.com/flights/airlines/swiss)), and that its airlines' partner networks reach 380+ ([Duffel blog](https://duffel.com/blog/access-routes-from-more-than-380-airlines-on-duffel)). Test mode does not show real coverage.
