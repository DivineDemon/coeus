---
type: area
status: active
tags: [secretary, icp, outreach]
last_synced: 2026-07-22
aliases: [Ideal Customer Profile, Secretary ICP]
---

# ICP — Ideal targets

Who the secretary should pursue per channel. Update when strategy shifts; re-mine after edits.

## Job hunt

**Target roles:** AI Engineer, ML Engineer, Full-stack with AI/agentic focus.

| Signal | Fit |
|--------|-----|
| Stack overlap (Python, TypeScript, LLM/RAG, agents) | High |
| Remote or UAE-friendly | Required |
| Early-stage startup or product team | Preferred |
| Pure infra/SRE with no AI surface | Low — skip |

**Sources:** LinkedIn, Wellfound, company career pages, YC jobs, remote boards.

**Resume pick:** [[03-resources/resumes/resume-ai-engineer|AI Engineer]] vs [[03-resources/resumes/resume-fullstack|Fullstack]] — match job description; see [[02-areas/career/resume-conflicts|resume conflicts]].

**Exclude:** Roles requiring clearance, on-site-only outside target regions, or factual conflicts with resume claims.

## Investor outreach

**Ventures in rotation:**

| Venture | Angle | Evidence |
|---------|-------|----------|
| [[02-areas/startups/haga\|Haga]] | Robotics / physical-AI verification, simulation benchmarks | Public site, benchmark artifacts |
| [[02-areas/startups/clearbeam\|Clearbeam]] | (Update with current wedge) | Repo + deployment notes |
| [[02-areas/startups/ezra-bid-assistant\|Ezra Bid Assistant]] | (Update with current wedge) | Repo + deployment notes |

**Target investor profile:**

- Pre-seed / seed funds and angels with AI, robotics, or devtools thesis
- Prior portfolio in adjacent space (agents, simulation, B2B SaaS)
- Warm intro preferred; cold only when personalization score ≥ threshold (see voice note)

**Exclude:** Generic blast lists, investors with explicit no-cold-email policy, duplicates on suppression list.

## Lead gen (B2B pipeline)

Pattern from inactive Duqm workflows — generalize for future campaigns.

| Field | Guidance |
|-------|----------|
| Company size | SMB to mid-market unless campaign-specific |
| Geography | Campaign-specific (e.g. GCC for regional plays) |
| Trigger | Hiring signal, funding, product launch, pain point from search |
| Enrichment | Hunter via n8n `secretary-enrich` webhook |

**Score before outreach:** company fit + contact role + personalization hooks available.

## Social ops

**Channels:** LinkedIn (company + personal), X — aligned with [[03-resources/infrastructure/n8n-overview|Haga Social Autopilot]].

**Content themes:** Haga trust/verification, portfolio builds, agentic tooling, n8n automation case studies.

**Audience:** Robotics builders, AI engineers, indie hackers, n8n community.

## Personalization minimum (all channels)

Before auto-send, require at least **two** of:

1. Specific company or role reference
2. Recent public artifact (post, launch, job listing)
3. Mutual connection or shared community
4. Clear tie to one of Mushood's ventures or shipped projects

If fewer than two hooks — **do not send**; leave in queue for manual review or more research.

## Related

- [[02-areas/secretary/secretary-overview|Secretary overview]]
- [[02-areas/secretary/voice|Voice]]
- [[02-areas/secretary/suppression-list|Suppression list]]
