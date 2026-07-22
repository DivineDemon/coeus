# Coeus Goose skills

Local secretary playbooks for the Goose **skills** extension. Goose discovers `SKILL.md` files recursively from project skill roots.

## Discovery paths (vault root)

| Symlink | Target (relative) |
|---------|-------------------|
| `.goose/skills` | `../tools/coeus-goose/skills` |
| `.agents/skills` | `../tools/coeus-goose/skills` |

`tools/coeus-goose/start.sh` recreates these symlinks on launch. Open the vault as the Goose project directory.

## Skills catalog

| Skill | Load when |
|-------|-----------|
| `secretary-core` | Any secretary / outreach workflow |
| `job-hunt` | Job search, applications, `daily-job-hunt` |
| `investor-outreach` | Seed/pre-seed cold email for ventures |
| `lead-gen` | B2B discover → enrich → outreach |
| `social-ops` | LinkedIn/X drafts and publish |
| `outbound-send` | Before calling n8n webhooks |
| `extension-routing` | Recipe extension setup, tool bloat |

## Usage in Goose

1. Ensure **skills** extension is enabled (global in `config.yaml`).
2. Ask Goose to load a skill, e.g. "load skill secretary-core" — or invoke `loadSkill` tool.
3. Channel recipes should load `secretary-core` first, then the channel skill.

## Memory rule

**Do not use Goose Memory.** Durable secretary config lives in `02-areas/secretary/` and MemPalace. Skills document this; they do not replace vault notes.

## Env

```bash
export N8N_BASE=https://self8n.sv.mushoodhanif.com
```

Set in shell profile or Goose session env for `outbound-send` curl examples.
