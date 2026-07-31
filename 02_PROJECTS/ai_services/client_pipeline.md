---
type: pipeline
category: sales
business: ai_services
tags: [pipeline, leads, clients, consultancy]
---

# Client & Deal Pipeline (AI Services)

Tracks prospective clients, founders, and businesses requiring 2nd Brain setups, custom agent workflows, or enterprise software.

---

## Pipeline Overview

| Client / Founder | Business / Niche | Service Interest | Deal Value | Lead Source | Status | Next Step | Follow-up |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Founder A** | E-commerce Brand | 2nd Org Brain + Email Agent | $3,500 | LinkedIn | Qualified | Send proposal draft | 2026-08-02 |
| **Business B** | Logistics / Supply | Custom n8n Automation | $5,000 | Inbound / X | Prospect | Schedule discovery call | 2026-08-04 |
| **Startup C** | Robotics / AI | Benchmark Consulting | $8,000 | Outreach | Initial Contact | Share Haga Lab case study | 2026-08-06 |

---

## Lead Qualification Criteria
1. Clear manual bottleneck or desire for automated AI agency capabilities.
2. Willingness to adopt Markdown-first or agent-integrated workflows.
3. Budget > $2,500 for custom builds.

---

## Agent Instructions for Hermes
- Scan `01_INBOX/` for lead notes.
- When a lead reaches `Qualified` status, generate a custom proposal draft in `02_PROJECTS/ai_services/proposals/`.
- Send a WhatsApp alert to user when follow-up date matches current date.
