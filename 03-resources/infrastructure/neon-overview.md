---
type: resource
status: active
tags: [infrastructure, neon, database]
url: https://console.neon.tech
last_synced: 2026-07-21
aliases: [Neon Inventory, Neon Databases]
---

# Neon Overview

Neon inventory for active projects backing portfolio and product deployments. This note stores infrastructure metadata and schema inventory only (no row data, no secrets).

## Account snapshot

| Field | Value |
|-------|-------|
| Organization | Mushood |
| Org ID | `org-old-cherry-81931348` |
| Projects | 3 |
| Regions | `aws-us-east-2` |

## Project inventory

| Neon project | Project ID | App mapping | Postgres | Branch status |
|--------------|------------|-------------|----------|---------------|
| `portfolio` | `curly-butterfly-51130033` | [[01-projects/portfolio\|Portfolio]] | 17 | production (`ready`) |
| `clearbeam` | `damp-pond-01261522` | [[01-projects/clearbeam\|Clearbeam]] | 17 | production (`archived`) |
| `suraya` | `holy-poetry-00255548` | [[01-projects/salon-pos\|Salon POS]] | 18 | production (`ready`) |

## Table inventory by project

### Portfolio (`curly-butterfly-51130033`)

Schemas and tables:

- `public.blog_posts`
- `public.clients`
- `public.n8n_workflows`
- `public.projects`
- `public._prisma_migrations`
- `drizzle.__drizzle_migrations`

### Clearbeam (`damp-pond-01261522`)

Schemas and tables:

- `public.Account`
- `public.Dashboard`
- `public.DashboardWidget`
- `public.EndUser`
- `public.Event`
- `public.EventCategory`
- `public.EventDailyRollup`
- `public.Quota`
- `public.Segment`
- `public.Session`
- `public.User`
- `public.VerificationToken`
- `public._prisma_migrations`

### Suraya / Salon POS (`holy-poetry-00255548`)

Schemas and tables:

- `public.attendance_sessions`
- `public.branches`
- `public.employees`
- `public.expenses`
- `public.sale_items`
- `public.sales`
- `public.service_categories`
- `public.services`

## High-level schema notes

- **Portfolio DB** stores site-managed content for projects, workflows, blog, and testimonials.
- **Clearbeam DB** contains product analytics domain entities (events, categories, dashboards, segments, users, quotas).
- **Suraya DB** contains salon operations entities (services, categories, sales, expenses, attendance, employees, branches).

## Safety and scope

- No database credentials are stored in this vault.
- No customer row-level data is stored in this vault.
- This note is metadata-only for architectural visibility and cross-linking.

## Related

- Projects: [[01-projects/portfolio|portfolio]], [[01-projects/clearbeam|clearbeam]], [[01-projects/salon-pos|salon-pos]]
- Repos: [[03-resources/github-repos/portfolio|portfolio]], [[03-resources/github-repos/clearbeam|clearbeam]], [[03-resources/github-repos/salon-pos|salon-pos]]
- Index: [[03-resources/infrastructure/n8n-overview|n8n Overview]]
- Home: [[home]]
