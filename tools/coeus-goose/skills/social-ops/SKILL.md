---
name: social-ops
description: Social content brief, draft, verify, and publish via n8n — extends Haga Social Autopilot pattern for LinkedIn and X. Use for social-publish recipe or daily social queue at 14:00 UTC.
---

# Social Ops

Aligns with **Haga Social Autopilot** (n8n, 14:00 UTC): research → rank → draft → verify → queue/publish.

## Channels and caps

| Channel | Cap (UTC day) | Webhook |
|---------|---------------|---------|
| LinkedIn post | 5 | `secretary-linkedin` |
| Social queue (sheet) | 3 | `channel: social` |
| X | Manual or recipe-specific | — |

## Content themes

- Haga trust/verification, simulation vs hardware honesty
- Portfolio builds, agentic tooling, n8n automation case studies
- Audience: robotics builders, AI engineers, indie hackers

Search MemPalace for facts: `mempalace_search("Haga social benchmark deployment", wing=coeus)`

## Workflow

```
1. mempalace_search venture facts + prior posts (wing=coeus)
2. secretary-search / arXiv / repo README for novelty
3. Draft per voice.md channel limits:
   - LinkedIn: 1–3 short paragraphs, evidence-backed
   - X: ≤280 chars unless thread explicitly allowed
4. Claim verification — no inflated metrics; sim vs hardware clear for Haga
5. POST secretary-linkedin (personalization_hooks required)
6. secretary-log + vault rollup
```

## LinkedIn publish request

```json
{
  "text": "Post copy…",
  "campaign": "social-publish",
  "channel": "linkedin-post",
  "personalization_hooks": ["product launch", "benchmark artifact"],
  "title": "Optional for article posts",
  "original_url": "https://example.com/post",
  "post_as": "person",
  "visibility": "PUBLIC"
}
```

## Haga Autopilot integration

- Autopilot queues approved drafts to Google Sheets at 14:00 UTC
- Goose `social-publish` recipe can inject on-demand posts via same webhook path
- Do not duplicate posts already in today's sheet queue — search queue first

## Forbidden

- Mentioning MemPalace, Goose, or internal tooling in public posts
- "Revolutionary", fake urgency, copy-paste templates without customization
