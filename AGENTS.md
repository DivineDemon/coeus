# Coeus — AGENTS.md

> **Self-Improving Documentation**: This file is the canonical reference for any agent (human or AI) working in this repository. It must be updated whenever the vault structure, purpose, or conventions change. If you discover something not documented here, add it. If you find something outdated, fix it.

---

## 1. What This Repository Is

**Coeus** (pronounced *SEE-us* or *KOH-us*) is the **personal "Second Brain" vault** for Mushood Hanif, founder of **Haga** (independent physics verification for physical AI/robotics). It is an Obsidian-based knowledge management system augmented with Hermes Agent tooling for autonomous AI-assisted operations.

### Core Identity
- **Owner**: Mushood Hanif (`@mohdmushood` on X, `DivineDemon` on GitHub, `mushood-hanif` on LinkedIn)
- **Location**: `/Users/mushood/Documents/code/personal/coeus` (macOS, Apple Silicon)
- **Primary Interface**: Obsidian (vault) + Hermes Agent (AI automation layer)
- **Version Control**: Git (GitHub: `DivineDemon/coeus`)
- **Sync**: Git + manual; no cloud sync (iCloud, Syncthing, etc.)

### What It Is NOT
- ❌ Not a public documentation site
- ❌ Not a project management tool (though it tracks projects)
- ❌ Not a CRM (though it contains CRM-adjacent data in `04_RESOURCES/Career/`)
- ❌ Not a code repository (code lives in separate repos under `/Users/mushood/Documents/code/`)

---

## 2. The Purpose of This Repository

### Primary Purpose: Cognitive Offloading & Decision Support
Coeus exists to **reduce the cognitive load** of running a deep-tech startup (Haga) while simultaneously managing:
- AI services consultancy pipeline
- Job/investor/partner outreach campaigns
- Technical knowledge accumulation
- Personal productivity & life administration

### Secondary Purposes
| Purpose | Description |
|---------|-------------|
| **Context Persistence** | Provide Hermes Agent (and future agents) with durable, queryable context across sessions |
| **Automation Substrate** | Serve as the data layer for automated outreach, lead enrichment, CRM updates, and reporting |
| **Audit Trail** | Maintain immutable logs of decisions, contacts, and actions for accountability |
| **Knowledge Synthesis** | Enable cross-domain connections (robotics ↔ LLMs ↔ business ↔ physics) via linking |

### The "Why Now"
As a solo founder operating across time zones (Pakistan → global), Mushood needs a system that:
1. Works **asynchronously** (no real-time dependencies)
2. Scales **without hiring** (AI agents do the grunt work)
3. Surfaces **signal from noise** (structured queries > manual search)
4. Survives **context switches** (deep work → outreach → investor calls → coding)

---

## 3. How It Is Organized: The PARA+ Method

Coeus uses a **modified PARA framework** (Projects, Areas, Resources, Archives) with two additions: **00_SYSTEM** (meta-configuration) and **01_INBOX** (capture buffer).

```
coeus/
├── 00_SYSTEM/           # Meta: agent config, credentials, prompts, skills index
├── 01_INBOX/            # Transient capture (processed → PARA within 48h)
├── 02_PROJECTS/         # Active efforts with defined outcomes & deadlines
├── 03_AREAS/            # Ongoing responsibilities (no end date)
├── 04_RESOURCES/        # Reference material, data, templates, archives
├── 05_ARCHIVE/          # Completed/abandoned projects, cold leads, deprecated docs
├── AGENTS.md            # This file
├── LICENSE              # MIT
├── .gitignore
├── .env.local           # Local secrets (NOT committed)
└── .hermes/             # Hermes Agent local state (skills, cron, memory)
```

### Folder Numbering Convention
Prefixes (`00_`, `01_`, etc.) enforce **sort order** in file explorers and `ls` output. Do not rename or reorder.

---

## 4. What It Contains (Deep Dive)

### 00_SYSTEM/ — Agent & Vault Configuration
| File | Purpose | Update Frequency |
|------|---------|------------------|
| `Credentials/accounts.md` | Service accounts, URLs, auth methods (no secrets — refs to 1Password/keychain) | As needed |
| `Credentials/api-keys.md` | API key *names* and scopes (values in `.env.local` or keychain) | As needed |
| `hermes_context.md` | **Master context** for Hermes Agent: user profile, mission, tooling, sync log | Weekly or on major changes |
| `prompt_templates.md` | Reusable prompt snippets for common agent tasks | As needed |
| `skills_index.md` | Index of Hermes skills available to this vault | When skills added/removed |

