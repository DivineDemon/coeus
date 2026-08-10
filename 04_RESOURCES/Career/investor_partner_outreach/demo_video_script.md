# Haga Demo Video Script (3-5 minutes)

## Overview
**Target length:** 3-5 minutes
**Style:** Technical founder demo — screen recording + narration
**Audience:** Investors, potential design partners, simulation platform teams
**Goal:** Show Haga working end-to-end, prove technical depth, create "wow" moment

---

## Scene 1: Hook (0:00-0:30)
**Visual:** Split screen — simulation vs. real robot failing
**Narration:**
> "This robot learned to pick up a can in simulation. In the real world, it fails — the physics didn't transfer. This is the sim-to-real gap, and it's a $1B+ problem blocking every physical AI deployment."

**Visual:** Haga logo animation → title card: "Haga: Independent Physics Verification"

---

## Scene 2: The Problem in 30 Seconds (0:30-1:00)
**Visual:** Diagram showing sim → policy → real world → failure
**Narration:**
> "Physical AI — humanoids, autonomous vehicles, world models — all train in simulation. But simulation physics is approximate. Mass, friction, contact dynamics... they never perfectly match reality. Companies discover this *after* deployment. That's too late."

**Visual:** Bullet points appearing:
- Internal testing = biased
- Vendor tools = locked in  
- Random sampling = misses edge cases
- **No independent, automated physics audit exists. Until Haga.**

---

## Scene 3: Pillar 1 — Policy Stress-Testing Live Demo (1:00-2:00)
**Visual:** Terminal recording — `haga-benchmark` running

**Commands shown:**
```bash
# Run Pillar 1 stress test on PickPlaceCan
haga-benchmark --task pickplacecan --stress-tier moderate --episodes 50
```

**Visual:** Real-time output showing:
- Episode progress bar
- Mass/friction values being randomized per episode
- Success/failure per episode
- Grasp failure detection (5-step debounce)

**Narration:**
> "Pillar 1: Policy Stress-Testing. We take your policy — or our scripted OSC_POSE baselines — and hammer it with adversarial mass and friction randomization. Look at this: geom_priority=1 ensures the sampled friction actually governs the grasp interface. Each tier — mild, moderate, severe — uses independent RNG seeded per episode. No leakage, no cheating."

**Visual:** Results summary appearing:
```
=== PICKPLACECAN MODERATE STRESS ===
Episodes: 50
Success Rate: 0.62 (gate threshold: 0.80) ❌
Grasp Failure Rate: 0.28 (delta vs baseline: +0.18) ❌
Failure Modes Found:
  - Light object slip (mass < 0.1kg): 12 episodes
  - High friction stall (μ > 1.5): 8 episodes
  - Contact instability: 5 episodes
```

**Narration:**
> "The benchmark fails the gate — success rate 62% vs 80% threshold. But look at what we found: 12 episodes of light object slip, 8 high-friction stalls. These are the edge cases random sampling misses. This is your sim-to-real gap, quantified before deployment."

---

## Scene 4: Pillar 2 — Physics-Consistency Scoring Live Demo (2:00-3:15)
**Visual:** Terminal recording — `haga-physicsiq` running on tracked video

**Commands shown:**
```bash
# Score Physics-IQ video with CoTracker3 tracking
haga-physicsiq --video data/physics_iq/throw_001.mp4 \
  --tracker cotrack3 --profile video_checks
```

**Visual:** Split screen — original video + tracked trajectories (dots on objects)
**Narration:**
> "Pillar 2: Physics-Consistency Scoring. We take real-world video — or generated video from world models — track objects with CoTracker3, and apply position-only detectors. No force sensors, no privileged info. Just position over time."

**Visual:** Detector outputs animating:
- **Permanence:** Object doesn't teleport
- **Ballistic:** Free-fall follows parabola
- **Contact:** No interpenetration at impact
- **Static Hover:** Object stays put when stationary

**Visual:** Results JSON:
```json
{
  "video": "throw_001.mp4",
  "detectors": {
    "permanence": {"score": 0.98, "violations": 0},
    "ballistic": {"score": 0.94, "violations": 2},
    "contact": {"score": 0.99, "violations": 0},
    "static_hover": {"score": 0.96, "violations": 1}
  },
  "overall_physics_iq": 0.967,
  "held_out_protocol": "v1",
  "cohort": "physics_iq_throw"
}
```

