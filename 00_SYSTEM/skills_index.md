# Hermes Agent Skills & Cron Index

## Registered Skills Overview

| Skill Name | Purpose | Location / Handler | Trigger | Install |
| :--- | :--- | :--- | :--- | :--- |
| `coeus_crm_sync` | Syncs lead states, parses `01_INBOX/`, updates frontmatter | `~/.hermes/skills/coeus_crm_sync.md` | Manual / Cron | Installed |
| `outreach_drafter` | Generates tailored email/DM copy from templates and auto-sends | `~/.hermes/skills/outreach_drafter.md` | Pipeline Update / Cron | Installed |
| `whatsapp_notifier` | Sends formatted alerts/summaries to WhatsApp bridge | `~/.hermes/skills/whatsapp_notifier.md` | Schedule / Event | Installed |
| `codebase_indexer` | Scans `/Documents/code/` for commit logs & updates `codebase_registry.md` | `~/.hermes/skills/codebase_indexer.md` | Weekly Cron | Installed |
| `linkedin_prospecting` | Extracts info from LinkedIn profiles via CDP | `~/.hermes/skills/linkedin_prospecting.md` | Manual / Cron | Installed |

---

## Cron → Skill Attachment Table

| Job Name | Cron | Skills Attached | Notes |
| :--- | :--- | :--- | :--- |
| `morning_briefing` | `0 13 * * *` | `whatsapp_notifier` | Delivers 5-bullet digest (1:00 PM) |
| `inbox_triage` | `15 13,17,21 * * *` | `coeus_crm_sync` | Moves processed inbox items into projects (1:15 PM, 5:15 PM, 9:15 PM) |
| `investor_outreach` | `0 14 * * 2,4` | `outreach_drafter` | Physical AI/Robotics VCs/angels (2:00 PM Tue/Thu) |
| `agency_lead_gen` | `30 14 * * 1,3` | `outreach_drafter` | 2nd Brain/AI automation leads (2:30 PM Mon/Wed) |
| `competitor_research` | `0 15 * * 5` | — | Standalone research run (3:00 PM Fridays) |
| `social_sync` | `30 15 1 * *` | `linkedin_prospecting` | Syncs LinkedIn/X/GitHub into hermes_context.md (3:30 PM 1st of month) |

---

## Active Cron Automations

```yaml
schedules:
  - id: morning_briefing
    cron: "0 13 * * *"
    prompt: "Run whatsapp_notifier to send morning agenda and pipeline updates from coeus vault."
    enabled: true

  - id: inbox_triage
    cron: "15 13,17,21 * * *"
    prompt: "Scan 01_INBOX in coeus vault, classify new notes/leads, and move to appropriate 02_PROJECTS subfolder."
    enabled: true

  - id: investor_outreach
    cron: "0 14 * * 2,4" # Every Tue and Thu at 2:00 PM
    prompt: "Research new Physical AI/Robotics VCs/Angels, extract info, draft cold emails highlighting CogVideoX metrics/MuJoCo tests, and auto-send via CDP."
    enabled: true

  - id: agency_lead_gen
    cron: "30 14 * * 1,3" # Every Mon and Wed at 2:30 PM
    prompt: "Identify founders needing 2nd brain/AI automation. Draft and auto-send cold outreach emails offering consultancy services via CDP."
    enabled: true

  - id: competitor_research
    cron: "0 15 * * 5" # Every Friday at 3:00 PM
    prompt: "Scrape news and updates on Haga competitors (Instance, Robocurve, Antioch, Patronus AI) and generate intelligence brief in 02_PROJECTS/haga/competitors/"
    enabled: true

  - id: social_sync
    cron: "30 15 1 * *" # 1st of every month at 3:30 PM
    prompt: "Scrape Mushood's LinkedIn, Twitter, and GitHub to extract recent professional developments and inject them into hermes_context.md for fresh outreach context."
    enabled: true
```