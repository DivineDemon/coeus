---
type: repo
status: active
tags: [repo, ai, robotics, startup, haga, private, deployed]
url: https://github.com/DivineDemon/haga-core
stack: [Python, pytest, Jupyter, GitHub Actions]
deployed: true
private: true
last_synced: 2026-07-21
aliases: [haga-core]
---

<p align="center">
  <img src="docs/logo/haga.png" alt="Haga" width="160" />
</p>

# Haga (haga-core)

[![CI](https://github.com/DivineDemon/haga-core/actions/workflows/ci.yml/badge.svg)](https://github.com/DivineDemon/haga-core/actions/workflows/ci.yml)
[![version](https://img.shields.io/badge/version-v0.1.0-blue)](https://github.com/DivineDemon/haga-core/releases/tag/v0.1.0)

**Live site:** [https://haga.mushoodhanif.com](https://haga.mushoodhanif.com) · **Public evidence:** [Lab](https://haga.mushoodhanif.com/lab) · [Methodology](https://haga.mushoodhanif.com/methodology)

**Note:** Engineering repos (`haga-core`, `haga-web`) are **private** operationally. Public trust surface = site Lab + methodology + published metrics JSON — not repo access.

**Independent benchmarking and verification for robot learning — starting with manipulation (locomotion on the Phase 5 roadmap).**

Haga treats a robot's learned policy or a synthetic training environment's output as a system to be stress-tested, broken, and reported on — not something to take on faith. The name and brand language are inspired by **Makoto Haga**, the protagonist of *Quality Assurance in Another World* — a QA tester who instinctively probes reality for bugs, exploits, and broken physics rather than accepting it as sacred lore. That posture is the product: find the bugs in AI's simulated worlds.

This repository is **haga-core**: the Python package, tests, notebooks, experiments, and the **publisher of sanitized public metrics JSON** consumed by haga-web (`apps/site` Lab + `apps/dataroom` Evidence).

---

## Table of Contents

- [The Bet](#the-bet)
- [Problem](#problem)
- [Market Context](#market-context)
- [Why Manipulation and Locomotion](#why-manipulation-and-locomotion)
- [Product Scope (v0)](#product-scope-v0)
- [Technical Stack](#technical-stack)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Decision Gates](#decision-gates)
- [Risks](#risks)
- [Getting Started](#getting-started)
- [Public metrics API](#public-metrics-api)
- [Sources](#sources)
- [Brand](#brand)
- [License](#license)

---

## The Bet

You do not build a world model, a robot, or a foundation model.

You build the **independent trust and verification layer** that well-funded robotics and physical-AI companies urgently need and do not want to build themselves — starting in the narrowest vertical you can ship, using free and open tooling, and proving the idea with **reproducible, numeric results**.

The barrier is **focus**, not capital. Speed and a single sharp result matter more than platform ambition.

---

## Problem

Robot learning labs and synthetic-data vendors increasingly train policies and generate training data in simulation. Yet:

- Labs largely **self-report benchmark results** with no independent verification.
- Synthetic training data is rarely checked for **physics consistency** — impossible accelerations, sensor noise that does not match stated conditions, policies that fail under realistic perturbation.
- Continuous, independent robotics benchmarking is still scarce — real-robot arenas (e.g. RoboArena) exist, but sim-first dual-pillar verification (policy stress + world-model physics) remains an open gap.

Robocurve states this gap explicitly: reproducible, third-party robotics benchmarks are missing. Instance applies a similar lens to physics-consistency for AI-generated video. The category is real, funded, and not yet won.

**Haga v0** is deliberately narrow: not a platform, but one focused benchmark or checker that outputs a clear pass/fail or scored report with numbers.

---

## Market Context

The layer Haga targets — verification, evaluation, and tooling underneath large robot-model builders — is already validated at this scale of ambition:

| Company | Funding | Focus |
|---------|---------|-------|
| Antioch | $8.5M seed, $60M valuation | Simulation tools for robot builders without in-house sim capacity |
| Bifrost AI | $8M Series A ($8.56M total raised) | Synthetic labeled 3D data for Physical AI |
| Patronus AI\* | $50M Series B ($70M total) | Simulation-based evaluation of AI agents before deployment |
| Instance | YC-backed, early | Physics-consistency quality layer for AI-generated video |
| Robocurve | YC-backed, early | Independent, reproducible robotics benchmarks (real-world, not sim-based — see [Risks](#risks)) |

\* *Patronus AI's "Digital World Models" target software/agent environments (web apps, internal systems), not physical robotics. Included as evidence that the verification/simulation layer is a live commercial category, not as a direct comparable to Haga.*

Broader market signals:

- **AI world models market** (the verified, primary figure): **$5.8B in 2025 → $28.6B by 2034** (58.2% CAGR), with "Interactive Physics Simulators" — the sub-category closest to Haga's target environments — making up roughly 31.5% of that market.
- A narrower, more specific figure — **$170M in 2026 → $3.06B by 2036** for "world model simulators" specifically — is widely repeated in secondary sources but could not be traced to a primary report; treat as directional context, not a verified data point.
- **Synthetic data**: estimates vary by methodology — $710M (2026) → $3.67B (2031) per Mordor Intelligence, or $791M (2026) → $6.9B (2034) per Fortune Business Insights. Prior rounds in the category (Parallel Domain, MOSTLY AI, Synthesis AI, Gretel) confirm this is an established commercial space, even where individual companies have since shut down or been acquired (see [Sources](#sources)).
- **Physical AI and robotics startups** raised **$27.6B across 1,009 deals in 2025** — more than double 2024 — confirming real capital in the ecosystem Haga would sell into.

---

## Why Manipulation and Locomotion

An initial wedge in **drone/aerial robotics** was considered and rejected for technical reasons on Apple Silicon hardware.

| Option | Issue |
|--------|-------|
| Aerial Gym Simulator, Pegasus Simulator | Built on NVIDIA Isaac stack; require CUDA; **cannot run on Apple Silicon** |
| Crazyflow (JAX-based drone sim) | Smaller, less mature ecosystem; more scaffolding before anything demoable |

**Manipulation and locomotion on MuJoCo** is dramatically more executable in week one:

| Tool | Role |
|------|------|
| **MuJoCo** | Core physics engine; free, open-source; runs natively on macOS including Apple Silicon; no GPU vendor lock-in for the base engine |
| **MJX** | JAX reimplementation of MuJoCo. On Apple Silicon, the Metal GPU backend is **structurally broken for `mjx.step()`** — Apple's Metal/MPS backend is missing the `mhlo.cholesky` operation MJX requires internally for physics constraint solving, and `jax-metal` (the plugin that would provide this) has been abandoned by Apple as of late 2024. The community replacement (`jax-mps`) is too early-stage to close the gap. In practice: **run MJX on the CPU backend on Apple Silicon** (`JAX_PLATFORMS=cpu`), and don't expect Metal GPU acceleration to become available soon. Base MuJoCo (non-MJX) is unaffected and runs natively regardless. See [Sources](#sources). |
| **Robosuite** | Manipulation benchmarking framework on MuJoCo; officially supports macOS; standardized tasks (Lift, Stack, PickPlace, Door); Gym-style API. macOS requires the `mjpython` launcher instead of `python` when using the on-screen viewer |
| **MuJoCo Menagerie** | Ready-made robot models (Unitree Go2 quadruped, Franka arm) with no asset-building work |

General robotics benchmarking (Robocurve) and general synthetic-data QA (Instance) already have YC-backed players. Haga differentiates by **shipping one credible, reproducible benchmark fast** in a vertical executable on modest local hardware — not by picking the least crowded niche at the cost of velocity.

If you have a genuine personal edge in another vertical (warehouse logistics, agriculture, manufacturing), the method below does not change; only the simulator and stress-test question do.

---

## Product Scope (v0)

Pick **one concrete benchmark question** and do not widen it until v0 is done.

**Example questions:**

1. *Does this manipulation policy's behavior stay physically consistent across randomized object mass and friction?*
2. *How much does a locomotion policy trained in simulation degrade under realistic sensor noise?*

**Output:** A clear, numeric report — pass/fail thresholds or scores — not a dashboard, not a platform, not a suite of tools.

**Success criteria for v0:**

- One working demo
- One public GitHub repo
- README with reproducible results on a public model or task
- Results clear enough that an engineer can re-run the benchmark and get the same numbers

---

## Technical Stack

Everything below is free unless noted. Cloud compute is rented only when a specific task genuinely exceeds local capacity.

### Local (Apple Silicon / macOS)

| Component | Purpose |
|-----------|---------|
| MuJoCo | Physics simulation |
| MJX | Parallel simulation via JAX; CPU backend only on Apple Silicon — Metal GPU backend is structurally unsupported for `mjx.step()` (see [Why Manipulation and Locomotion](#why-manipulation-and-locomotion)) |
| Robosuite | Manipulation benchmark tasks and Gym-style API |
| MuJoCo Menagerie | Pre-built robot models (Unitree Go2, Franka arm) |
| Qwen3:8b via Ollama | Offline coding assistant for boilerplate, test harnesses, docstrings, scenario script drafts — avoids burning API credits on grunt work |

### Cloud (sparingly, after local prototype proves the concept)

| Component | Purpose |
|-----------|---------|
| Google Colab free tier | Early prototyping |
| Kaggle free GPU quota (~30 hr/week) | Early prototyping |
| RunPod / Vast.ai spot instances | Large-scale parallel policy training or synthetic data at volume — pennies per hour, only when local capacity is insufficient |

**Principle:** Do not pay for compute until you have to. Prove the concept on your laptop first.

---

## Roadmap

Engineering SSOT: [`ROADMAP.md`](ROADMAP.md) (phases 0–5, checkboxes, GitHub
Milestones). Changelog: [`CHANGELOG.md`](CHANGELOG.md). How we work:
[`CONTRIBUTING.md`](CONTRIBUTING.md).

**Current focus:** Soft raise open ($1.0M pack) + Phase 4 design-partner conversions (awaiting replies) + parallel ICP demand signal
([milestone](https://github.com/DivineDemon/haga-core/milestone/5)). Intake +
branded report + reply→Scoped runbook: [`docs/design-partner-intake.md`](docs/design-partner-intake.md)
(`python -m haga.reports init|wrap --partner-id …`). All Priority A conversion scopes:
[`docs/partner-eval-scopes.md`](docs/partner-eval-scopes.md). Outreach:
[`docs/icp-outreach.md`](docs/icp-outreach.md). Public article:
[`docs/article-sim-physics-consistency-v1.md`](docs/article-sim-physics-consistency-v1.md)
([live](https://haga.mushoodhanif.com/article/sim-physics-consistency-v1)).
Investor snapshot is curated in [`progress/digest.yaml`](progress/digest.yaml) →
`artifacts/public/digest.json` (Issues/WIP TODOs are not mirrored).

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup, CHANGELOG / ROADMAP /
Milestone conventions, and how to refresh the public digest without leaking
internal TODOs.

---

## Decision Gates

Be honest at each gate. Pivot the **vertical or framing**, not the overall method, when signal is zero.

| Gate | Question | If no |
|------|----------|-------|
| **Day 14** | Do you have a real, reproducible result — not a toy demo? | Cut scope further. Do not add features. |

---

## Risks

- **Robocurve and Instance are already moving** in adjacent space. Being early does not guarantee a win against funded, motivated teams.
- **Sim-only evaluation has a real, acknowledged limitation.** Robocurve's own public positioning argues that "simulation only goes so far, since models that look strong in sim can show large performance gaps once deployed in the real world" — and builds real-hardware benchmarking specifically because of this. Haga v0 is deliberately sim-only, for cost and speed reasons. That's a legitimate scoping choice for a v0, not a rebuttal of Robocurve's point — document this limitation next to any reported numbers rather than presenting sim-based results as equivalent to real-world validation.
- **Competitors can integrate or replicate** a narrow tool once its value is proven.

The genuine edge available is **speed and focus**: ship one sharp, credible, reproducible result before building anything broader.

---

## Getting Started

**v0 stress test (locked):** Option A — per-episode cube mass / friction randomization on robosuite **Lift** / **Panda**, scored against a deterministic OSC_POSE reach–grasp–lift baseline. Spec: [`docs/benchmark-spec.md`](docs/benchmark-spec.md).

### Prerequisites

- macOS with Apple Silicon (M1/M2/M3) recommended for the documented stack
- Python 3.10+
- [Ollama](https://ollama.com/) (optional, for local Qwen3:8b assistance)

### Setup

```bash
# Team access required — repos are private
git clone git@github.com:DivineDemon/haga-core.git
cd haga-core

# Creates .venv, pip install -e ".[dev]", and pins JAX_PLATFORMS=cpu in the venv activate script
bash scripts/setup_env.sh
source .venv/bin/activate

# Pillar 1 — policy stress benchmark (default): 50 nominal + 50 per severity tier
# (mild/moderate/severe) → results/report.{json,md} + plot.png
python -m haga.benchmark --task lift --report
# Equivalent: haga-benchmark --task lift --report

# Pillar 2 — world-model checker calibration: known physics violations vs
# MuJoCo ground truth → results/worldmodel/report.{json,md} + plot.png (~5 s)
python -m haga.worldmodel --seeds 50 --report

# For Physics-IQ video scoring (default --tracker cotracker), install extras:
#   HAGA_EXTRAS=dev,physicsiq,cotracker bash scripts/setup_env.sh
# Pillar 2 — video case study: real Physics-IQ clip vs synthetic failure proxies
# → results/physicsiq-case-study/report.{json,md}
python -m haga.physicsiq --case-study --tracker cotracker

# Pillar 2 — CogVideoX generative cohort (scored pilot in results/physicsiq-cogvideox/)
# → results/physicsiq-cogvideox/report.{json,md}
python -m haga.physicsiq \
  --videos data/physics-iq-model/cogvideox \
  --compare-real --tracker cotracker \
  --out results/physicsiq-cogvideox
```

Notes:

- Headless runs use `has_renderer=False` under normal `python`. On-screen MuJoCo viewer on macOS needs `mjpython` (ships with mujoco) — not required for scoring.
- `mujoco` is pinned `<3.10` until robosuite adopts the 3.10 `mj_fullM` signature (see `requirements.txt`). It is an intentional Robosuite backend dependency even though `haga/` does not import it directly.
- Physics-IQ / CoTracker need `.[physicsiq,cotracker]`. CogVideoX cloud generation needs `.[cogvideox]` on a CUDA host (see `docs/cogvideox-colab.md`) — not part of the default laptop setup.
- Published headline rates for diligence: [haga.mushoodhanif.com/lab](https://haga.mushoodhanif.com/lab) (sanitized metrics JSON via `HAGA_METRICS_BASE_URL`).

### Sample results (Apple Silicon laptop)

Run: `python -m haga.benchmark --task lift --report` on arm64 / Python 3.12, mujoco 3.9.0, robosuite 1.5.2. Seeds `0..49`, paired across all conditions. Realized nominal cube mass ≈ **0.0702 kg**, friction **(1.0, 0.005, 0.0001)**. Rates carry Wilson 95% confidence intervals.

| metric | nominal | mild | moderate | severe |
|---|---|---|---|---|
| success rate | 1.0000 | 1.0000 | 0.9000 | 0.2600 |
| success 95% CI | [0.93, 1.00] | [0.93, 1.00] | [0.79, 0.96] | [0.16, 0.40] |
| grasp-failure rate | 0.0000 | 0.0000 | 0.1000 | 0.7400 |
| grasp-fail 95% CI | [0.00, 0.07] | [0.00, 0.07] | [0.04, 0.21] | [0.60, 0.84] |
| mean peak EE force (contact proxy) | 7.30 | 7.82 | 12.77 | 14.15 |
| mean EE force variance | 0.40 | 0.62 | 6.51 | 7.35 |
| score (tier / nominal) | — | 1.00 | 0.90 | 0.26 |
| verdict at gate thresholds | — | PASS | PASS | **FAIL** |

**Result (gate tier `mild`): PASS** — but the point of the tiers is the degradation curve, not the gate. Under the **severe** tier (cube mass 0.5–2.5 kg, sliding friction 0.02–0.4), the gripper acquires the cube and then **loses the grasp (slip) in 74% of episodes** — a concrete, reproducible failure mode (see `results/report.md` for per-seed failure cases with the exact sampled physics parameters). Grasp failure follows the spec definition: never grasped, or grasp lost before lift credit (5-step debounce; successful regrasps don't count as failures).

Thresholds (applied per tier): tier success ≥ 80% of nominal, grasp-fail increase ≤ 15 pp. Gate = `mild` (the locked v0 spec ranges).

**Sim-only limitation:** these numbers are not a substitute for real-hardware validation (see [Risks](#risks)).

Artifacts land in gitignored `results/` (`report.json`, `report.md`, `plot.png`).

Publish sanitized Lab/Evidence metrics (no episode dumps) with:

```bash
haga-publish-public --results-root results --out artifacts/public
```

See [Public metrics API](#public-metrics-api).

### World-model checker results (Pillar 2, v0)

Physics-consistency detectors for world-model outputs — position-only checks (the same interface as tracked video), validated against MuJoCo ground truth with known, labeled violations. Spec: [`docs/worldmodel-spec.md`](docs/worldmodel-spec.md).

| class | role | n | flag rate | checks fired |
|---|---|---|---|---|
| clean | negative | 100 | 0.000 | — |
| clean + 2 mm tracking noise | negative | 100 | 0.000 | — |
| teleport (0.3–0.8 m) | positive | 100 | 1.000 | permanence |
| hover (10–20 frames) | positive | 99 | 1.000 | ballistic |
| impulse (1.5–3 m/s) | positive | 100 | 1.000 | ballistic |
| penetration (3–10 cm) | positive | 100 | 1.000 | contact |

**Recall 1.000, precision 1.000, zero false positives under realistic tracking noise.** Sensitivity floor: a 3-frame (60 ms) hover, a 0.2 m/s causeless impulse, or 1 cm of interpenetration is caught at 100%; smaller magnitudes degrade gracefully and are documented in the report. Full study runs in ~5 s on an M2 laptop.

**Scope honesty:** v0 validates the *detector* on labeled synthetic violations. The video case study (`python -m haga.physicsiq --case-study`) shows real Physics-IQ footage at **0%** flag rate vs synthetic generative-failure proxies (teleport/hover) at **100%**.

| cohort | source | flag rate | status |
|---|---|---|---|
| Real | Physics-IQ Verified testing clip | **0%** | shipped |
| Synthetic (positive control) | teleport/hover injectors | **100%** | shipped |
| CogVideoX discovery | I2V, 3 views × seeds 0–1 | **100%** | post-hoc — `static_hover` on all 6 |
| CogVideoX held-out v1 | I2V, 3 views × seeds 2–4 (n=9) | **100%** · CI [0.701, 1.000] | confirmatory — frozen protocol |

**Generative path (honest):** open **CogVideoX** on free Colab/Kaggle T4 — not Cosmos. NVIDIA NIM / `build.nvidia.com` is geo-restricted in some regions; local M2 cannot run Cosmos-scale models. **Discovery** (`results/physicsiq-cogvideox/`, `pillar2-generative.json`): n=6 seeds 0–1 — **post-hoc**. **Held-out** (`results/physicsiq-cogvideox-heldout-v1/`, `pillar2-generative-heldout.json`): n=9 seeds 2–4 — protocol frozen before generation; public writeup + Lab + [/demo](https://haga.mushoodhanif.com/demo). Spec: [`docs/physicsiq-scoring.md`](docs/physicsiq-scoring.md). Kit: [`docs/cogvideox-colab.md`](docs/cogvideox-colab.md) + held-out notebook. Never relabel CogVideoX as Cosmos.

**Open / proprietary posture:** methodology, detector definitions, and Lab evidence are the trust signal; customer artifacts, engagement workflows, and comparative data stay private. See [`docs/thesis.md`](docs/thesis.md).

### Repository structure

```
haga-core/
├── haga/                        # Core installable package
│   ├── benchmark/               # Pillar 1 stress tests
│   ├── worldmodel/              # Pillar 2 physics checker
│   ├── physicsiq/               # Video / CogVideoX scoring
│   ├── reports/                 # Raw report writers + plots
│   ├── publish/                 # Sanitized public metrics publisher
│   ├── scenarios/
│   └── config/
├── artifacts/public/            # Schema-versioned metrics for haga-web
├── progress/digest.yaml         # Curated investor digest (not Issues/TODOs)
├── scripts/
├── docs/                        # Technical specs + public-metrics-api.md
├── notebooks/
├── tests/
├── results/                     # Raw reports — gitignored, never committed
├── CHANGELOG.md
├── ROADMAP.md                   # Phases ↔ GitHub Milestones
├── CONTRIBUTING.md
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

Web UI lives in the sibling **haga-web** monorepo (`apps/site`, `apps/dataroom`, `packages/brand`) — private, team access only.

---

## Public metrics API

haga-core publishes; haga-web reads. Contract: [`docs/public-metrics-api.md`](docs/public-metrics-api.md).

| On disk | HTTP / Release asset |
|---------|----------------------|
| `artifacts/public/metrics/pillar1-lift.json` | `pillar1-lift.json` |
| `artifacts/public/metrics/pillar1-stack.json` | `pillar1-stack.json` |
| `artifacts/public/metrics/pillar1-pickplacecan.json` | `pillar1-pickplacecan.json` |
| `artifacts/public/metrics/pillar1-door.json` | `pillar1-door.json` |
| `artifacts/public/metrics/pillar2-checker.json` | `pillar2-checker.json` |
| `artifacts/public/metrics/pillar2-generative.json` | `pillar2-generative.json` |
| `artifacts/public/metrics/pillar2-generative-heldout.json` | `pillar2-generative-heldout.json` |
| `artifacts/public/digest.json` | `digest.json` |
| `artifacts/public/manifest.json` | `manifest.json` |

**v0 transport:** rolling GitHub Release tag `metrics-latest` (workflow
**Publish public metrics**). Consumers set:

```
HAGA_METRICS_BASE_URL=https://github.com/DivineDemon/haga-core/releases/download/metrics-latest
HAGA_METRICS_GITHUB_TOKEN=<PAT with Contents: Read>   # while this repo is private
```

While the repo is private, haga-web fetches via the GitHub Releases Assets API
(browser `/releases/download/...` URLs 404 even with a PAT). See
[`docs/public-metrics-api.md`](docs/public-metrics-api.md).

Raw `results/` never leave this repo.

---

## Sources

Every figure and claim in this README is sourced in [docs/sources.md](docs/sources.md). Market-size estimates vary meaningfully by research firm and methodology — ranges are given where credible sources disagree, and figures that could not be independently verified against a primary source are flagged explicitly rather than stated as fact.

---

## Brand

Web brand SSOT is `@haga/brand` in **haga-web**. Core docs keep a short narrative + logo files in [`docs/brand.md`](docs/brand.md) / [`docs/logo/`](docs/logo/) for plots and README use.

---

## License

Licensed under the Apache License, Version 2.0 — see [LICENSE](LICENSE). Apache 2.0 was chosen deliberately: it is a permissive license with an explicit patent grant, signaling to companies evaluating whether to depend on, fork, or integrate Haga's benchmark logic that they can do so with legal confidence — consistent with Haga's positioning as a tool meant to be inspected and trusted, not taken on faith.

## Related

- Startup: [[02-areas/startups/Haga|Haga]]
- Web monorepo: [[03-resources/github-repos/haga-web|haga-web]]
- Projects: [[01-projects/haga-web-site|haga-web-site]], [[01-projects/haga-web-dataroom|haga-web-dataroom]]
- Automation: [[03-resources/infrastructure/n8n-overview|n8n — Haga Social Autopilot]]
- Skills: [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- Index: [[03-resources/github-repos/github-overview|GitHub Repos]]
