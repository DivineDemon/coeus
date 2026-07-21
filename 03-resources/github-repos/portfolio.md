---
type: repo
status: active
tags: [repo, nextjs, portfolio, deployed]
url: https://github.com/DivineDemon/portfolio
stack: [Next.js 16, React 19, Tailwind CSS 4, shadcn/ui, Prisma 7, Neon, Bun, Biome]
deployed: true
private: false
last_synced: 2026-07-21
aliases: [portfolio-site]
---

# Mushood Hanif — Portfolio

Personal portfolio site for [mushoodhanif.com](https://mushoodhanif.com). Built with Next.js 16 App Router, a sidebar layout, and a hybrid content model: static markdown for long-form pages, PostgreSQL (via Prisma) for blog posts and case studies.

## Stack

- **Framework:** Next.js 16 (Cache Components / PPR, React Compiler)
- **UI:** React 19, Tailwind CSS 4, shadcn/ui, Radix
- **Data:** Prisma 7 + PostgreSQL (Neon)
- **Content:** Markdown files (`docs/content/`) + database-backed blog & case studies
- **Workflows:** n8n JSON rendered with React Flow (`@xyflow/react`)
- **Contact:** EmailJS (server action)
- **Analytics:** Vercel Analytics, Speed Insights, GA4, PostHog, Web Vitals
- **Tooling:** Bun, Biome, TypeScript

## Routes

| Path | Source |
|------|--------|
| `/` | `docs/content/about.md` |
| `/skills` | `docs/content/skills.md` |
| `/blog`, `/blog/[slug]` | `blog_posts` table |
| `/case-studies/projects`, `/case-studies/projects/[slug]` | `projects` table |
| `/case-studies/workflows`, `/case-studies/workflows/[slug]` | `n8n_workflows` table |
| `/testimonials` | `clients` table |
| `/contact` | Contact form (EmailJS) |

SEO routes: `/sitemap.xml`, `/robots.txt`, `/llms.txt`

## Project structure

```
src/
├── app/                  # App Router pages & SEO routes
├── components/           # UI, layout, case studies, analytics
├── lib/
│   ├── data/             # Cached data fetchers (blog, case studies, content)
│   └── seo/              # Metadata, JSON-LD, sitemap helpers
docs/
├── content/              # Static markdown (about, skills)
└── dev/                  # Internal dev docs (SEO playbook, etc.)
prisma/
└── schema.prisma         # blog_posts, projects, n8n_workflows, clients, pages
```

## Content model

**Static pages** — markdown in `docs/content/` (`about.md` → homepage, `skills.md` → skills page).

**Dynamic content** — managed via the database: blog posts (`blog_posts`), project case studies (`projects`), workflow case studies (`n8n_workflows` with `workflowJson` for the canvas), testimonials (`clients`). Data fetchers use Next.js 16 `'use cache'` with `cacheTag` / `cacheLife`.

## SEO

Root metadata, per-route `generateMetadata` + JSON-LD (`Person`, `WebSite`, `Article`, `BreadcrumbList`), dynamic `sitemap.ts`, `robots.ts`, and `llms.txt`.

## Deploy

Designed for [Vercel](https://vercel.com). Neon Postgres integration. `bun run build` → deploy.

## Related

- Backend: [[03-resources/github-repos/portfolio-backend|portfolio-backend]]
- Admin panel: [[03-resources/github-repos/portfolio-panel|portfolio-panel]]
- Project: [[01-projects/portfolio|portfolio]]
- Database: [[03-resources/infrastructure/neon-overview|Neon — portfolio]]
- Deployed at: https://mushoodhanif.com
- Index: [[03-resources/github-repos/github-overview|GitHub Repos]]
