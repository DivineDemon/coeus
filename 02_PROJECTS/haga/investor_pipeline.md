---
type: pipeline
project: haga
category: investor_relations
last_updated: 2026-07-31
tags: [haga, investors, vc, fundraising]
---

# Haga Investor & VC Pipeline

This document tracks venture capital firms, angel investors, and accelerator programs for Haga. It is formatted for both human review in Obsidian Dataview and autonomous management by Hermes Agent.

---

## Pipeline Dataview

```dataview
table stage, target_amount, contact, status, next_action, next_date
from "02_PROJECTS/haga/investors"
sort next_date asc
```

## Legacy Pipeline

| Name | Firm / Angel | Stage | Target Amount | Contact | Status | Next Action | Next Date |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **YC (Y Combinator)** | Y Combinator | Pre-Seed | $500k | YC Portal | Application Submitted | Track interview call | 2026-08-15 |
| **Robotics VC Candidate 1** | Physical AI Fund | Seed | $1.0M | Partner Email | Prospect | Draft cold outreach email | 2026-08-03 |
| **Deep Tech Angel 1** | Angel Syndicate | Pre-Seed | $100k | X DM | Outreach Sent | Follow up if no reply | 2026-08-05 |

---

## Detailed Target Profiles

### Y Combinator (YC)
- **Status**: Application In Flight
- **Thesis**: Independent verification for AI & Physical Robotics
- **Key Highlight**: 100% recall on physics violation detection in generative world models (CogVideoX).

### Target: Physical AI / Robotics Micro-VCs
- **Focus Areas**: Robotics infrastructure, simulation tools, verification layers.
- **Hermes Action**: Search for partners investing in robotics/world models, append to pipeline table above, and prepare initial warm-intro draft.

---

## Agent Automation Rules for Hermes
1. Read status updates from emails/CDP sessions.
2. If `Status` changes to `Call Scheduled`, log call notes in a new note inside `02_PROJECTS/haga/investors/`.
3. Push WhatsApp notification to user whenever a reply is received from an investor.
