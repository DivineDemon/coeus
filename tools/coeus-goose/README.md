# Coeus + Goose

Local agent chat over your Obsidian vault — no Cursor tokens, no Docker.

## Stack

```text
Goose (desktop or CLI)
  ├── Ollama qwen3:8b (or any model you set)
  ├── MemPalace MCP (vault memory + knowledge graph)
  └── Coeus filesystem MCP (read/write markdown)
```

Config: `~/.config/goose/config.yaml`  
Permissions: `~/.config/goose/permission.yaml`  
Project hints: `.goosehints` in vault root

**Global extensions (secretary core):** `developer`, `mempalace`, `coeus-filesystem`, `tom`, `skills`, `code_execution`, `todo`, `chatrecall`, `computercontroller`, `playwright`. Recipe-scoped extensions (`github`, `neon`, `vercel`, `pdfreader`, `reddit`, etc.) are installed but disabled globally — enable per-recipe only.

## Secretary skills

Playbooks live in `tools/coeus-goose/skills/` (seven `SKILL.md` files). Goose discovers them via symlinks:

- `.goose/skills` → `tools/coeus-goose/skills`
- `.agents/skills` → `tools/coeus-goose/skills`

`start.sh` creates these links automatically. Desktop app: run once:

```bash
mkdir -p .goose .agents
ln -sf ../tools/coeus-goose/skills .goose/skills
ln -sf ../tools/coeus-goose/skills .agents/skills
```

| Skill | Purpose |
|-------|---------|
| `secretary-core` | Persona, vault paths, MemPalace-only memory, caps, audit |
| `job-hunt` | Search, score, apply, job-apply cap |
| `investor-outreach` | Haga/Clearbeam/Ezra cold email |
| `lead-gen` | Serper → Hunter → outreach |
| `social-ops` | Haga Social Autopilot / LinkedIn publish |
| `outbound-send` | n8n webhook contracts |
| `extension-routing` | Per-recipe extension sets; never Goose Memory |

Load via Goose skills extension (`loadSkill`) or ask "load skill secretary-core". Catalog: [[skills/README|skills/README.md]].

**GitHub PAT:** stored via `GITHUB_PERSONAL_ACCESS_TOKEN` env/keyring (not in config). Rotate any PAT that was previously in `config.yaml`.

## Quick start

1. **Ollama** — running with `qwen3:8b` pulled
2. **MemPalace** — indexed: `mempalace mine /Users/mushood/Documents/code/coeus`
3. **Goose** — installed (`brew install --cask block-goose`)

### Option A: Desktop app

Open **Goose.app** → Settings → Provider: **Ollama**, model **qwen3:8b**  
Extensions **mempalace** and **coeus-filesystem** should appear (from config.yaml).  
Open this vault folder as the project directory.

### Option B: Terminal

```bash
chmod +x tools/coeus-goose/start.sh
tools/coeus-goose/start.sh
```

Override model:

```bash
GOOSE_MODEL=qwen3:14b tools/coeus-goose/start.sh
```

Use Ollama Cloud instead of local:

```bash
OLLAMA_HOST=https://ollama.com GOOSE_MODEL=... tools/coeus-goose/start.sh
```

## After editing Obsidian notes

```bash
mempalace mine /Users/mushood/Documents/code/coeus
```

## Secretary recipes

Headless workflows live in `tools/coeus-goose/recipes/` (six YAML files + schedule installer). Validate and run:

```bash
GOOSE=/Applications/Goose.app/Contents/Resources/bin/goose
export GOOSE_RECIPE_PATH="$(pwd)/tools/coeus-goose/recipes"

"$GOOSE" recipe validate tools/coeus-goose/recipes/morning-brief.yaml
"$GOOSE" run --recipe daily-job-hunt.yaml --no-session -q
```

Install UTC cron schedules (morning brief 08:00, job hunt 09:00, investor Mon/Wed/Fri 10:00, leads 11:00, social 14:00):

```bash
tools/coeus-goose/recipes/install-schedules.sh
goose schedule list
```

Catalog: [[recipes/README|recipes/README.md]].

## Secretary n8n webhooks

Goose recipes call n8n for search, enrich, send, and audit. Contracts and caps: [[n8n/secretary-webhooks|secretary-webhooks.md]].

```bash
export N8N_BASE=https://self8n.sv.mushoodhanif.com
curl -s -X POST "$N8N_BASE/webhook/secretary-search" \
  -H "Content-Type: application/json" \
  -d '{"query":"your search","num":10}'
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Asks permission instead of searching | Restart Goose after config update; routing rules in `mempalace-routing.md` inject every turn |
| `kg_query` on "mushood" returns empty | Expected — use `mempalace_search` (see `.goosehints`) |
| Tools not working | `GOOSE_TOOLSHIM=true` in config; try `qwen3:14b` |
| MemPalace empty | Run `mempalace mine` on the vault |
| Goose CLI not in PATH | Use `tools/coeus-goose/start.sh` or Desktop app |
| Permission prompts | `GOOSE_MODE: auto` in config; secretary tools in `permission.yaml` `always_allow`; restart Goose after edits |

**Desktop app:** quit and reopen Goose so it reloads `~/.config/goose/config.yaml`. Open this vault as the project folder so `.goosehints` loads.

See [[03-resources/infrastructure/local-llm-memory]] for full MemPalace setup.