> **Critical**: `hermes_context.md` is the **single source of truth** for agent identity. If it conflicts with this AGENTS.md, `hermes_context.md` wins for agent behavior; this file wins for vault structure.

### 01_INBOX/ — Capture Buffer
```
01_INBOX/
├── .gitkeep
└── templates/           # Raw templates before promotion to 04_RESOURCES/
```
**Rules**:
- Everything here is **unprocessed**
- Target: **empty** (or < 5 items) at all times
- Processing = move to PARA + add YAML frontmatter + link related items
- Automation: Hermes cron job checks inbox size daily; alerts if > 10 items

### 02_PROJECTS/ — Active Efforts (Defined Outcome + Deadline)
```
02_PROJECTS/
├── ai_services/         # Consultancy pipeline
│   ├── client_pipeline.md     # Active deals: stage, value, next action, decision date
│   └── service_catalog.md     # Standardized offerings, pricing, delivery specs
└── haga/                # Haga startup
    ├── competitors/           # Per-competitor intel (YYYY-MM-DD-name.md)
    ├── grant_tracker.md       # Applications: status, deadlines, artifacts
    ├── haga_index.md          # Master project dashboard (links to all Haga artifacts)
    └── investor_pipeline.md   # Fundraising: stage, amount, terms, next action
```

**Project Criteria** (must have ALL):
- [ ] Clear **outcome** (shippable artifact or decision)
- [ ] **Deadline** (date or milestone)
- [ ] **Owner** (Mushood or delegated agent)
- [ ] **Next action** (always defined)
- [ ] **Status** in YAML frontmatter: `active | on_hold | blocked | done | abandoned`

**Naming**: `kebab-case` for folders; `snake_case.md` for files.

### 03_AREAS/ — Ongoing Responsibilities (No End Date)
```
03_AREAS/
├── Infrastructure/
│   ├── Cloudflare.md      # DNS, WAF, Workers, tunnels config + credentials refs
│   └── Vercel.md          # Deployments, env vars, domains, preview settings
└── Social_Profiles.md     # Consolidated bio/handles/tone for outreach drafting
```

**Area Criteria**:
- Ongoing maintenance/improvement (no "done")
- Has **standards** (not goals): uptime, response time, quality bar
- Reviewed **quarterly** for relevance

### 04_RESOURCES/ — Reference & Data (The Largest Folder)
```
04_RESOURCES/
├── Career/                    # Job hunting, investor/partner outreach, CRM
│   ├── investor_partner_outreach/  # Haga-specific fundraising collateral
│   ├── logos/                 # Company logos for docs/deck
│   ├── skill-logos/           # Tech stack badges for portfolio
│   ├── *.json                 # CRM state, sponsor lists, priority companies
│   ├── resume.pdf/.tex        # Current CV
├── Codebases/                 # Registry of all code repos (external)
│   ├── Freelance_Projects.md
│   ├── Haga_Ecosystem.md
│   ├── Personal_Projects.md
│   └── Work_Enterprise.md
├── haga/                      # Haga-specific reference (non-project)
│   ├── HAGA_LEAD_GENERATION_NOTES.md
│   └── evidence_packet.pdf
├── lead_templates/            # Promoted from inbox
├── outreach_templates/        # Reusable email/LinkedIn templates
├── secretary-log/             # Raw meeting notes, interview transcripts
├── codebase_registry.md       # Master index of all repos + tech stack
└── leadfinder.py              # Core lead discovery module
```

**Resource Criteria**:
- Reference-only (no actions required)
- Versioned or dated
- Linked *from* Projects/Areas, never the reverse

### 05_ARCHIVE/ — Cold Storage
```
05_ARCHIVE/
└── .gitkeep
```
**Archival Triggers**:
- Project `status: done | abandoned` → move folder here
- Lead `status: lost | unresponsive > 90d` → move to `04_RESOURCES/Career/archived_leads/`
- Resource superseded by newer version → move old version here
- **Never delete** — git history is the archive; this is for filesystem cleanliness

---

## 5. Why It Contains What It Contains

### Design Principle: **Separation of Concerns by Temporal Horizon**

