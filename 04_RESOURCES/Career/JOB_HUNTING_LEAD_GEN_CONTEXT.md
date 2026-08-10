# Job Hunting & Lead Generation — Full Context Document

**Generated:** 2026-08-09
**Purpose:** Complete context for automated daily job hunting & lead generation cron job
**Location:** `/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/JOB_HUNTING_LEAD_GEN_CONTEXT.md`

---

## 👤 CANDIDATE PROFILE

### Identity
- **Name:** Mushood Hanif
- **Email:** haga@mushoodhanif.com
- **Current Location:** Pakistan
- **Relocation Preference:** Worldwide (excluding third-world countries)
- **Visa Status:** Requires Skilled Worker sponsorship (UK) or equivalent employer-sponsored visa
- **Role:** Sole Founder, **Haga** — Independent physics verification for physical AI/robotics

### Target Roles (Priority Order)
1. **Senior AI Engineer** — Physical AI, robotics, simulation, world models
2. **ML Engineer** — Production MLOps, model serving, evaluation, fine-tuning
3. **Robotics Engineer** — MuJoCo, Robosuite, sim-to-real, policy optimization
4. **Research Scientist** — World models, physics consistency, video generation verification

### Core Expertise (Evidence-Backed)
| Domain | Specific Technologies | Proof Points |
|--------|----------------------|--------------|
| **Robotics Simulation** | MuJoCo, Robosuite, Isaac Sim, OSC_POSE controllers | haga-core Pillar 1: 4-task adversarial benchmark (Lift/Stack/PickPlaceCan/Door) |
| **World Models** | JAX, CogVideoX, Physics-IQ, CoTracker3 | haga-core Pillar 2: Position-only detectors (permanence, ballistic, contact, static_hover) |
| **Physics Verification** | Adversarial stress testing, tiered severity (mild/moderate/severe), held-out protocols | Frozen held-out protocol v1 (2026-07-19); CogVideoX I2V seeds 2-4, n=9 |
| **MLOps/Production** | vLLM, QLoRA/PEFT, dynamic batching, adapter swapping, Prometheus, PSI drift monitoring | ADCP (92% latency reduction), agbsim (92% latency, 64% cost), rtfsp (<180ms p95, 1.2M/day) |
| **Fine-tuning/Serving** | LLaMA-3 8B, 4-bit NF4, bitsandbytes, ONNX INT8 quantization | oplftsf (6 wks → 9 days), brsc (470MB → 117MB), ue-sc (89% on 12k tickets) |
| **Search/RAG** | FAISS HNSW, sentence-transformers, TF-IDF reranking, active learning | brsc, faq-srp (62% → 80%), fbf-re (340ms → 60ms) |
| **ML Orchestration** | LangGraph (6-agent), MCP (9 tools), Celery/Redis, FastAPI, Next.js | ADCP, RTFSP, CRM pipeline board |

---

## 🏗️ HAGA — THE VENTURE (Primary Asset)

### What It Is
Independent third-party physics verification layer for physical AI/robotics companies. Not tied to any simulator vendor. Objective physics audits before deployment.

### Two Technical Pillars
| Pillar | Focus | CLI | Key Innovation |
|--------|-------|-----|----------------|
| **1. Policy Stress-Testing** | Mass/friction randomization on robosuite Lift/Stack/PickPlaceCan/Door with scripted OSC_POSE baselines | `haga-benchmark` | Tiered stress (mild/moderate/severe), independent RNG per tier, geom_priority=1 on stressed objects |
| **2. Physics-Consistency Scoring** | Position-only detectors validated on MuJoCo GT, applied to tracked video (Physics-IQ, CogVideoX) | `haga-worldmodel`, `haga-physicsiq` | Sliding quadratic fits (window 11) for acceleration; VIDEO_CHECKS profile with static_hover |

### Metrics Pipeline (Hard Invariant)
```
haga-core results/ → haga-publish-public → GitHub Release `metrics-latest`
    → @haga/metrics client (GitHub Releases Assets API + PAT)
    → apps/site LabHub + apps/dataroom EvidenceCharts (IDENTICAL NUMBERS)
```

