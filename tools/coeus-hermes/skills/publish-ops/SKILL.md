---
name: publish-ops
description: "End-to-end content publishing workflow: create/publish via CMS or backend API, attach generated media, integrate into site code, deploy, and produce exact public URLs for verification."
version: 1.0.0
metadata:
  hermes:
    tags: [coeus, publishing, cms, deployment, content]
---

# Publish Ops

Class-level workflow for durable, verifiable content publishing across CMS, blog, site code, and deploy.

## Fallback publish order

1. **Primary API** — use the most specific available API first:
   - CMS backend endpoints (`/api/blog-posts`, admin panel)
   - Platform-native SDKs/webhooks (n8n, LinkedIn, etc.)
2. **Direct browser login** — if primary API is unavailable, blocked, or returned a middleware/reauth response, and Mushood has provided credentials, complete login in-browser and finish the action.
3. **Never stop at draft created** — ensure published state is enabled before moving on.

## Blog and content creation pattern

- Required validation before create:
  - unique slug
  - non-empty title, excerpt, body/content
  - SEO fields when available: `seoTitle`, `seoDescription`, `keywords`
  - state: `published=true`
- If image generation was requested: generate first, then attach `coverImage` in the same update or immediately after creation.
- If backend returns a 500 from create, confirm whether the draft was actually created via list/get before trying update-by-ID.

## Site integration pattern

- Prefer editable/lightweight route additions in the live repo over broad shared-layout changes when speed matters.
- Add nav + sitemap entries for every new route or external content item linked from the site.
- Build validation: run production build and confirm no static-generation regressions.
- Deploy via the repo’s standard path: `git push` to the origin remote linked to the deployment target.
- Do not claim publish/site-embed success without verifying the deploy path and whether the target is production or preview-only.