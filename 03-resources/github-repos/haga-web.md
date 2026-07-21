---
type: repo
status: active
tags: [repo, nextjs, turborepo, startup, haga, deployed]
url: https://github.com/DivineDemon/haga-web
stack: [Next.js, TypeScript, pnpm, Turborepo, Auth.js, MDX]
deployed: true
private: true
last_synced: 2026-07-21
aliases: []
---

# Haga Web

Private monorepo for Haga's web surfaces.

| Path | Purpose |
|------|---------|
| `apps/site` | Public marketing site + Lab |
| `apps/dataroom` | Invite-only diligence room (Auth.js allowlist + MDX) |
| `packages/brand` | Brand SSOT — tokens, logos, chart theme (`@haga/brand`) |
| `packages/metrics` | Shared metrics client + fixtures (`@haga/metrics`) |

## Setup

```bash
pnpm install
pnpm dev:site      # http://localhost:3000
pnpm dev:dataroom  # http://localhost:3001
```

## Data room auth

No public signup. Founders sign in with an invite password. Investor emails authenticate only after incorporation gates in `apps/dataroom/lib/incorporation.ts` are all `met`.

Document tree: `apps/dataroom/content/00_Start_Here` … `09_Appendix`.

## Metrics

Both apps read sanitized metrics via `HAGA_METRICS_BASE_URL` (GitHub Release `metrics-latest` from `haga-core`). Public readers see Lab + Evidence charts only. Both apps import `@haga/metrics` so Lab and Evidence cannot drift.

## Related

- Core engine: [[03-resources/github-repos/haga|haga-core]]
- Startup: [[02-areas/startups/Haga|Haga]]
- Projects: [[01-projects/haga-web-site|haga-web-site]], [[01-projects/haga-web-dataroom|haga-web-dataroom]]
- Deployed at: https://haga.mushoodhanif.com (site), dataroom (invite-only)
- Index: [[03-resources/github-repos/github-overview|GitHub Repos]]
