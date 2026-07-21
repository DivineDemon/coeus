---
type: repo
status: active
tags: [repo, react, vite, admin, deployed]
url: https://github.com/DivineDemon/portfolio-panel
stack: [React 19, Vite, TypeScript, Redux Toolkit, RTK Query, Tailwind CSS 4, shadcn/ui, React Hook Form, Zod, Biome]
deployed: true
private: false
last_synced: 2026-07-21
aliases: [portfolio-admin]
---

# Portfolio Panel

Admin dashboard for managing portfolio content — projects and clients — backed by a REST API.

## Features

- **Landing page** — public marketing entry with sign-in CTA
- **Single-user auth** — password login via Vercel serverless functions and httpOnly JWT cookie
- **Dashboard** — project and client counts with link to analytics
- **Analytics** — GA4 key event catalog, PostHog product analytics, and reporting shortcuts
- **Outreach** — LinkedIn optimization, directory listings, guest posts, client backlinks, Product Hunt checklists and templates
- **Projects** — list, create, edit, and delete portfolio projects via a 4-step form (basics, story, tech & media, SEO & links)
- **Clients** — create, edit, and delete clients in a slide-over sheet
- **Quick Link** — link or reassign existing projects to clients without the full project wizard
- **Image uploads** — cover, gallery, and client photos uploaded to ImgBB
- **Dark / light theme** — system-aware theme toggle
- **OpenAPI-driven API client** — RTK Query hooks generated from the backend OpenAPI schema

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | React 19, Tailwind CSS 4, shadcn/ui (New York) |
| Build | Vite |
| State | Redux Toolkit + RTK Query |
| Forms | React Hook Form + Zod |
| Routing | React Router |
| Linting | Biome |

## Routes

| Path | Access | Page |
|------|--------|------|
| `/` | Public | Landing |
| `/login` | Public | Admin login |
| `/dashboard` | Protected | Dashboard overview |
| `/dashboard/projects` | Protected | Project list |
| `/dashboard/projects/new` | Protected | Create project |
| `/dashboard/projects/:id` | Protected | Edit project |
| `/dashboard/clients` | Protected | Client list and management |
| `/dashboard/analytics` | Protected | GA4 key events, PostHog, and reporting shortcuts |

## Deploy

Configured for Vercel with SPA rewrites. Auth routes (`/api/auth/*`) are serverless functions.

## Related

- Frontend: [[01-projects/portfolio|portfolio]]
- Backend: [[03-resources/github-repos/portfolio-backend|portfolio-backend]]
- Project: [[01-projects/portfolio-panel|portfolio-panel]]
- Deployed at: https://cms.mushoodhanif.com
- Index: [[03-resources/github-repos/github-overview|GitHub Repos]]
