---
type: project
status: active
cloudflare: true
github_repo: DivineDemon/portfolio
tags: [project, deployed, portfolio, personal]
last_synced: 2026-07-26
aliases: [Portfolio Site, mushoodhanif.com]
---

# Portfolio

## Summary

Personal portfolio site at [mushoodhanif.com](https://mushoodhanif.com) — hybrid content model with static markdown pages and database-backed blog, case studies, and testimonials. Hosted on Cloudflare Workers as service `portfolio`.

## Deployment

|| Field | Value |
||-------|-------|
|| Cloudflare Worker | `portfolio` |
|| Production URL | https://mushoodhanif.com |
|| GitHub repo | [[03-resources/github-repos/portfolio|portfolio]] |
|| Framework | Next.js |
|| Node version | 24.x |

## Environment hints

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL via Neon |
| EmailJS vars | Contact form (server action) |
| Analytics | GA4 / Web vitals via env |

## Related

- Database: [[03-resources/infrastructure/neon-overview|Neon — portfolio]]
- Repo: [[03-resources/github-repos/portfolio|portfolio]]
- Infrastructure: [[03-resources/infrastructure/cloudflare-overview|Cloudflare Overview]]

## Links

- Production: https://mushoodhanif.com
- GitHub: https://github.com/DivineDemon/portfolio