| Horizon | Folder | Example Content | Update Cadence |
|---------|--------|-----------------|----------------|
| **Immediate** (days) | `01_INBOX/` | Raw emails, fleeting ideas, web clips | Daily processing |
| **Active** (weeks–months) | `02_PROJECTS/` | Haga fundraising, client delivery | Daily/weekly |
| **Continuous** (years) | `03_AREAS/` | Infra standards, personal brand | Quarterly review |
| **Reference** (indefinite) | `04_RESOURCES/` | Codebase registry, templates, CRM data | As discovered |
| **Historical** (forever) | `05_ARCHIVE/` | Completed projects, old leads | On closure |

### Why This Specific Structure?

1. **Agent-First Design**: Every folder has machine-readable conventions (YAML frontmatter, consistent naming, JSON exports) so Hermes can query/update without parsing prose.

2. **Solo Founder Constraints**: No team to delegate organization to → structure must be self-enforcing via simple rules (numbered prefixes, status fields, inbox zero target).

3. **Haga-Centric**: The startup is the primary "project" → gets top-level folder in `02_PROJECTS/` with its own sub-structure (competitors, grants, investors).

4. **Career as Resource**: Job hunting/investor outreach is *supporting* Haga, not a project itself → lives in `04_RESOURCES/Career/` with heavy automation.

5. **No Duplication**: Code lives in `/Users/mushood/Documents/code/` (separate repos); Coeus only *references* them via `codebase_registry.md` and `Codebases/*.md`.

---

## 6. Updating Methodology

### When to Update
| Trigger | Action |
|---------|--------|
| New project started | Create folder in `02_PROJECTS/` with `haga_index.md` or `client_pipeline.md` entry |
| Project completed/abandoned | Move to `05_ARCHIVE/`; update index files |
| New responsibility acquired | Add to `03_AREAS/` with standards doc |
| New reference material found | Save to `04_RESOURCES/` with date/version in filename |
| Agent behavior needs change | Update `00_SYSTEM/hermes_context.md` + this AGENTS.md |
| Vault structure convention changes | Update this AGENTS.md **first**, then migrate |

### Update Rules
1. **Atomic Commits**: One logical change per commit (structure + content + AGENTS.md if needed)
2. **Frontmatter Discipline**: Every `.md` in PARA folders **must** have YAML frontmatter:
   ```yaml
   ---
   status: active | on_hold | blocked | done | abandoned
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   tags: [tag1, tag2]
   related: [path/to/related.md]
   ---
   ```
3. **Link, Don't Copy**: Use `[[wiki-links]]` or relative paths; never duplicate content.
4. **Date-Stamp Data Files**: Versioned reference files only
5. **No Secrets in Repo**: `.env.local` is gitignored; credentials reference external stores.

### Migration Protocol (When Structure Changes)
1. Document the change in this AGENTS.md
2. Create migration script in `04_RESOURCES/Career/automation_scripts/migrate_YYYYMMDD.py`
3. Run script, verify with `git diff --stat`
4. Commit: `chore: migrate [description] per AGENTS.md vX.Y`

---

## 7. Usage Methodology

### For Humans (Mushood)
| Workflow | Tools | Frequency |
|----------|-------|-----------|
| **Daily Capture** | Obsidian Quick Capture, email forward, browser clipper | Continuous |
| **Inbox Processing** | Obsidian (drag/drop, frontmatter template) | Daily AM / PM |
| **Project Review** | `02_PROJECTS/` folder scan, update `next_action` | Weekly (Sunday) |
| **Area Standards Review** | `03_AREAS/` read-through | Quarterly |
| **Resource Curation** | Save to `04_RESOURCES/` with tags | As found |
| **Agent Supervision** | Hermes chat, review cron outputs | Daily |

### For Hermes Agent (Autonomous)
| Capability | Implementation | Config Location |
|------------|----------------|-----------------|
| **Context Loading** | Reads `00_SYSTEM/hermes_context.md` + this AGENTS.md on session start | `hermes_context.md` |
| **Cron Jobs** | Scheduled automation (outreach, enrichment, CRM sync) | `~/.hermes/cron/` + `cronjob` tool |
| **Browser Automation** | CDP at `http://127.0.0.1:9222` for Gmail/LinkedIn | `hermes_context.md:41` |
| **Alerts** | Saved to vault logs (no push channel) | — |
| **Code Execution** | Local Python/Bash via terminal tool | Native |
| **Memory Persistence** | SQLite in `~/.hermes/` + this vault's memory | `hermes_context.md:43` |

