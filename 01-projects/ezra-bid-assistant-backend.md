---
type: project
status: active
vercel_url: https://eba.ezraglobal.co.za
github_repo: DivineDemon/ezra-bid-assistant
tags: [project, deployed, startup, ezra, ai, private]
last_synced: 2026-07-21
aliases: [Ezra Backend, EBA API]
---

# Ezra Bid Assistant Backend

## Summary

Next.js API backend for the Ezra Bid Assistant Chrome extension — generates Freelancer.com proposal drafts via Gemini. Deployed from the `backend/` workspace in the [[03-resources/github-repos/ezra-bid-assistant|ezra-bid-assistant]] monorepo.

## Deployment

| Field | Value |
|-------|-------|
| Vercel project | `ezra-bid-assistant-backend` (`prj_kaAebUMqGmBCmQt1IoBg7JWk9PSm`) |
| Production URL | https://eba.ezraglobal.co.za |
| GitHub repo | [[03-resources/github-repos/ezra-bid-assistant\|ezra-bid-assistant]] (`backend/`) |
| Framework | Next.js |
| Node version | 24.x |
| Project created | 2026-07-03 |
| Last deployed | 2026-07-04 (READY) |
| Deployment ID | `dpl_7WTRjdgH5TbJqrRG5H8A49Rf2xXV` |

### Domains

- https://eba.ezraglobal.co.za
- https://ezra-bid-assistant-backend-mushood-hanifs-projects.vercel.app
- https://ezra-bid-assistant-backend-git-main-mushood-hanifs-projects.vercel.app

## Environment hints

| Variable | Purpose |
|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API (server-side only) |
| `GEMINI_MODEL` | Model ID (default `gemini-3.1-flash-lite`) |
| `GEMINI_TEMPERATURE` | Sampling temperature |
| `ALLOWED_ORIGINS` | Extra CORS origins for Chrome extension |

## Related

- Startup: [[02-areas/startups/Ezra-Bid-Assistant|Ezra Bid Assistant]]
- Chrome extension: [[03-resources/github-repos/ezra-bid-assistant|ezra-bid-assistant]]
- Sibling deployment: [[01-projects/ezra-global|ezra-global]]
- Repo: [[03-resources/github-repos/ezra-bid-assistant|ezra-bid-assistant]]

## Links

- Production: https://eba.ezraglobal.co.za
- GitHub: https://github.com/DivineDemon/ezra-bid-assistant
- Vercel: https://vercel.com/mushood-hanifs-projects/ezra-bid-assistant-backend
