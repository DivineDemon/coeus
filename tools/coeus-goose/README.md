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
Project hints: `.goosehints` in vault root

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

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Asks permission instead of searching | Restart Goose after config update; routing rules in `mempalace-routing.md` inject every turn |
| `kg_query` on "mushood" returns empty | Expected — use `mempalace_search` (see `.goosehints`) |
| Tools not working | `GOOSE_TOOLSHIM=true` in config; try `qwen3:14b` |
| MemPalace empty | Run `mempalace mine` on the vault |
| Goose CLI not in PATH | Use `tools/coeus-goose/start.sh` or Desktop app |
| Permission prompts | `GOOSE_MODE: smart_approve` — approve write tools carefully |

**Desktop app:** quit and reopen Goose so it reloads `~/.config/goose/config.yaml`. Open this vault as the project folder so `.goosehints` loads.

See [[03-resources/infrastructure/local-llm-memory]] for full MemPalace setup.