### Agent Operating Rules (Enforced via `hermes_context.md`)
1. **Auto-send enabled** for drafted outreach (no human approval gate)
2. **Vault root** = `/Users/mushood/Documents/code/personal/coeus`
3. **SSOT** = `02_PROJECTS/`, `03_AREAS/`, `04_RESOURCES/`
4. **YAML frontmatter mandatory** on all lead/project files
5. **Inbox processing** = move to PARA + enrich metadata

---

## 8. Organization Methodology

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Folders (PARA) | `NN_CATEGORY/` (numbered) | `02_PROJECTS/haga/` |
| Project subfolders | `kebab-case` | `competitors/` |
| Markdown files | `snake_case.md` | `grant_tracker.md` |
| Dated files | `YYYY-MM-DD-descriptor.md` | `2026-08-09-competitor-intel.md` |
| JSON exports | `descriptor_YYYY-MM-DD.json` | `reference_data_2026-08-09.json` |
| Python scripts | `snake_case.py` | `data_processing.py` |
| Tags (YAML) | `kebab-case` | `haga`, `outreach`, `investor` |

### Linking Strategy
- **Wiki-links** (`[[page-name]]`) for Obsidian graph view
- **Relative paths** (`../03_AREAS/Infrastructure/Cloudflare.md`) for portability
- **No absolute paths** except in `hermes_context.md` (agent config)
- **Backlinks maintained**: If A links to B, B should have `related:` pointing to A

### Metadata Standards
**Required YAML frontmatter on all PARA `.md` files**:
```yaml
---
status: active | on_hold | blocked | done | abandoned
created: 2026-08-10
updated: 2026-08-10
tags: [primary-tag, secondary-tag]
related: 
  - path/to/related-file.md
  - path/to/another.md
owner: mushood | agent:hama | agent:hermes
next_action: "Specific, actionable, time-bounded"
deadline: 2026-08-15  # optional, for projects
---
```

### Tag Taxonomy (Controlled Vocabulary)
| Category | Tags |
|----------|------|
| **Domain** | `haga`, `ai-services`, `career`, `personal`, `infra` |
| **Type** | `project`, `area`, `resource`, `template`, `log`, `draft` |
| **Stage** | `discovery`, `drafting`, `review`, `sent`, `replied`, `closed-won`, `closed-lost` |
| **Priority** | `p0-critical`, `p1-high`, `p2-medium`, `p3-low` |
| **Automation** | `auto-generated`, `needs-review`, `verified` |

---

## 9. Organization Usage Methodology

### Creating a New Project
```bash
# 1. Create folder structure
mkdir -p 02_PROJECTS/new-project/{assets,notes}

# 2. Create index file with frontmatter
cat > 02_PROJECTS/new-project/new_project_index.md << 'EOF'
---
status: active
created: 2026-08-10
updated: 2026-08-10
tags: [haga, project]
related: []
owner: mushood
next_action: "Define success criteria and milestone dates"
deadline: 2026-09-10
---

# New Project

## Outcome
[Clear, measurable definition of done]

## Milestones
- [ ] M1: ... (date)
- [ ] M2: ... (date)

## Resources
- [[04_RESOURCES/...]]
EOF
```

### Processing Inbox Items
1. Open `01_INBOX/` in Obsidian
2. For each item:
   - **Actionable + dated** → `02_PROJECTS/` (new or existing)
   - **Actionable + recurring** → `03_AREAS/` (update standards)
   - **Reference** → `04_RESOURCES/` (tag, date, link)
   - **Trash** → Delete
3. Add frontmatter + `related:` links
4. Move file (drag/drop or `mv`)

### Adding a Resource
```bash
# Example: New competitor intel
cp source.pdf 04_RESOURCES/haga/competitors/2026-08-10-new-competitor.pdf
# Create companion .md with frontmatter + summary + tags
```

### Archiving a Project
```bash
# 1. Update status in index file
# status: done (or abandoned)

# 2. Move folder
mv 02_PROJECTS/old-project 05_ARCHIVE/2026-08-10_old-project

# 3. Update any referencing files' related: links
```

---

## 10. Best Practices for This Repo

### 🟢 DO
- ✅ Keep `01_INBOX/` near empty (process daily)
- ✅ Write YAML frontmatter **first** when creating files
- ✅ Use `related:` links bidirectionally
- ✅ Date-stamp all data exports (`_YYYY-MM-DD.json`)
- ✅ Reference code repos via `codebase_registry.md` (not symlinks)
- ✅ Update `updated:` field on every edit
- ✅ Commit after each logical session (human or agent)
- ✅ Let Hermes manage `04_RESOURCES/Career/` automation outputs
- ✅ Store secrets in `.env.local` or 1Password (ref only in vault)

