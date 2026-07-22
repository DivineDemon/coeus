---
name: outbound-send
description: n8n secretary webhook contracts — search, enrich, email, LinkedIn, audit log. Required fields, curl examples, HTTP status handling, retries, and cap behavior. Use before any auto-send or when calling n8n hands.
---

# Outbound Send (n8n Hands)

Goose plans and personalizes; **n8n sends**. Base URL:

```
N8N_BASE=https://self8n.sv.mushoodhanif.com
```

Full reference: `tools/coeus-goose/n8n/secretary-webhooks.md`

## Endpoints

| Path | Action |
|------|--------|
| `/webhook/secretary-search` | Serper web search |
| `/webhook/secretary-enrich` | Hunter enrich |
| `/webhook/secretary-email` | Gmail auto-send |
| `/webhook/secretary-linkedin` | LinkedIn publish |
| `/webhook/secretary-log` | Audit entry |

## Required on all sends

- `personalization_hooks` — non-empty JSON array (webhook rejects without it)
- `campaign` — recipe name (e.g. `investor-cold-email`, `lead-pipeline`)
- Pre-check suppression list + rate limits in vault

## Email

```bash
curl -s -X POST "$N8N_BASE/webhook/secretary-email" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Subject",
    "body": "<p>HTML body</p>",
    "campaign": "investor-cold-email",
    "channel": "email",
    "personalization_hooks": ["hook one", "hook two"]
  }'
```

| `channel` | Daily cap |
|-----------|-----------|
| `email` (default) | 20 |
| `job-apply` | 10 |

## LinkedIn

```bash
curl -s -X POST "$N8N_BASE/webhook/secretary-linkedin" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Post copy",
    "campaign": "social-publish",
    "channel": "linkedin-post",
    "personalization_hooks": ["hook"]
  }'
```

`linkedin-dm` returns **400** — API not supported.

## Audit log

```bash
curl -s -X POST "$N8N_BASE/webhook/secretary-log" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "email",
    "recipient": "user@example.com",
    "campaign": "test",
    "subject_or_title": "Subject",
    "personalization_hooks": ["hook"],
    "status": "sent"
  }'
```

| `status` | Counts toward cap? |
|----------|-------------------|
| `sent` | Yes |
| `failed`, `bounced` | No |
| `cap_reached`, `suppressed` | No |

## HTTP responses

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Log vault rollup |
| 400 | Validation (missing hooks, bad email) | Fix draft; do not retry blindly |
| 429 | `cap_reached` | Stop channel until UTC midnight; queue remainder |
| 5xx | n8n/provider error | Retry once after 60s; then log `failed` |

## Retry policy

1. **429** — never retry same day for that channel
2. **400** — fix payload; no automatic retry
3. **5xx** — one retry; if fail, `secretary-log` with `status: failed`
4. Bounce → add to suppression list; no retry

## Post-send

1. Confirm `ok: true` in response
2. `secretary-log` if send workflow didn't auto-log
3. Append `03-resources/secretary-log/YYYY-MM-DD-log.md`
4. On bounce/unsubscribe → `02-areas/secretary/suppression-list.md`
