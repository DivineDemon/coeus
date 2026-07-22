---
name: secretary-core
description: Coeus secretary persona, vault paths, MemPalace-first memory (never Goose Memory), rate limits, suppression checks, and audit logging. Use for any outreach, job hunt, lead gen, social ops, or auto-send workflow.
---

# Secretary Core

Foundation playbook for Coeus secretary recipes. Load this before channel-specific skills.

## How to load skills (critical — do not use Code Mode)

Skills are **markdown playbooks**, not JavaScript functions. There is no `investorColdEmail()` or `load_skill()` in code.

1. Call the **`loadSkill`** tool (skills extension) once per skill — **top-level tool call only**.
2. **Never** call `loadSkill`, `load_skill`, or skill names inside **`execute_typescript` / `code_execution`** — the sandbox has no Goose tools (`ReferenceError: load_skill is not defined`).
3. For full outreach runs, prefer **`goose run --recipe`** (recipes embed instructions; loading skills in chat is optional).

**Chat sequence:** `loadSkill` → `secretary-core` → channel skill → `outbound-send` → `mempalace_search` → **`shell` curl** to n8n webhooks.

## Memory plane (critical)

- **MemPalace + Obsidian only** — search `wing: coeus` before drafting or sending.
- **Never enable or use Goose Memory** — durable prefs live in vault notes, not `.goose/memory/`.
- After editing secretary vault notes: `mempalace mine /Users/mushood/Documents/code/coeus`

## Vault paths

| Path | Purpose |
|------|---------|
| `02-areas/secretary/icp.md` | Who to target per channel |
| `02-areas/secretary/voice.md` | Tone, structure, sign-off |
| `02-areas/secretary/rate-limits.md` | Daily/weekly caps (hard stops) |
| `02-areas/secretary/suppression-list.md` | Do-not-contact |
| `00-inbox/secretary-queue/` | Pending candidates |
| `03-resources/secretary-log/` | Vault-side send archive |

## Pre-send checklist

```
- [ ] mempalace_search ICP + voice + caps + suppression (wing=coeus)
- [ ] Recipient not on suppression list
- [ ] Channel cap not reached (see rate-limits.md)
- [ ] ≥2 personalization hooks (see icp.md)
- [ ] Copy follows voice.md (no filler, one venture angle)
- [ ] Send via n8n webhook only (not raw Gmail/LinkedIn APIs in Goose)
- [ ] Log success via secretary-log + vault rollup
```

## Automation split

- **Goose** — plan, research, personalize, queue vault notes, browse
- **n8n** — Serper search, Hunter enrich, Gmail send, LinkedIn publish, Sheets/Neon audit

## Cap hit behavior

1. Stop sending for that channel until next UTC midnight.
2. Move queue items to tomorrow — do not delete.
3. Log `cap_reached` via `secretary-log` webhook.
4. `mempalace_diary_write` brief note.

## Related skills

- `job-hunt`, `investor-outreach`, `lead-gen`, `social-ops` — channel workflows
- `outbound-send` — n8n webhook contracts
- `extension-routing` — which Goose extensions to enable per recipe