### 🔴 DON'T
- ❌ Put code in this repo (code → `/Users/mushood/Documents/code/`)
- ❌ Duplicate content (link instead)
- ❌ Use spaces in filenames (use `-` or `_`)
- ❌ Commit `.env.local`, `__pycache__/`, `.DS_Store`, `.hermes/`
- ❌ Leave `status:` undefined on PARA files
- ❌ Create folders without a clear PARA category
- ❌ Edit automation outputs manually (re-run the script instead)
- ❌ Hardcode absolute paths (except in `hermes_context.md`)

### ����� AUTOMATION BEST PRACTICES
1. **Scripts output to versioned files** → `04_RESOURCES/Career/reference_data_YYYY-MM-DD.json`
2. **Scripts read from vault** → use relative paths from repo root
3. **Scripts write to vault** → only `04_RESOURCES/Career/` and `01_INBOX/`
4. **Cron jobs are idempotent** → safe to re-run
5. **Agent edits use `patch` tool** → not `write_file` (preserves history)

---

## 11. Critical Reference Files (Quick Access)

| File | Purpose | Last Verified |
|------|---------|---------------|
| `00_SYSTEM/hermes_context.md` | Agent identity, mission, tooling | 2026-08-10 |
| `04_RESOURCES/codebase_registry.md` | All external repos index | 2026-08-10 |
| `02_PROJECTS/haga/haga_index.md` | Haga master dashboard | 2026-08-10 |
| `02_PROJECTS/ai_services/client_pipeline.md` | Consultancy pipeline | 2026-08-10 |
| `03_AREAS/Social_Profiles.md` | Unified bio for outreach | 2026-07-31 |

---

## 12. Version History & Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-08-10 | Hermes Agent (Mushood) | Initial creation from vault analysis |
| 1.1 | 2026-08-10 | Mushood | [Update after review] |

> **Next Review**: 2026-08-17 (weekly) or on next structural change

---

## 13. Appendices

### A. Hermes Agent Skills Loaded for This Vault
(From `00_SYSTEM/skills_index.md` and `hermes_context.md`)
- `hermes-agent` (core)
- `github-*` (repo management, PRs, issues)
- `computer-use` (background desktop control)
- `web_search` / `web_extract` (research)
- `terminal` / `execute_code` (automation)
- `cronjob` (scheduled tasks)
- `memory` (cross-session persistence)
- `delegate_task` (sub-agents)
- Obsidian, Notion, Google Workspace integrations

### B. External Dependencies
| System | Purpose | Access |
|--------|---------|--------|
| Obsidian | Primary UI for vault | Local app |
| GitHub (`DivineDemon/coeus`) | Version control + backup | HTTPS/SSH |
| Hermes Agent | AI automation layer | Desktop app |
| Chrome CDP (`:9222`) | Browser automation | Local browser |
| Hermes Gateway | Cron job execution | Local daemon |
| 1Password / Keychain | Secret storage | CLI (`op`) |

### C. Glossary
| Term | Definition |
|------|------------|
| **PARA** | Projects, Areas, Resources, Archives (Tiago Forte) |
| **SSOT** | Single Source of Truth |
| **Haga** | Mushood's startup: physics verification for physical AI |
| **Coeus** | This vault (Greek Titan of intellect & inquiry) |
| **Inbox Zero** | `01_INBOX/` contains ≤ 5 unprocessed items |
| **Frontmatter** | YAML metadata block at top of `.md` files |
| **Wiki-link** | Obsidian `[[page-name]]` internal link |

---

## 14. Self-Improvement Protocol

> **This file is alive.** If you (human or agent) encounter:
> - A convention not documented here → **Add it**
> - A documented convention that's wrong → **Fix it**
> - A missing cross-reference → **Link it**
> - A better way to organize → **Propose it in `01_INBOX/`, then migrate**

**Update Checklist** (run before committing changes to this file):
- [ ] Does the change reflect *actual* vault state?
- [ ] Are all folder paths accurate?
- [ ] Are YAML frontmatter examples current?
- [ ] Is the version history updated?
- [ ] Have you told Hermes to reload context? (`hermes_context.md` + this file)

---

*End of AGENTS.md — This file is the contract between the vault, the human, and the agents. Honor it.*