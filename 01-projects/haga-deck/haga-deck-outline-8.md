# Haga — Deck Outline (8 slides)

Use this as a literal slide script, not a narrative. Each slide should have one claim, one diagram/metric, and one consequence for the investor.

---

## Slide 1 — Problem
**Headline:** Sim-to-real gap is not a hardware problem. It is a physics-trust problem.

**Show:**
- Benchmark screenshot/source: 89.4% sim success → 12% real household task success.
- One-line cause: unverified physics inside simulators/world models.

**Consequence for investor:** Companies are scaling training compute on worlds that no one independently audits.

---

## Slide 2 — Market signal
**Headline:** Physical-AI capital is already flowing. Verification infrastructure is not.

**Show:**
- $27.6B / 2025 physical-AI/robotics deals.
- World-model market CAGR 58.2% to 2024.
- Antithesis quote: labs spend on sim infra, not eval infra.

**Consequence:** Haga is selling to teams that already have budget, not convincing a new market to exist.

---

## Slide 3 — What Haga verifies
**Headline:** Two artifacts. One adversarial methodology.

**Show:**
- Pillar 1: policy stress under physics variation.
- Pillar 2: physics-consistency checker for world-model outputs.
- Diagram: world model → Haga checker → report; policy → Haga stress → report.

**Consequence:** No competitor spans both.

---

## Slide 4 — Evidence 1: policy stress
**Headline:** Success degrades under stress. We quantify it.

**Show:**
- Lift: 1.00 → 0.26
- Stack: 0.96 → 0.20
- PickPlaceCan: 1.00 → 0.24
- Door: 0.60 → 0.52
- Note: nominal → severe, reproducible seeds, Wilson CIs, failure modes shown.

**Consequence:** Buyers get a reproducible benchmark, not a pass/fail stamp.

---

## Slide 5 — Evidence 2: physics checker
**Headline:** Calibrated detection, not heuristic flagging.

**Show:**
- Recall 1.000 on 399 violated trajectories.
- 0 false positives on 200 negatives under tracking noise.
- Violation categories: teleportation, anti-gravity, causeless impulses, interpenetration.

**Consequence:** Labs can integrate this into release pipelines or safety cases.

---

## Slide 6 — Evidence 3: world-model cohort
**Headline:** Real video says no. World-model video says yes.

**Show:**
- Physics-IQ real quiet: 0%
- CogVideoX held-out (n=9, protocol v1): 100% static_hover flag rate.
- One generative failure mode documented.

**Consequence:** Haga can falsify world models that look visually correct.

---

## Slide 7 — Positioning vs simulation platforms
**Headline:** They build the world. We audit it.

**Show:**
- Antioch / Genesis / Lightwheel = sim data, sim infra, sim evaluation.
- Haga = independent eval of world models and policies.
- Buyer difference: simulator buyer vs safety/QA buyer.

**Consequence:** Haga is the layer insurers, OEM validators, and cautious labs actually need.

---

## Slide 8 — Traction and use of funds
**Headline:** Already shipped. Raising to prove demand.

**Show:**
- Shipped: 4 stress benchmarks, physics-checker v0, Physics-IQ cohort, live site, evaluation intake.
- Ask: $75k soft angel / SAFE.
- Use: US incorporation, eval hardware, 3 pilots, compute, travel.

**Call to action:**
- Open the lab first: haga.mushoodhanif.com/lab
- Submit an eval if you have a policy or world model.
- Warm intro to one design partner = more valuable than another deck review.
