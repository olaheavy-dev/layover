# Documentation index

## Folder structure

```
docs/
├── README.md            this index
├── product/             the main product documents (numbered, read in order)
├── decisions/           one record per decision, plus the register
├── design/              the design brief, information architecture, design tokens and boards
├── planning/            the status file, the ordered backlog and working plans
├── references/          data sources and official third-party documentation
├── reviews/             dated reviews and research
└── superpowers/         specs and plans written with the Superpowers skills (added when first used)
```

Planned folders, added when their stage starts: `docs/specs/` for the specification, `docs/architecture/` for system diagrams, `docs/assets/` with an asset register before any image is committed, and `docs/floorplan/` for the Floorplan map snapshot published at each stage gate.

## What each document is for

| Document | Owns | Status |
|---|---|---|
| [01 Research and direction](product/01-research-and-direction.md) | What Layover is, what it shows, build order, open design questions | Draft |
| [Design brief](design/brief.md) | Tone, style, benchmark, component inventory, accessibility | Approved |
| [Information architecture](design/information-architecture.md) | Screens, links, navigation, flows for each intent, interface wording | Approved |
| [Design tokens](design/tokens.css) | Colours (light and dark), fonts, spacing, shapes, motion; checked for contrast by `make check` | Approved |
| [Decision register](decisions/README.md) | Every decision's status and record | Current |
| [Ordered backlog](planning/backlog.md) | Every open issue in order, by stage milestone, and the stage gate | Current |
| [Status](planning/status.md) | Open pull requests, next steps, blockers and the owner's to-dos; overwritten every session | Current |
| [Data sources](references/data-sources.md) | Each outside source's access, terms, limits and when it was checked | Current |
| [Third-party documentation](references/third-party.md) | Official documentation links, and pinned versions once dependencies exist | Current |
| [TripMate review, 19 Nov 2026](reviews/2026-11-19-tripmate-reference-review.md) | Lessons from a public tutorial travel planner | Record |

Accepted decision records override anything in the documents that contradicts them. For process, `AGENTS.md` is the rulebook.

**Reading order for someone new:** 01, then the decision register.

## Naming conventions

- Lowercase words separated by hyphens; no spaces.
- Numbered prefixes where order matters: `01-` for product documents, `0001-` upwards for decisions.
- Dates as `YYYY-MM-DD` at the start of dated files, for example reviews.
