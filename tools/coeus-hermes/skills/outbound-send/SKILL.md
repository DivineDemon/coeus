---
name: outbound-send
description: n8n secretary webhook contracts — search, enrich, email, LinkedIn, audit log. Required fields, curl examples, HTTP status handling, retries, and cap behavior.
version: 1.0.0
metadata:
  hermes:
    tags: [coeus, n8n, email, outreach]
---

# Outbound Send (n8n Hands)

```
N8N_BASE=https://self8n.sv.mushoodhanif.com
```

Full reference: `tools/coeus-hermes/n8n/secretary-webhooks.md`.

## Endpoints

| Path | Action |
|------|--------|
| `/webhook/secretary-search` | Serper |
| `/webhook/secretary-enrich` | Hunter |
| `/webhook/secretary-email` | Gmail auto-send |
| `/webhook/secretary-linkedin` | LinkedIn publish |
| `/webhook/secretary-log` | Audit |

## Required on sends

- `personalization_hooks` — non-empty array
- `campaign` — e.g. `investor-cold-email`, `lead-pipeline`
- Pre-check suppression + rate limits in vault

## Email example

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

| HTTP | Action |
|------|--------|
| 200 | Log vault rollup |
| 400 | Fix payload |
| 429 | Stop channel until UTC midnight |
| 5xx | Retry once after 60s |
