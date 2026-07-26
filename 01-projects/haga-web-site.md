---
type: project
status: active
cloudflare: true
github_repo: DivineDemon/haga-web
tags: [project, deployed, startup, haga, private]
last_synced: 2026-07-26
aliases: [Haga Site, Haga Marketing Site]
---

# Haga Web Site

## Summary

Public marketing site and Lab for Haga. Deployed from `apps/site` in the private [[03-resources/github-repos/haga-web|haga-web]] monorepo. Hosted on Cloudflare Workers as service `haga-web`; live domain `haga.mushoodhanif.com` returns `200`.

## Step status

- Step 1-4: Completed previously; confirmed live via `haga.mushoodhanif.com`.
- Step 5 — site-parity MVP: completed in `apps/site` as of the latest parity-plan pass; shipped artifacts include `/about`, `/faq`, `/privacy`, `/terms`, on-site `/blog/physics-iq-held-out-cohort`, homepage `How it works` section, and `/lab` featured evidence refresh.
- Current capital focus: submitted-program replies, grant decision follow-up, survival paid audit only on real interest; do not chase cold capital until an evidence trigger lands.

### Domains

- https://haga.mushoodhanif.com

## Deployment

|| Field | Value |
||-------|-------|
|| Cloudflare Worker | `haga-web` |
|| GitHub app/deploy target | `apps/site` in [[03-resources/github-repos/haga-web|haga-web]] |
|| Framework | Next.js |
|| Node version | 24.x |

## Environment hints

| Variable | Purpose |
|----------|---------|
| `HAGA_METRICS_BASE_URL` | Sanitized metrics JSON from `haga-core` GitHub Release |
| `HAGA_METRICS_GITHUB_TOKEN` | PAT for private metrics release (if repo is private) |
| Auth.js vars | Site-specific auth configuration |

## Related

- Startup: [[02-areas/startups/Haga|Haga]]
- Sibling deployment: [[01-projects/haga-web-dataroom|haga-web-dataroom]]
- Core engine: [[03-resources/github-repos/haga|haga-core]]
- Repo: [[03-resources/github-repos/haga-web|haga-web]]
- Infrastructure: [[03-resources/infrastructure/cloudflare-overview|Cloudflare Overview]]

## Links

- Production: https://haga.mushoodhanif.com
- GitHub: https://github.com/DivineDemon/haga-web
