---
type: repo
status: active
tags: [repo, hono, bun, api, deployed]
url: https://github.com/DivineDemon/portfolio-backend
stack: [Bun, Hono, TypeScript, Prisma 7, PostgreSQL, Zod, Scalar, Pino]
deployed: true
private: false
last_synced: 2026-07-21
aliases: []
---

# Portfolio Backend API

Type-safe backend API built with **Bun**, **Hono**, **TypeScript**, **Prisma**, and **PostgreSQL** for managing portfolio projects and clients. This package is the **single source of truth** for database migrations.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Bun |
| Framework | Hono |
| Language | TypeScript |
| Database | PostgreSQL (Neon) |
| ORM | Prisma 7 |
| Validation | Zod |
| API Docs | Scalar (interactive OpenAPI) |
| OpenAPI Gen | @asteasolutions/zod-to-openapi |
| Logging | Pino |

## Project Structure

```
portfolio-backend/
├── prisma/
│   ├── schema.prisma           # Database schema
│   └── migrations/             # Migration history
├── generated/prisma/           # Generated Prisma client
└── src/
    ├── index.ts                # Application entry point
    ├── lib/db.ts               # Prisma client
    ├── models/                 # Insert type definitions
    ├── queries/                # Database operations
    ├── routes/                 # Hono route handlers (projects, clients, quickLink)
    ├── schemas/                # Zod validation + OpenAPI schemas
    └── utils/                  # Logger, openapi, revalidate
```

## Database Schema

**Clients** — client profiles and testimonials (image, company, content, designation, clientName, feedback).

**Projects** — portfolio case studies with slug, title, headlineResult, problem/approach/results, metrics (JSONB), techStack/infrastructure/integrations arrays, media, and visibility flags. One client → many projects.

## API Endpoints

| Route | Methods | Description |
|-------|---------|-------------|
| `/api/projects` | GET, POST | List / create projects |
| `/api/projects/:id` | GET, PUT, DELETE | CRUD by ID |
| `/api/clients` | GET, POST | List / create clients |
| `/api/clients/:id` | GET, PUT, DELETE | CRUD by ID |
| `/api/quick-link` | GET, PUT | Link projects to clients |
| `/api/quick-link/bulk` | PUT | Bulk link/unlink |

Interactive docs at `/docs`, OpenAPI spec at `/openapi.json`.

## On-Demand Revalidation

When projects or clients change, the backend notifies the portfolio site to refresh cached pages via `PORTFOLIO_REVALIDATE_URL`.

## Related

- Frontend: [[01-projects/portfolio|portfolio]]
- Admin panel: [[01-projects/portfolio-panel|portfolio-panel]]
- Deployed at: https://pb.sv.mushoodhanif.com
- Index: [[03-resources/github-repos/github-overview|GitHub Repos]]
