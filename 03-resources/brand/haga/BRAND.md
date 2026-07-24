---
type: brand
status: active
tags: [brand, haga, instagram, social, assets]
last_synced: 2026-07-23
source_repo: https://github.com/DivineDemon/haga-web/tree/main/packages/brand
aliases: [Haga Brand Package]
---

# Haga Brand Package

Single source of truth for colors, type, and logo use.

## Colors

| Role | Hex | Use |
|------|-----|-----|
| Primary | `#c23030` | Mark, accents, emphasis |
| Secondary | `#ede8d0` | Warm cream backgrounds |
| Secondary alt | `#e2dac0` | Footer / alt cream |
| Black | `#000000` | Text, outlines |
| Card | `#f5f1e4` | Raised surfaces, tooltips |
| Muted | `#e4dcc4` | Soft UI fills |
| Muted foreground | `#4a4a4a` | Secondary text, alt series |
| Border | `#d4cbb0` | Borders, chart grid |
| Chart muted | `#a89f86` | Axis / quiet chart ink |
| Destructive | `#b91c1c` | Errors |

## Typography

| Use | Font |
|------|------|
| Headings | Fraunces |
| Body / UI | Inter |

## Logo

| File | Use | Path in vault |
|------|-----|---------------|
| `logo.svg` | Preferred vector mark | `03-resources/brand/haga/assets/logo.svg` |
| `logo.png` | Raster fallback (1024²) | `03-resources/brand/haga/assets/logo.png` |

## Tone / Voice

Brand language is inspired by **Makoto Haga** (*Quality Assurance in Another World*): probe for bugs and broken physics rather than accepting the world on faith.

- **Tone:** Independent verification over faith — stress-test, break, report.
- **Messaging:** Plain-language metrics, reproducible evidence, no hype.

## Notes

- These tokens feed visuals for the website, dataroom, and social assets.
- For Instagram reels/photos: base compositions on primary `#c23030`, cream backgrounds, and Fraunces/Inter pairing.
- Keep charts and diagrams using chart-muted tones to reduce visual noise.

## Related

- Web brand SSOT: [[03-resources/github-repos/haga-web|haga-web]] `packages/brand`
- Startup: [[02-areas/startups/haga|Haga]]
- Site: [[01-projects/haga-web-site|haga-web-site]]
