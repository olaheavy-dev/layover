# Decisions

Hard-to-reverse decisions get a numbered record in this folder (template: [0001](0001-record-decisions.md)). Easily reversible ones get a line in the register below. Accepted records aren't rewritten: a new record supersedes an old one.

## Records

| No. | Decision | Status |
| --- | --- | --- |
| [0001](0001-record-decisions.md) | Record decisions in this folder | Accepted |
| [0002](0002-start-from-house-template.md) | Start from the house template layers | Accepted |
| [0003](0003-purpose-and-traveller.md) | Purpose, audience and the traveller | Accepted |
| [0004](0004-flight-data-sources.md) | Flight data: cached real fares to browse, a sandbox to book | Accepted |
| [0005](0005-python-and-langgraph.md) | Python backend with LangGraph | Accepted |
| [0006](0006-nextjs-frontend.md) | Next.js frontend | Accepted |
| [0007](0007-agent-design.md) | Agent design: one planner agent, a fixed booking flow, and parallel research agents | Accepted |
| [0008](0008-retrieval-no-knowledge-graph.md) | Retrieval over official advice and guides; no knowledge graph | Accepted |
| [0009](0009-tools-as-mcp-servers.md) | Tools become MCP servers from build step 2 | Accepted |
| [0010](0010-repository-and-stages.md) | Repository: code name Layover, public, design before code | Accepted |
| [0011](0011-product-integrity-rules.md) | Product integrity rules | Accepted |

## Register

| Date | Choice | Why |
| --- | --- | --- |
| 2026-11-19 | Join only the Aviasales programme on Travelpayouts for now | It is the only brand that gives flight data; the others give affiliate links or feeds Layover doesn't use yet |
| 2026-11-19 | Send the Travelpayouts token in the `X-Access-Token` header, never as a URL parameter | Keys in URLs end up in logs |
| 2026-11-19 | Create the Travelpayouts "project" after the repository or site exists (superseded in part: see "Commission is built but switched off…") | It asks for a link to a traffic source; owner: "We can defer this creation" |
| 2026-11-19 | Numeric code is built test-first with the `test-first` skill; a test's expected figure is a hand-worked example with its working and source (#4) | Adopted from Vestagraph so a wrong calculation can't confirm itself; owner chose "Test-first + checks (Recommended)" in a prompt window. Builds on [0011](0011-product-integrity-rules.md) point 3. Money is integer minor units or `Decimal`, never a float. Enforced by the Code Review Rules now; once numeric code exists, a test check fails a numeric-module test whose docstring has no `Working:` and `Source:` section, and a lint rule bans `float` in money modules |
| 2026-11-19 | `AGENTS.md` lists the Superpowers skill or reviewer agent and the model for each workflow step (#4) | Owner: "Add Vestagraph's table to Layover (Recommended)" |
| 2026-11-19 | Live-service tests are marked `live` and kept out of `make check` and CI; the merge check uses recorded responses in `tests/recorded/<provider>/` with their capture date and no secrets, refreshed by a `live` run when the provider's API version or response changes (#5) | Outside services fail for reasons unrelated to the change (Vestagraph decision 0029); owner chose it in a prompt window. A review rule until the Python layer exists; then `make check` runs pytest with `-m "not live"` and unknown markers fail (`--strict-markers`) |
| 2026-11-19 | Evaluation cases and spec scenarios carry permanent IDs (`AREA-NN`, at least two digits; an area code is created with its first case), never reused, withdrawn rather than deleted; running Gherkin specs as tests is not adopted yet (#6). Applies to the evaluations in [0007](0007-agent-design.md) | Lets each criterion, test and evaluation be found with one search (Vestagraph decision 0043); owner chose the light version. A review rule until evaluation files exist; then a check that IDs are unique. pytest-bdd would need owner approval |
| 2026-11-19 | Each stage ends with a gate and a whole-repository audit; open issues are ordered in `docs/planning/backlog.md` with milestones (#7) | Stops contradictions and debt piling up between stages (Vestagraph decision 0016); owner chose it in a prompt window |
| 2026-11-19 | Fallback review when Codex is unavailable (usage limit, outage, or a review stuck for over an hour), documentation-only PRs only (was over 24 hours, any PR) (#7) | Matches the owner's house rules; owner chose "Gates, backlog, fallback fix" in a prompt window. Owner-only merge (merge rules) |
| 2026-11-19 | When commission is switched on, Aviasales links are built by the backend through the Travelpayouts partner links API with the partner marker and a SubID naming the feature that produced them (fixed list such as chat, fare_card, compare; never traveller data); a private dashboard shows clicks, bookings and earnings per feature from the booking statistics API | Owner chose 'Labels and dashboard'. Shows which AI feature drives real user actions; makes the Open-Meteo non-commercial question more pressing (agent's wording; the owner chose "Keep the drafted reason" in a prompt window). Needs a Travelpayouts project ID (`trs`), so the project is created before commission is switched on (see the next line); terms in [data sources](../references/data-sources.md#earnings-travelpayouts) |
| 2026-11-19 | Commission is built but switched off: a feature flag (off by default) controls partner links and the earnings dashboard. While it is off, fare cards link to plain Aviasales URLs with no partner ID or SubID, the partner links and statistics APIs are exercised only in tests with recorded responses, and no Travelpayouts project is needed. Layover stays non-commercial, so free non-commercial API tiers can be used. Before switching it on: check every source's commercial terms, the CAP Code on affiliate labelling, and create the Travelpayouts project. Enforced at build step 4 by tests: the default configuration has the flag off, and fare-card URLs contain no `marker` or `sub_id` while it is off. The Data API requirements page sets no rule on how fares link out ("Access is allowed without restrictions, but you must have a token", read in a browser on 19 Nov 2026); the Travelpayouts partner agreement is not yet read and is read before build step 4 | Owner: "switch commission off but have it built in i want as many free api integrations as possible that can add value to the project"; chose "Plain Aviasales links (Recommended)" in a prompt window |
| 2026-11-19 | Free APIs chosen for integration (#14): Open-Meteo Historical, Climate and Marine; sunrise-sunset.org; OpenFreeMap; Wikipedia and Wikidata; Unsplash; the Foursquare Open Source Places dataset; the TfL Unified API; the Python `holidays` library; plus the IANA time zone database (agent's default). Flight CO2, public transport feeds, OpenSky and the hazard feeds are kept as ideas ([data sources](../references/data-sources.md#free-apis-chosen-for-integration-14)) | Owner: "i want as many free api integrations as possible that can add value to the project"; picks made in prompt windows. On OpenSky the owner asked whether a portfolio counts as a live product, then chose "Move to ideas" |
