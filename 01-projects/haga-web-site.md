---
type: project
status: active
vercel_url: https://haga-web-site-mushood-hanifs-projects.vercel.app
github_repo: DivineDemon/haga-web
tags: [project, deployed, startup, haga, private]
last_synced: 2026-07-21
aliases: [Haga Site, Haga Marketing Site]
---

# Haga Web Site

## Summary

Public marketing site and Lab for Haga. Deployed from `apps/site` in the private [[03-resources/github-repos/haga-web|haga-web]] monorepo. Intended custom domain per repo docs: `haga.mushoodhanif.com` (not yet attached in Vercel).

## Step status

- Step 1-4: Completed previously; production last successfully deployed 2026-07-20 (`dpl_BNKaUrnzVw22zrFJiLKfaHFdnrpM`).
- Step 5 — site-parity MVP: completed in `apps/site` as of the latest parity-plan pass; shipped artifacts include `/about`, `/faq`, `/privacy`, `/terms`, on-site `/blog/physics-iq-held-out-cohort`, homepage `How it works` section, and `/lab` featured evidence refresh.
- Current focus: Capital/revenue: submitted-program replies, grant decision follow-up, survival paid audit only on real interest, do not chase cold capital until an evidence trigger lands

> **Note:** The three most recent production deployments were canceled (likely superseded by concurrent builds). Production is still served by the last READY deployment from 2026-07-20.

### Domains

- https://haga-web-site-mushood-hanifs-projects.vercel.app
- https://haga-web-site-git-main-mushood-hanifs-projects.vercel.app

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

## Links

- Production: https://haga-web-site-mushood-hanifs-projects.vercel.app
- GitHub: https://github.com/DivineDemon/haga-web
- Vercel: https://vercel.com/mushood-hanifs-projects/haga-web-site
