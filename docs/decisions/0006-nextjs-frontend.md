# 0006. Next.js frontend

Status: Accepted (19 Nov 2026)

## Context

Decision 0003 sets the bar at a real product that convinces a recruiter. The traveller-facing frontend carries most of that impression.

## Decision

Build the frontend with Next.js from `house-template-nextjs` (owner chose the recommended option), applied when building starts (decision 0010).

## Consequences

- Two languages: Python for the backend, TypeScript for the frontend.
- The template brings design tokens, accessibility and screenshot checks.
- The frontend can stream the agent's progress and answers as they arrive.
- Duffel's card form is a browser component, which fits here.

## Alternatives considered

- **Python-only pages** (FastAPI serving HTML with a little JavaScript): one language and a quicker start, but much harder to make feel like a real product, and no template layer for it.

## Sources

- Next.js documentation: https://nextjs.org/docs
