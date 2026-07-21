---
type: project
status: active
vercel_url: https://cms.mushoodhanif.com
github_repo: DivineDemon/portfolio-panel
tags: [project, deployed, portfolio, admin]
last_synced: 2026-07-21
aliases: [Portfolio CMS, Portfolio Admin]
---

# Portfolio Panel

## Summary

Admin dashboard for managing portfolio content — projects, clients, analytics, and outreach checklists. Vite SPA with Vercel serverless auth routes. Pairs with [[01-projects/portfolio|portfolio]] (frontend) and [[03-resources/github-repos/portfolio-backend|portfolio-backend]] (API).

## Deployment

| Field | Value |
|-------|-------|
| Vercel project | `portfolio-panel` (`prj_KZlPloRXITLyMbG7yslfAFiCLUY2`) |
| Production URL | https://cms.mushoodhanif.com |
| GitHub repo | [[03-resources/github-repos/portfolio-panel\|portfolio-panel]] |
| Framework | Vite |
| Node version | 22.x |
| Project created | 2025-10-18 |
| Last deployed | 2026-07-06 (READY) |
| Deployment ID | `dpl_HQah6kiAejPqRwcPkgCfQdF28Cmh` |

### Domains

- https://cms.mushoodhanif.com
- https://portfolio-panel-mushood-hanifs-projects.vercel.app
- https://portfolio-panel-git-main-mushood-hanifs-projects.vercel.app

## Environment hints

| Variable | Purpose |
|----------|---------|
| `VITE_API_URL` | Backend API base URL (portfolio-backend) |
| JWT / auth secrets | Serverless `/api/auth/*` routes — httpOnly cookie |
| ImgBB API key | Image uploads for projects and clients |

## Related

- Frontend: [[01-projects/portfolio|portfolio]]
- Backend API: [[03-resources/github-repos/portfolio-backend|portfolio-backend]]
- Repo: [[03-resources/github-repos/portfolio-panel|portfolio-panel]]

## Links

- Production: https://cms.mushoodhanif.com
- GitHub: https://github.com/DivineDemon/portfolio-panel
- Vercel: https://vercel.com/mushood-hanifs-projects/portfolio-panel
