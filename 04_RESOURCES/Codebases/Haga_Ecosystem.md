# Haga Ecosystem Architecture & Map of Content

> **Core Focus**: Independent trust and verification layer for robot learning policies & generative world models.

---

## The Core Thesis
Haga is built on a singular bet: **You do not build a world model, a robot, or a foundation model. You build the independent trust and verification layer that well-funded robotics and physical-AI companies urgently need and do not want to build themselves.**

The name and brand language are inspired by **Makoto Haga**, the protagonist of *Quality Assurance in Another World* — a QA tester who instinctively probes reality for bugs, exploits, and broken physics rather than accepting it as sacred lore. That posture is the product: find the bugs in AI's simulated worlds.

The market context targets a verified AI world models market size growing from $5.8B in 2025 to $28.6B by 2034, and physical AI robotics startups which raised $27.6B across 1,009 deals in 2025. Competitors include Antioch, Bifrost AI, Patronus AI, Instance, and Robocurve.

---

## Repositories Overview

### 1. haga-core (`/Documents/code/haga/haga-core`)
- **Type**: Python Package & Benchmark Engine
- **Stack**: Python 3.12, MuJoCo, MJX, JAX, Robosuite, CoTracker, CogVideoX, Ollama (Qwen3:8b)
- **Key Features & Pillars**:
  - **Pillar 1 - Policy Stress Testing**: Physics benchmark engine for manipulation and locomotion. Evaluates Robosuite tasks (Lift, Stack, PickPlaceCan, Door) under a severity gradient (mild, moderate, severe). For example, the `v0` stress test evaluated per-episode cube mass / friction randomization on Robosuite Lift/Panda scored against a deterministic OSC_POSE reach–grasp–lift baseline. Severe condition performance dropped from 1.00 success rate to 0.26, showcasing verifiable fail states.
  - **Pillar 2 - World Model Physics-Consistency Scoring**: Validated against MuJoCo ground truth with known violations (1.000 recall on corrupted trajectories, zero false positives). Detects teleportation, hover, and impulse violations. 
  - **Generative Video Evaluation**: Uses CoTracker3 RGB tracking to score clips. Evaluated CogVideoX (I2V generated via Colab/Kaggle free T4) which flagged a 100% failure rate using the `static_hover` detector vs a 0% flag rate on real Physics-IQ footage.
  - **Architecture Choices**: Actively avoided NVIDIA Isaac stack (Aerial Gym, Pegasus) in favor of MuJoCo/Robosuite to maintain compatibility with Apple Silicon local execution. Due to Apple's jax-metal missing `mhlo.cholesky`, MJX is run entirely on the CPU backend (`JAX_PLATFORMS=cpu`).
  - **Outputs**: Generates sanitised public metrics JSON (`pillar1-lift.json`, `digest.json`, etc.) without leaking internal episode dumps, shipped via a rolling GitHub release tag `metrics-latest`.

### 2. haga-web (`/Documents/code/haga/haga-web`)
- **Type**: Next.js Monorepo (Web Platform)
- **Stack**: Next.js 15, TypeScript, Tailwind CSS, Turbopack, Auth.js
- **Structure**:
  - `apps/site`: Public landing page & Lab evidence browser (`haga.mushoodhanif.com`). Fetches public metrics from `haga-core` via the GitHub Releases API.
  - `apps/dataroom`: Invite-only investor diligence room using MDX. Founders authenticate via `DATAROOM_INVITE_SECRET`. Investor authentication is gated behind incorporation checks (`lib/incorporation.ts`) and unlocks when Gate A -> Atlas criteria are met. Document tree covers `00_Start_Here` through `09_Appendix`.
  - `packages/brand`: Shared design tokens & UI components (`@haga/brand`).
  - `packages/metrics`: Shared metrics client and fixtures (`@haga/metrics`), consuming `HAGA_METRICS_BASE_URL`.
- **Key Role**: Consumes public metrics JSON from `haga-core` to present reproducible, numeric proof to investors and labs without requiring repository access.

---

## Roadmap execution phases:
- Phase 0 (Foundation) - Locked thesis, shipped v0 benchmark. (Done)
- Phase 1 (Benchmark depth) - Lift, Stack, PickPlaceCan, Door under multiple tiers. (Done)
- Phase 2 (World-model scoring) - CoTracker + CogVideoX kit, first documented failure case. (Started)
- Phase 3 (Public methodology) - Publishable report + methodology page. (Done)
- Phase 4 (Design partners) - Private evaluations for early teams, branded reports, scopes ready. (Current)
- Phase 5 (Continuous scoring) - API-integrated release-pipeline checks. (Future)
