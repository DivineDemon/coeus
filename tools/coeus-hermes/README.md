# Coeus + Hermes

Second-brain secretary: **Hermes** (brain) + **Obsidian vault** (memory) + **n8n** (hands).

```
Hermes Agent (Nous free model)
  ├── Project Coeus → /Users/mushood/Documents/code/coeus
  ├── SOUL.md + memories → vault-first persona
  ├── skills/coeus/* → secretary playbooks
  └── terminal.cwd = vault
n8n @ self8n.sv.mushoodhanif.com
  └── secretary-* webhooks (search / enrich / email / linkedin / log)
```

## Skills

Installed via symlink: `~/.hermes/skills/coeus` → `tools/coeus-hermes/skills/`.

| Skill | Role |
|-------|------|
| `secretary-core` | Persona, vault paths, caps, suppression |
| `outbound-send` | n8n webhook contracts |
| `investor-outreach` | Haga / Clearbeam / Ezra cold email |
| `lead-gen` | Haga B2B pipeline |
| `job-hunt` | Daily applications |
| `social-ops` | LinkedIn publish |

## Daily use

```bash
hermes

hermes -z 'What is Haga? Answer from the vault only.' --yolo
```

Working directory for terminal tools is the vault. Prefer reading `02-areas/secretary/` and `02-areas/startups/` before drafting outreach.

## Webhooks

Contracts: [[n8n/secretary-webhooks|secretary-webhooks.md]].

`N8N_BASE=https://self8n.sv.mushoodhanif.com`

## Agent rules

1. Obsidian vault is the only durable second brain — not Hermes MEMORY.md dumps.
2. Check suppression + rate limits before any send.
3. Send only via n8n webhooks; log to `03-resources/secretary-log/`.
