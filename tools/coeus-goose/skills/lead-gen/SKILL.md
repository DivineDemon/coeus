---
name: lead-gen
description: B2B lead pipeline — Serper search, Hunter enrich via n8n, fit scoring, and cold outreach. Revives Duqm discovery/enrichment pattern for lead-pipeline recipe.
---

# Lead Gen

Generalizes inactive Duqm workflows (Company Discovery + POC Enrichment) into a Goose-driven pipeline.

## Pipeline stages

```
Discover → Enrich → Score → Draft → Send → Log
```

## 1. Discover (`secretary-search`)

```bash
curl -s -X POST "$N8N_BASE/webhook/secretary-search" \
  -H "Content-Type: application/json" \
  -d '{"query":"{campaign query}","num":10,"gl":"om"}'
```

Search queries come from campaign brief in queue or ICP note. Log promising domains/companies to `00-inbox/secretary-queue/`.

## 2. Enrich (`secretary-enrich`)

Domain search (bulk contacts):

```json
{ "domain": "example.com", "limit": 10 }
```

Named contact:

```json
{ "domain": "example.com", "first_name": "Jane", "last_name": "Doe" }
```

Verify email:

```json
{ "email": "jane@example.com" }
```

Pick contacts with `confidence` ≥80 and role aligned to campaign ICP.

## 3. Score before outreach

| Factor | Weight |
|--------|--------|
| Company size (SMB–mid-market) | Fit gate |
| Geography matches campaign | Required |
| Trigger signal (hiring, funding, launch) | +3 |
| Contact role matches buyer persona | +2 |
| ≥2 personalization hooks available | Required to send |
| On suppression list | Hard reject |

## 4. Send + log

- Draft per `voice.md`; `campaign: lead-pipeline`
- `secretary-email` with `channel: email` (counts toward 20/day cold cap)
- `secretary-log` on success; append vault daily log
- Hard bounce / unsubscribe → `suppression-list.md` immediately

## Campaign queue template

```markdown
---
type: secretary-queue
channel: lead-gen
campaign: {name}
status: discovered
---

# {Company}

- Domain:
- Trigger:
- Contacts: []
- Hooks: []
- Score:
```

## Weekly cap

**5** discovery runs per week. Spread across UTC days; do not batch all in one session.

## Related

- ICP B2B section: `02-areas/secretary/icp.md`
- Webhook details: `tools/coeus-goose/n8n/secretary-webhooks.md`
