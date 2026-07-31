# Hermes Agent Prompt Templates & Workflows

## 1. Investor & Grant Outreach Draft
```markdown
Context: Preparing outreach for [Investor Name / Grant Program]
Goal: Secure pitch meeting or grant submission for Haga.
Variables:
  - Target: {{TARGET_NAME}}
  - Org/Firm: {{ORGANIZATION}}
  - Thesis Alignment: {{THESIS_FOCUS}}
  - Key Metric: {{LAB_METRIC_HIGHLIGHT}} (e.g., "100% recall on physics violation detection in world models")

Instructions for Hermes:
1. Load `02_PROJECTS/haga/investor_pipeline.md` or `grant_tracker.md`.
2. Extract target details and choose template from `04_RESOURCES/outreach_templates/investor_outreach.md`.
3. Customize intro based on target's recent investments/posts.
4. Output draft to `01_INBOX/draft_{{TARGET_NAME}}_email.md` or present directly to user.
```

---

## 2. Lead Discovery & Outreach for AI Services
```markdown
Context: Finding potential founders or business owners needing AI automations or 2nd Brains.
Goal: Prospect qualification and cold email/DM draft.
Variables:
  - Lead Name: {{LEAD_NAME}}
  - Company: {{COMPANY_NAME}}
  - Identified Bottleneck: {{BOTTLENECK}} (e.g., manual data processing, lack of internal AI agent workflow)

Instructions for Hermes:
1. Search web/LinkedIn/X for company size and tech stack.
2. Draft tailored pitch framing 2nd Brain / Agentic Workflow benefits.
3. Record entry in `02_PROJECTS/ai_services/client_pipeline.md` with status `Prospect`.
```

---

## 3. Daily Executive Briefing (WhatsApp)
```markdown
Context: Morning digest sent to user's WhatsApp.
Timing: 08:00 AM Daily

Instructions for Hermes:
1. Query active items in `02_PROJECTS/haga/investor_pipeline.md` and `02_PROJECTS/ai_services/client_pipeline.md` where `next_action_date` = Today.
2. Check `01_INBOX/` for unread/unprocessed files.
3. Format 5-bullet summary.
4. Send via WhatsApp tool interface.
```