### Web Stack (haga-web monorepo)
| App | Framework | Purpose | Auth |
|-----|-----------|---------|------|
| **site** | Astro 7 + React 19 | Public marketing + Lab (experiments, charts) | None (public) |
| **dataroom** | Astro 7 + Auth.js (NextAuth v5) | Investor diligence room | Staged: founders-only → external-sharing (4 gates) |
| **crm** | Next.js 16 (App Router) | Internal CRM | NextAuth v5 credentials |

### Shared Packages
- **@haga/brand** — Design tokens (CSS vars), chart theme, `cn()` utility, Fraunces/Inter fonts
- **@haga/metrics** — Typed client fetching from GitHub Releases (fixtures fallback)

### CRM Data Sources (Operational, Not Empty)
- `dataroom/content/03_Commercial/DESIGN_PARTNERS.mdx`
- `dataroom/content/03_Commercial/PIPELINE_LOG.mdx`
- `docs/business/investor-raise-targets.md`
- All private assets in CRM vault — never exposed publicly

---

## 💼 PRIORITY TARGET COMPANIES (17) — UK Sponsor License Holders

| # | Company | Location | Domain | Strategic Fit |
|---|---------|----------|--------|---------------|
| 1 | JBS Applied A.I & Robotics Research Ltd | London | jbs-ai-robotics.com | Applied AI/robotics research — sim-to-real, policy optimization |
| 2 | Shadow Robot Company Ltd | London | shadowrobot.com | Dexterous Hand, teleoperation — needs physics verification |
| 3 | Apollo Research AI Ltd | London | apolloresearch.ai | AI safety/interpretability — adversarial stress testing complements alignment |
| 4 | CGA Simulation Ltd | Liverpool | cga-simulation.com | Defense/simulation, synthetic data — physics validation critical |
| 5 | HPi Verification Services Ltd | Wallingford | hpi-verification.com | Verification services — direct domain overlap |
| 6 | Fieldwork Robotics Limited | Cambridge | fieldworkrobotics.com | Agricultural robotics — deformable object manipulation |
| 7 | Oxford Robotics Ltd | Reading | oxfordrobotics.institute | Mobile autonomy, legged locomotion — dynamic physics verification |
| 8 | Prosper Robotics Ltd | London | prosper-robotics.com | Home robotics — adversarial stress testing for domestic safety |
| 9 | Perceptual Robotics Limited | Bristol | perceptualrobotics.com | Wind turbine inspection drones — GPS-denied physics verification |
| 10 | Extend Robotics Limited | London | extendrobotics.com | Human-robot interface, teleoperation — sim-to-operator mental model |
| 11 | Human Digital Twin Limited | London | humandigitaltwin.com | Biomechanical simulation — human motion physics validation |
| 12 | Mistral AI UK Limited | London | mistral.ai | Frontier models — physics grounding for code/simulation generation |
| 13 | Stability AI Ltd | London | stability.ai | Video/3D generation — CogVideoX verification for physical plausibility |
| 14 | Tecosim Technical Simulation Ltd | Basildon | tecosim.com | CAE/simulation for automotive/aerospace — simulation fidelity validation |
| 15 | The Simulator Company Limited | London | thesimulatorcompany.com | Simulation platform — physics consistency as a service |
| 16 | General Physics (UK) Ltd | London | generalphysics.com | Scientific consulting — AI-driven simulation verification |
| 17 | Innovative Physics Limited | Shanklin | innovativephysics.co.uk | Radiation/physics simulation + AI — AI-generated simulation verification |

---

## 📧 OUTREACH PERSONALIZATION TEMPLATES

### Company-Specific Tech Overlaps (Pre-Written)
Each company in the priority list has a tailored `tech_overlap` paragraph in `run_automation.py:150-168` connecting Haga's capabilities to their specific domain. Examples:

- **Shadow Robot:** "Dexterous Hand and teleoperation systems are exactly the kind of physical AI platforms that need independent physics verification. My MuJoCo/Robosuite expertise and CogVideoX-based world model validation could strengthen your sim-to-real pipeline."
- **Apollo Research:** "Adversarial policy stress testing for physical systems complements your alignment work — ensuring policies don't just optimize reward but respect physical laws."
- **Stability AI:** "Stable Video Diffusion and 3D assets need physics consistency. CogVideoX verification expertise directly applies to ensuring generated dynamics are physically plausible."

