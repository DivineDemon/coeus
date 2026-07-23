---
type: moc
status: active
tags: [moc, home]
aliases: [Dashboard, Index]
---
# Coeus

Personal second brain for career, startups, projects, and technical knowledge. Built on the [PARA method](https://fortelabs.com/blog/para/) and synced from GitHub, Vercel, and other external sources.

## Quick links

| Section | Description |
|---------|-------------|
| [[00-inbox]] | Capture zone — dump notes here, process weekly |
| [[01-projects/projects-overview\|Projects]] | Live Vercel deployments |
| [[02-areas/startups/startups-overview\|Startups]] | Haga, Clearbeam, Ezra, Scintia |
| [[02-areas/career/career-overview\|Career]] | Resumes, timeline, employers, education |
| [[03-resources/github-repos/github-overview\|GitHub Repos]] | README snapshots (13 repos) |
| [[03-resources/social-profiles/social-overview\|Social Profiles]] | LinkedIn, GitHub, website, etc. |
| [[03-resources/infrastructure/neon-overview\|Neon]] · [[03-resources/infrastructure/n8n-overview\|n8n]] · [[tools/coeus-hermes/README\|Hermes]] | Infrastructure |
| [[02-areas/immigration/immigration-overview\|Immigration]] | Private scaffold |
| [[03-resources/skills-matrix/skills-overview\|Skills Matrix]] | Skills with evidence links |
| [[04-archives]] | Completed or inactive material |

## PARA workflow

- **Inbox** (`00-inbox/`) — capture anything unsorted
- **Projects** — active deployments with deadlines
- **Areas** — ongoing responsibilities (career, startups, immigration)
- **Resources** — reference material (repos, resumes, profiles)
- **Archives** — move finished items here, set `status: archived`

External imports: see [[03-resources/social-profiles/ingestion-guides|Ingestion Guides]].

## Maps of content

- **[[03-resources/github-repos/github-overview|GitHub Repos]]** — all repository snapshots
- **[[03-resources/social-profiles/social-overview|Social Profiles]]** — platform profile snapshots
- **[[03-resources/skills-matrix/skills-overview|Skills Matrix]]** — derived skills inventory
- **[[02-areas/startups/startups-overview|Startups]]** — venture overviews
- **[[02-areas/career/career-overview|Career]]** — resumes and employment history
- **[[01-projects/projects-overview|Projects]]** — live deployments

## Recently indexed repos

```dataview
TABLE status, url, last_synced
FROM "03-resources/github-repos"
WHERE type = "repo"
SORT last_synced DESC
LIMIT 7
```

## Live deployments

```dataview
TABLE vercel_url, github_repo, last_synced
FROM "01-projects"
WHERE type = "project" AND contains(tags, "deployed")
SORT file.name ASC
```

## Tags

- `#repo` `#startup` `#deployed` `#ai` `#saas` `#private`
