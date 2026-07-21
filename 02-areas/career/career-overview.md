---
type: moc
status: active
tags: [moc, career]
last_synced: 2026-07-21
aliases: [Career Index]
---

# Career

Employment history, dual role-targeted resumes, and a permanent conflict audit.

## Resumes (dual-track — keep both)

```dataview
TABLE target_role, status, last_synced
FROM "03-resources/resumes"
WHERE type = "resume"
SORT file.name ASC
```

| Resume | Target role | Note |
|--------|-------------|------|
| AI Engineer | LLM / RAG / agentic AI | [[03-resources/resumes/resume-ai-engineer\|Resume — AI Engineer]] |
| Fullstack | Full-stack / platform engineering | [[03-resources/resumes/resume-fullstack\|Resume — Fullstack]] |

Pick the resume that matches the job. **Do not merge into one master resume.**

## Conflict audit (kept by design)

- [[resume-conflicts]] — documents every factual difference between the two resumes
- Conflicts are **intentionally preserved** — not a backlog to fix

## Master timeline

- [[master-timeline]] — employers + evidence on file; does not override per-resume claims

## Employers (documents on file)

- [[companies-overview]] — Ailaaj, Prodago, PureLogics, SoftSquare, F&C Properties
- [[education-overview]] — degrees and transcripts

## Related

- [[03-resources/social-profiles/social-overview|Social Profiles]]
- [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- [[02-areas/startups/startups-overview|Startups]]
- [[home]]
