---
name: investor-outreach
description: Cold investor email for Haga, Clearbeam, Ezra — vault ICP, personalization, n8n auto-send.
version: 1.0.0
metadata:
  hermes:
    tags: [coeus, investors, haga, outreach]
---

# Investor Outreach

## Ventures

Read vault: `02-areas/startups/` and `02-areas/secretary/icp.md`

| Venture | Angle |
|---------|-------|
| Haga | Benchmark-as-a-Service — robotics / physical-AI verification |
| Clearbeam | From vault notes |
| Ezra | From vault notes |

**One primary venture per email.**

## Workflow

1. Search/read vault for venture facts + prior outreach log
2. `secretary-search` for funds / partners
3. `secretary-enrich` when domain known
4. Score: thesis fit + ≥2 hooks + not suppressed
5. Draft per `voice.md` (≤150 words)
6. POST `secretary-email` with `campaign: investor-cold-email` — **auto-send** after steps 1–5; do not wait for confirmation
7. Append `03-resources/secretary-log/YYYY-MM-DD-log.md`

Fewer than 2 hooks → queue in `00-inbox/secretary-queue/`; do not send. Do not ask Mushood to pick targets when research can rank them.
