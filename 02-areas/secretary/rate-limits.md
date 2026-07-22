---
type: area
status: active
tags: [secretary, safety, rate-limits]
last_synced: 2026-07-22
aliases: [Daily Caps, Send Limits]
---

# Rate limits

Hard daily caps for full auto-send. n8n webhooks should enforce these; Goose must not attempt to bypass.

## Daily caps (UTC day)

| Channel | Cap | Notes |
|---------|-----|-------|
| Cold email (Gmail) | **20** | Investor + lead gen combined |
| Job applications / recruiter email | **10** | Distinct from cold outreach |
| LinkedIn posts | **5** | Company + personal combined |
| LinkedIn DMs | **15** | Connection requests count toward cap |
| Social queue (n8n sheet) | **3** | Align with Haga Social Autopilot |

## Weekly caps

| Channel | Cap |
|---------|-----|
| Investor cold email batches | **3 runs** max (e.g. Mon/Wed/Fri) |
| Lead pipeline discovery runs | **5** |

## Behavior when cap hit

1. Stop sending for that channel until next UTC midnight.
2. Move remaining queue items to next day — do not delete.
3. Log `cap_reached` in n8n audit + diary entry via `mempalace_diary_write`.
4. Morning brief recipe should surface cap status.

## Warm-up (new accounts or after pause)

If Gmail or LinkedIn has been idle >30 days, halve all caps for the first 7 days.

## Audit requirement

Every send counts toward cap only after n8n `secretary-log` returns success. Failed sends do not count; retries count once on success.

## Related

- [[02-areas/secretary/secretary-overview|Secretary overview]]
- [[02-areas/secretary/suppression-list|Suppression list]]
- [[03-resources/infrastructure/n8n-overview|n8n Overview]]
