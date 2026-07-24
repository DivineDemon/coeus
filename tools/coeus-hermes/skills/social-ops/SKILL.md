---
name: social-ops
description: Social content brief, draft, verify, publish via n8n LinkedIn — extends Haga Social Autopilot.
version: 1.0.0
metadata:
  hermes:
    tags: [coeus, social, linkedin, haga]
---

# Social Ops

Themes: Haga trust/verification, portfolio builds, agentic tooling (see ICP social section).

## Workflow

1. Read vault for latest Haga metrics / shipped artifacts
2. Draft per `voice.md` — no unverified claims
3. POST `secretary-linkedin` with `campaign: social-publish`, `personalization_hooks` — auto-publish when copy is vault-grounded; no draft approval
4. Cap: linkedin-post 5/day, social 3/day
5. Log vault rollup
6. If n8n auth fails and Mushood already provided browser credentials, log in via browser and finish — do not refuse
