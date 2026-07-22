---
name: extension-routing
description: Goose extension selection for Coeus secretary recipes — global core set, recipe-scoped extensions, Memory extension forbidden, Playwright over Chrome DevTools. Use when configuring recipes or troubleshooting tool-schema bloat on local 8B models.
---

# Extension Routing

Local `qwen3-coeus-agent` (8B) breaks with 20+ tool schemas. Keep **≤6–8 extensions per recipe**; use sub-recipes for more.

## Global core (always on)

| Extension | Use |
|-----------|-----|
| `developer` | Shell, file edits |
| `mempalace` | Vault RAG (primary memory) |
| `coeus-filesystem` | Direct markdown R/W |
| `tom` | MemPalace routing every turn |
| `skills` | Load playbooks from `.goose/skills` |
| `code_execution` | Shrink tool surface |
| `todo` | Multi-step tracking |
| `chatrecall` | Past session recall |
| `computercontroller` | Browse when Playwright insufficient |
| `playwright` | Job boards, structured web automation |

## Recipe-scoped (enable only in matching recipe)

| Extension | Recipe |
|-----------|--------|
| `github` | Repo/README research |
| `neon` | Audit log / portfolio DB |
| `vercel` | Deploy checks |
| `pdfreader` | Resume, investor decks |
| `reddit` | Social listening |
| `fetch` | Simple URL pulls |
| `summon` | Heavy multi-step runs |
| `orchestrator` | Parallel subagents |
| `summarize` | Large doc digests |
| `extensionmanager` | Config sessions only |

## Never use for secretary

| Extension | Why |
|-----------|-----|
| `memory` | Duplicate memory plane — use MemPalace + vault |
| `gotohumanmcpserver` | Conflicts with full auto-send |
| `councilofmine` | Needs cloud LLMs |
| `apps` | Desktop UI, not ops |
| `autovisualiser` | Charts, not outreach |
| `tutorial` | Onboarding only |
| `chromedevtools` | Overlaps Playwright — prefer Playwright |

## Recipe extension sets

| Recipe | Extensions beyond core |
|--------|------------------------|
| `secretary.yaml` (router) | core only |
| `daily-job-hunt` | + `fetch` |
| `investor-cold-email` | + `fetch`, `pdfreader` |
| `lead-pipeline` | + `fetch` |
| `social-publish` | + `reddit` (optional) |
| `morning-brief` | core only (+ `chatrecall` already global) |

Recipe files: `tools/coeus-goose/recipes/`. Schedules: `install-schedules.sh`.

## Model selection

| Context | Model |
|---------|-------|
| Default secretary | `qwen3-coeus-agent` |
| Tool-heavy ops recipes | `qwen3-coder:8b` |

Set via `GOOSE_MODEL` in `tools/coeus-goose/start.sh`.

## Code execution vs native tools

| Use | Tool |
|-----|------|
| Load skills | **`loadSkill`** (native) — never inside `execute_typescript` |
| n8n webhooks (search/enrich/send/log) | **`shell`** curl batches — OK inside `code_execution` if batched |
| MemPalace / vault | **`mempalace_search`**, **`coeus-filesystem`** (native) |
| Full secretary run | **`goose run --recipe`** (headless) — most reliable on 8B |

`code_execution` is for **curl/shell batches only**, not for skill loading or MCP tool calls.

## Troubleshooting tool bloat

1. Disable recipe-scoped extensions not needed for current task
2. Load skills via **`loadSkill`** (native tool) instead of dumping all instructions in prompt
3. Use `code_execution` only for batched **curl** to n8n — not for `loadSkill` or MemPalace
4. Never enable `memory` to "remember" secretary prefs — write vault notes instead
