---
type: area
status: active
tags: [secretary, icp, outreach]
last_synced: 2026-07-22T14:35:00Z
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
| [[02-areas/startups/haga\|Haga]] | Benchmark-as-a-Service (B2B): robotics / physical-AI verification, simulation benchmarks, world-model consistency | [haga.mushoodhanif.com](https://haga.mushoodhanif.com), benchmark artifacts, dataroom |
| [[02-areas/startups/clearbeam\|Clearbeam]] | (Update with current wedge) | Repo + deployment notes |
| [[02-areas/startups/ezra-bid-assistant\|Ezra Bid Assistant]] | (Update with current wedge) | Repo + deployment notes |

**Target investor profile:**

- Pre-seed / seed funds and angels with AI, robotics, or devtools thesis
- Prior portfolio in adjacent space (agents, simulation, B2B SaaS)
- Warm intro preferred; cold only when personalization score ≥ threshold (see voice note)

**Exclude:** Generic blast lists, investors with explicit no-cold-email policy, duplicates on suppression list.

## Lead gen (B2B pipeline)

Pattern from inactive Duqm workflows — generalize per campaign. Default active campaign: **Haga B2B clients**.

### Haga B2B clients (Benchmark-as-a-Service)

**Product:** Independent verification layer — simulation stress tests, physics-consistency checks, reproducible benchmark reports. **Not** a robot or foundation-model builder.

**Buyer personas (priority order):**

| Persona | Titles | Why they buy |
|---------|--------|--------------|
| Robotics ML / sim lead | Head of Simulation, Robotics ML Lead, VP Engineering (robotics) | Need reproducible sim benchmarks before hardware spend |
| Robot OEM / platform | Robotics PM, Manipulation Lead, Locomotion Lead | Policy/world-model validation before deployment |
| Physical-AI / world-model team | Research lead, Sim-to-real engineer | Physics-consistency QA on generative world models |
| Design partner / early adopter | CTO, Founder (robotics startup) | Fast, credible benchmark artifact for investors |

**Company signals:** hiring sim/robotics engineers, public sim demos, "sim-to-real gap" posts, new robot SKU, research lab spinning out hardware.

**Geography:** Global remote-friendly; prioritize US/EU robotics hubs and GCC if regional angle fits.

**Serper queries (`secretary-search`, campaign `lead-pipeline`, `gl: us` or unset):**

- `robotics simulation benchmark startup`
- `physical AI world model verification`
- `robot policy stress test simulation`
- `manipulation benchmark MuJoCo robotics company`
- `sim-to-real robotics ML team hiring`

**Enrichment:** Hunter domain search → pick VP Engineering, Head of ML, Robotics PM (`confidence` ≥80).

**Pitch angle:** Reproducible benchmark artifact + public metrics workflow; design-partner / pilot call (not hard sell on first email).

**Exclude:** Pure hardware vendors with no sim stack, academic-only labs with no product path, duplicates on suppression list.

### Generic B2B (other campaigns)

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
