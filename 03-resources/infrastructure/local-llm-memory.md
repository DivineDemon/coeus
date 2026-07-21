---
type: moc
status: active
tags: [infrastructure, ai, mempalace, ollama]
aliases: [Local LLM, Memory Layer]
last_synced: 2026-07-21
---

# Local LLM Memory

Free, local memory over this vault using [MemPalace](https://github.com/MemPalace/mempalace) — no API costs for retrieval.

## Why MemPalace

| Capability | Details |
|------------|---------|
| Retrieval | Structured wings/rooms/drawers, hybrid search |
| Agent UI | [Goose](https://github.com/aaif-goose/goose) + MemPalace MCP + Ollama (free, local) |
| Re-index | `mempalace mine` after vault updates |
| Cost | Free, local |

## Current setup

| Item | Value |
|------|-------|
| Wing | `coeus` |
| Palace data | `~/.mempalace/palace` |
| Config | `mempalace.yaml` (gitignored) |
| Drawers indexed | 356 markdown files |
| Embeddings | Local (CoreML on M2) |

## Daily commands

```bash
# After adding/updating vault notes
mempalace mine /Users/mushood/Documents/code/coeus

# Search vault
mempalace search "what stack does Clearbeam use?" --wing coeus

# Context for new Cursor session (optional)
mempalace wake-up --wing coeus
```

## Agent chat (Goose — recommended)

Free local agent with chat UI. Replaces Cursor for palace-aware work.

**Config:** `~/.config/goose/config.yaml` (Ollama + MemPalace MCP + vault filesystem)  
**Launch:** `tools/coeus-goose/start.sh` or open **Goose.app** with this vault as the project

```bash
# Terminal session (from vault root)
tools/coeus-goose/start.sh

# Or open Goose desktop → Ollama qwen3:8b → chat in this folder
```

After vault edits: `mempalace mine /Users/mushood/Documents/code/coeus`

See [[../../tools/coeus-goose/README|coeus-goose]] for troubleshooting.

Goose is configured to **search MemPalace first** (not `kg_query` on `"mushood"`). Routing rules: `tools/coeus-goose/mempalace-routing.md` + `.goosehints`.

## Cursor MCP (optional)

Add to Cursor MCP settings if you still use Cursor for coding:

```json
"mempalace": {
  "command": "/Users/mushood/.local/bin/mempalace-mcp",
  "args": []
}
```

Then Cursor can search your vault memory directly in chat.

## Optional: Ollama only (no agent)

Retrieval needs no API key. For richer answers, use Ollama separately:

```bash
ollama run qwen3:8b
```

MemPalace retrieval + your local LLM = full free stack on M2 16GB.

## Optional: mine PDFs locally (gitignored folders)

Employment docs, degrees, etc. stay out of git but can be indexed locally:

```bash
uv tool install 'mempalace[extract]'
mempalace mine /Users/mushood/Documents/code/coeus/02-areas/career/companies --mode extract --wing coeus
```

## Related

- [[neon-overview]] · [[n8n-overview]]
- [[03-resources/github-repos/coeus|coeus repo]]
- [[home]]
