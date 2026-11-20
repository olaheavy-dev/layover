# Build tasks: Layover boards

Issue: [#28](https://github.com/olaheavy-dev/layover/issues/28). Made from the [design brief](../brief.md), the [information architecture](../information-architecture.md), the [tokens](../tokens.css) and the [sample data](sample-data.md) on 20 Nov 2026, with the `brief-to-tasks` skill.

Style: warm editorial (brief, "Aesthetic direction"). Photos and type carry the warmth; figures sit in calm cards with their source and age. The first build task sets this look, so the owner can check it before the other boards are built.

## How the boards work

- **Screens and board pages.** Each screen state is one HTML file in `screens/` that fills the browser window, like the real app would. A board page in this folder shows that screen twice, in frames 390 px and 1440 px wide, with a light and dark switch. A board page can show several states of the same screen, one above the other.
- **Shared files.** `boards.css` holds the components (top bar, buttons, chips, source label, chat, cards, section index), built only from `var(--…)` tokens. `board.css` and `board.js` hold the board page itself (frames, theme switch). Every page links `../tokens.css`, so a token change reaches every board.
- **Rules from `make check`** (`tools/check_boards.py`): no literal colours, never the word "safe", no local paths, nothing loaded from outside the repository, the label "Sample data, not real" on every page, and every image, font and illustration registered in `docs/assets/README.md` first.
- **Figures** come only from [sample-data.md](sample-data.md). A figure that is not there is added there first, with its working.

Already in place, reused as they are: `tokens.css` (both themes), `sample-data.md`, `tools/check_boards.py` and `tools/check_contrast.py`. Everything else is new: no components exist yet (brief, "Existing patterns").

## Foundation

- [x] **Asset register and files**: create `docs/assets/README.md` first; then commit the Source Serif 4 and Source Sans 3 WOFF2 files with their OFL text, the Lucide icons used (copied in as SVG) with the ISC and MIT notices, and three Unsplash photos (Lisbon, Valencia, Valletta), each under 1 MB, after reading the Unsplash licence again. Done when `make check` passes with every file registered with its source, terms and date checked. _New._
- [ ] **Board shell and the chosen place, Lisbon (first look)**: the board page (two frames, theme switch, sample label), `boards.css` with the top bar, section index, chat column, message input, source label, buttons and widget card, and one complete screen: the working trip on the chosen place, with the comparison folded and the key facts (`fare_card`, `cost_estimate`, `advice_card`, `climate_chart`, `money`) on the first screen. Done when the owner has seen it in both themes at both widths. _New. Sets the look for everything after it._ **Owner checkpoint.**
- [ ] **Logo marks**: two or three marks drawn as SVG, each shown in the real top bar at both widths and in both themes on one board. The owner picks one in a prompt window; the chosen mark is registered and used everywhere after. _Depends on: board shell._ **Owner choice.**
- [ ] **Illustration test**: the welcome screen drawn three times: an isometric illustration drawn for Layover, an editorial travel-poster line drawing drawn for Layover, and a recoloured free-library illustration. With it, one or two proposed libraries whose licence allows changes and commercial use without credit, each with its licence text and the date checked. The owner picks the style and the library in a prompt window. Then a one-page style guide (shapes, line, light, colours from the tokens). _Depends on: board shell._ **Owner choice.**

## Widget gallery

Every `kind` with every state in the [state table](../brief.md#widget-states) that is not "not applicable", plus the extra states, at canvas width and phone width, in both themes.

- [ ] **Place widgets**: `fare_card`, `cost_estimate`, `advice_card`, `climate_chart` (with its table alternative), `money`, `sea_conditions`, `daylight`, `place_intro` (with Fallback) and `map` (the drawn sample map). Covers: filled, loading, error (Unavailable), not known, and each kind's extra states. _Reuses: the widget card and source label._
- [ ] **Journey widgets**: `brief_summary`, `comparison_table` (including the phone cards in a horizontal scroll), `hotel_list`, `itinerary_day`, `booking_approval`, `web_results` and `not_known`, plus the phone compact card in the chat. Covers: every state in the table, including empty, the folded rows and every booking state.
- [ ] **Proposals for the kinds without a `kind`** ([#26](https://github.com/olaheavy-dev/layover/issues/26)): local holidays, the time difference, fares "to anywhere" and TfL journeys, each drawn as a widget with its source label. The figures they need are added to `sample-data.md` first. Plan 1 fixes the schemas.

## Screens

Each screen follows the checklist in [#28](https://github.com/olaheavy-dev/layover/issues/28) and is drawn at 390 px and 1440 px, in both themes.

- [ ] **Welcome** (`/`), with the illustration the owner picked, the four example prompts and the honesty line. Includes the mood-scene prompts for the owner to make in ChatGPT (welcome and "How Layover works" only), written to the image rules in the brief. _Depends on: illustration test._
- [ ] **Starting a trip**: the empty canvas after the first message; the brief waiting for confirmation, editing a chip and confirmed.
- [ ] **Comparing**: three loading cards; one failed card with "Try again"; a "Not known" row (Valencia's stay); a swapped place; no place fits.
- [ ] **The chosen place, finished**: the remaining place widgets below the first screen; a side answer inline in the chat with "Add to trip", and the same answer pinned under "Added from the chat". _Reuses: the first-look screen._
- [ ] **Stay and Days**: hotel chosen; hotel skipped (days from the centre); Days with a "Not known" opening time and an empty afternoon; the itinerary-only trip (the place, then Stay and Days, with no Compare section).
- [ ] **Booking**: waiting for approval, approved, declined and price changed, always with "Sandbox: no real booking or payment".
- [ ] **Chat-only replies and interruptions**: `web_results` in the chat; "I can't help with that yet"; the `not_travel` decline; lost connection with "Try again"; the "New trip" confirmation; the "Share trip" step.
- [ ] **Phone and navigation**: Chat and Trip tabs, the Trip tab badge, compact widget cards, the sideways section index; folded sections and the section index on desktop.
- [ ] **Pages outside the trip**: the shared trip (`/s/{share_id}`) with "as of" dates; How Layover works with "no evaluation results yet"; link not found or expired; limit reached, with wording that needs no figure.

## Review and handover

- [ ] **Board index**: `index.html` in this folder links every board, with the state each one shows, so the reviewers can check coverage against #28 and the state table.
- [ ] **Accessibility pass**: contrast from the tokens, visible focus on every control, targets of at least 24 by 24 px, reduced motion, text alternatives for charts and illustrations (brief, "Accessibility requirements").
- [ ] **Design review**: the `design-reviewer` against the 12 "bar for Layover" rules and the state table; the `visual-reviewer` at 390, 768, 1024 and 1440 px.
- [ ] **Handover**: tick #28's checklist, update `docs/planning/status.md` and `docs/planning/backlog.md`, run `make check`, then the pre-push review and the pull request.
