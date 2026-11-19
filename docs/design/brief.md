# Design brief: Layover screens and widgets

Status: approved by the owner on 19 Nov 2026 ("Approve (Recommended)", prompt window). Issue [#25](https://github.com/olaheavy-dev/layover/issues/25). Journey spec: [2026-11-19-layover-journey-design.md](../superpowers/specs/2026-11-19-layover-journey-design.md), §5d.

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
- How the fonts are served is open. Google's font servers receive each visitor's IP address, and spec §5c treats an IP address as personal data. The OFL allows self-hosting. The agent recommends self-hosting, and the owner decides in the frontend plan.
- Colour: the Harbour palette in [tokens.css](tokens.css). It has blue-grey neutrals, one deep harbour blue for actions, one lighter blue for small markers, and one warning colour for problems only. The owner rejected a first round of palettes: "the colros make it look all iver the place and not something that was designed intentionally". The owner then said "Harbour feels like a very good start", saw three refined versions, and chose "Harbour as before". Warmth comes from the photos and the type, not from the interface colours.
- Source labels: Live and Cached use the normal text colours with different dot shapes. Fallback and Unavailable use the warning colour. Not known uses quiet italic text. Words always name the state, so colour never carries the meaning alone.
- Unavailable and Not known **(agent's call)**: "Unavailable" is one of the four labels in decision 0011, rule 2. It means that Layover asked the source and the source failed. "Not known" means that no source Layover uses has the value. Both follow rule 4: neither shows a zero or a favourable value.
- Highlight: the lighter blue is for small markers only. It is never text, and never the only cue. For example, the current section in the index is also bold.
- Photos: tall destination photos with the place name over them, from Unsplash, with the photographer credited on the photo ([data sources](../references/data-sources.md)). Text over a photo always sits on a dark gradient (a scrim) so that it meets the contrast target.
- Icons: Lucide. The owner chose "Lucide (Recommended)". The licence is ISC, and the icons that come from the Feather project are under MIT. Both allow commercial use when their notices are kept ([licence](https://github.com/lucide-icons/lucide/blob/main/LICENSE), checked 19 Nov 2026).
- Illustrations: for the welcome screen, empty states and error states. They must be world class and match warm editorial. The owner said: "Our iluustrations have to be wolrd class and match our choice", then chose "Side-by-side test (Recommended)". In the boards phase, the welcome screen is drawn twice. One version uses an illustration drawn for Layover, and the other uses a recoloured free-library illustration whose licence is checked first. The owner picks from the two.
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
- Phone: two tabs, Chat and Trip. When a widget appears in the canvas, the chat shows a compact card that opens it in the Trip tab.
- Shared trip page: the canvas on its own, without the chat, as a frozen copy with "as of" dates (spec §8, item 2).

## Component inventory

All components are new. "Widget" means a block that shows one tool result, tagged with its `kind` (spec §5d).

### Screen components

| Component | Notes |
|---|---|
| Top bar | Logo, trip name, "Share trip" |
| Chat and Trip tabs | Phone only |
| Chat message | Traveller and Layover messages, streamed |
| Tool step line | One short line for each tool call, for example "Checked fares for 3 places". It shows the agent work without filling the chat |
| Compact widget card in chat | Phone: opens the full widget in the Trip tab |
| Message input | With send, and a stop button while Layover is answering |
| Source and age label | Shared by every widget: the source name, a link, and Live, Cached (with its age), Fallback or Unavailable (decision 0011, rule 2) |
| Sample and sandbox label | Marks sandbox bookings and test data |
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

Every widget has these four states, and the boards draw each one (spec §5d):

1. Loading.
2. Empty.
3. Error.
4. Not known.

## Key interactions

- Brief: Layover restates the brief in a `brief_summary` widget. The traveller confirms it or edits a chip. An edit updates the summary before any search starts.
- Comparing: while the research agents work, the three place cards show a loading state, and each card fills in as its agent finishes. The chat shows one tool step line for each step.
- Choosing: "Choose Lisbon" moves the canvas to the trip summary for Lisbon. The comparison stays above it and folds to a short row, so the traveller can go back.
- Swapping a place: the traveller can replace one of the three places with a place of their own (spec §5, step 2, agent's call).
- Booking: the `booking_approval` widget pauses the flow. Nothing is ordered until the traveller presses Approve. The widget always carries the sandbox label.
- Sharing: "Share trip" gives a link to the frozen canvas. The page shows the "as of" date of every fare and every advice date.
- Stopping: the traveller can stop an answer while it streams.
- Motion **(agent's call)**: widgets settle into place with a short fade and rise. Loading uses a soft shimmer. When the traveller asks for reduced motion, changes are instant.

## Responsive behaviour

| Width | Behaviour |
|---|---|
| Phone (390 px wide is the reference) | Chat and Trip tabs. Widgets are one column. The comparison becomes cards in a horizontal scroll with snap points, and each card shows the same rows in the same order |
| Tablet (768 px) | Chat and Trip tabs, or chat as a narrow column, decided in the information architecture |
| Desktop (1024 px and 1440 px) | Chat column on the left and canvas on the right. The comparison shows three columns |

The boards are drawn at 390 px and 1440 px. The `visual-reviewer` checks 390, 768, 1024 and 1440 px.

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
- Accounts, sign-in and saved trips other than shared links.
- Real bookings and payments. The booking is a sandbox.
- Hotel prices.
- Marketing pages other than the welcome screen.
- Native mobile apps. Layover is a responsive website.
