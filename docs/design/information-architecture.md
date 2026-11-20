# Information architecture: Layover

Status: approved by the owner on 19 Nov 2026 ("Approve (Recommended)", prompt window). Issue [#25](https://github.com/olaheavy-dev/layover/issues/25). Amended on 20 Nov 2026 for the boards ([#31](https://github.com/olaheavy-dev/layover/issues/31)): one section order for the itinerary-only trip, and one place for pinned answers. It follows the approved [design brief](brief.md) and the [journey spec](../superpowers/specs/2026-11-19-layover-journey-design.md).

The owner's answers here come from prompt windows on 19 Nov 2026. They are quoted as chosen. The agent's own proposals are marked **(agent's call)**.

## Site map

| Screen | URL | Who sees it |
|---|---|---|
| Welcome and new trip | `/` | Every visitor. The chat with an empty canvas |
| Working trip | `/trip/{trip_id}` | Only the traveller who has the link. Chat and canvas |
| Shared trip | `/s/{share_id}` | Anyone with the link. The canvas only, as a frozen, read-only copy |
| How Layover works | `/how-it-works` | Every visitor, and recruiters in particular |
| Link not found or expired | Shown at the requested URL | A visitor whose link is wrong, or whose link has passed its time limit |
| Limit reached | A state of `/` and `/trip/{trip_id}`, not a page | A visitor who has reached the limit per visitor or the cost cap (spec §5c) |

Both `trip_id` and `share_id` are long random values that are hard to guess. The owner chose "Working + shared links (Recommended)". A working link lets the traveller reload the page and continue planning. "Share trip" makes a separate frozen copy at its own link, so a friend cannot change the trip or use the traveller's limit.

What each link stores:

- Working trip: the chat and the trip state, on the server, so that a reload can continue the trip. This changes the agent's call in spec §8, item 2, which said that the chat transcript is not kept. The spec now has a note about this.
- Shared trip: the frozen canvas only, with no chat, as the spec says.
- How long each is kept is an open decision for the owner (see the open questions below).

## Navigation model

- Primary navigation: none in the usual sense. Layover has one main task, so the top bar holds the logo (a link to `/`), the trip name, "Share trip" and "How it works".
- Secondary navigation: the section index on the canvas. The owner chose "One scroll + section index (Recommended)". Sections stack in journey order, and a small sticky index jumps between them: Brief, Compare, the chosen place, Stay, Days, Booking. A section appears in the index only when it has content. The current section is bold and underlined, so colour is never the only cue.
- Utility navigation: "How it works", and "New trip", which starts again at `/` after a confirmation inside the page.
- Phone and tablet, below 1024 px **(agent's call)**: two tabs, Chat and Trip. The Trip tab shows a labelled badge, such as "3 new", when new content arrives. Once a trip exists, a trip strip sits above the message input on the Chat tab, with the place photo, the trip name, what is ready (for example "5 facts ready") and "View trip" (owner: "Trip strip + cards (Recommended)", 20 Nov 2026). The section index scrolls sideways at the top of the Trip tab.
- Desktop, from 1024 px **(agent's call)**: the chat column on the left and the canvas on the right. Both scroll on their own.

## Content hierarchy

### Welcome and new trip (`/`)

1. One question and the message input. The traveller can start typing at once.
2. Four example prompts, one for each main intent. One is for a traveller who does not know where to go (benchmark rule 9).
3. On the canvas: an illustration and one line about what will appear there. The illustration is chosen by the side-by-side test in the brief.
4. One short line about honesty: every figure shows its source and age.
5. A link to "How Layover works".

### Working trip (`/trip/{trip_id}`)

The chat column holds:

1. Messages, newest at the bottom.
2. One tool step line for each tool call.
3. Answers to side questions, inline.
4. The message input, always visible.

The canvas holds these sections, in journey order. Earlier sections fold to a short row when the traveller moves on:

1. Brief: the `brief_summary` widget, with Edit.
2. Compare: the `comparison_table` widget. After the pick, it folds to a row such as "Compared 3 places: you chose Lisbon".
3. The chosen place: photo and name first, then the key facts on the first screen (benchmark rule 10). The order is `fare_card`, `cost_estimate`, `advice_card`, `climate_chart`, `money`, then `sea_conditions`, `daylight`, `place_intro` and `map`.
4. Stay: the `hotel_list` widget. The chosen hotel becomes the base for the days.
5. Days: one `itinerary_day` widget for each day, built from the chosen hotel (spec §5, step 5).
6. Booking: the `booking_approval` widget, with the sandbox label.

Pinned answers: side answers that the traveller adds with "Add to trip" go at the end of the chosen place section, under the heading "Added from the chat". They have no index entry of their own, because they belong to the place **(agent's call, 20 Nov 2026, #31)**.

The order of the key facts is the agent's call. Cost and fares come first because the brief has a budget, and FCDO advice comes next because it can stop a trip.

### Shared trip (`/s/{share_id}`)

1. A header: the trip name, "Shared trip, as of" a date, and a line saying that fares and advice can change.
2. The same canvas sections as the working trip, read only, with no chat and no input.
3. Each fare and advice date stays as it was when the trip was shared, with its "as of" date.
4. A "Plan your own trip" link to `/`.

Budget and travellers on a shared trip: the "Share trip" step has a tick box "Include my budget and who's travelling", off by default. Without it, the shared copy leaves out the budget and traveller chips and every "under/over your budget" line (owner: "Ask when sharing", 20 Nov 2026).

### How Layover works (`/how-it-works`)

The owner chose "Yes, one page (Recommended)":

1. What Layover does, in two sentences.
2. The agent team as a diagram: the supervisor, the brief agent, the three research agents, the itinerary agent and booking ([0012](../decisions/0012-agent-team.md)).
3. The integrity rules in plain words ([0011](../decisions/0011-product-integrity-rules.md)).
4. The data sources, with their terms.
5. The evaluation score, with the size of its trip set, and the team against the single-agent baseline. Until scores exist, the page says "no evaluation results yet".
6. A link to the GitHub repository.

## User flows

### Plan a trip (`plan_trip`)

1. The traveller lands on `/` and types a request, or taps an example prompt.
2. Layover makes a working trip and moves to `/trip/{trip_id}`.
3. The brief agent asks for what is missing, then shows the `brief_summary` widget.
   - If the traveller edits a chip, the summary updates, and nothing is searched yet.
   - If the traveller confirms it, the comparison starts.
4. The Compare section shows three loading place cards. Each card fills in as its research agent finishes.
   - If one agent fails, its card shows the error state with "Try again". The other two cards stay.
   - If a place has too little data for a row, that row says "not known".
5. The traveller chooses a place, or swaps one for a place of their own.
6. The canvas adds the chosen place, then the Stay section.
   - If the traveller picks a hotel, the Days section is built from it.
   - If the traveller skips the hotel, the days start from the centre of the place and say so **(agent's call)**.
   - If the traveller changes the hotel later, the days are rebuilt from the new base **(agent's call)**.
7. The traveller opens "Try booking". If the brief has only a month, Layover first asks which dates to fly and never picks them **(agent's call, 20 Nov 2026)**. The `booking_approval` widget then waits for approval.
   - If the traveller approves, the sandbox order runs, and the widget shows the sandbox result.
   - If the traveller declines, nothing is ordered.
8. The traveller presses "Share trip" and copies the `/s/{share_id}` link.

### The first message

**(Agent's call)** Layover makes a working trip at the first message of any intent except `not_travel`, so that a reload keeps the chat. The canvas stays empty until a widget joins it. A `not_travel` message makes no trip. Every message counts towards the limit per visitor, because the limit protects model spending (spec §5c).

### A side question (`destination_facts`, `fares_and_transport`)

1. The traveller asks a question in the chat, for example "Do I need a visa for Turkey?".
2. The answer widget appears inline in the chat, with its source and age. The owner chose "Chat, with 'Add to trip' (Recommended)".
3. If the answer is about the trip's place, the widget offers "Add to trip". The widget then also appears in the canvas, under that place. If the trip has no place yet, the widget does not offer "Add to trip". If the canvas already holds that widget, the answer says "Already in your trip · View" instead, so nothing shows twice (owner, 20 Nov 2026).

### Itinerary only (`itinerary`)

1. The traveller asks for a plan for a named place, for example "Three days in Porto".
2. Layover makes a working trip with no Compare section. The canvas starts at the place, then Stay and Days, because the days start from the hotel, or from the centre if the traveller skips it (spec §5, step 5). The trip is named by the place alone until the traveller gives dates. The place section shows the introduction and the map at once; fares, costs, weather and daylight appear only after the traveller gives dates or an airport, which Layover offers in the chat (owner, 20 Nov 2026).

### A travel question that Layover does not support (`unsupported_travel`)

1. The chat shows a `web_results` widget with the label "from a web search, not checked by Layover", and says what Layover can do.
2. If the search finds nothing usable, the chat says "I can't help with that yet". It shows no widget.
3. A web result never offers "Add to trip" **(agent's call)**, because Layover has not checked it.

### Vague or unclear messages

1. A trip request with missing details: the brief agent asks for what is missing, one short question at a time, with quick-answer chips where the answers are few (for example the nearest airports). The canvas stays empty until the brief has fields.
2. A message whose meaning is unclear: Layover asks one clarifying question rather than guessing (spec §4).
3. A place name with more than one match, such as "Valencia": Layover asks "Which Valencia?" and offers the matches as choices. It never guesses (spec §4, `BRIEF-03`).
4. A side question before any place is chosen: the answer shows in the chat without "Add to trip".

### Not about travel (`not_travel`)

1. The chat declines politely in one line and gives an example of what Layover can do. It shows no widget.

### Limits and errors

- Limit reached: the input turns off and a notice explains the limit and when it resets. The canvas stays readable, and the traveller can still share the trip.
- Lost connection: the message keeps its text, and the chat offers "Try again".
- Link not found or expired: the page says that the link does not work, without saying whether a trip ever existed, and offers "Plan a new trip".

## Naming conventions

| Concept | Label in the interface | Notes |
|---|---|---|
| The whole plan | Trip | Never "itinerary" for the whole thing |
| The traveller's request after confirmation | Your trip, in the Brief section | "Brief" is the section name only |
| The three options | Places | Not "destinations" in copy, which is longer |
| The day plan | Days | Each day is "Day 1", "Day 2" and so on |
| A hotel chosen as the base | Where you're staying | |
| The sandbox booking | Try booking | Always with the label "Sandbox: no real booking or payment" |
| A cached fare | Cached, with its age | For example "Cached, 3 days old" (decision 0011, rule 2). This is the interface wording; "found 2 days ago" in decision 0004 is the earlier form. The label for each source is in the [brief](brief.md#source-labels) |
| Missing data | Not known | Never "N/A", "0", "TBC" or a dash |
| A web search answer | From a web search, not checked by Layover | Spec §5a wording |
| The shared copy | Shared trip | With "as of" and a date |
| FCDO advice | FCDO travel advice | Always with "updated" and a date. Never "safe" (decision 0011, rule 6) |

## Component reuse map

| Component | Used on | Differences |
|---|---|---|
| Top bar | Every screen | The shared trip has no "Share trip". "How it works" has no trip name |
| Canvas and its section index | Working trip, shared trip | Shared: read only, with no Edit, Choose or Add actions |
| Widgets | Chat (inline or compact), canvas, shared trip | On a phone, a widget that is also on the canvas shows in the chat as a compact card that opens it in the Trip tab. A widget that lives only in the chat (a side answer not added to the trip, or `web_results`) shows in full inline, so that it stays readable without the canvas |
| Source and age label | Every widget | The shared trip adds "as of" with the share date |
| Chat column | Welcome, working trip | Welcome shows the example prompts |
| Illustration | Welcome, empty states, errors, link not found | |

## Content growth

A trip grows to at most one comparison, one place, a few days, one hotel list and one booking, plus pinned answers. A long trip relies on the section index and on folded sections, so it needs no pages or search. The chat grows without limit during a session. It scrolls, and the canvas keeps what matters. The tool steps for one answer fold into one row, such as "4 checks · Show", and "Jump to latest" appears when the traveller scrolls up (owner: "Group steps + jump (Recommended)", 20 Nov 2026). Layover has no list of trips, because it has no accounts.

## URL strategy

- Pattern: short fixed paths (`/`, `/how-it-works`) and two kinds of link: `/trip/{trip_id}` and `/s/{share_id}`.
- Dynamic segments: only the two random values. The URL never contains a place name, a date, a budget or any traveller detail **(agent's call)**, so a link shows nothing about the trip if it is seen or logged.
- Query parameters: none.
- Section anchors: `#brief`, `#compare`, `#place`, `#stay`, `#days`, `#booking`, so the section index can link to a section.

## Open questions

- Some answers in the spec have no widget `kind` yet: local holidays and the time difference (spec §5, step 4, and the `destination_facts` route), fares "to anywhere" (a list of places, not one fare), and TfL journeys to the airport. The boards PR proposes how each is shown, and plan 1 fixes the schemas. Tracked in a `noticed` issue.

- How long working and shared links last. This was already open in spec §8, item 2, and it now applies to both kinds of link. A working link keeps the chat, so it holds more personal data than a shared link. The owner decides this before the build plan for trip links.
