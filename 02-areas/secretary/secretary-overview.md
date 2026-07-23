---
type: moc
status: active
tags: [moc, secretary, automation]
last_synced: 2026-07-23
aliases: [Secretary Index, Ops Secretary]
---

# Secretary

Autonomous outreach and ops surface for **Hermes** + n8n webhooks. The **Obsidian vault is the only durable memory plane** — Hermes `MEMORY.md` holds short pointers only.

## Core config

| Note | Purpose |
|------|---------|
| [[02-areas/secretary/icp\|ICP]] | Who to target per channel (jobs, investors, leads, social) |
| [[02-areas/secretary/voice\|Voice]] | Tone, sign-off, personalization rules |
| [[02-areas/secretary/rate-limits\|Rate limits]] | Daily caps — hard stops for auto-send |
| [[02-areas/secretary/suppression-list\|Suppression list]] | Do-not-contact: sent, bounced, unsubscribed |

## Queues and logs

| Path | Role |
|------|------|
| `00-inbox/secretary-queue/` | Today's candidates awaiting action |
| `03-resources/secretary-log/` | Sent/applied archive (Sheets/Neon is primary; vault is daily rollup) |

## Automation split

- **Hermes** — plan, personalize, decide, browse, write vault notes
- **n8n** — search (Serper), enrich (Hunter), send (Gmail/LinkedIn), audit (Sheets + Neon)

Webhook contracts: [[tools/coeus-hermes/n8n/secretary-webhooks|secretary-webhooks]].

Playbooks: [[tools/coeus-hermes/README|tools/coeus-hermes]] — skills under `tools/coeus-hermes/skills/` (symlinked into `~/.hermes/skills/coeus`).

## Skills (Hermes)

| Skill | Use |
|-------|-----|
| `secretary-core` | Load first — vault paths, caps, checklist |
| `outbound-send` | n8n curl contracts |
| `investor-outreach` | Cold investor email |
| `lead-gen` | Haga B2B pipeline |
| `job-hunt` | Applications |
| `social-ops` | LinkedIn publish |

## Agent rules

1. **Search the vault first** for ICP, voice, caps, and prior outreach before drafting.
2. **Check suppression list** before any send; reject if recipient is listed.
3. **Respect rate limits** — if cap reached, queue for tomorrow; do not bypass via n8n.
4. **Log every send** — n8n `secretary-log` webhook + vault markdown in `03-resources/secretary-log/`.
5. **Write durable facts into vault notes** — not a parallel Hermes fact dump.

## Related

- [[02-areas/startups/startups-overview|Startups]] — venture context for investor/social outreach
- [[02-areas/career/career-overview|Career]] — resumes and job-hunt targets
- [[03-resources/infrastructure/n8n-overview|n8n]] — webhook hands
- [[tools/coeus-hermes/README|Hermes + Coeus]] — brain setup
- [[home]]
