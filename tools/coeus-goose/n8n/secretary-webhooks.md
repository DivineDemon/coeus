# Secretary n8n webhooks

Goose calls these webhooks as **hands** for search, enrichment, send, and audit. Base URL:

`https://self8n.sv.mushoodhanif.com/webhook/`

All endpoints accept `POST` with `Content-Type: application/json`. Responses are JSON.

## Workflows (active)

| Webhook path | Workflow | ID |
|--------------|----------|-----|
| `/webhook/secretary-search` | Secretary: Search | `OG3PyZPXG0u5pzlH` |
| `/webhook/secretary-enrich` | Secretary: Enrich | `X1uHo4QTRpBcbmBj` |
| `/webhook/secretary-email` | Secretary: Email | `oInXfvpD9KvxCk9s` |
| `/webhook/secretary-linkedin` | Secretary: LinkedIn | `bOTlrNLAlqeF8heq` |
| `/webhook/secretary-log` | Secretary: Log | `pM57uKzyOtN7Kacj` |

Audit storage: n8n Data Table **Secretary Audit Log** (`LmL4cznvDtTDvFe7`) + Neon `secretary_actions` (portfolio DB; Neon insert node disabled until **Portfolio Neon** Postgres credential is added in n8n).

## Daily caps (enforced on email / LinkedIn)

Caps align with [[02-areas/secretary/rate-limits|rate limits]] (UTC day, `status: sent` rows only):

| Channel | Daily cap |
|---------|-----------|
| `email` (cold outreach) | 20 |
| `job-apply` | 10 |
| `linkedin-post` | 5 |
| `linkedin-dm` | 15 (reserved; API does not support DMs) |
| `social` | 3 |

When cap is hit, email/LinkedIn return HTTP **429** with `error: cap_reached`.

## `secretary-search`

**Request**

```json
{
  "query": "AI startups Oman",
  "num": 10,
  "gl": "om"
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `query` | yes | Serper search string |
| `num` | no | 1–20, default 10 |
| `gl` | no | Geo hint, default `om` |

**Response (200)**

```json
{
  "ok": true,
  "query": "...",
  "result_count": 5,
  "results": [{ "title": "", "link": "", "snippet": "", "position": 1 }],
  "knowledge_graph": null,
  "searched_at": "2026-07-22T08:00:00.000Z"
}
```

## `secretary-enrich`

**Request** (one of):

```json
{ "domain": "example.com", "limit": 10 }
```

```json
{ "domain": "example.com", "first_name": "Jane", "last_name": "Doe" }
```

```json
{ "email": "jane@example.com" }
```

**Response (200)**

```json
{
  "ok": true,
  "mode": "domainSearch",
  "domain": "example.com",
  "organization": "Example Inc",
  "contact_count": 3,
  "contacts": [{ "email": "", "first_name": "", "last_name": "", "position": "", "confidence": 90 }],
  "enriched_at": "2026-07-22T08:00:00.000Z"
}
```

## `secretary-email`

**Request**

```json
{
  "to": "investor@fund.com",
  "subject": "Quick intro — Haga",
  "body": "<p>Personalized HTML body</p>",
  "campaign": "investor-cold-email",
  "channel": "email",
  "personalization_hooks": ["recent Series A", "robotics portfolio"]
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `channel` | no | `email` (default, cap 20) or `job-apply` (cap 10) |
| `personalization_hooks` | yes | Non-empty array; webhook rejects without it |
| `to` | yes | Valid email |
| `subject`, `body` | yes | HTML body supported via `emailType: html` |

**Success (200):** `{ "ok": true, "sent": true, "sent_today": 1, "cap": 20, ... }`  
**Cap (429):** `{ "ok": false, "error": "cap_reached", ... }`  
**Validation (400):** missing fields, invalid email, missing personalization

## `secretary-linkedin`

**Request**

```json
{
  "text": "Post copy…",
  "campaign": "social-publish",
  "channel": "linkedin-post",
  "personalization_hooks": ["product launch"],
  "title": "Optional title for article posts",
  "original_url": "https://example.com/post",
  "post_as": "person",
  "person_urn": "",
  "visibility": "PUBLIC"
}
```

| Field | Required | Notes |
|-------|----------|-------|
| `channel` | no | `linkedin-post` (default), or `social` (cap 3). `linkedin-dm` returns 400 |
| `personalization_hooks` | yes | Non-empty array |
| `person_urn` | no | Set in n8n LinkedIn node if default OAuth person is not selected |

**Success (200):** `{ "ok": true, "published": true, "linkedin_urn": "...", "sent_today": 1, "cap": 5 }`

## `secretary-log`

Explicit audit entry (email/LinkedIn workflows also log on successful send).

**Request**

```json
{
  "channel": "email",
  "recipient": "user@example.com",
  "campaign": "investor-cold-email",
  "subject_or_title": "Subject line",
  "personalization_hooks": ["hook one"],
  "status": "sent",
  "n8n_execution_id": "optional",
  "metadata": {}
}
```

| `status` | Meaning |
|----------|---------|
| `sent` | Counts toward daily cap |
| `failed` | Does not count |
| `bounced` | Does not count; add to suppression list |
| `cap_reached` | Logged when cap blocks send |
| `suppressed` | Blocked recipient |

**Response (200):** `{ "ok": true, "logged": true, "data_table_row_id": 1, ... }`

## Goose curl examples

```bash
# Search
curl -s -X POST "$N8N_BASE/webhook/secretary-search" \
  -H "Content-Type: application/json" \
  -d '{"query":"robotics startups GCC","num":5}'

# Enrich domain
curl -s -X POST "$N8N_BASE/webhook/secretary-enrich" \
  -H "Content-Type: application/json" \
  -d '{"domain":"example.com","limit":5}'

# Log only
curl -s -X POST "$N8N_BASE/webhook/secretary-log" \
  -H "Content-Type: application/json" \
  -d '{"channel":"email","recipient":"a@b.com","campaign":"test","subject_or_title":"Hi","personalization_hooks":["x"],"status":"sent"}'
```

Set `N8N_BASE=https://self8n.sv.mushoodhanif.com` in Goose env or skills.

## Setup checklist

1. **Portfolio Neon** — Create Postgres credential `Portfolio Neon` in n8n (portfolio project connection string from Neon console). Enable **Insert Neon Audit** node in Secretary: Log and re-publish.
2. **LinkedIn person** — Open Secretary: LinkedIn → Publish LinkedIn Post → select your person URN once (or pass `person_urn` in webhook body).
3. **Serper** — Secretary: Search → Serper Search node should use **Google Serper** header auth (assign in UI if missing).

## Related

- [[02-areas/secretary/secretary-overview|Secretary overview]]
- [[02-areas/secretary/rate-limits|Rate limits]]
- [[03-resources/infrastructure/n8n-overview|n8n Overview]]
