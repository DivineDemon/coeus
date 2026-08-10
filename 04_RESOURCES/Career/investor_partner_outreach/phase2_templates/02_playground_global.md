---
to: info@playgroundglobal.com
cc: 
subject: Haga: Physics Verification for Physical AI — Strategic Partnership with Playground Global
---

Hi Playground Global Team,

Andy Rubin's vision for hardware-focused deep tech — from Android to Figure AI, Light, and Tendril — is exactly why I'm reaching out. The companies you back are pushing the boundaries of physical AI, and they all face the same fundamental challenge: **the sim-to-real gap.**

**Haga in 30 seconds:** Independent physics verification for physical AI/robotics systems. Two technical pillars:

1. **Policy Stress-Testing (Pillar 1):** Adversarial mass/friction randomization on robosuite (Lift, Stack, PickPlaceCan, Door) with scripted OSC_POSE baselines. Tiered stress tiers, independent RNG per tier, geom_priority=1 on grasp interface.

2. **Physics-Consistency Scoring (Pillar 2):** Position-only detectors (permanence, ballistic, contact, static_hover) calibrated on MuJoCo ground truth, applied to tracked video (Physics-IQ, CogVideoX). Sliding quadratic fits (window 11), VIDEO_CHECKS profile for RGB video.

**Why this matters for Playground's portfolio:** Figure AI, Light, Tendril, and future investments all need to prove their simulated physics transfers to reality. Haga provides objective, third-party verification — not internal testing, not vendor-specific tools.

**Technical moat:** 
- Position-only checks (lowest common denominator across MuJoCo, tracked video, latent states)
- Tiered stress with independent RNG per tier (mixes base_seed, episode_seed, tier name)
- Held-out protocol v1 (frozen 2026-07-19): CogVideoX I2V on Physics-IQ, seeds 2-4, n=9, all static_hover
- mujoco pinned <3.10 for robosuite 1.5 compatibility

**Founder background:** 7+ years in robotics simulation (MuJoCo, Robosuite, JAX), world models, physics consistency, adversarial testing. Built simulation infrastructure for physical AI teams. Now running Haga as a verification layer.

**The ask:** I'd love to discuss a strategic partnership where Haga becomes the verification layer for Playground's robotics portfolio companies — and potentially a seed investment ($500k-$2M SAFE).

Can we schedule a 20-minute call this week? I'll share a pitch deck and technical deep-dive beforehand.

Best regards,
Mushood Hanif
Founder, Haga
haga@mushoodhanif.com
https://mushoodhanif.com
Building in Pakistan; open to global relocation with wife