### Email Template Structure
```
Subject: Physics verification for {company}'s physical AI systems — Mushood Hanif (Haga founder)

Body:
- Personal intro: Founder of Haga, independent physics verification
- Company-specific tech overlap (pre-written per domain)
- Job reference (if found via Serper) OR generic value proposition
- Why Haga matters (4 bullet points: physics consistency, adversarial stress testing, video verification, independent third-party)
- Background: 7+ years robotics simulation, world models, physics consistency, adversarial testing
- Visa: Requires Skilled Worker sponsorship (UK), company on Home Office A-rated sponsor register
- CTA: Brief call to explore verification value or role fit
```

---

## 🤖 AUTOMATION SYSTEM (coeus/)

### Daily Cron Job (Mon-Fri, 12:00 PKT)
**Script:** `/Users/mushood/Documents/code/personal/coeus/run_automation.py`

### Pipeline Steps
1. **Serper Search** — Query: `site:{domain} (job OR career OR hiring OR "software engineer" OR "robotics engineer" OR "ML engineer" OR "research scientist" OR "AI engineer")`
   - Filters for engineering roles in title/snippet
   - Top 5 results per company
   - Fallback if API credits exhausted

2. **Hunter.io Enrichment** — Domain search for personal emails
   - Filters for engineering/hiring/leadership roles (keywords: engineer, hiring, talent, recruit, hr, people, lead, head, director, vp, cto, founder, manager, principal, senior, staff, tech, research, science, robotics, ai, ml, machine learning, simulation, physics)
   - Top 3 contacts by confidence score

3. **Draft Generation** — Personalized .md files in `01_INBOX/outreach_drafts/`
   - Filename: `{DATE}_{CompanyName}_{FirstName}_{LastName}.md`
   - Includes company-specific tech overlap + job reference (if found)

4. **Output Persistence**
   - `04_RESOURCES/Career/job_matches_{DATE}.json`
   - `04_RESOURCES/Career/enriched_contacts_{DATE}.json`
   - `04_RESOURCES/Career/automation_log_{DATE}.json`

### Required Environment Variables (`.env.local`)
```
SERPER_API_KEY=...
HUNTER_API_KEY=...
RESEND_API_KEY=...
```

### Rate Limiting
- 1 second delay between companies
- Serper credits monitored; graceful fallback to Hunter-only mode

---

## 📁 KEY FILE PATHS

| Purpose | Path |
|---------|------|
| Automation script | `/Users/mushood/Documents/code/personal/coeus/run_automation.py` |
| Outreach drafts | `/Users/mushood/Documents/code/personal/coeus/01_INBOX/outreach_drafts/` |
| Career data (JSON) | `/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/` |
| Lead templates | `/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/lead_templates/` |
| Outreach templates | `/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/outreach_templates/` |
| Haga monorepo | `/Users/mushood/Documents/code/haga/` |
| Haga core (Python) | `/Users/mushood/Documents/code/haga/haga-core/` |
| Haga web (TS) | `/Users/mushood/Documents/code/haga/haga-web/` |

---

## 🏷️ CRM INTEGRATION (haga-web/apps/crm)

### Data Models (Prisma)
- **Partner** — ICP, region, fit, motion, priority, stage (9-stage enum), techStack
- **Investor** — Firm, thesisMatch, portfolio, stage (9-stage enum), warmIntroPath
- **PipelineLog** — Unified activity log for partners/investors (countsTowardDemand)
- **Outreach** — Email tracking (sentAt, openedAt, repliedAt, resendId, threadId)
- **InvestorApplication** — Kanban board (Applied/Skipped/Rejected), channel (FORM/EMAIL)
- **DataroomAccess** — Provision/revoke investor access (password stored — needs hashing)
- **Document/Vault** — Categorized, tagged, isPrivate flag (never exposed to dataroom)

### API Endpoints (Relevant)
- `POST /api/webhooks/leads` — Lead ingestion (partner/investor), dedupes by email, protected by `x-webhook-secret`
- `POST /api/dataroom/provision` — Creates DataroomAccess, emails credentials
- `GET/PATCH/DELETE /api/settings/email-accounts` — Resend config (secrets never returned)

