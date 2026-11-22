// The wording of the "How Layover works" page, copied from the approved board
// (docs/design/boards/screens/how-it-works.html). The data sources list
// (docs/references/data-sources.md) is the record of the sources and their terms.

export const SUPERVISOR = { name: "Supervisor", text: "Routes the work and keeps the shared trip" };

export const TEAM_STEPS = [
  {
    name: "Brief agent",
    text: "Holds the chat. Asks for what is missing, then shows your brief and waits for your OK.",
  },
  {
    name: "Research agents",
    text: "One for each place, working at the same time. Each checks fares, costs and weather. Layover then compares the places side by side and checks the budget in code.",
  },
  {
    name: "Itinerary agent",
    text: "Builds your days from places that have a source, starting from the hotel you chose.",
  },
  {
    name: "Booking",
    text: "Fixed steps, not an agent. Nothing is ordered until you approve it, and it is a sandbox: no real booking or payment.",
  },
];

export const RULES = [
  {
    name: "No invented facts",
    text: "A price, rule or opening time comes from a named source, or Layover does not show it.",
  },
  {
    name: "Every outside value has a label",
    text: "Live, Cached with its age, Fallback or Unavailable. You can see how fresh a figure is.",
  },
  {
    name: "The AI does not do the sums",
    text: "Totals, currency conversions and comparisons come from tested code, not from the model.",
  },
  {
    name: "Missing data is never shown as zero",
    text: "If Layover does not know something, it says “Not known”. It never shows a zero or a favourable guess.",
  },
  {
    name: "No scraping",
    text: "Data comes from APIs and feeds that Layover is allowed to use, under their terms.",
  },
  {
    name: "Travel advice links to the FCDO",
    text: "Entry and travel advice always links to the FCDO page and shows its update date. Layover does not tell you a place is free of risk: you read the advice and decide.",
  },
];

export const SOURCES = [
  {
    name: "Travelpayouts: Aviasales Data API",
    href: "https://support.travelpayouts.com/hc/en-us/articles/203956163",
    gives: "Lowest cached fares and price calendars.",
    terms:
      "Free with a token. The fares come from other people’s searches and are kept for 2 to 7 days, so Layover shows them as Cached.",
  },
  {
    name: "Duffel (test mode)",
    href: "https://duffel.com/docs/api/overview/test-mode",
    gives: "Search, offers and orders for the booking demo.",
    terms: "Free sandbox. Prices are fake and the test airline is fictional, so nothing is real.",
  },
  {
    name: "GOV.UK Content API: FCDO travel advice",
    href: "https://content-api.publishing.service.gov.uk/",
    gives: "Entry requirements and travel advice for each country, with update dates.",
    terms: "Free, no key. Open Government Licence.",
  },
  {
    name: "Wikivoyage",
    href: "https://en.wikivoyage.org/",
    gives: "Destination guides.",
    terms: "Free, no key. The text is CC BY-SA 4.0: Layover credits it and links back.",
  },
  {
    name: "Open-Meteo",
    href: "https://open-meteo.com/en/docs",
    gives: "Weather forecasts and history.",
    terms:
      "Free for non-commercial use, no key. The data is CC BY 4.0, with a credit link next to it.",
  },
  {
    name: "Frankfurter",
    href: "https://frankfurter.dev/",
    gives: "European Central Bank exchange rates.",
    terms: "Free, no key. Daily reference rates.",
  },
  {
    name: "OurAirports",
    href: "https://ourairports.com/data/",
    gives: "Airports, countries and regions.",
    terms: "Public domain download.",
  },
  {
    name: "Open-Meteo Marine",
    href: "https://open-meteo.com/en/docs/marine-weather-api",
    gives:
      "Sea surface temperature, waves and swell. The page says accuracy at coastal areas is limited.",
    terms: "Free for non-commercial use, no key. CC BY 4.0: Layover credits the model providers.",
  },
  {
    name: "sunrise-sunset.org",
    href: "https://sunrise-sunset.org/api",
    gives: "Sunrise, sunset, twilight and golden hour for any date and place, in local time.",
    terms:
      "No sign-up or key. Layover shows a visible link to sunrise-sunset.org where the data is shown.",
  },
  {
    name: "IANA time zone database",
    href: "https://data.iana.org/time-zones/tz-link.html",
    gives:
      "The history of local time for places worldwide, so Layover can work out the time difference from the UK.",
    terms: "Offline, public domain.",
  },
  {
    name: "OpenFreeMap",
    href: "https://openfreemap.org/",
    gives: "Vector map tiles and styles for the base map.",
    terms: "No key and no registration. Attribution is required.",
  },
  {
    name: "Wikipedia and Wikidata",
    href: "https://www.mediawiki.org/wiki/Wikimedia_APIs",
    gives: "Article summaries, and structured facts such as population and languages.",
    terms:
      "No key. Wikipedia text is CC BY-SA, with a credit and a link to the page. Wikidata is CC0.",
  },
  {
    name: "OpenStreetMap, through Overpass",
    href: "https://wiki.openstreetmap.org/wiki/Overpass_API",
    gives: "Points of interest near a place, and hotel names and locations, with no prices.",
    terms:
      "No key. ODbL: Layover credits OpenStreetMap and its contributors. Its wiki says commercial use should use a self-hosted or paid server.",
  },
  {
    name: "Unsplash API",
    href: "https://unsplash.com/documentation",
    gives: "Destination photos.",
    terms:
      "Key and app registration. Layover credits Unsplash and the photographer, with a link to their profile.",
  },
  {
    name: "TfL Unified API",
    href: "https://api-portal.tfl.gov.uk/",
    gives: "London transport data, for getting to a London airport.",
    terms:
      "Free key. Credit “Powered by TfL Open Data” and “Contains OS data © Crown copyright and database rights 2016”.",
  },
  {
    name: "Tavily search API",
    href: "https://docs.tavily.com/documentation/api-reference/endpoint/search",
    gives: "Web search results, for travel questions Layover does not otherwise support.",
    terms:
      "API key, free plan of 1,000 credits a month. Its terms say queries may be used for AI training and outputs may be inaccurate.",
  },
  {
    name: "Python holidays library",
    href: "https://github.com/vacanza/holidays",
    gives: "Public holidays for 250 country codes.",
    terms: "Offline library, MIT licence.",
  },
];
