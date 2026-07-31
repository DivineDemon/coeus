# Freelance & Client Projects Architecture

> **Core Focus**: Custom client solutions, AI bid tools, and enterprise management software.

---

## Repositories Overview

### 1. ezra-bid-assistant (`/Documents/code/freelance/ezra-bid-assistant`)
- **Type**: Web Extension & Backend Service
- **Stack**: Bun, Next.js, Chrome Manifest V3 Extension, Tailwind CSS, Biome, Gemini API (`gemini-3.1-flash-lite`).
- **Description**: Private Chrome Extension side-panel assistant that extracts Freelancer.com project details, communicates with a Next.js backend, and drafts custom proposals using Gemini.
- **Features & Architecture**: Implements a Chrome MV3 architecture interfacing with a Next.js backend. Features include project detection, proposal style/length selection, draft management, and manual bid insertion directly into the Freelancer DOM.

### 2. ezra-global (`/Documents/code/freelance/ezra-global`)
- **Type**: Web Application
- **Stack**: Next.js (App Router), React, `next/font` (Geist).
- **Description**: Initial infrastructure web application serving the Ezra ecosystem. Features Next.js 14/15 modern App Router paradigms. Designed for eventual deployment via the Vercel Platform.

### 3. salon-pos (`/Documents/code/freelance/salon-pos`)
- **Type**: Point of Sale system
- **Stack**: Next.js 16 (App Router), Tailwind CSS 4, shadcn/ui, next-intl (Bilingual EN/AR, RTL), Drizzle ORM, Neon Postgres, Bun.
- **Description**: Comprehensive web-based Point of Sale system developed for Suraya Beauty Point Salon (Oman). 
- **Features & Architecture**:
  - Guided sale wizard for fast transactions.
  - Secure employee PIN authentication and attendance check-in/out tracking.
  - Multi-branch expense tracking with OMR currency formatting.
  - Administrative reporting and dashboard capabilities.
  - Fully bilingual interface (English and Arabic) with complete Right-to-Left (RTL) support via `next-intl`.
  - Live deployment target: `salon-pos-opal.vercel.app`.