### Email Templates (Resend, Haga-branded)
- Fraunces font, #c23030 accent
- Templates in `src/lib/email/resend.ts`

---

## 🔬 RESEARCH PORTFOLIO (Evidence of Depth)

| Project | Repo | Key Result |
|---------|------|------------|
| **ION (PMI-NN)** | `personal/research/ion/` | Inductive invariant for length generalization & depth stability; beats GRU/LSTM/MLP on Dyck/parity/cumsum |
| **ADCP** | `work/adcp/` | 6-agent LangGraph; 92% doc processing time reduction; 81%→96% F1; hallucination 11%→<2% |
| **agbsim** | `work/agbsim/` | CPU→GPU streaming; p95 2.1s→180ms (92%); 64% cost reduction; blue-green canary <5min rollback |
| **brsc** | `work/brsc/` | Urdu/English RAG; FAISS HNSW; INT8 quantization (470MB→117MB); 95+ req/s |
| **faq-srp** | `work/faq-srp/` | TF-IDF reranker + active learning; 62%→80% accuracy; 3000→<200 labeling backlog |
| **fbf-re** | `work/fbf-re/` | Multilingual MiniLM + FAISS HNSW; 340ms→60ms; 80% hallucination reduction; hot-reload |
| **oplftsf** | `work/oplftsf/` | QLoRA + vLLM; 6 weeks→9 days model-to-prod; 45% GPU memory savings; self-service CLI |
| **rtfsp** | `work/rtfsp/` | 1.2M txns/day at <180ms p95; FPR 14%→3.5%; recall +22%; PSI drift; canary rollback |
| **ue-sc** | `work/ue-sc/` | 89% on 12k bilingual tickets; 45% faster retraining; 70% tagging reduction; active learning 93% workload reduction |

---

## ⚙️ TECHNICAL STANDARDS & CONVENTIONS

### Code Quality
- **Biome:** Import sorting, no `console.log`, no empty functions, `--write --unsafe`
- **TypeScript:** Strict mode everywhere (`astro check` / `tsc --noEmit`)
- **Python:** Black (line-length 100, py310), pytest
- **Tailwind v4:** `@theme` directive, CSS variables for design tokens

### Git/Workflow
- Monorepo: pnpm workspaces (`haga-web/`)
- Root scripts: `dev`, `build`, `typecheck`, `lint`, `format`, `deploy`
- PR-driven, CI gates on typecheck + lint

### Deployment
| App | Target | Command | Port |
|-----|--------|---------|------|
| site | Cloudflare Pages | `wrangler pages deploy ./dist` | — |
| dataroom | Cloudflare Pages | `wrangler pages deploy ./dist` | 3001 (dev) |
| crm | Node.js server | `next start` | 3000 |

---

## 🎯 STRATEGIC POSITIONING FOR OUTREACH

### Unique Value Proposition
> **"I build the verification layer that ensures physical AI systems respect physics before they touch the real world."**

### Differentiators (Lead With These)
1. **Physics verification as a service** — Independent third-party, not tied to NVIDIA/Google/Meta simulators
2. **End-to-end ML production experience** — Research (ION) → Fine-tuning (QLoRA) → Serving (vLLM/MCP) → Evaluation → Deployment
3. **Robotics + ML intersection** — Rare combination: MuJoCo/Robosuite expertise + world models + video generation verification
4. **Operational rigor** — Automated pipelines, staged investor access, CRM with real data, evidence-based analysis

### Conversation Starters (Per Company Type)
| Company Type | Hook |
|--------------|------|
| **Robotics OEMs** (Shadow, Fieldwork, Prosper) | "Your robots operate in unstructured environments. Haga finds the sim-to-real gaps before deployment — adversarial stress testing that catches what random sampling misses." |
| **AI Labs** (Apollo, Mistral, Stability) | "Frontier models generate code/simulations/video. Haga verifies the physics is consistent — not just 'looks right' but obeys conservation laws, contact dynamics, ballistic trajectories." |
| **Simulation Vendors** (CGA, Tecosim, The Simulator Company) | "Your customers trust your physics. Haga provides independent validation — a physics audit layer that increases buyer confidence and reduces your support burden." |
| **Verification/Simulation Services** (HPi, General Physics, Innovative Physics) | "Haga's JAX-based world model checking and CogVideoX verification could enhance your toolkit — especially for AI-generated simulation content." |

