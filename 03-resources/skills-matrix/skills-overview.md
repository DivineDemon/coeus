---
type: moc
status: active
tags: [moc, skills]
last_synced: 2026-07-21
aliases: [Skills Index]
---

# Skills Matrix

Skills inventory derived from resumes, repo tech stacks, and project notes. Each skill links to vault notes that demonstrate proficiency.

## Derived skills matrix

| Skill | Proficiency | Evidence |
|-------|-------------|----------|
| RAG / Agentic AI Systems | Expert | [[03-resources/resumes/resume-ai-engineer\|resume-ai-engineer]], [[03-resources/github-repos/rpeh\|rpeh]], [[03-resources/github-repos/research\|research]] |
| Multi-Agent Orchestration | Expert | Resume claims (LangGraph, CrewAI, AutoGen), [[03-resources/resumes/resume-ai-engineer\|resume-ai-engineer]] |
| Python Backend Engineering | Expert | [[03-resources/resumes/resume-ai-engineer\|resume-ai-engineer]], [[03-resources/github-repos/rpeh\|rpeh]], [[03-resources/github-repos/research\|research]] |
| TypeScript / Fullstack Web | Expert | [[03-resources/resumes/resume-fullstack\|resume-fullstack]], [[03-resources/github-repos/clearbeam\|clearbeam]], [[03-resources/github-repos/salon-pos\|salon-pos]], [[03-resources/github-repos/ezra-bid-assistant\|ezra-bid-assistant]] |
| Next.js / React | Expert | [[03-resources/github-repos/clearbeam\|clearbeam]], [[03-resources/github-repos/salon-pos\|salon-pos]], [[03-resources/github-repos/ezra-bid-assistant\|ezra-bid-assistant]] |
| Product Analytics & Event Systems | Advanced | [[03-resources/github-repos/clearbeam\|clearbeam]] |
| Chrome Extension Development | Advanced | [[03-resources/github-repos/ezra-bid-assistant\|ezra-bid-assistant]] |
| PostgreSQL Data Modeling | Advanced | [[03-resources/github-repos/clearbeam\|clearbeam]], [[03-resources/github-repos/salon-pos\|salon-pos]], resume evidence |
| SaaS Billing & Payments (Stripe) | Advanced | [[03-resources/github-repos/clearbeam\|clearbeam]], [[03-resources/resumes/resume-fullstack\|resume-fullstack]] |
| n8n Automation | Expert | Verified n8n Creator in both resumes, [[02-areas/startups/Scintia\|Scintia]] context |

## Method and confidence

- This matrix is derived from documented repo READMEs plus both resumes.
- Skills with only resume support (no repository evidence) should be treated as self-reported until cross-validated in later phases.

## Notes tagged by skill

Browse by tag in the tag pane, or use the queries below.

### `#ai` notes

```dataview
LIST
FROM ""
WHERE contains(tags, "ai")
SORT file.name ASC
```

### `#saas` notes

```dataview
LIST
FROM ""
WHERE contains(tags, "saas")
SORT file.name ASC
```

### `#deployed` notes

```dataview
LIST
FROM ""
WHERE contains(tags, "deployed")
SORT file.name ASC
```

### `#startup` notes

```dataview
LIST
FROM ""
WHERE contains(tags, "startup")
SORT file.name ASC
```

### `#automation` notes

```dataview
LIST
FROM ""
WHERE contains(tags, "automation")
SORT file.name ASC
```

## Related

- [[03-resources/resumes/resume-ai-engineer|AI Engineer Resume]]
- [[03-resources/resumes/resume-fullstack|Fullstack Resume]]
- [[03-resources/github-repos/github-overview|GitHub Repos]]
- [[home]]
