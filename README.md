# Coeus

Personal knowledge vault for Mushood Mohammed Hanif — career history, startup ventures, GitHub repos, deployments, and skills. Open this folder as an [Obsidian](https://obsidian.md/) vault.

Start from **[[home]]** inside Obsidian for the full navigation dashboard.

## Structure (PARA)

| Folder | Purpose |
|--------|---------|
| `00-inbox/` | Unsorted captures — process weekly into PARA folders |
| `01-projects/` | Active work with a deadline or live deployment |
| `02-areas/` | Ongoing responsibilities (`career/`, `startups/`, `immigration/`) |
| `03-resources/` | Reference — `github-repos/`, `resumes/`, `social-profiles/`, `skills-matrix/`, `infrastructure/` |
| `04-archives/` | Completed or inactive items |
| `templates/` | Note scaffolds |
| `tools/coeus-memory/` | Local Ollama RAG harness |

> **Note:** Top-level PARA folders use numbered prefixes (`00-inbox`, etc.) for sort order. All subfolders and files use **kebab-case** (`career-overview.md`, `github-repos/`).

## Obsidian setup

1. Clone this repo and open the root folder in Obsidian.
2. Install community plugins from `.obsidian/community-plugins.json`:
   - **Dataview** — dynamic tables and queries
   - **Templater** — advanced templates
   - **Calendar** — optional daily notes
3. Core plugins (search, graph, backlinks, templates, tags) are pre-enabled.

### Naming conventions

| Item | Convention | Example |
|------|------------|---------|
| Folders | kebab-case | `github-repos/`, `social-profiles/` |
| Files | kebab-case | `resume-ai-engineer.md`, `github-overview.md` |
| Wikilinks | prefer full path for duplicates | `[[02-areas/startups/haga]]` vs `[[03-resources/github-repos/haga]]` |
| Frontmatter | `type`, `status`, `tags`, `url`, `last_synced` | on every note |

## Local AI memory (free — MemPalace)

Uses [MemPalace](https://github.com/MemPalace/mempalace) — local semantic search + Cursor MCP. No API costs.

```bash
uv tool install mempalace
mempalace mine /Users/mushood/Documents/code/coeus   # re-run after vault updates
mempalace search "What startups am I building?" --wing coeus
mempalace wake-up --wing coeus                        # session context for Cursor
```

See [[03-resources/infrastructure/local-llm-memory]] for MCP setup and optional Ollama chat.

## Sync cadence

| Source | Target folder | Method |
|--------|---------------|--------|
| GitHub READMEs | `03-resources/github-repos/` | `gh api` / GitHub CLI |
| Vercel deployments | `01-projects/` | Vercel MCP |
| Social profiles | `03-resources/social-profiles/` | Web fetch / browser |
| Neon databases | `03-resources/infrastructure/` | Neon MCP |
| Google Drive / Notion | `00-inbox/` → process | manual export (see ingestion guides) |

Set `last_synced` in frontmatter when updating a note from an external source.

## License

See [LICENSE](LICENSE).
