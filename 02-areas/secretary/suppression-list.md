---
type: area
status: active
tags: [secretary, suppression, compliance]
last_synced: 2026-07-22
aliases: [Do Not Contact, DNC List]
---

# Suppression list

Recipients and domains that must **never** receive automated outreach. Check before every send.

## How to use

1. Hermes searches this file (and the vault) before drafting.
2. n8n `secretary-email` webhook should reject if `to` matches any entry.
3. On bounce or unsubscribe — add immediately; log to [[03-resources/secretary-log/secretary-log-overview|secretary log]].

## Format

```markdown
| Email or domain | Reason | Added |
|-----------------|--------|-------|
| example@corp.com | unsubscribed | 2026-07-22 |
| *@competitor.com | block domain | 2026-07-22 |
```

## Entries

| Email or domain | Reason | Added |
|-----------------|--------|-------|
| contact@notablecap.com | invalid recipient / not found | 2026-07-23 |
| *@notablecap.com | block domain pending review | 2026-07-23 |
| investors@categoryvc.com | campaign reset — revisit later | 2026-07-23 |
|| *@categoryvc.com | campaign reset — revisit later | 2026-07-23 |
|| hello@greenfield-growth.com | hard bounce | 2026-07-24 |
|| *@greenfield-growth.com | hard bounce | 2026-07-24 |
|| tone@abstract.com | hard bounce | 2026-07-24 |
|| *@abstract.com | hard bounce | 2026-07-24 |

## Auto-add rules

| Event | Action |
|-------|--------|
| Gmail bounce (hard) | Add address + log |
| "Unsubscribe" reply | Add address + log |
| LinkedIn "not interested" | Add profile URL if available |
| Duplicate send same campaign | Block second attempt |
| User manual add | Append row above |

## Related

- [[02-areas/secretary/secretary-overview|Secretary overview]]
- [[02-areas/secretary/rate-limits|Rate limits]]
- [[03-resources/secretary-log/secretary-log-overview|Secretary log]]
