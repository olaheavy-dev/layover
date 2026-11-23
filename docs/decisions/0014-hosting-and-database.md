# 0014. Hosting: a shared DigitalOcean server in London, with the database in Neon

Status: Accepted (23 Nov 2026).

## Context

Hosting and the database were open owner decisions for build step 7 ([01 §4](../product/01-research-and-direction.md#4-build-order)). On 23 Nov 2026, the owner's infrastructure work planned one DigitalOcean server in London to host two of the owner's apps, including Layover, with each app's database in Neon (a managed PostgreSQL service). The owner then asked: "record the decision". In prompt windows the owner chose:

- what is decided: "Server and database (Recommended)";
- how much this public repository names: "Provider and region only (Recommended)";
- Neon's plan and data region: "Leave them open (Recommended)".

`AGENTS.md` (rule 2) keeps infrastructure details out of this public repository. Host names, addresses, access tunnels and the other app's name stay in the owner's private infrastructure repository.

## Decision

1. **Server:** Layover runs on a DigitalOcean server in London, shared with another of the owner's apps.
2. **Database:** Layover's PostgreSQL database is in Neon.
3. **Left open, settled with the owner in build step 7's plan:**
   - Neon's plan, data region and running cost, before any traveller data is stored;
   - how images are published and deployed;
   - backups;
   - where traces go once Layover is hosted ([0013](0013-microsoft-agent-framework.md)).

## Consequences

- Build step 7's plan works inside this choice and doesn't compare hosts again.
- Neon's region decides where travellers' trips are stored (UK GDPR). The step 7 plan states the region and its terms, for the owner's approval, before the first trip is saved.
- The server is shared, so Layover's images, memory and disk use must fit beside the other app. The step 7 plan measures them.
- The step 7 notes in the [status file](../planning/status.md) still apply. The backend image needs `--build-context samples=schemas/samples`, and uptime checks watch the backend's `/health/ready`.
- Changes to infrastructure and running costs stay owner-only merges (`AGENTS.md`, "When merging").

## Alternatives considered

Layover's records don't compare other hosts. The choice was made with the owner's wider infrastructure plan for the shared London server. A later record can supersede this one if step 7 finds the shared server doesn't fit.

## Sources

- The owner's infrastructure session, message of 23 Nov 2026 (private infrastructure repository): one London DigitalOcean server for two of the owner's apps, each app's database in Neon.
- Owner, 23 Nov 2026: "record the decision", and the three prompt-window answers above.
- DigitalOcean: https://www.digitalocean.com/
- Neon: https://neon.com/
