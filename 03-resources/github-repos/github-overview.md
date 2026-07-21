---
type: moc
status: active
tags: [moc, repo]
url: https://github.com/DivineDemon
last_synced: 2026-07-21
aliases: [GitHub Index, Repo Index]
---

# GitHub Repos

README snapshots from [github.com/DivineDemon](https://github.com/DivineDemon). Each note mirrors the repo README and links to related startups and projects.

## All repos

```dataview
TABLE status, url, deployed, private, last_synced, tags
FROM "03-resources/github-repos"
WHERE type = "repo"
SORT file.name ASC
```

## Manual index (fallback)

| Repo | Note | Status |
|------|------|--------|
| Profile README | [[profile]] | active |
| clearbeam | [[clearbeam]] | active |
| coeus | [[coeus]] | active |
| ezra-bid-assistant | [[ezra-bid-assistant]] | active |
| ezra-global | [[ezra-global]] | archived (private) |
| haga-core | [[haga]] | active (private) |
| haga-web | [[haga-web]] | active (private) |
| portfolio | [[portfolio]] | active |
| portfolio-backend | [[portfolio-backend]] | active |
| portfolio-panel | [[portfolio-panel]] | active |
| research | [[research]] | active |
| rpeh | [[rpeh]] | active |
| salon-pos | [[salon-pos]] | active |

## Pending ingestion

Repos on GitHub not yet documented in this vault: **none** — all 13 repos indexed.

> `ezra-bid-assistant-backend` is not a separate GitHub repo; it lives in the `backend/` workspace of [[ezra-bid-assistant]].

## Related

- [[03-resources/social-profiles/social-overview|Social Profiles]] — GitHub profile metadata
- [[02-areas/startups/startups-overview|Startups]] — ventures backed by these repos
- [[01-projects/projects-overview|Projects]] — live deployments
- [[home]]