---

## 📅 CRON JOB SPECIFICATION

### Schedule
- **Frequency:** Daily, Monday–Friday
- **Time:** 12:00 PKT (UTC+5)
- **Timezone:** Pakistan Standard Time (PKT)

### Execution Requirements
- **True sequential execution** — Single cron entry with wrapper script, fail-fast
- **No parallel runs** — Each day completes before next starts
- **Background delivery** — Results saved to files, not requiring interactive session

### Success Metrics (Track in automation_log)
- Companies processed (target: 17)
- Total drafts generated
- Serper API credits status
- Total contacts enriched
- Any errors/warnings

### Failure Handling
- If Serper out of credits → continue with Hunter-only mode (log warning)
- If Hunter fails for a domain → log error, continue to next company
- If draft generation fails → log error, continue
- All partial progress saved to JSON files

---

## 🔄 LEAD GENERATION WORKFLOW (Semi-Automated)

```
Daily Cron (12:00 PKT)
       │
       ▼
Serper Search (jobs) + Hunter.io (contacts)
       │
       ▼
Personalized Draft Generation (.md files)
       │
       ▼
Human Review (Mushood reviews 01_INBOX/outreach_drafts/)
       │
       ▼
Manual Send via Resend (or email client)
       │
       ▼
Track in CRM (Outreach model + PipelineLog)
```

### CRM Population Sources
1. **Dataroom** — DESIGN_PARTNERS, PIPELINE_LOG
2. **Investor targets** — docs/business/investor-raise-targets.md
3. **Automation output** — job_matches, enriched_contacts JSON
4. **Manual entry** — Network referrals, conference contacts

---

## 📋 ACTION ITEMS FOR CRON JOB AGENT

When the scheduled job runs, it should:

1. **Execute `run_automation.py`** — Full pipeline
2. **Verify outputs exist** — Check draft files, JSON logs
3. **Log summary** — Companies processed, drafts generated, any API issues
4. **Alert on anomalies** — Serper credits exhausted, Hunter failures, zero drafts generated
5. **Prepare next-day context** — Save state for continuity

The agent should have access to:
- This context document (JOB_HUNTING_LEAD_GEN_CONTEXT.md)
- The automation script (run_automation.py)
- Environment variables (.env.local)
- Output directories (01_INBOX/outreach_drafts/, 04_RESOURCES/Career/)

---

## 📎 APPENDIX: QUICK REFERENCE

### Haga Core CLI Commands
```bash
haga-benchmark        # Pillar 1: Policy stress testing
haga-worldmodel       # Pillar 2: Checker calibration (MuJoCo GT)
haga-physicsiq        # Pillar 2: Video scoring (CoTracker3 → VIDEO_CHECKS)
haga-publish-public   # Sanitize results → public JSON for web apps
```

### Haga Web Commands
```bash
cd haga-web
pnpm dev:site       # Public site + Lab (port 4321)
pnpm dev:dataroom   # Dataroom (port 3000)
pnpm dev:crm        # CRM (port 3000)
pnpm build          # All apps
pnpm typecheck      # All apps
pnpm lint           # All apps
```

### Key Environment Variables
```bash
# haga-web apps
HAGA_METRICS_BASE_URL=https://github.com/DivineDemon/haga-core/releases/download/metrics-latest
HAGA_METRICS_GITHUB_TOKEN=ghp_...  # Fine-grained PAT, Contents: Read

# Dataroom auth
AUTH_SECRET=...
DATAROOM_FOUNDER_EMAILS=haga@mushoodhanif.com
DATAROOM_INVESTOR_EMAILS=...  # Empty until incorporation gates met
DATAROOM_INVITE_SECRET=...

# CRM
LEAD_WEBHOOK_SECRET=...
RESEND_API_KEY=...
```

### Contact for Questions
- **Primary:** haga@mushoodhanif.com
- **Portfolio:** https://mushoodhanif.com (to be verified)
- **GitHub:** DivineDemon (haga-core, haga-web, and all work/ repos)

---

*This document is the single source of truth for the job hunting & lead generation automation. Update it when any material fact changes.*