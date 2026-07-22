---
type: moc
status: active
tags: [moc, secretary, automation]
last_synced: 2026-07-22
aliases: [Secretary Index, Ops Secretary]
---

# Secretary

Autonomous outreach and ops surface for Goose recipes + n8n webhooks. **MemPalace is the only memory plane** — do not use Goose Memory; persist durable facts here and re-mine after edits.

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
| `03-resources/secretary-log/` | Sent/applied archive (Sheets/Neon is primary; vault is weekly summary) |

## Automation split

- **Goose** — plan, personalize, decide, browse, write vault notes
- **n8n** — search (Serper), enrich (Hunter), send (Gmail/LinkedIn), audit (Sheets + Neon)

Webhook contracts: [[tools/coeus-goose/n8n/secretary-webhooks|secretary-webhooks]] (live on n8n).

**E2E smoke test:** `tools/coeus-goose/scripts/smoke-test.sh` — self-send to Gmail, verify audit log + vault rollup. Recipe: `smoke-test.yaml`.

## Recipes

YAML in `tools/coeus-goose/recipes/`. Install schedules: `tools/coeus-goose/recipes/install-schedules.sh`.

| Recipe | Schedule (UTC) | Goose schedule ID |
|--------|----------------|-------------------|
| `morning-brief` | 08:00 daily | `secretary-morning-brief` |
| `daily-job-hunt` | 09:00 daily | `secretary-daily-job-hunt` |
| `investor-cold-email` | 10:00 Mon/Wed/Fri | `secretary-investor-cold-email` |
| `lead-pipeline` | 11:00 daily | `secretary-lead-pipeline` |
| `social-publish` | 14:00 daily (Haga Autopilot) | `secretary-social-publish` |
| `secretary` (router) | On demand | — |

## Agent rules

1. **Search MemPalace first** for ICP, voice, caps, and prior outreach before drafting.
2. **Check suppression list** before any send; reject if recipient is listed.
3. **Respect rate limits** — if cap reached, queue for tomorrow; do not bypass via n8n.
4. **Log every send** — n8n `secretary-log` webhook + vault markdown in `03-resources/secretary-log/`.
5. **Never enable Goose Memory** — write durable prefs to this folder instead.

## Related

- [[02-areas/startups/startups-overview|Startups]] — venture context for investor/social outreach
- [[02-areas/career/career-overview|Career]] — resumes and job-hunt targets
- [[03-resources/infrastructure/n8n-overview|n8n]] — webhook hands
- [[03-resources/infrastructure/local-llm-memory|Local LLM]] — MemPalace + Goose setup
- [[home]]
