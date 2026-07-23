---
type: resource
status: active
tags: [secretary, audit, log]
last_synced: 2026-07-22
aliases: [Secretary Log, Outreach Archive]
---

# Secretary log

Immutable record of sent outreach. **Primary audit trail:** Google Sheets + Neon via n8n `secretary-log` webhook. This folder holds vault-side summaries and weekly rollups.

## What gets logged

| Field | Required |
|-------|----------|
| `timestamp` | UTC ISO-8601 |
| `channel` | email, linkedin-post, linkedin-dm, job-apply, social |
| `recipient` | email or profile URL |
| `campaign` | campaign name (e.g. `investor-cold-email`) |
| `subject_or_title` | email subject or post title |
| `personalization_hooks` | JSON array of hooks used |
| `n8n_execution_id` | for traceability |
| `status` | sent, failed, bounced |

## Vault file naming

```
YYYY-MM-DD-log.md          # daily rollup (optional, written by Hermes)
YYYY-Www-weekly-summary.md # weekly digest
```

## Daily rollup template

```markdown
---
type: secretary-log
date: YYYY-MM-DD
tags: [secretary, log]
---

# Secretary log — YYYY-MM-DD

| Time (UTC) | Channel | Recipient | Campaign | Status |
|------------|---------|-----------|----------|--------|
| | | | | |

## Caps used

| Channel | Sent today | Cap |
|---------|------------|-----|
| Cold email | 0 | 20 |
| Job apply | 0 | 10 |
| LinkedIn post | 0 | 5 |

## Notes

(any bounces, unsubscribes → update suppression list)
```

## Retention

- Sheets/Neon: system of record (indefinite)
- Vault daily files: keep 90 days, then fold into weekly summary
- Weekly summaries: keep 1 year

## Related

- [[02-areas/secretary/secretary-overview|Secretary overview]]
- [[02-areas/secretary/rate-limits|Rate limits]]
- [[02-areas/secretary/suppression-list|Suppression list]]
- [[03-resources/infrastructure/n8n-overview|n8n Overview]]
- [[03-resources/infrastructure/neon-overview|Neon Overview]]