**Narration:**
> "Every detector is calibrated on MuJoCo ground truth first — we inject known violations, measure recall at 95%+, false positive rate under 2%. Then we apply to tracked video. The VIDEO_CHECKS profile relaxes gravity tolerances for RGB noise and enables static_hover. Overall Physics-IQ score: 0.967. This is objective, reproducible, vendor-agnostic."

---

## Scene 5: Metrics Pipeline — Identical Numbers Everywhere (3:15-3:45)
**Visual:** Diagram animation:
```
haga-core results/ → haga-publish-public → GitHub Release `metrics-latest`
                                    ↓
                    @haga/metrics client (GitHub API + PAT)
                                    ↓
                    apps/site LabHub ←→ apps/dataroom EvidenceCharts
                    (IDENTICAL NUMBERS — HARD INVARIANT)
```

**Narration:**
> "Our metrics pipeline is a hard invariant: identical numbers in the public Lab and the investor dataroom. Raw results never leave haga-core. Sanitized, schema-versioned JSON goes to GitHub Releases. The @haga/metrics client fetches from GitHub — works for private repos with PAT, public repos without. Zero drift, zero manual steps."

---

## Scene 6: Real-World Application — Figure 01 Case Study (3:45-4:15)
**Visual:** Mock case study document scrolling
**Narration:**
> "Here's what a verification report looks like for a humanoid like Figure 01. We stress-test manipulation policies in sim, track real robot video, quantify the sim-to-real gap per task. The deliverable: failure cases with confidence intervals, deployment readiness score, specific physics parameters to tune in simulation."

**Visual:** Key findings highlights:
- Sim-to-real gap: 18% success rate drop
- Critical failure: Light object (<0.2kg) slip at 34% rate
- Recommendation: Increase sim friction noise floor, add contact damping

---

## Scene 7: Vision & Ask (4:15-4:45)
**Visual:** Title card: "Every Physical AI System Verified by Haga"
**Narration:**
> "In five years, Haga is the SSL certificate for physical AI. No robot deploys, no world model releases, no simulation ships without a Haga physics audit. We're seeking design partners for paid pilots and seed investment to build the platform. Let's verify the physics before you deploy."

**Visual:** Contact info:
```
Mushood Hanif, Founder
haga@mushoodhanif.com
https://mushoodhanif.com
github.com/DivineDemon/haga-core
```

---

## Technical Recording Notes

### Screen Recording Setup
- **Resolution:** 1920x1080 minimum
- **Terminal:** Clean theme (dark), large font (14pt+)
- **Recording tool:** OBS, ScreenFlow, or macOS built-in (Cmd+Shift+5)
- **Audio:** Separate high-quality mic recording, sync in post

### Terminal Commands to Record
```bash
# 1. Show haga-core structure
ls -la haga-core/

# 2. Run Pillar 1 benchmark (use smaller episode count for demo)
haga-benchmark --task pickplacecan --stress-tier moderate --episodes 20

# 3. Show results directory
ls -la results/

# 4. Run Pillar 2 on sample video
haga-physicsiq --video data/physics_iq/throw_001.mp4 --tracker cotrack3 --profile video_checks

# 5. Show metrics pipeline
haga-publish-public --results-root results --out artifacts/public
ls -la artifacts/public/metrics/

# 6. Show web app consuming metrics (optional)
cd haga-web/apps/site && npm run dev
# Navigate to /lab in browser
```

### B-roll Footage to Capture
- [ ] `haga-benchmark` running with live progress
- [ ] `haga-physicsiq` tracking visualization
- [ ] GitHub Release page with metrics artifacts
- [ ] LabHub charts rendering live metrics
- [ ] Code snippets: detector math, config YAML, held-out protocol
- [ ] ADCP/agbsim dashboards (production systems)

### Post-Production
- **Music:** Subtle, technical, ambient (epidemic sound / artlist)
- **Transitions:** Clean cuts, no flashy effects
- **Captions:** Key technical terms on screen
- **Chapters:** YouTube chapters for each pillar
- **Thumbnail:** "Haga: Physics Verification for Physical AI" + terminal screenshot

---

## Short Version (60 seconds) for Cold Email
**Cut down to:** Hook → Pillar 1 result → Pillar 2 result → Vision → Contact
**Use:** LinkedIn video messages, email embeds, Twitter/X

---

## Distribution Checklist
- [ ] YouTube (unlisted for pitch deck, public for marketing)
- [ ] Loom (trackable links for investor emails)
- [ ] Google Drive / Dropbox (high-res download)
- [ ] Embed in Notion pitch deck
- [ ] LinkedIn native video
- [ ] Twitter/X native video