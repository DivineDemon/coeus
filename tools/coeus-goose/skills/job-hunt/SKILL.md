---
name: job-hunt
description: Daily job hunt workflow — source discovery, resume match scoring, apply/email via n8n, queue management, and job-apply daily caps. Use for job boards, applications, recruiter outreach, or daily-job-hunt recipe.
---

# Job Hunt

## Target roles

AI Engineer, ML Engineer, full-stack with AI/agentic focus. Remote or UAE-friendly required.

## Sources (priority order)

1. LinkedIn jobs (Playwright if needed)
2. Wellfound, YC jobs, remote boards
3. Company career pages (Fetch or Playwright)
4. `secretary-search` webhook for niche queries

## Resume selection

| Job signal | Resume |
|------------|--------|
| LLM/RAG/agents/ML heavy | `03-resources/resumes/resume-ai-engineer.md` |
| Full-stack + product | `03-resources/resumes/resume-fullstack.md` |

Search MemPalace: `mempalace_search("resume conflicts career", wing=coeus)` before claiming skills.

## Match scoring

| Signal | Score |
|--------|-------|
| Stack overlap (Python, TS, LLM/RAG, agents) | +3 |
| Remote / UAE-friendly | Required — skip if missing |
| Early-stage / product team | +2 |
| Pure infra/SRE, no AI surface | Skip |
| Clearance or on-site-only outside target regions | Skip |
| Factual conflict with resume | Skip |

Score ≥5 → queue in `00-inbox/secretary-queue/`. Score 3–4 → research more. Below 3 → discard.

## Apply workflow

```
1. mempalace_search job targets + resume + voice (wing=coeus)
2. secretary-search → find listings matching ICP
3. Score each listing; write top candidates to secretary-queue/
4. For email apply / recruiter contact:
   - Draft per voice.md (≤150 words, channel=job-apply)
   - personalization_hooks: ≥2 real hooks
   - POST secretary-email with channel "job-apply" (cap 10/day)
5. For form apply: Playwright fill + log status in queue note
6. secretary-log + append 03-resources/secretary-log/YYYY-MM-DD-log.md
```

## Daily cap

**10** job applications / recruiter emails per UTC day (`channel: job-apply`). Combined cold investor/lead email uses separate cap (20).

## Queue file template

```markdown
---
type: secretary-queue
channel: job-apply
status: pending
score: 7
---

# {Company} — {Role}

- URL:
- Resume: ai-engineer | fullstack
- Hooks: [hook1, hook2]
- Notes:
```

## Exclude

Roles requiring clearance, on-site-only outside target regions, or resume conflicts.
