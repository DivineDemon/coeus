---
type: project
status: active
cloudflare: true
github_repo: DivineDemon/haga-web
tags: [project, deployed, startup, haga, private]
last_synced: 2026-07-26
aliases: [Haga Dataroom, Haga Investor Room]
---

# Haga Web Dataroom

## Summary

Invite-only investor diligence room with Auth.js allowlist and MDX content. Deployed from `apps/dataroom` in the private [[03-resources/github-repos/haga-web|haga-web]] monorepo. Hosted on Cloudflare Workers as service `haga-dataroom`.

> Note: As of 2026-07-26, the custom domain `dataroom.mushoodhanif.com` does not resolve to a live surface from here, but the codebase and Cloudflare Worker deployment are present.

## Deployment

|| Field | Value |
||-------|-------|
|| Cloudflare Worker | `haga-dataroom` |
|| GitHub app/deploy target | `apps/dataroom` in [[03-resources/github-repos/haga-web|haga-web]] |
|| Framework | Next.js |
|| Node version | 24.x |
|| Project created | 2026-07-17 |
|| Last known ready build | 2026-07-20 (`dpl_5fZuRxPLjk72dijP5DF1nkuwcFMi`) |
|| Latest commit | `33b4599` on `main` |

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
- Infrastructure: [[03-resources/infrastructure/cloudflare-overview|Cloudflare Overview]]

## Links

- Intended production: https://dataroom.mushoodhanif.com
- GitHub: https://github.com/DivineDemon/haga-web
