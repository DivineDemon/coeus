---
type: project
status: active
vercel_url: https://dataroom.mushoodhanif.com
github_repo: DivineDemon/haga-web
tags: [project, deployed, startup, haga, private]
last_synced: 2026-07-21
aliases: [Haga Dataroom, Haga Investor Room]
---

# Haga Web Dataroom

## Summary

Invite-only investor diligence room with Auth.js allowlist and MDX content. Deployed from `apps/dataroom` in the private [[03-resources/github-repos/haga-web|haga-web]] monorepo.

## Deployment

| Field | Value |
|-------|-------|
| Vercel project | `haga-web-dataroom` (`prj_6DMS2cpnH3LzvayZ5IgzOdTh7dy9`) |
| Production URL | https://dataroom.mushoodhanif.com |
| GitHub repo | [[03-resources/github-repos/haga-web\|haga-web]] (`apps/dataroom`) |
| Framework | Next.js |
| Node version | 24.x |
| Project created | 2026-07-17 |
| Last deployed | 2026-07-20 (READY) |
| Deployment ID | `dpl_5fZuRxPLjk72dijP5DF1nkuwcFMi` |
| Latest commit | `33b4599` on `main` |

### Domains

- https://dataroom.mushoodhanif.com
- https://haga-web-dataroom-mushood-hanifs-projects.vercel.app
- https://haga-web-dataroom-git-main-mushood-hanifs-projects.vercel.app

## Environment hints

| Variable | Purpose |
|----------|---------|
| `HAGA_METRICS_BASE_URL` | Sanitized metrics JSON from `haga-core` GitHub Release |
| `HAGA_METRICS_GITHUB_TOKEN` | PAT for private metrics release (if repo is private) |
| Auth.js vars | Invite-only access; investor email allowlist |

## Related

- Startup: [[02-areas/startups/Haga|Haga]]
- Sibling deployment: [[01-projects/haga-web-site|haga-web-site]]
- Core engine: [[03-resources/github-repos/haga|haga-core]]
- Repo: [[03-resources/github-repos/haga-web|haga-web]]

## Links

- Production: https://dataroom.mushoodhanif.com
- GitHub: https://github.com/DivineDemon/haga-web
- Vercel: https://vercel.com/mushood-hanifs-projects/haga-web-dataroom
