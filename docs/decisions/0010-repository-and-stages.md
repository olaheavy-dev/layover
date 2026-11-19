# 0010. Repository: code name Layover, public, design before code

Status: Accepted (19 Nov 2026)

## Context

The owner wants this project set up the way Vestagraph (homescout-platform) was: "I think before all these questions we setup a github project first mirroring what homescout does". The owner also wants the product designed properly before code: "We can defer this creation we need to properly design the application".

## Decision

1. **Name:** `layover` for the repository and folder, chosen by the owner. Treated as the working name; a public brand needs a brand and domain check before launch.
2. **Visibility:** public, all rights reserved (owner chose the recommended option), like Vestagraph.
3. **Templates:** `house-template-base` v0.7.0 now, with no stack layer. The FastAPI and Next.js layers are added when the design is approved and building starts (owner chose the recommended option). Checked on 19 Nov 2026: the base with no stack passes `make check`; the base with both stacks selected but no layers applied would fail in CI (no `frontend/package.json` or `.node-version`).
4. **Documents mirror Vestagraph's shape:** numbered product documents, decision records, dated reviews, references, specifications later, and the status file.

## Consequences

- Until building starts, the repository holds documents only.
- Adding the stacks later means `copier update -a .copier-answers.base.yml --data stacks=...` and then applying each layer with its own answers file.
- The Travelpayouts "project" (which asks for a link to a traffic source) is created once the repository or site exists.

## Alternatives considered

- **All template layers now:** backend and frontend code before the design exists, and CI needs Docker from day one.
- **Copying Vestagraph's files by hand:** no update path, and its project-specific rules don't apply here.
- **Private repository:** hides progress from recruiters and limits some free GitHub security features.

## Sources

- house-template-base README (v0.7.0): https://github.com/olaheavy-dev/house-template-base
