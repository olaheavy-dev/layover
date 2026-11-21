# Design brief: Layover screens and widgets

Status: approved by the owner on 19 Nov 2026 ("Approve (Recommended)", prompt window). Issue [#25](https://github.com/olaheavy-dev/layover/issues/25). Amended on 20 Nov 2026 for the boards ([#31](https://github.com/olaheavy-dev/layover/issues/31)): widget states and source labels, images, sample content, the logo and the trip name, and how the fonts are served for the boards. Journey spec: [2026-11-19-layover-journey-design.md](../superpowers/specs/2026-11-19-layover-journey-design.md), §5d.

The owner's answers in this brief come from prompt windows on 19 Nov 2026. They are quoted as chosen. The agent's own proposals are marked **(agent's call)**, and the owner can change them.

## Problem

A UK holidaymaker wants a break but has not chosen where to go. Today they open many tabs: flight search, weather sites, travel guides and government advice. Each tab shows a different piece, and the prices are often out of date or pushed with sales tricks. The traveller cannot tell which figures are real, how old they are, or what is missing. Planning feels like work, not like the start of a holiday.

## Solution

The traveller describes the trip they want in a chat. Layover answers in the chat, and at the same time it builds the trip on a canvas beside the chat. The canvas shows the confirmed brief, three places to compare, and then the chosen place with fares, weather, money, advice, a day-by-day plan and a sandbox booking. Every figure shows where it came from and how old it is. When Layover does not know something, it says so plainly. The screens feel like a travel magazine: large photos and confident type in a calm interface. The facts underneath stay clean and easy to check.

## Experience principles

1. Inspiration on top, evidence underneath. Photos, place names and type carry the warmth. Figures sit in calm, structured cards, and each card shows its source and age. Decoration never hides a source.
2. Honest gaps over smooth guesses. A "not known" state is a designed state with its own look and words, not an error. It never shows a zero, a dash that reads as zero, or a favourable value.
3. The conversation drives, the canvas keeps. The chat is where the traveller talks. The canvas is where the trip stays, in order, and the shared trip page reuses it.

## Aesthetic direction

- Philosophy: warm editorial. The owner chose "C. Warm editorial (Recommended)" after a comparison of three styles drawn on the same trip screen. The comparison page was a private working page, so it is not linked here.
- Tone: warm and inspiring. The owner chose "Warm and inspiring" over "Calm and trustworthy", which the agent recommended.
- Type: Source Serif 4 for place names and headings, and Source Sans 3 for body text and figures. Both are under the SIL Open Font License. The owner compared three pairings on the trip screen and asked for research on the fonts that the benchmark sites use. The owner then chose "Source Serif 4 + Source Sans 3". The agent recommended Fraunces and DM Sans.
- Font research: the agent observed the fonts in each site's page source on 19 Nov 2026. Airbnb uses its own font, Airbnb Cereal. Google Flights uses Google Sans and Roboto. Lonely Planet uses paid fonts (ABC Arizona Flare, ABC Monument Grotesk and American Grotesk). Mindtrip uses Inter. Layla uses the fonts of the device. Skyscanner refused the request, so its font, Skyscanner Relative, comes from its public design-system code ([backpack-ios](https://github.com/Skyscanner/backpack-ios)).
- How the fonts are served: Google's font servers receive each visitor's IP address, and spec §5c treats an IP address as personal data. The OFL allows self-hosting. For the boards, the owner chose "Commit font files (Recommended)" on 20 Nov 2026: the WOFF2 files and their OFL text are committed and registered in `docs/assets/README.md`. The frontend plan reuses them unless it records a reason not to.
- Colour: the Harbour palette in [tokens.css](tokens.css). It has blue-grey neutrals, one deep harbour blue for actions, one lighter blue for small markers, and one warning colour for problems only. The owner rejected a first round of palettes: "the colros make it look all iver the place and not something that was designed intentionally". The owner then said "Harbour feels like a very good start", saw three refined versions, and chose "Harbour as before". Warmth comes from the photos and the type, not from the interface colours.
- Source labels: Live and Cached use the normal text colours with different dot shapes. Fallback and Unavailable use the warning colour. Not known uses quiet italic text. Words always name the state, so colour never carries the meaning alone.
- Unavailable and Not known **(agent's call)**: "Unavailable" is one of the four labels in decision 0011, rule 2. It means that Layover asked the source and the source failed. "Not known" means that no source Layover uses has the value. Both follow rule 4: neither shows a zero or a favourable value.
- Spark (owner: "E: combined (Recommended)", 20 Nov 2026, after comparing six whole-screen versions of the Lisbon screen in both themes): a richer "harbour at night" dark theme (deep navy surfaces, a soft glow from the place photo behind the place header, slightly lifted cards); small photos of the compared places in the folded Compare row and a photo beside the place introduction; editorial type (large serif figures, an italic place line, a small heading above each card title, the place introduction as a pull-quote); and two small line drawings in the highlight blue (a tile band under the place photo, a sun over water in the daylight card). The palette stays one colour family. The owner said: "the dark looks to plain and also i feel like both themes still needs some spark".
- Highlight: the lighter blue is for small markers only. It is never text, and never the only cue. For example, the current section in the index is also bold.
- Photos: tall destination photos with the place name over them, from Unsplash, with the photographer credited on the photo ([data sources](../references/data-sources.md)). Text over a photo always sits on a dark gradient (a scrim) so that it meets the contrast target, in `--color-text-on-photo`, which stays white in both themes. More in "Images" below.
- Icons: Lucide. The owner chose "Lucide (Recommended)". The licence is ISC, and the icons that come from the Feather project are under MIT. Both allow commercial use when their notices are kept ([licence](https://github.com/lucide-icons/lucide/blob/main/LICENSE), checked 19 Nov 2026).
- Illustrations: for the welcome screen, empty states and error states. They must be world class and match warm editorial. The owner said: "Our iluustrations have to be wolrd class and match our choice", then chose "Side-by-side test (Recommended)". On 20 Nov 2026, after the agent compared homescout's approach, the owner chose "Two own styles + library (Recommended)": the welcome screen is drawn three times, with an isometric illustration drawn for Layover (as homescout uses), an editorial line drawing in a travel-poster style drawn for Layover, and a recoloured free-library illustration. The agent proposes one or two libraries whose licence allows changes and commercial use without credit, with the licence text and the date checked, and the owner picks the library (owner: "Own SVG vs free library (Recommended)"). On 20 Nov 2026, after the logo was chosen, the owner set the illustrations' feel to match it: friendly, playful, classic travel ("Match the logo (Recommended)"). After the owner picks a style, a one-page style guide (shapes, line, light and colour from the tokens) comes before any more drawings, so that every illustration matches. Chosen on 20 Nov 2026: isometric scenes around the logo's suitcase (owner: "1: Isometric (Recommended)"); the free library was checked (Open Doodles, CC0) and not used. The rules are in the [illustration guide](boards/illustration-guide.html).
- Reference points: the benchmark below.
- Anti-references: the owner chose these three:
  - Pushy booking sites: countdown timers, "only 2 left", crossed-out prices and deal banners.
  - Generic AI chatbots: walls of text with no structure.
  - Cluttered travel portals: adverts, dense menus and many filters.

## Benchmark

The benchmark studies four kinds of product. The owner chose all four:

- AI trip planners.
- Flight and travel search.
- Editorial travel guides.
- Products known for their craft.

Each observation cites its source. The agent's research checked all sources on 19 Nov 2026 from public pages, without logging in. Some sources are reviews by third parties, and the table says so.

| Product | Does well | Avoid |
|---|---|---|
| Mindtrip (AI planner) | The plan sits beside a map and updates as the traveller picks items ([Afar](https://www.afar.com/magazine/we-tested-ai-travel-planning-apps-here-are-the-3-that-actually-worked), review). The assistant says why each pick fits ([mindtrip.ai](https://mindtrip.ai/)) | Afar found confident errors, for example dates said to be in the past. The home page shows crossed-out prices with a "Price drop" label and no source or age ([mindtrip.ai](https://mindtrip.ai/)) |
| Layla (AI planner) | It opens with one prompt and preset prompts, including "Not sure where to go yet". Prices say "from" and "p.p." and link to "About this price" ([layla.ai](https://layla.ai/)) | Discount badges such as "-53%" and crossed-out prices ([layla.ai](https://layla.ai/)) |
| Google AI Mode Canvas (AI planner) | A day-by-day plan in a side panel next to the chat, with flights, hotels and maps beside the plan. It is the closest match to Layover's layout ([engine.com](https://engine.com/blog/inside-googles-travel-ai-upgrade-ai-mode-canvas-conversational-flight-deals-and-review-summaries-in-maps), review). Afar found Gemini's links the most accurate of the tools it tested | The review says it is not clear where each claim comes from. Gemini's answers in Afar's test were text only |
| Google Flights (search) | It labels current prices in words, "low, typical or high compared to past averages for the same route" ([Google blog](https://blog.google/products/travel/google-flights-find-deals/)) | The sources did not confirm a problem |
| Skyscanner (search) | Its partner documentation says that cached prices are kept for up to 15 days and "serve as a useful indicator for pricing trends on a given route" ([partner help](https://skyscannerpartnersupport.zendesk.com/hc/en-us/articles/4686923517981-Why-does-the-Browse-Cache-API-not-match-that-of-the-live-pricing)) | The same page says that "for less popular routes the cache can be out of date and may not have any results" |
| Lonely Planet (editorial guide) | The March 2026 refresh aims to balance inspiration with practical use (paraphrased from [Breaking Travel News](https://www.breakingtravelnews.com/news/article/lonely-planet-unveils-new-app-and-bookable-experiences-as-it-evolves-to-a-d/)) | A 2019 review found practical facts hard to find ([Nomadic Matt](https://www.nomadicmatt.com/travel-blogs/lonely-planet/), from before the refresh) |
| Airbnb (craft) | It shows the total price, and before booking, "guests can still view a full price breakdown" of fees, discounts and taxes ([Airbnb news](https://news.airbnb.com/airbnb-is-introducing-total-price-display-and-updating-guest-checkout)) | The total price became standard for guests worldwide only on 21 April 2025 ([Airbnb news](https://news.airbnb.com/total-price-display-is-now-standard-globally)). Layover shows the total from the start |
| Linear (craft) | It makes its light and dark themes from three inputs: base colour, accent and contrast. Before, it set 98 variables by hand. It tests each design choice in every view ([Linear](https://linear.app/now/how-we-redesigned-the-linear-ui)) | Its quiet, dense look suits a work tool. Layover takes the method, not the look **(agent's call)** |

### The bar for Layover

The boards and the design review test these rules:

1. Every price shows its label and age as visible text next to the figure, for example "Cached, 2 days old". The label is never only in a tooltip. Estimates are called estimates.
2. A price judgement uses words, with colour as an extra only.
3. Layover makes a "cheaper than usual" claim only when it can name the comparison: the period and the data source. Layover never shows crossed-out prices or discount badges.
4. A total includes every known cost and lists the unknown parts as "not known". The breakdown is one tap away.
5. When a route or a place has too little data, the widget says "not known" or "too little data". It never shows an old figure as current, and it never shows zero.
6. On desktop, the canvas keeps fares, stay, money and advice beside the day plan, with no tabs to switch between.
7. Every fact in the chat or on the canvas has a visible source link. The model never gives opening hours, travel times or entry rules without one.
8. Chat replies stay short. Detail goes into widgets, and links appear without the traveller asking.
9. The welcome screen offers a few example prompts, including one for a traveller who is not sure where to go. It has one main action.
10. A place leads with its photo and name, but its key facts sit on the first screen of the canvas.
11. One set of tokens makes both themes, with contrast as a setting. Every widget is checked in both themes and at phone and desktop widths.
12. Loading states are placeholder shapes in the form of the widget. Motion respects the traveller's reduced-motion setting.

### Not checked

The research could not confirm these points:

- The current Lonely Planet destination page. The site refused the request.
- How Lonely Planet sizes city pages against country pages. The only source found was a designer's Dribbble post from about 2015, which may be a concept, so the brief does not use it.
- Google Flights' price graph and its use of colour. The help page was not read in full.
- Airbnb's design system and its motion library. Those pages did not load.
- The views inside Mindtrip and Layla, because they need an account.
- Whether Google AI Mode Canvas is available in the UK. The source says US desktop only.

## Existing patterns

The repository holds documents and their checks only, so no components, tokens or fonts existed before this brief. This brief starts the visual system. The Next.js layer arrives when frontend work starts ([0006](../decisions/0006-nextjs-frontend.md), [0010](../decisions/0010-repository-and-stages.md)).

## Layout

The owner chose "1. Chat + trip canvas (Recommended)".

- Desktop: the chat sits in a column on the left, and the trip canvas fills the right.
- Phone: two tabs, Chat and Trip. When a widget appears in the canvas, the chat shows a compact card that opens it in the Trip tab. A widget that lives only in the chat, such as a side answer or web results, shows in full in the chat.
- Shared trip page: the canvas on its own, without the chat, as a frozen copy with "as of" dates (spec §8, item 2). The "Share trip" step has a tick box "Include my budget and who's travelling", off by default; without it, the shared copy leaves out the budget and traveller chips and every "under/over your budget" line (owner: "Ask when sharing", 20 Nov 2026).

## Component inventory

All components are new. "Widget" means a block that shows one tool result, tagged with its `kind` (spec §5d).

### Screen components

| Component | Notes |
|---|---|
| Top bar | Logo, trip name, "Share trip", "How it works" and "New trip" ([information architecture](information-architecture.md#navigation-model)) |
| Chat and Trip tabs | Phone only |
| Chat message | Traveller and Layover messages, streamed |
| Tool step line | One short line for each tool call, for example "Checked fares for 3 places". The steps for one answer fold into one row ("4 checks · Show") that opens on tap, so a long chat is not a list of steps |
| Jump to latest | Appears in the chat when the traveller has scrolled up |
| Trip strip | Phone, Chat tab: a slim bar above the message input once a trip exists, with the place photo, the trip name, what is ready and "View trip" |
| Compact widget card in chat | Phone: opens the full widget in the Trip tab |
| Message input | With send, and a stop button while Layover is answering |
| Source and age label | Shared by every widget: the source name, a link, and Live, Cached (with its age), Fallback or Unavailable (decision 0011, rule 2) |
| Sample and sandbox label | Marks sandbox bookings and test data. Every board carries "Sample data, not real" (see "Sample content on the boards") |
| Buttons | Primary, secondary and link |
| Place photo with credit | Unsplash credit on the photo; a designed fallback when no photo exists |
| Illustration | Welcome, empty and error states |
| Welcome screen | The first screen for a new visitor: what Layover does, example prompts, and an empty canvas |
| Limit reached notice | Shown when a visitor reaches the trip limit or the cost cap (spec §5c) |

### Widgets (one for each `kind`)

| `kind` | What it shows |
|---|---|
| `brief_summary` | The confirmed brief as chips (small labelled tags, one for each field), with an Edit action |
| `comparison_table` | Three places side by side: photo, fares, weather, cost estimate, "not known" rows, and a Choose action. On a phone, the places are cards that the traveller swipes or scrolls |
| `fare_card` | A cached fare range, its age, and a link to check the live price on Aviasales |
| `climate_chart` | Typical temperature and rain for the month |
| `sea_conditions` | Sea temperature, where relevant |
| `daylight` | Sunrise, sunset and day length |
| `money` | The exchange rate, with its date and source |
| `advice_card` | A link to the FCDO page and its update date. It never says that a place is "safe" (decision 0011, rule 6) |
| `place_intro` | A short introduction with its Wikivoyage or Wikipedia source |
| `map` | OpenFreeMap tiles with places and the chosen hotel |
| `itinerary_day` | One day's stops, each linked to its source, with notes where data is missing |
| `hotel_list` | OpenStreetMap hotels with names and locations and no prices. The traveller picks one as the base |
| `cost_estimate` | Flights, stay and meals against the budget, with the listing count and page date. Unknown parts say "not known" |
| `booking_approval` | The sandbox booking summary that waits for the traveller's approval before any order |
| `web_results` | Short quotes with links and the retrieval date, labelled "from a web search, not checked by Layover" |
| `not_known` | A standalone "not known" answer that says what is missing and why |

### Widget states

Issue [#31](https://github.com/olaheavy-dev/layover/issues/31). The agent drafted this table and the source labels, and the owner approved them on 20 Nov 2026 ("Approve (Recommended)", prompt window). The boards draw every cell that is not "not applicable", and the reviewers test the boards against it.

The states:

- **Filled:** the widget with its data, its source and its label.
- **Loading:** placeholder shapes in the form of the widget while its tool runs (benchmark rule 12).
- **Empty:** the source answered, but it has no items for a list widget. For example, OpenStreetMap has no hotels tagged near the place. The widget says what it looked for and what the traveller can do next. A widget that shows one value has no Empty state: a missing value is "Not known".
- **Error:** Layover asked the source and the source failed. The label says "Unavailable", the widget says what could not be checked, and it offers "Try again" where a retry can help. An error never shows a zero, an old figure as current, or a favourable value (decision 0011, rule 4).
- **Not known:** no source that Layover uses has the value. It is quiet italic text with an empty dot, and it says what is missing (brief, "Unavailable and Not known"). It can be the whole widget or one row inside it.
- **Fallback:** Layover used a second recorded source because the first had no data. The label says "Fallback" and names the source. Only `place_intro` has a second source today (Wikipedia when Wikivoyage has no guide). A new fallback needs its own row in [data sources](../references/data-sources.md) first.

| `kind` | Loading | Empty | Error (Unavailable) | Not known | Other states the boards draw |
|---|---|---|---|---|---|
| `brief_summary` | Chip shapes while the brief agent writes | Not applicable: the widget appears only when the brief has fields, and the brief agent asks for missing fields in the chat | Not applicable: no outside source. A failed reply is the chat's "Try again" | Not applicable: a missing field is asked for, never guessed | Waiting for confirmation; editing a chip; confirmed; folded row |
| `comparison_table` | Three card shapes; each fills in when its research agent finishes | No place fits the brief: it says which part of the brief rules places out, and offers "Edit brief" | One card failed, with "Try again"; the other two cards stay | A row in a card says "Not known" | A place swapped for the traveller's own; chosen, folded to "Compared 3 places: you chose Lisbon"; phone cards in a horizontal scroll |
| `fare_card` | Card shape | Not applicable: no cached fare for the route and month is "Not known" (bar rule 5) | Travelpayouts failed: no figure, "Try again", and the plain Aviasales search link | No cached fare for this route and month; the Aviasales link is still offered | Cached with its age ("Cached, 3 days old"); an old fare shows its age clearly (the plan sets when a fare is too old to show) |
| `climate_chart` | Chart frame | Not applicable | Open-Meteo failed | One series (temperature or rain) is not known; the other still shows | The table alternative with the same figures |
| `sea_conditions` | Card shape | Not applicable | Open-Meteo Marine failed | No sea temperature for this coast | Inland place: the widget is not shown at all, with no empty card |
| `daylight` | Card shape | Not applicable | sunrise-sunset.org failed | No times for this place and date | — |
| `money` | Card shape | Not applicable | Frankfurter failed | The currency is not in the European Central Bank's reference rates | A conversion of an amount ("£500 is about …"), worked out by tested code |
| `advice_card` | Card shape | Not applicable | The FCDO page could not be read: the link to it still shows, with "Layover could not read it just now" | No FCDO page for this place: a link to the FCDO travel advice index | Never says "safe" (rule 6) |
| `place_intro` | Text lines | Not applicable | Wikivoyage failed | Neither Wikivoyage nor Wikipedia has a page | Fallback: the Wikipedia introduction, labelled "Fallback: Wikipedia" |
| `map` | Map frame | Not applicable | The map could not load: the places show as a list with links, so the map never holds anything the list does not | Not applicable | The place centre only, before a hotel or stops exist |
| `itinerary_day` | Stop shapes | Too few sourced places for this day: it says so and suggests a wider area | Overpass or Wikivoyage failed, with "Try again" | One stop's opening times are not known | Days start from the centre ("Days start from the centre of Lisbon") when no hotel is chosen; rebuilt after a hotel change |
| `hotel_list` | List row shapes | No hotels tagged near the place: it says so, and the days start from the centre | Overpass failed, with "Try again" and "Skip" | Stars or website not tagged: "Not known" in that row | One hotel chosen; skipped; changed (the days rebuild) |
| `cost_estimate` | Row shapes | Not applicable | A source failed: that line says "Unavailable", and the total says it is partial. A partial total never looks complete | Lines that no source covers (local transport, activities) say "Not known" | Over budget, in words ("about £X over your £800 budget"); estimates with their listing count and page date |
| `booking_approval` | Sandbox search running | No sandbox offer for the route and date | The sandbox failed | Not applicable | Waiting for approval; approved, with the sandbox result; declined (nothing ordered); the price changed at the price check, and Layover asks again; flights only, if the Nuitee sandbox fails or the account is closed. Always with "Sandbox: no real booking or payment" |
| `web_results` | The tool step line only | Not applicable: no usable result is the chat line "I can't help with that yet", with no widget (information architecture) | The search failed: the same chat line, with "Try again" | Not applicable | Always labelled "From a web search, not checked by Layover", with the retrieval date; never "Add to trip" |
| `not_known` | Not applicable: Layover writes it without an outside call | Not applicable | Not applicable | It is the Not known state: it says what is missing, why, and what Layover can do instead | — |
| `public_holidays` | Row shapes | No public holidays in the trip month: it says so | The holidays library could not run | No country for this place | National holidays only: local or regional holidays may be missing, and the card says so. Cached, with the release date of the library |
| `time_difference` | Card shape | Not applicable | The time zone data could not be read | No time zone for this place | Same time as the UK; an hour or more ahead or behind. When the dates are not set, it uses the middle of the month and says so. Cached, with the release date of the time zone database |
| `fare_list` | Row shapes | No cached fares from this airport for the month: it says what Layover looked for | Travelpayouts failed: no figures, "Try again" | A row says "Not known" when it has no cached fare, never a zero | Cached with its age on each row, lowest first |
| `transport_route` | Step shapes | Not applicable | TfL failed, with "Try again" | No journey found | Live. When the dates are not set, it plans for the middle of the month and says so |

On a phone, every widget that is also on the canvas has a compact card in the chat: the kind's icon, its title and its label, and a tap opens it in the Trip tab.

### Source labels

The label each source carries (agent's draft, approved with the table). Live means fetched for this answer. Cached means stored earlier, by Layover or by the provider, and it always shows the age. On the shared trip, every label adds "as of" and the share date.

How often labels show (owner: "One per card, prices always (Recommended)", 20 Nov 2026): a widget shows its label once, in its source line, when all its figures share one source and age. A row or figure gets its own label only when its source or age differs from the rest of the widget. A price always has its label beside it (bar rule 1). "Live" is drawn more quietly than Cached, Fallback and Unavailable, but it is still written in words. This meets decision 0011, rule 2, because every outside value still has a visible label.

| Source | Label |
|---|---|
| Travelpayouts fares | Cached, with the fare's age ("Cached, 3 days old") |
| Frankfurter exchange rate | Live, with the date of the European Central Bank rate |
| FCDO travel advice (from Layover's index, [0008](../decisions/0008-retrieval-no-knowledge-graph.md)) | Cached, with the age of Layover's copy, and always the FCDO's own "updated" date |
| Wikivoyage (from Layover's index) | Cached, with the age of Layover's copy and the page's edit date |
| Wikipedia | Live, or "Fallback: Wikipedia" when it stands in for Wikivoyage |
| Open-Meteo (climate and marine) | Live, with the period that the averages cover |
| sunrise-sunset.org | Live |
| OpenStreetMap through Overpass (hotels and stops) | Live |
| Foursquare Open Source Places (only if it is added: spec §6 keeps it waiting unless Overpass proves too slow) | Cached, with the dataset's release date |
| Duffel and Nuitee sandboxes | Live, and always the sandbox label |
| Holidays library and IANA time-zone database (offline, proposed for #26) | Cached, with the data's release date (owner, 20 Nov 2026) |
| Tavily web search | Its own label: "From a web search, not checked by Layover", with the retrieval date. Never Live or Cached |

Map tiles (OpenFreeMap, with the OpenStreetMap credit) and photos (Unsplash, with the photographer) carry a credit, not a label: they show no figure or fact. A new source gets its row here and in [data sources](../references/data-sources.md) before it is used.

## Images

Owner's answers on 20 Nov 2026, after the agent compared homescout's image direction. Each image is recorded in `docs/assets/README.md` with its source and terms before it is committed (AGENTS.md), and `make check` fails on an image under `docs/` that is not in the register (`tools/check_boards.py`).

| Role | Where | Source | Rules |
|---|---|---|---|
| Place photos | Place cards, the chosen place, the shared trip | Unsplash, real photos of the named place (owner: "Download and register (Recommended)"): three or four, downloaded, resized under 1 MB each, with the photographer, the link and the licence in the register. The Unsplash licence is read again before the first download | A photo shows the place it names. When no photo exists, the designed fallback shows |
| Mood scenes | Welcome and "How Layover works" only | Made by the owner with ChatGPT (OpenAI) from prompts the agent writes, as in homescout (owner: "AI for mood scenes only") | Never a named or recognisable place, never on a place card or next to a result, so no picture suggests a real place. No readable signs, brand logos or faces. The alt text starts "Illustrative photo:", and the page footer says "Some photos on this site are AI-generated illustrations". OpenAI's sharing and publication policy is read again by hand before Layover goes public |
| Illustrations | Welcome, empty states, errors, link not found | The style the owner picks in the side-by-side test | Decorative, with a text alternative, and never carrying information that the text does not give (as in homescout) |
| Sample map | The `map` widget on the boards | Drawn in the illustration style, with no map tiles | Marked as sample. The real `map` widget uses OpenFreeMap tiles |

**Why AI only for mood scenes** **(agent's reason)**: a generated picture of Lisbon would be an invented fact about a real place (decision 0011, rule 1). A generated suitcase by a window is not.

## Sample content on the boards

Owner: "Marked samples, one file (Recommended)", 20 Nov 2026.

- Every board page shows the label "Sample data, not real". `make check` fails on a board page without it.
- Every fare, price, total, rate, date and place fact on a board comes from [boards/sample-data.md](boards/sample-data.md). A board never has a figure that is not in that file.
- Links go to real pages (the FCDO page for the country, Aviasales search), so the reviewers can check where each link goes. No "updated" date or age on a board is presented as real.
- The "How Layover works" board shows "no evaluation results yet", because no scores exist.
- The limit-reached notice uses wording that needs no figure, because the limits are not set yet (spec §5c).

## Logo and trip name

- Logo: the owner chose "Design a logo mark now" over the agent's text wordmark (20 Nov 2026). The boards PR shows two or three marks inside the real top bar, at both widths and in both themes, and the owner picks one. The mark is recorded in `docs/assets/README.md`. Chosen on 20 Nov 2026 after five rounds of whole-screen samples: **S3, a friendly little suitcase character** (a tilted suitcase with a handle, straps, a smile, wheels and a sun sticker) next to a rounded, hand-drawn "Layover" in the brand blues; the logo's own lettering is used in the logo only, and the rest of the interface keeps Source Serif 4 and Source Sans 3 (owner: "S3: Suitcase character", after asking for "Friendly and playful, Classic travel").
- Trip name **(agent's call)**: made from the brief, as the place and the month ("Lisbon, May"). Before a place is chosen, it is the month and the feel ("Warm break, May"). Before the brief has fields, it is "New trip". An itinerary-only trip with no dates is named by the place alone ("Lisbon"), then by place and month once dates are given (owner, 20 Nov 2026). The name never holds the budget or the number of travellers, because a shared link shows it.

## Key interactions

- Brief: Layover restates the brief in a `brief_summary` widget. The traveller confirms it or edits a chip. An edit updates the summary before any search starts.
- Comparing: while the research agents work, the three place cards show a loading state, and each card fills in as its agent finishes. The chat shows one tool step line for each step.
- Choosing: "Choose Lisbon" moves the canvas to the trip summary for Lisbon. The comparison stays above it and folds to a short row, so the traveller can go back.
- Swapping a place: the traveller can replace one of the three places with a place of their own (spec §5, step 2, agent's call).
- Booking: the `booking_approval` widget pauses the flow. Nothing is ordered until the traveller presses Approve. The widget always carries the sandbox label.
- Sharing: "Share trip" gives a link to the frozen canvas. The page shows the "as of" date of every fare and every advice date.
- Stopping: the traveller can stop an answer while it streams.
- Dialogs (for the build): when a dialog opens, focus moves to the least destructive action (Cancel). Focus stays inside the dialog until it closes. Esc closes it. Focus returns to the button that opened it. The page behind is inert (not clickable, not readable by assistive technology). The dialog's body text is linked to it with `aria-describedby`.
- Motion **(agent's call)**: widgets settle into place with a short fade and rise. Loading uses a soft shimmer. When the traveller asks for reduced motion, changes are instant.

## Responsive behaviour

| Width | Behaviour |
|---|---|
| Phone (390 px wide is the reference) | Chat and Trip tabs. Widgets are one column. The comparison becomes cards in a horizontal scroll with snap points, and each card shows the same rows in the same order |
| Tablet (768 px) | Chat and Trip tabs, or chat as a narrow column, decided in the information architecture |
| Desktop (1024 px and 1440 px) | Chat column on the left and canvas on the right. The comparison shows three columns |

The boards are drawn at 390 px and 1440 px. Each board page shows one theme, with a switch between light and dark, because the dark tokens apply to the whole page. The `visual-reviewer` checks 390, 768, 1024 and 1440 px.

## Accessibility requirements

The owner chose "WCAG 2.2 AA (Recommended)" ([WCAG 2.2](https://www.w3.org/TR/WCAG22/)):

- Text contrast is at least 4.5:1, or 3:1 for large text ([1.4.3](https://www.w3.org/TR/WCAG22/#contrast-minimum)). The tokens are tested for this in both themes. Text over photos always sits on a scrim.
- Icons and control borders have a contrast of at least 3:1 ([1.4.11](https://www.w3.org/TR/WCAG22/#non-text-contrast)).
- Every control works with a keyboard and has a visible focus state ([2.4.7](https://www.w3.org/TR/WCAG22/#focus-visible)) that other content does not hide ([2.4.11](https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum)).
- Targets are at least 24 by 24 CSS pixels ([2.5.8](https://www.w3.org/TR/WCAG22/#target-size-minimum)).
- Streamed chat answers go into a polite live region, so that a screen reader reads new text without interrupting the traveller.
- Charts have a text or table alternative that gives the same figures.
- Colour never carries meaning alone. The Live, Cached, Fallback and Unavailable labels use words as well as colour.

## Out of scope

- Building the app. This brief and the boards are designs only. Code starts after the Design gate (decision 0010).
- Accounts, sign-in and saved trips other than working and shared links.
- Real bookings and payments. The booking is a sandbox.
- Hotel prices.
- Marketing pages other than the welcome screen.
- Native mobile apps. Layover is a responsive website.
