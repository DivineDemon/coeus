---
type: moc
status: active
tags: [moc, profile]
last_synced: 2026-07-21
aliases: [Social Index, Profiles Index]
---

# Social Profiles

Structured snapshots of public profiles and platforms.

## All profiles

```dataview
TABLE platform, url, last_synced
FROM "03-resources/social-profiles"
WHERE type = "profile" AND status = "active"
SORT platform ASC
```

## Synced

| Platform | URL | Note |
|----------|-----|------|
| Website | [mushoodhanif.com](https://mushoodhanif.com) | [[website]] |
| LinkedIn | [linkedin.com/in/mushood-hanif](https://linkedin.com/in/mushood-hanif) | [[linkedin]] |
| GitHub | [github.com/DivineDemon](https://github.com/DivineDemon) | [[github]] |
| Stack Overflow | [stackoverflow.com/users/9131774](https://stackoverflow.com/users/9131774) | [[stack-overflow]] |
| X / Twitter | [x.com/mohdmushood](https://x.com/mohdmushood) | [[x-twitter]] |
| Hugging Face | [huggingface.co/divinedemon97](https://huggingface.co/divinedemon97) | [[huggingface]] |
| DEV Community | [dev.to/mushood_hanif](https://dev.to/mushood_hanif) | [[devto]] |
| Medium | [medium.com/@supame123](https://medium.com/@supame123) | [[medium]] |
| YouTube | [youtube.com/@mushoodhanif305](https://www.youtube.com/@mushoodhanif305) | [[youtube]] |
| n8n Creator | [n8n.io/creators/divinedemon](https://n8n.io/creators/divinedemon/) | [[n8n-creator]] |

## Not applicable

- Freelancer.com / Upwork — no profiles

## Imports

[[ingestion-guides|Ingestion Guides]] — Google Drive folder map (9 folders)

## Related

- [[03-resources/github-repos/github-overview|GitHub Repos]]
- [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- [[02-areas/career/career-overview|Career]]
- [[home]]
