---
type: moc
status: active
tags: [moc, project]
last_synced: 2026-07-21
aliases: [Projects Index]
---

# Projects

Active work with live deployments or ongoing development. Each project note links to its GitHub repo and Vercel deployment metadata.

## All projects

```dataview
TABLE status, vercel_url, github_repo, last_synced
FROM "01-projects"
WHERE type = "project"
SORT file.name ASC
```

## Known Vercel deployments

| Vercel project | Project note | Repo | Startup |
|----------------|--------------|------|---------|
| clearbeam | [[01-projects/clearbeam\|clearbeam]] | [[03-resources/github-repos/clearbeam\|clearbeam]] | [[02-areas/startups/clearbeam\|Clearbeam]] |
| salon-pos | [[01-projects/salon-pos\|salon-pos]] | [[03-resources/github-repos/salon-pos\|salon-pos]] | — |
| haga-web-site | [[01-projects/haga-web-site\|haga-web-site]] | [[03-resources/github-repos/haga-web\|haga-web]] | [[02-areas/startups/haga\|Haga]] |
| haga-web-dataroom | [[01-projects/haga-web-dataroom\|haga-web-dataroom]] | [[03-resources/github-repos/haga-web\|haga-web]] | [[02-areas/startups/haga\|Haga]] |
| portfolio | [[01-projects/portfolio\|portfolio]] | [[03-resources/github-repos/portfolio\|portfolio]] | Personal |
| portfolio-panel | [[01-projects/portfolio-panel\|portfolio-panel]] | [[03-resources/github-repos/portfolio-panel\|portfolio-panel]] | Personal |
| ezra-bid-assistant-backend | [[01-projects/ezra-bid-assistant-backend\|ezra-bid-assistant-backend]] | [[03-resources/github-repos/ezra-bid-assistant\|ezra-bid-assistant]] | [[02-areas/startups/ezra-bid-assistant\|Ezra]] |
| ezra-global | [[01-projects/ezra-global\|ezra-global]] | [[03-resources/github-repos/ezra-global\|ezra-global]] | [[02-areas/startups/ezra-bid-assistant\|Ezra]] |

## Repos without Vercel deployment

| Repo | Notes |
|------|-------|
| [[03-resources/github-repos/research\|research]] | research monorepo |
| [[03-resources/github-repos/rpeh\|rpeh]] | RAG + eval harness |
| [[03-resources/github-repos/coeus\|coeus]] | this vault (meta) |

## Related

- [[03-resources/github-repos/github-overview|GitHub Repos]]
- [[02-areas/startups/startups-overview|Startups]]
- [[home]]
