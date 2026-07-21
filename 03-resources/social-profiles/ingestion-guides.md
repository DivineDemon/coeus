---
type: moc
status: active
tags: [ingestion]
last_synced: 2026-07-21
aliases: [Ingestion Guides, Google Drive Map]
---

# Ingestion Guides

## Status: Google Drive folders processed (2026-07-21)

All 9 Drive folders moved from inbox to PARA destinations. Binary files are **gitignored** — local only.

| Drive folder | Location | Index note |
|--------------|----------|------------|
| Colab Notebooks | `03-resources/colab-notebooks/` | [[03-resources/colab-notebooks-overview\|colab overview]] |
| Companies | `02-areas/career/companies/` | [[02-areas/career/companies-overview\|companies overview]] |
| Degrees | `02-areas/career/education/` | [[02-areas/career/education-overview\|education overview]] |
| Google AI Studio | `03-resources/ai-experiments/` | [[03-resources/ai-experiments-overview\|AI experiments]] |
| Musings | `02-areas/musings/` | [[02-areas/musings-overview\|musings overview]] |
| Samsung Notes | `02-areas/personal-notes/` | [[02-areas/personal-notes-overview\|personal notes]] |
| self-host-n8n | `03-resources/infrastructure/n8n-videos/` | [[03-resources/infrastructure/n8n-overview\|n8n overview]] |
| Tax Docs | `02-areas/finance/tax/` | gitignored — no index |
| Travel Docs | `03-resources/travel/` | [[03-resources/travel-overview\|travel overview]] |

## Inbox workflow (ongoing)

1. Drop new exports in `00-inbox/`
2. Process → move to destination above
3. Update index note
4. Re-index: `python tools/coeus-memory/index.py`

## Related

- [[social-overview|Social Profiles]]
- [[home]]
