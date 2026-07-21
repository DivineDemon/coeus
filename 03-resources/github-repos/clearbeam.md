---
type: repo
status: active
tags: [repo, saas, analytics, deployed, startup]
url: https://github.com/DivineDemon/clearbeam
stack: [Bun, Next.js 16, TypeScript, Prisma 7, Neon, NextAuth, Stripe, Resend, Redis]
deployed: true
private: false
last_synced: 2026-07-21
aliases: [Clearbeam Repo]
---

# Clearbeam

*Analytics that reach you.*

Track signups, revenue, and milestones. Instant email alerts and clear analytics for your SaaS — built for indie founders and small teams.

## Features

- **Event ingestion** — Send events from your app with a simple REST API and your project API key.
- **Instant email alerts** — Get notified via [Resend](https://resend.com) when important events happen (signups, sales, milestones).
- **Custom event categories** — Define categories with emoji, color, and custom fields.
- **Analytics dashboards** — Time-series charts, category breakdowns, field aggregates, and customizable widget layouts.
- **User segments** — Filter and group events by field values for targeted insights.
- **Real-time updates** — Server-sent events stream for live dashboard refreshes (requires Redis).
- **Usage quotas** — Free and Pro plans with monthly event limits.
- **Stripe billing** — Upgrade to Clearbeam Pro for higher limits and advanced analytics.

## Tech stack

| Layer | Technology |
| --- | --- |
| Runtime & package manager | [Bun](https://bun.sh/) (`bun@1.3.8`, pinned in `package.json`) |
| Framework | [Next.js](https://nextjs.org/) 16 (App Router, Turbopack) |
| Language | TypeScript |
| Auth | [NextAuth](https://authjs.dev/) v5 (email + password, email verification) |
| Database | PostgreSQL via [Prisma](https://www.prisma.io/) 7 + [Neon](https://neon.tech/) |
| Email | [Resend](https://resend.com/) (verification + event notifications) |
| Payments | [Stripe](https://stripe.com/) |
| Real-time | Redis (optional, for SSE event stream) |
| UI | Tailwind CSS 4, Radix UI, shadcn/ui, Recharts |
| Linting | [Biome](https://biomejs.dev/) |
| Deployment | [Vercel](https://vercel.com/) |

This project uses **Bun exclusively** — do not use npm, yarn, or pnpm.

## Getting started

**Prerequisite:** [Bun](https://bun.sh/) 1.3.8+

```bash
curl -fsSL https://bun.sh/install | bash
```

### 1. Clone and install

```bash
git clone https://github.com/your-username/clearbeam.git
cd clearbeam
bun install
```

`postinstall` runs `prisma generate` automatically.

### 2. Configure environment

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

See [Configuration](#configuration) for details on each variable.

### 3. Run database migrations

```bash
bun run db:migrate
```

For a quick schema sync without a migration file:

```bash
bun run db:push
```

Open Prisma Studio:

```bash
bun run db:studio
```

### 4. Start the dev server

```bash
bun run dev
```

The app runs at [http://localhost:3000](http://localhost:3000).

### Local verification

Before deploying, run:

```bash
bun run lint
bun run typecheck
bun run build
```

Vercel runs the build on each deployment when you push to the linked repository.

## Usage

### Sign up and sign in

1. Create an account at `/sign-up`.
2. Verify your email via the link sent by Resend.
3. Sign in at `/sign-in`.

### Dashboard

After signing in, open `/dashboard` to:

- View event categories and recent activity
- Manage categories (name, emoji, color)
- Copy integration snippets for each category

### Analytics

- **Analytics** (`/dashboard/analytics`) — Overview charts, quota usage, and custom dashboards.
- **Segments** (`/dashboard/segments`) — Build filters on event fields and inspect matching events.

### Settings

- **API Key** (`/dashboard/api-key`) — View or rotate your project API key.
- **Account Settings** (`/dashboard/account-settings`) — Update your profile.
- **Upgrade** (`/dashboard/upgrade`) — Subscribe to Clearbeam Pro via Stripe.

## Sending events

Events are sent to `POST /api/v1/events` with your API key in the `Authorization` header.

1. Create an event category in the dashboard (e.g. `sale`, `signup`).
2. Copy your API key from **Settings → API Key**.
3. Send events from your backend or serverless function.

```javascript
await fetch("https://your-app.com/api/v1/events", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer <YOUR_API_KEY>",
  },
  body: JSON.stringify({
    category: "sale",
    fields: {
      plan: "PRO",
      email: "user@example.com",
      amount: 49.0,
    },
    description: "Optional custom message for the email alert",
  }),
});
```

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `category` | `string` | Yes | Must match an existing category name (letters, numbers, hyphens). |
| `fields` | `Record<string, string \| number \| boolean>` | No | Custom key-value data attached to the event and shown in alerts. |
| `description` | `string` | No | Overrides the default notification message. |

On success, Clearbeam stores the event, sends an email alert to your account address, and publishes to the real-time stream (when Redis is configured).

## Configuration

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string (Neon recommended). |
| `AUTH_SECRET` | Secret for NextAuth session signing (min 32 characters). Generate with `openssl rand -base64 32`. |
| `RESEND_API_KEY` | Resend API key (`re_...`). |
| `RESEND_FROM_EMAIL` | Verified sender for transactional email (e.g. `notifications@yourdomain.com`). |
| `STRIPE_SECRET_KEY` | Stripe secret key (`sk_test_...` or `sk_live_...`). |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret (`whsec_...`). |
| `STRIPE_PRICE_ID` | Stripe Price ID for Clearbeam Pro (`price_...`). |
| `NEXT_PUBLIC_APP_URL` | Public app URL (e.g. `http://localhost:3000` in development). |
| `REDIS_URL` | Redis connection URL (optional; required for real-time SSE). Example: `redis://:password@host:6379` or `rediss://...` for TLS. |
| `NODE_ENV` | `development`, `test`, or `production`. |

Set `SKIP_ENV_VALIDATION=1` to bypass env validation during tooling-only commands.

## API reference

All event API routes require authentication via `Authorization: Bearer <API_KEY>`. The event stream also accepts an authenticated dashboard session.

### `POST /api/v1/events`

Record a new event and trigger an email notification.

**Request body:**

```json
{
  "category": "sale",
  "fields": { "amount": 49, "plan": "PRO" },
  "description": "optional"
}
```

**Responses:**

| Status | Meaning |
| --- | --- |
| `200` | Event processed; returns `{ "message": "Event Processed Successfully!", "eventId": "..." }`. |
| `400` | Invalid JSON body. |
| `401` | Missing or invalid API key. |
| `404` | Category not found. |
| `422` | Validation error (invalid payload shape). |
| `429` | Monthly quota exceeded — upgrade to Pro. |
| `500` | Server error or email delivery failure. |

### `GET /api/v1/events`

List events for the authenticated user.

**Query parameters:**

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| `category` | `string` | — | Filter by category name. |
| `startDate` | ISO date | — | Include events on or after this date. |
| `endDate` | ISO date | — | Include events on or before this date. |
| `page` | `number` | `1` | Page number (1-based). |
| `limit` | `number` | `50` | Page size (max 100). |

**Response:**

```json
{
  "events": [...],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 120,
    "totalPages": 3
  }
}
```

### `GET /api/v1/events/stream`

Server-sent events (SSE) stream for real-time dashboard updates. Requires Redis.

**Query parameters:**

| Param | Type | Description |
| --- | --- | --- |
| `category` | `string` | Optional category filter. |
| `lastEventId` | `string` | Resume from a previous stream ID (default `0-0`). |

**Event types:** `connected`, `event.created`, `reconnect`.

### `POST /api/webhooks/stripe`

Stripe webhook endpoint for subscription lifecycle events. Configure in the Stripe dashboard and set `STRIPE_WEBHOOK_SECRET` in your environment.

### Internal RPC API

Dashboard analytics (charts, segments, dashboards) are served via the Hono RPC layer at `/api/[[...route]]` and consumed by the React client — not intended for external API key access.

## Plans and quotas

| | Free | Clearbeam Pro |
| --- | --- | --- |
| Events per month | 100 | 1,000 |
| Event categories | 3 | 10 |
| Analytics & segments | ✓ | ✓ |
| Email alerts | ✓ | ✓ |
| Priority support | — | ✓ |

## Project scripts

| Command | Description |
| --- | --- |
| `bun run dev` | Start dev server with Turbopack |
| `bun run build` | Production build |
| `bun run start` | Start production server |
| `bun run lint` | Run Biome linter |
| `bun run format` | Format with Biome |
| `bun run typecheck` | TypeScript check |
| `bun run db:migrate` | Run Prisma migrations |
| `bun run db:push` | Push schema to database |
| `bun run db:studio` | Open Prisma Studio |

## Contributing

Contributions are welcome. Please fork the repo, create a feature branch, and open a pull request. Run `bun run lint`, `bun run typecheck`, and `bun run build` before submitting.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Related

- Startup: [[02-areas/startups/Clearbeam|Clearbeam]]
- Project: [[01-projects/clearbeam|clearbeam (Vercel)]]
- Database: [[03-resources/infrastructure/neon-overview|Neon — clearbeam]]
- Skills: [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- Index: [[03-resources/github-repos/github-overview|GitHub Repos]]
