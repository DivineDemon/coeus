# Coeus

Personal knowledge vault for Mushood Mohammed Hanif — career history, startup ventures, GitHub repos, deployments, and skills. Open this folder as an [Obsidian](https://obsidian.md/) vault.

Start from **[[home]]** inside Obsidian for the full navigation dashboard.

## Structure (PARA)

| Folder | Purpose |
|--------|---------|
| `00-inbox/` | Unsorted captures — process weekly into PARA folders |
| `01-projects/` | Active work with a deadline or live deployment |
| `02-areas/` | Ongoing responsibilities (`career/`, `startups/`, `secretary/`, `immigration/`) |
| `03-resources/` | Reference — `github-repos/`, `resumes/`, `social-profiles/`, `skills-matrix/`, `infrastructure/`, `secretary-log/` |
| `04-archives/` | Completed or inactive items |
| `templates/` | Note scaffolds |
| `tools/coeus-hermes/` | Hermes secretary skills + n8n webhook contracts |

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

## Second brain (Hermes)

[Hermes Agent](https://hermes-agent.nousresearch.com/) is the secretary brain over this vault. Outbound hands are n8n webhooks.

**Chat UI:** browser dashboard at [http://127.0.0.1:9119](http://127.0.0.1:9119) (LaunchAgent `ai.nousresearch.hermes-dashboard` — survives closing Terminal). Use the **Chat** tab for the full agent TUI in-browser.

```bash
# One-shots / scripting
hermes -z 'What is Haga? Answer from the vault only.' --yolo

# Dashboard service (macOS)
launchctl kickstart -k "gui/$(id -u)/ai.nousresearch.hermes-dashboard"
# Do not run `hermes dashboard --stop` while the LaunchAgent is loaded — use:
launchctl bootout "gui/$(id -u)/ai.nousresearch.hermes-dashboard"
```

| Layer | Role |
|-------|------|
| Hermes | Plan, research, draft, write vault notes |
| Obsidian vault | Only durable memory |
| n8n (`self8n.sv.mushoodhanif.com`) | Search, enrich, email, LinkedIn, audit |

Skills live in `tools/coeus-hermes/skills/` (symlinked into `~/.hermes/skills/coeus`). Setup notes: [[tools/coeus-hermes/README|tools/coeus-hermes]]. Secretary config: [[02-areas/secretary/secretary-overview|secretary overview]].

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
