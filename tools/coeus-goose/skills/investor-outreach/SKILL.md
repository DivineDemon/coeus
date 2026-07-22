---
name: investor-outreach
description: Cold investor email workflow for Haga, Clearbeam, and Ezra — ICP targeting, MemPalace personalization, voice-compliant copy, auto-send via n8n, and investor batch caps. Use for investor-cold-email recipe or seed/pre-seed outreach.
---

# Investor Outreach

## Ventures in rotation

Search MemPalace before drafting: `mempalace_search("Haga Clearbeam Ezra startup wedge deployment", wing=coeus)`

| Venture | Angle |
|---------|-------|
| Haga | Robotics / physical-AI verification, simulation benchmarks |
| Clearbeam | Dev from vault — repo + deployment notes |
| Ezra Bid Assistant | Dev from vault — repo + deployment notes |

**One primary venture per email** — never dual-pitch.

## Target investor ICP

- Pre-seed / seed funds and angels: AI, robotics, or devtools thesis
- Portfolio in agents, simulation, or B2B SaaS
- Warm intro preferred; cold only when personalization ≥2 hooks

**Exclude:** generic blast lists, explicit no-cold-email funds, suppression list matches.

## Research workflow

```
1. mempalace_search venture facts + prior outreach (wing=coeus)
2. secretary-search → fund portfolio, recent investments, partner posts
3. secretary-enrich → partner email if domain known
4. Score: fund thesis fit + hook availability + not duplicate
5. Draft email (voice.md structure)
6. POST secretary-email (channel: email, campaign: investor-cold-email)
7. secretary-log + vault log + update queue
```

## Email structure (voice.md)

1. **Hook** — why them, why now (from research)
2. **Credibility** — one shipped artifact or venture fact from vault
3. **Ask** — single CTA (15-min call or intro)
4. **Sign-off** — `Best,\nMushood Hanif` (+ optional one venture link)

≤150 words body; subject ≤60 chars; no attachments on first touch.

## Personalization minimum

Require ≥2 of:

1. Specific fund/portfolio company reference
2. Recent public artifact (post, investment, thesis piece)
3. Mutual connection or shared community
4. Clear tie to one venture or shipped project

Fewer than two → leave in `00-inbox/secretary-queue/` for more research.

## Caps

| Limit | Value |
|-------|-------|
| Cold email (all campaigns) | 20/day UTC |
| Investor batch runs | 3/week max (e.g. Mon/Wed/Fri) |

## Campaign field

Always set `campaign: investor-cold-email` on webhook calls for audit traceability.
