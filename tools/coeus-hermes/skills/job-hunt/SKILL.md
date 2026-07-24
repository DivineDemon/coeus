---
name: job-hunt
description: Daily job hunt — search, score vs resumes, apply/email via n8n, queue management.
version: 1.0.0
metadata:
  hermes:
    tags: [coeus, jobs, career]
---

# Job Hunt

ICP: `02-areas/secretary/icp.md` (Job hunt). Resumes: `03-resources/resumes/`.

## Workflow

1. Read ICP + pick resume (AI engineer vs fullstack)
2. `secretary-search` / browse for listings
3. Score fit; queue ≥5 in `00-inbox/secretary-queue/`
4. Apply/email via `secretary-email` with `channel: job-apply` (cap 10/day) — auto-send when fit score is clear; no approval gate
5. Log to `03-resources/secretary-log/`
