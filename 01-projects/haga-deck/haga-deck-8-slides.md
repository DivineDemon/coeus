# Haga — 8-Slide Deck for Angel Raise

Audience: pre-seed / micro angel  
Style: one claim per slide, metric-forward, evidence first  
Tone: independent verification, no hype  
Color refs: primary `#c23030`, cream `#ede8d0`, black `#000000`, muted `#4a4a4a`

---

## Slide 1 — Problem

**World models are training tomorrow's robots. Nobody independently checks their physics.**

- Benchmark source: Stanford AI Index 2026
- Simulation success on manipulation tasks: 89.4%
- Real-world household task success: 12%

The gap is where unverified physics lives. Simulators get better. Evaluation does not.

**Bottom line:** Physical-AI teams are scaling on simulated performance no one else can reproduce or audit.

---

## Slide 2 — Market signal

**Physical-AI capital is already flowing. Verification infrastructure is not.**

- $27.6B raised by physical AI/robotics startups in 2025 across 1,009 deals
- AI world-model market forecast: $5.8B → $28.6B by 2034
- Interactive physics simulators, closest to Haga's target envs: ~31.5% of that market

Spending is concentrated in sim data, sim infrastructure, and foundation models. Independent eval remains an open gap.

**Bottom line:** Buyers already have budget. They do not yet have a credible external verifier.

---

## Slide 3 — What Haga verifies

**Two artifacts. One adversarial methodology.**

- Pillar 1 — policy verification: does the robot policy survive physical stress?
- Pillar 2 — world-model verification: is the generated physics consistent?

Same methodology, two outputs:
- reproducible numeric reports
- defined thresholds
- shown failure cases

No competitor spans both artifacts.

**Bottom line:** Haga is the trust layer that sits above simulators, world models, and robot policies.

---

## Slide 4 — Evidence 1: policy stress

**Success degrades under stress. We quantify it.**

| Task | Nominal success | Severe success | Dominant failure mode |
|---|---|---|---|
| Lift | 1.00 | 0.26 | grasp acquired, then lost |
| Stack | 0.96 | 0.20 | grasp acquired, then lost |
| PickPlaceCan | 1.00 | 0.24 | grasp acquired, then lost |
| Door | 0.60 | 0.52 | door did not open |

- Wilson confidence intervals
- Reproducible seeds
- Public lab pages with failure-case breakdowns

**Bottom line:** Buyers do not have to trust a pass/fail stamp. They receive auditable degradation data.

---

## Slide 5 — Evidence 2: physics checker

**Calibrated detection, not heuristic flagging.**

- 1.000 recall on 399 violated trajectories
- 0 false positives on 200 negatives, even under tracking noise

Violation categories checked:
- teleportation
- anti-gravity
- causeless impulses
- interpenetration

**Bottom line:** A lab can integrate this into safety cases or release pipelines without building it themselves.

---

## Slide 6 — Evidence 3: world-model cohort

**Real video says no. World-model video says yes.**

- Real-video negative control: 0% flag rate
- CogVideoX I2V held-out cohort, protocol v1: 100% flag rate via `static_hover`
- n=9, interval [0.701, 1.000]
- One generative failure mode documented

**Bottom line:** Visual realism is not physics fidelity. Haga exposes the difference reproducibly.

---

## Slide 7 — Positioning vs simulation platforms

**They build the world. We audit it.**

- Antioch / Genesis / Lightwheel = simulators, synthetic data, sim evaluation
- Haga = independent verification of world models and policies

Different buyer, different budget line:
- simulator buyer: R&D / training
- Haga buyer: safety, QA, compliance, insurer / OEM validator

**Bottom line:** Haga does not compete for simulator budget. It captures eval and safety budget.

---

## Slide 8 — Traction and ask

**Already shipped. Raising to prove demand.**

Live public artifacts:
- 4 policy stress benchmarks
- Physics-checker v0
- Physics-IQ world-model cohort
- Public lab, methodology, and evaluation intake

Target raise: **$75k soft angel / SAFE**

Use of funds:
- US incorporation and entity setup
- Eval hardware: robotic arm and sensor kit
- Three paid pilot evaluations
- Cloud compute for expanded suites
- Visibility: one conference presence

Call to action:
- Open the lab: `haga.mushoodhanif.com/lab`
- Submit an eval if you have a policy or world model
- Intro to one design partner > another deck review

---
Contact: Mushood Hanif  
LinkedIn: linkedin.com/in/mushood-hanif  
Site / lab: haga.mushoodhanif.com / haga.mushoodhanif.com/lab

