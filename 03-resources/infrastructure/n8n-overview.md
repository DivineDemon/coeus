---
type: resource
status: active
tags: [infrastructure, n8n, automation]
url: https://n8n.io
last_synced: 2026-07-22
aliases: [n8n Integrations, n8n Inventory]
---

# n8n Overview

n8n workspace inventory and integration snapshot. This note documents workflow coverage, connected services, and how n8n ties into active projects.

## Profile summary

- Identity context: **Verified n8n Creator** — [[03-resources/social-profiles/n8n-creator|Creator profile]]
- Workspace workflows discovered: **11**
- Active workflows: **6**
- Stored credentials discovered: **8**

## Credential inventory (names only)

| Credential | Type | Typical usage |
|------------|------|---------------|
| Gemini | `googlePalmApi` | LLM drafting / extraction |
| My Gemini | `googlePalmApi` | Alternate LLM credential |
| OpenRouter | `openRouterApi` | Model routing fallback |
| Google Serper | `httpHeaderAuth` | Web search enrichment |
| Google Sheets | `googleSheetsOAuth2Api` | Queue/review sheet updates |
| Gmail | `gmailOAuth2` | Email-triggered or outbound automation |
| LinkedIn | `linkedInOAuth2Api` | Social publishing flows |
| Hunter | `hunterApi` | Prospect enrichment |

## Workflow inventory

| Workflow | Status | Purpose |
|----------|--------|---------|
| Haga Social Autopilot | active | Daily research, draft, verify, and queue social posts |
| Secretary: Search | active | Webhook — Serper search for Goose recipes |
| Secretary: Enrich | active | Webhook — Hunter domain/email enrichment |
| Secretary: Email | active | Webhook — Gmail auto-send with caps + audit |
| Secretary: LinkedIn | active | Webhook — LinkedIn publish with caps + audit |
| Secretary: Log | active | Webhook — immutable audit (Data Table + Neon) |
| Duqm WF1: Company Discovery | inactive | Daily company discovery pipeline |
| Duqm WF2: POC Enrichment | inactive | Lead and contact enrichment |
| Duqm Data Cleanup | inactive | One-time cleanup utility |
| Duqm WF0: Zoomlion ICP Setup | inactive | One-time ICP bootstrapping |
| Duqm Sheet Restructure | inactive | One-time sheet schema setup |

## Integration overview

### Secretary webhooks (active)

Goose **hands** for full auto-send. Base URL: `https://self8n.sv.mushoodhanif.com/webhook/`. Full contracts: [[tools/coeus-goose/n8n/secretary-webhooks|secretary-webhooks.md]].

| Path | Action | Integrations |
|------|--------|--------------|
| `secretary-search` | Web search | Google Serper |
| `secretary-enrich` | Contact enrich | Hunter.io |
| `secretary-email` | Auto-send email | Gmail |
| `secretary-linkedin` | Publish post | LinkedIn OAuth |
| `secretary-log` | Audit log | Data Table + Neon `secretary_actions` |

**Daily caps** (UTC, enforced on send webhooks): cold email 20, job-apply 10, LinkedIn post 5, social queue 3. See [[02-areas/secretary/rate-limits|rate limits]].

**Audit:** n8n Data Table `Secretary Audit Log` (`LmL4cznvDtTDvFe7`). Neon mirror uses portfolio DB table `secretary_actions` — enable the disabled Postgres node in Secretary: Log after adding a **Portfolio Neon** credential.

**Safety:** `personalization_hooks` required on sends; suppression checked on email; cap returns HTTP 429.

### Haga Social Autopilot (active)

Current active automation orchestrates:

1. Scheduled daily trigger (`14:00 UTC`).
2. Source collection (search + arXiv + Haga public pages + repo README).
3. Candidate ranking and novelty checks.
4. Multi-channel draft generation (company, personal, X).
5. Claim verification and deterministic publish gating.
6. Queueing approved content to Google Sheets.
7. Recording outcomes to an n8n data table.

### How this maps to projects

- Supports Haga communication operations and evidence-backed social output.
- Reuses AI tooling stack already reflected across [[03-resources/github-repos/profile\|GitHub Profile README]] and resume notes.
- Connects with portfolio ecosystem where workflow case studies are stored in `n8n_workflows` (Neon).

## Recommended profile-sync workflow (design only)

Proposed reusable workflow for Coeus sync:

1. Schedule trigger (weekly).
2. Pull profile/repo changes (GitHub + HTTP sources).
3. Generate markdown updates with strict templates.
4. Open commit/PR in vault repo for review.

This is documented only and has not been executed from MCP in this phase.

## Related

- Portfolio workflows: [[03-resources/github-repos/portfolio|portfolio]] (`n8n_workflows` table)
- Haga startup: [[02-areas/startups/haga|Haga]]
- Setup videos (local): `03-resources/infrastructure/n8n-videos/` — create-a-neon-db.mov, deploy-n8n-on-render.mov, setup-n8n.mov
- Skills: [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- Database: [[03-resources/infrastructure/neon-overview|Neon Overview]]
- Home: [[home]]
