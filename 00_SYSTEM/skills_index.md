# Hermes Agent Skills & Cron Index

## Registered Skills Overview

| Skill Name | Purpose | Location / Handler | Trigger |
| :--- | :--- | :--- | :--- |
| `coeus_crm_sync` | Syncs lead states, parses `01_INBOX/`, updates frontmatter | `~/.hermes/skills/coeus_crm_sync.md` | Manual / Cron |
| `outreach_drafter` | Generates tailored email/DM copy from templates and auto-sends | `~/.hermes/skills/outreach_drafter.md` | Pipeline Update / Cron |
| `whatsapp_notifier` | Sends formatted alerts/summaries to WhatsApp bridge | `~/.hermes/skills/whatsapp_notifier.md` | Schedule / Event |
| `codebase_indexer` | Scans `/Documents/code/` for commit logs & updates `codebase_registry.md` | `~/.hermes/skills/codebase_indexer.md` | Weekly Cron |
| `linkedin_prospecting` | Extracts info from LinkedIn profiles via CDP | `~/.hermes/skills/linkedin_prospecting.md` | Manual / Cron |

---

## Active Cron Automations

```yaml
schedules:
  - id: morning_briefing
    cron: "0 8 * * *"
    prompt: "Run whatsapp_notifier to send morning agenda and pipeline updates from coeus vault."
    enabled: true

  - id: inbox_triage
    cron: "0 */4 * * *"
    prompt: "Scan 01_INBOX in coeus vault, classify new notes/leads, and move to appropriate 02_PROJECTS subfolder."
    enabled: true

  - id: competitor_research
    cron: "0 10 * * 5" # Every Friday at 10 AM
    prompt: "Scrape news and updates on Haga competitors (Instance, Robocurve, Antioch, Patronus AI) and generate intelligence brief in 02_PROJECTS/haga/competitors/"
    enabled: true

  - id: job_application
    cron: "0 9 * * *" # Every Morning at 9 AM
    prompt: "Scrape remote job boards for 'Senior AI Engineer' ($3k-$3.5k/mo min, remote, USD), tailor resume.tex from /resume/, and autonomously apply or prepare drafts."
    enabled: true

  - id: investor_outreach
    cron: "0 11 * * 2,4" # Every Tue and Thu at 11 AM
    prompt: "Research new Physical AI/Robotics VCs/Angels, extract info, draft cold emails highlighting CogVideoX metrics/MuJoCo tests, and auto-send via CDP."
    enabled: true

  - id: agency_lead_gen
    cron: "0 13 * * 1,3" # Every Mon and Wed at 1 PM
    prompt: "Identify founders needing 2nd brain/AI automation. Draft and auto-send cold outreach emails offering consultancy services via CDP."
    enabled: true

  - id: social_sync
    cron: "0 12 1 * *" # 1st of every month at 12 PM
    prompt: "Scrape Mushood's LinkedIn, Twitter, and GitHub to extract recent professional developments and inject them into hermes_context.md for fresh outreach context."
    enabled: true
```
