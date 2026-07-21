---
type: project
status: active
vercel_url: https://clearbeam.mushoodhanif.com
github_repo: DivineDemon/clearbeam
tags: [project, deployed, saas, startup]
last_synced: 2026-07-21
aliases: [Clearbeam]
---

# Clearbeam

## Summary

SaaS analytics platform for indie founders — event ingestion, instant email alerts, dashboards, segments, and Stripe billing. Deployed from the [[03-resources/github-repos/clearbeam|clearbeam]] repo.

## Deployment

| Field | Value |
|-------|-------|
| Vercel project | `clearbeam` (`prj_4mqCer94XXpdj2ZngWPlL52256gu`) |
| Production URL | https://clearbeam.mushoodhanif.com |
| GitHub repo | [[03-resources/github-repos/clearbeam\|clearbeam]] |
| Framework | Next.js |
| Node version | 24.x |
| Project created | 2026-06-18 |
| Last deployed | 2026-06-18 (READY) |
| Deployment ID | `dpl_BRP6Lvir1c53MM19TGnZQfQqWioi` |

### Domains

- https://clearbeam.mushoodhanif.com
- https://clearbeam-mushood-hanifs-projects.vercel.app
- https://clearbeam-git-main-mushood-hanifs-projects.vercel.app

## Environment hints

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | PostgreSQL via Neon |
| `AUTH_SECRET` | NextAuth session signing |
| `RESEND_API_KEY` | Transactional email |
| `RESEND_FROM_EMAIL` | Verified sender address |
| `STRIPE_SECRET_KEY` | Stripe billing |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook verification |
| `STRIPE_PRICE_ID` | Clearbeam Pro price |
| `NEXT_PUBLIC_APP_URL` | Public app URL |
| `REDIS_URL` | Optional — real-time SSE stream |

## Related

- Startup: [[02-areas/startups/Clearbeam|Clearbeam]]
- Database: [[03-resources/infrastructure/neon-overview|Neon — clearbeam]]
- Repo: [[03-resources/github-repos/clearbeam|clearbeam]]

## Links

- Production: https://clearbeam.mushoodhanif.com
- GitHub: https://github.com/DivineDemon/clearbeam
- Vercel: https://vercel.com/mushood-hanifs-projects/clearbeam
