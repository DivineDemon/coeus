---
name: lead-gen
description: B2B lead pipeline for Haga and other campaigns — Serper discover, Hunter enrich, cold email via n8n.
version: 1.0.0
metadata:
  hermes:
    tags: [coeus, leads, b2b, haga]
---

# Lead Gen

Default campaign: **Haga B2B clients** — see `02-areas/secretary/icp.md` section **Haga B2B clients**.

## Pipeline

```
Discover → Enrich → Score → Draft → Send → Log
```

1. POST `secretary-search` with ICP Serper queries (`gl: us` ok)
2. POST `secretary-enrich` — pick confidence ≥80, ICP roles
3. Require ≥2 personalization hooks
4. POST `secretary-email` with `campaign: lead-pipeline`
5. Vault log + queue updates

Hard reject suppression list matches. Stop on HTTP 429.
