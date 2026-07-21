---
type: profile
status: active
platform: Personal Website
url: https://mushoodhanif.com
tags: [profile, website, portfolio, deployed]
last_synced: 2026-07-21
aliases: [mushoodhanif.com]
---

# Personal Website

## Headline

**Mushood Hanif** — SaaS & AI Systems Architect (Fractional CTO)

## Bio

Senior Fullstack & AI Systems Engineer based in Lahore, Pakistan. Works with founders, business owners, and product leaders across FinTech, HealthTech, Real Estate, and B2B SaaS. Sells outcomes — fewer support tickets, faster load times, shorter sales cycles, and systems that don't fall over when they matter most.

> *"I build the systems your business runs on — not just the screens people click."*

## Key metrics

| Metric | Value |
|--------|-------|
| Domain | mushoodhanif.com |
| Page title | SaaS & AI Systems Architect (Fractional CTO) |
| Hosted on | Vercel |
| Database | Neon PostgreSQL (`portfolio` project) |
| Haga subdomain | haga.mushoodhanif.com |
| Analytics | Vercel Analytics, Speed Insights, GA4, PostHog |

## Architecture

Three-repo monorepo powering the portfolio:

| Repo | Role | Deploy URL |
|------|------|------------|
| [[03-resources/github-repos/portfolio\|portfolio]] | Next.js 16 frontend (App Router, PPR) | https://mushoodhanif.com |
| [[03-resources/github-repos/portfolio-backend\|portfolio-backend]] | Bun + Hono API, Prisma migrations | https://pb.sv.mushoodhanif.com |
| [[03-resources/github-repos/portfolio-panel\|portfolio-panel]] | React admin dashboard | Vercel (portfolio-panel) |

**Content model:** Static markdown (`about.md`, `skills.md`) + Neon-backed dynamic content (projects, workflows, blog, testimonials). Admin panel manages all DB content with on-demand cache revalidation.

## Site sections

| Route | Source | Description |
|-------|--------|-------------|
| `/` | `docs/content/about.md` | Homepage — positioning, proof points, FAQ |
| `/skills` | `docs/content/skills.md` | Skills organized by problem type |
| `/case-studies/projects` | `projects` table | Software project case studies |
| `/case-studies/workflows` | `n8n_workflows` table | n8n automation case studies |
| `/testimonials` | `clients` table | Client testimonials |
| `/blog` | `blog_posts` table | AI systems & production engineering blog |
| `/contact` | EmailJS server action | Contact form |

## Published projects (Neon)

| Project | Industry | Role | Live URL |
|---------|----------|------|----------|
| [[02-areas/startups/startups-overview\|Scintia]] | AI Voice Automation / B2B SaaS | Frontend Team Lead | [scintia.ai](https://scintia.ai) |
| Ezra Bid Assistant | Agency Operations | Full-Stack Developer | — (private Chrome extension) |
| [[02-areas/startups/startups-overview\|Clearbeam]] | SaaS / Data Analytics | Founder | [clearbeam.mushoodhanif.com](https://clearbeam.mushoodhanif.com) |

**Scintia highlights:** 4 role-specific portals, Stripe billing, Twilio/Vapi telephony, 16-month engagement, team of 4.

**Ezra highlights:** Chrome Manifest V3 extension, 5 proposal styles, 3 lengths, server-side Gemini, no auto-submit safety model.

## Published workflows (Neon)

| Workflow | Summary | Integrations |
|----------|---------|--------------|
| Zoomlion Duqm Lead Generation | 68-node n8n pipeline for AI-qualified B2B lead discovery in Duqm, Oman | Gemini, Google Sheets, Hunter, HTTP |

## Blog posts (Neon)

| Title | Published |
|-------|-----------|
| Inkling by Thinking Machines Lab: Inside the New 975B-Parameter Open-Weights Multimodal Model | Jul 16, 2026 (featured) |
| Cursor Compile 26: Inside Cursor's First Conference and What It Means for AI-Native Development | Jul 16, 2026 |
| Anthropic Just Found a 'Workspace' Inside Claude's Mind — Here's What It Means | Jul 11, 2026 |
| Stop Prompting AI. Start Building Loops. Why Boris Cherny Thinks the Future Is AI Orchestrating AI | Jul 11, 2026 |

## Testimonials (Neon)

| Client | Company | Role |
|--------|---------|------|
| Tom Knell | Llux AI | Director |
| Azmi Fekiri | Scintia Callflow | CEO |
| Muhammad Abdullah | Digimark Developers | CEO |
| Desmond Smith | Ezra Global | Founder & CEO |
| Farrukh Iminov | F&C Properties LLC | Founder & CEO |

## Proof points (homepage)

- Cut physician lookup time by **60%** across 100,000+ patients (Agentic RAG, HealthTech)
- Reduced deploy time from **2 hours to under 12 minutes** (zero-downtime CI/CD on AWS)
- Tripled qualified B2B lead throughput with a **68-node n8n** automation (Oman)
- Grew inbound real-estate leads **40%+ in 90 days** (SSR Next.js, 1,000+ listings)
- **99.9%** alert delivery reliability (Redis-backed multi-tenant SaaS)
- Led **10 engineers** across 7 concurrent projects with **98% client retention**

## Services

| Service | Description |
|---------|-------------|
| AI Systems & RAG Architecture | Naive, Conversational, and Agentic RAG with pgvector, FastAPI, LLM APIs |
| Fullstack Product Engineering | React, Next.js, TypeScript — fast, type-safe, production-grade |
| Automation & Workflow Systems | Verified n8n Creator; 60+ node production pipelines |
| Fractional CTO / Technical Advisory | Architecture, hiring, AI integration strategy for founders |

## Skills (by problem domain)

**AI & Intelligent Systems:** RAG Architecture, pgvector, OpenAI, Gemini Live, LangChain, Ollama

**Automation & Workflow:** n8n (Verified Creator), AI qualification pipelines, Stripe/Twilio/Vapi/Mapbox orchestration

**Frontend:** React, Next.js, TypeScript, Tailwind CSS, shadcn/ui, Radix UI, Redux Toolkit, TanStack Query, Vite

**Backend & Infrastructure:** FastAPI, ElysiaJS, Express, Bun, tRPC, PostgreSQL, Prisma, Drizzle, Redis, Neon, AWS, Docker, GitHub Actions

**Product & Design:** Figma, Cursor AI, Biome, ESLint, Husky

## Credentials

- Verified n8n Creator
- GitHub Arctic Code Vault Contributor
- Advisor to founders on SaaS architecture and AI strategy

## Related vault notes

- [[03-resources/github-repos/portfolio|portfolio (frontend)]]
- [[03-resources/github-repos/portfolio-backend|portfolio-backend (API)]]
- [[03-resources/github-repos/portfolio-panel|portfolio-panel (admin)]]
- [[03-resources/social-profiles/GitHub|GitHub]]
- [[03-resources/social-profiles/LinkedIn|LinkedIn]]
- [[01-projects/projects-overview|Projects]]
- [[02-areas/startups/startups-overview|Startups]]
- [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- [[home]]

## Links

- Website: https://mushoodhanif.com
- Haga: https://haga.mushoodhanif.com
- Backend API: https://pb.sv.mushoodhanif.com
- Admin panel: Vercel deployment (portfolio-panel)
