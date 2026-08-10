---
to: info@refactor.capital
cc: 
subject: Haga: Early-Stage Robotics Verification — Partnership with Refactor Capital
---

Hi Refactor Capital Team,

Founded by ex-Playground partners with a focus on pre-seed to Series A robotics/AI/automation — Piaggio Fast Forward, Tortuga, Vicarious — you're investing at the stage where physics verification provides maximum ROI: before deployment, before costly recalls.

**Haga: Independent physics verification for physical AI/robotics.**

**Two pillars:**
1. **Policy Stress-Testing:** Adversarial mass/friction randomization on robosuite (Lift/Stack/PickPlaceCan/Door), scripted OSC_POSE baselines, tiered stress with independent RNG per tier.

2. **Physics-Consistency Scoring:** Position-only detectors (permanence, ballistic, contact, static_hover) calibrated on MuJoCo GT → tracked video (Physics-IQ, CogVideoX). Sliding quadratic fits, VIDEO_CHECKS profile.

**Why Refactor's portfolio needs Haga:**
- Early-stage robotics companies can't afford internal verification teams
- Vendor tools (NVIDIA, MuJoCo, Unity) don't provide independent audits
- Sim-to-real gaps discovered post-deployment are 10-100x more expensive

**Technical rigor:** 
- Held-out protocol v1 frozen 2026-07-19
- mujoco <3.10 pinned for robosuite 1.5
- geom_priority=1 ensures sampled friction governs grasp interface
- 5-step debounce on grasp failure definition

**Founder:** Mushood Hanif — 7+ years MuJoCo/Robosuite/JAX, world models, adversarial testing. Peer-reviewed ION/PMI-NN. Production systems: ADCP, agbsim.

**The ask:** Partner with Haga as verification layer for Refactor portfolio. Pre-seed/seed investment ($250k-$500k SAFE) to build platform.

20-min call this week? Deck + technical docs attached.

Best,
Mushood Hanif
Founder, Haga
haga@mushoodhanif.com | https://mushoodhanif.com
Building in Pakistan; open to global relocation with wife