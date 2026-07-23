---
name: secretary-core
description: Coeus secretary persona, Obsidian vault paths, rate limits, suppression checks, and audit logging. Use for any outreach, job hunt, lead gen, social ops, or auto-send workflow.
version: 1.0.0
metadata:
  hermes:
    tags: [coeus, secretary, vault, obsidian]
---

# Secretary Core (Hermes + Obsidian)

Foundation playbook. Load before channel skills.

## Memory plane

- **Obsidian vault only** for durable facts: `/Users/mushood/Documents/code/coeus`
- Use builtin **obsidian** skill + `search_files` / `read_file` / `write_file`
- Hermes MEMORY.md is short pointers — write real facts into vault notes

## Vault paths

| Path | Purpose |
|------|---------|
| `02-areas/secretary/icp.md` | Who to target |
| `02-areas/secretary/voice.md` | Tone, structure, sign-off |
| `02-areas/secretary/rate-limits.md` | Daily/weekly caps |
| `02-areas/secretary/suppression-list.md` | Do-not-contact |
| `00-inbox/secretary-queue/` | Pending candidates |
| `03-resources/secretary-log/` | Vault send archive |

## Pre-send checklist

```
- [ ] Searched vault for ICP + voice + caps + suppression
- [ ] Recipient not on suppression list
- [ ] Channel cap not reached
- [ ] ≥2 personalization hooks
- [ ] Copy follows voice.md
- [ ] Send via n8n webhook only
- [ ] Log via secretary-log + vault rollup
```

## Automation split

- **Hermes** — plan, research, personalize, write vault notes, browse
- **n8n** — Serper, Hunter, Gmail, LinkedIn, audit

`N8N_BASE=https://self8n.sv.mushoodhanif.com`

## Cap hit

Stop that channel until next UTC midnight; queue remainder; log `cap_reached`.
