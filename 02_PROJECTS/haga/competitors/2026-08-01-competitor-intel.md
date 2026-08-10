# Haga Competitor Intelligence Brief
**Date:** 2026-08-01  
**Scope:** Antioch, Bifrost AI, Patronus AI, Instance, Robocurve  
**Classification:** Internal — Founder’s Eyes Only

---

## 1. Summary for Haga

The five named competitors cluster around three adjacent layers in the physical-AI stack: **simulation/data generation** (Antioch, Bifrost), **digital-world simulation** (Patronus), **robot-policy evaluation** (Instance, Robocurve). None currently spans **both** world-model physics-consistency checking **and** adversarial policy-stress verification the way Haga does. Instance is the closest direct threat in the evaluation layer; Robocurve is the closest in the open-source benchmark layer.

---

## 2. Individual Profiles

### 2.1 Antioch
**URL:** antioch.com / antioch.ai  
**HQ:** New York, NY  
**Founded:** 2025  
**Stage:** Seed (post-product)  
**Employees:** ~9  

**Funding**
- **$8.5M Seed** (April 2026) at **$60M valuation**
- Total raised: ~$12.6M
- Investors: A\*, Category Ventures (co-leads), MaC Venture Capital, Abstract, Box Group, Icehouse Ventures + angels

**Product & Positioning**
- Cloud-based simulation platform for robotics and autonomous systems.
- Onboards existing hardware/software stacks (ROS, custom middleware) into digital twins; defines scenarios via Python SDK; runs thousands of parallel simulations; replays failures frame-by-frame.
- Core pitch: “Develop autonomy at the speed of software” — eliminate physical test facilities and hardware staging.
- Launched **Antioch Agent** with MCP support for autonomous debugging/validation.
- Enterprise customers in drones, construction, smart security; MIT CSAIL using it for LLM-designed robot evaluation.

**Recent Updates (Apr–Jul 2026)**
- Seed announcement and public launch (antioch.com/blog/seed).
- Active product iteration with scenario suites (lobby detection, warehouse forklift, data-center intrusion, etc.).
- Hiring across engineering.

**Competitive Angle vs. Haga**
- Antioch is a **simulation execution environment**; Haga is an **independent verification layer**.
- Overlap: both touch policy evaluation.
- Gap: Antioch does not check whether its own simulated worlds are physically consistent, nor does it provide adversarial physics-perturbation stress tests. Haga can verify both the world and the policy inside it.
- Potential future competitive risk if Antioch builds or acquires an internal QA team.

---

### 2.2 Bifrost AI
**URL:** bifrost.ai  
**HQ:** San Francisco, CA  
**Founded:** 2020  
**Stage:** Series A (expanding commercialization)  
**Employees:** ~22  

**Funding**
- **$8M Series A** (October 2024)
- Total raised: ~$13.7M
- Investors: Carbide Ventures (lead), Airbus Ventures, Peak XV’s Surge, Wavemaker Partners, MD One, Techstars
- Site also lists Sequoia and Lux Capital as backers (likely earlier/co-investors)

**Product & Positioning**
- Generative 3D data platform for physical AI.
- **Stardust:** photorealistic, multi-modal synthetic data (RGB, IR, depth, segmentation, bbox) with neural rendering for domain randomization. Python-first, no 3D expertise required.
- **Manifold:** evaluation harness for robotics policies — runs LIBERO, RoboCasa, CALVIN, etc. across simulators with sharded GPU execution. Open-source release coming soon.
- Customers: NASA JPL, NTT DATA, Honda, Saronic, Seadronix, ST Engineering, Privateer, Havoc.
- Heavy-industry focus: aerospace, maritime, manufacturing, defense.

**Recent Updates (Mar–Jul 2026)**
- Product cadence: multi-camera rendering, thermal+depth, neural rendering preview, panoptic segmentation masks, organization-wide sharing, decoupled notebooks, faster offline render workflow, custom asset requests, AI assistant in docs.
- Manifold positioning as the “Inspect AI for robotics.”

**Competitive Angle vs. Haga**
- Bifrost is **upstream infrastructure** (training data + eval harness); Haga is **downstream trust/verification**.
- Overlap: Manifold’s eval platform could eventually encroach on policy robustness testing.
- Gap: Bifrost does not claim to provide physics-consistency scoring of generated videos or world models, nor does it offer adversarial stress with calibrated detectors. Haga fills that trust gap.
- Complementary angle: Bifrost generates synthetic worlds; Haga independently audits them.

---

### 2.3 Patronus AI
**URL:** patronus.ai  
**HQ:** San Francisco, CA  
**Founded:** Pre-2023 (exact year not disclosed)  
**Stage:** Series B (post-DWM preview)  
**Employees:** Not disclosed  

**Funding**
- **$50M Series B** (June 25, 2026)
- Led by Greenfield Partners; participation from Lightspeed Venture Partners, Notable Capital, Datadog, Samsung, Gokul Rajaram, Factorial Capital + AI lab leaders.
- Earlier products used by “hundreds of thousands of developers.”

**Product & Positioning**
- Frontier lab building **Digital World Models (DWM)** — language-diffusion world models that predict and steer agent actions in **digital** workflows.
- Domains: coding, research, GUI/UX, customer service, finance.
- DWM preview includes playground and documentation; benchmarked on InterCode, CoderForge, SWE-smith, τ-bench, DeepResearchQA, BFCL-v4, Toolathlon, Pandora.
- Prior products: FinanceBench, Lynx (hallucination detection), Percival, MEMTRACK, TRAIL, Prompt Tester/Management, Patronus Evaluators.
- Thesis: next phase of LLM training is defined by simulations of the digital world.

**Recent Updates (Aug 2025–Jun 2026)**
- Generative Simulators launch (Dec 2025).
- Percival Chat, Patronus Evaluators, Prompt Tester/Management, MEMTRACK, TRAIL.
- Series B announcement with DWM preview and research paper on masked diffusion language models as world models.

**Competitive Angle vs. Haga**
- **Different plane entirely:** Patronus simulates the *digital* world; Haga simulates and verifies the *physical* world.
- No direct product overlap, but both claim “simulation infrastructure for the next frontier of intelligence.”
- Haga can cite Patronus as proof that world-model infrastructure is attracting major capital, without positioning as a head-to-head competitor.

---

### 2.4 Instance
**URL:** instancelabs.ai  
**HQ:** San Francisco, CA  
**Founded:** 2026  
**Stage:** YC S26 (pre-seed)  
**Employees:** 2  

**Funding**
- **Y Combinator S26** (standard $500k pre-seed)
- No additional public rounds disclosed.

**Product & Positioning**
- **Automated evals for robot policies**, starting with a **success detector**.
- Takes task descriptions + video rollouts; returns success/failure verdicts with detailed subtask captions.
- Benchmarked on 10,000+ held-out human-labeled episodes across 7 robot platforms; claims higher accuracy than Claude Opus 4.8 at lower latency.
- Roadmap: full autonomous evaluation rig — robot rolls out, Instance judges success, second robot resets, next rollout starts.
- MIT-licensed open-source focus.

**Team**
- Claire Mao (CEO): MIT Math + CS; NASA JPL, BCG, MIT Media Lab.
- Lucy Cai (CTO): MIT CS + AI; robotics research @ MIT LIS Lab; SpaceX, AWS.

**Recent Updates**
- YC S26 launch (Summer 2026).
- Live demo at demo.instancelabs.ai.

**Competitive Angle vs. Haga**
- **Closest direct competitor** in the evaluation layer.
- Instance = success detection / RL labeling. Haga = physics-consistency scoring + adversarial policy stress.
- Overlap: both produce numeric reports on robot performance.
- Gap: Instance does not check physics consistency of generative world models, nor does it apply adversarial mass/friction/impulse probes. Haga spans both artifacts (world + policy) with calibrated detectors.
- Threat: Instance could expand from success labels into world-model QA, or be acquired by a robotics giant for in-house eval.

---

### 2.5 Robocurve
**URL:** robocurve.org  
**Legal:** Public Benefit Corporation  
**Founded:** Not explicitly stated (active ~2024–2025 based on GitHub history)  
**Stage:** Early / research-focused  
**Employees:** Not disclosed  

**Funding**
- **Not publicly disclosed.** “Backed by” section on website is empty. No Crunchbase/PitchBook funding rounds found in this sweep.

**Product & Positioning**
- Open-source evaluation framework and benchmark catalog for physical AI.
- **Inspect Robots:** run any LLM/VLA on any arm/humanoid against any real/sim benchmark with trace logs and live visualization. MIT-licensed.
- **World Evals:** curated catalog of benchmarks from sandwich-making to data-center construction.
- **KitchenBench:** 10 bimanual kitchen tasks (pour, lid removal, folding, part-mating, handover, scooping).
- **DataCenterBench:** racking servers, routing cable.
- **LaundryBench, CoffeeBench:** deformable manipulation tasks.
- Real-world first, with digital-twin simulation support.
- Integrates ROS, Isaac Lab, Robolab, Cap-X, XPolicyLab (40+ VLAs).

**Recent Activity**
- Very active GitHub: inspect-robots (104 stars), worldevals (6 stars), kitchenbench (8 stars).
- Recent adapters: YAM (I2RT), SO-ARM (LeRobot), Unitree G1 (GR00T), WidowX (OpenVLA), Franka (openpi), AgiBot A2 (GO-1).
- Evaluating Claude Opus 5, Gemini Robotics-ER, MolmoAct2, GR00T N1.7 on real hardware.

**Team**
- Experience from Amazon Robotics, Amazon AGI Labs, AWS, UK AI Security Institute, Harvard Computational Robotics Lab.
- Published at ICML, ACL, EMNLP, ACM EC, IEEE RA-L.

**Competitive Angle vs. Haga**
- **Overlap:** independent physical-AI evaluation, emphasis on reproducible benchmarks.
- **Gap:** Robocurve is benchmark/community-first (PBC mission), not a commercial trust layer. Haga is a paid eval/verification service with investor-grade reporting and API scoring.
- Robocurve’s real-world, multi-embodiment breadth vs. Haga’s physics-consistency depth and adversarial stress methodology.
- Potential collaboration: Robocurve could adopt Haga’s physics-violation detectors as a plugin, or Haga could publish selected detectors to boost credibility.

---

## 3. Comparative Matrix

| Dimension | Haga | Antioch | Bifrost AI | Patronus AI | Instance | Robocurve |
|-----------|------|---------|------------|-------------|----------|-----------|
|| **Domain** | Physical AI verification | Physical AI simulation | Physical AI synthetic data + eval | Digital world simulation | Robot policy eval | Physical AI benchmarks | Human-behavior simulation |
|| **World-Model QA** | ✅ Core (Pillar 2) | ❌ | ❌ | ✅ (digital only) | ❌ | ❌ | ❌ |
|| **Policy Stress** | ✅ Core (Pillar 1) | ✅ (parallel sim) | ✅ (Manifold) | ❌ | ✅ (success labels) | ✅ (benchmark suites) | ❌ |
|| **Physics-Consistency Scoring** | ✅ Calibrated detectors | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
|| **Human-behavior simulation** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ Core product |
|| **Open Source** | Partial (metrics JSON) | ❌ | Partial (Manifold coming) | ❌ | ✅ MIT | ✅ MIT | ❌ |
|| **Monetization** | BaaS / enterprise contracts / API | SaaS / platform | Subscription / SaaS | Enterprise / research | BaaS / demo-driven | Donations / grants (PBC) | Enterprise SaaS / simulation platform |
|| **Total Funding** | Pre-seed (building) | ~$12.6M | ~$13.7M | $50M+ | ~$0.5M (YC) | Undisclosed / likely <$2M | >$200M Series B at $2B post-money |
|| **Recent Momentum** | Phase 4 partners | Seed + enterprise deals | Manifold launch + 15+ blog posts | Series B + DWM preview | YC S26 launch | 104 GH stars + real-robot adapters | Series B + Fortune 100 deployments |

---

## 4. Key Market Signals

- **Physical AI fundraising surged to $27.6B in 2025** (1,009 deals), per PitchBook / Mean CEO (May 2026).
- **AI world models market:** $5.8B in 2025 → $28.6B by 2034 (CAGR 58.2%), per MarketIntelo.
- **Stanford AI Index 2026:** sim benchmark success 89.4% vs real household task success 12% — the exact gap Haga targets.
- **Competitive whitespace remains:** no named player publicly claims both world-model physics-consistency scoring *and* adversarial policy stress with calibrated detectors.

---

---

## 7. Simile AI

**URL:** https://www.simile.com  /  https://simile.com  
**Legal:** Simile AI, Inc.  
**Founded:** 2025  
**Stage:** Series B  
**Employees:** 50+ (as of Series B announcement, July 2026)  
**HQ:** Palo Alto, CA  

**Funding**
- **>$100M Series A** led by Index Ventures (public signal circa Feb 2026).
- **>$200M Series B** at **$2B post-money valuation** (July 30, 2026), co-led by **Greenoaks** and **Index Ventures**.
- Additional/participating investors: **Hanabi**, **Bain Capital Ventures**, **A\***, **Factory**, **CVS Health Ventures**, **Definition**.
- Combined disclosed funding to date: **>$300M**; likely closer to **$300M–$400M** across Series A + B given phrasing.

**Product & Positioning**
- Self-described as **“The Simulation Company.”**
- Core product: **AI-based simulation of human behavior** at enterprise/population scale.
- Claims a new **foundation model for human behavior** with a first-of-its-kind **confidence model** that predicts simulation accuracy.
- Enterprise use cases cited: product launch strategy, customer-experience optimization, market entry, policy/pricing/messaging tests.
- Value prop phrasing: “verifiably predict the future” by simulating people rather than asking them.

**Customers / Partners**
- **CVS Health** (named case study + blog post, Feb 2026).
- **Wealthfront**.
- **Deloitte**.
- **Gallup**.
- **Garnett Station Partners** shown in demo-modal customer set.
- Public signals imply Fortune 100 enterprise usage and tens of millions of simulations run.

**Website Design & Content**
- **Stack:** Next.js with Sanity headless CMS; large hero JSON payloads; noindex on homepage in some crawls, but blog is indexable.
- **Design:** high-production motion hero with depth-frame city imagery; animated logo/mascot; strong typographic hierarchy.
- **Navigation:** Validations / Customers / Research / Careers / Blog.
- **Copy themes:** decision-making under AI abundance, keeping humans at the center, simulating all eight billion people accurately and honestly.

**Research & Academic Anchors**
Stanford-linked foundational work tied directly to Simile’s narrative:
- “Foundation Models” paper—Stanford CRFM.
- “Social Simulacra” (UIST).
- “Generative Agents” / Smallville (UIST).
- “Generative Agent Simulations of 1,000 People.”
- “Finetuning LLMs for Human Behavior Prediction in Social Science Experiments” (EMNLP).

**Blog & Press**
- Blog posts include: “Announcing Simile’s Series B” (July 30, 2026); “Simulation: The Next Frontier for AI” (Percy Liang, Mar 10, 2026); “CVS Health x Simile” (Feb 24, 2026).
- Press: NYT Dealbook “To Know What Your Customers Think, Just Ask Their A.I. Twins” (July 30, 2026); WSJ “Can AI Replace Humans for Market Research?” (Mar 6, 2026); YouTube/Bloomberg features on Joon Sung Park.

**Social / Reach Signals**
- **LinkedIn:** `linkedin.com/company/simile-ai-inc` (authwall in direct crawl).
- **X/Twitter:** `@simile_ai`
  - Joined May 2025.
  - 15,130 follows; 92 posts in sampled window.
  - High-engagement post example: 66,040 views, 320 likes, 32 reposts (Feb 14, 2026 generative-agents Valentine post).
- **Jobs:** hosted on Ashby at `jobs.ashbyhq.com/simile`.

**Team & Founders**
- **Joon Sung Park** — primary public face; researcher-founder lineage in generative agents/Smallville.
- **Percy Liang** — Co-founder & Chief Scientist; Stanford professor, SQuAD/HELM creator, Presidential Early Career Award, IJCAI Computers and Thought Award; founding director of Stanford CRFM.
- **Michael Bernstein** — Co-founder & Chief Data Officer; Stanford HAI Senior Fellow, Sloan Fellow, Tech for Humanity Prize recipient.
- Team growth post-Series A to 50+ implies aggressive recruiting across research, engineering, design, operations.

**Branding & Philosophy**
- Mission: **simulate all eight billion people on earth, accurately and honestly.**
- Tone: academic-enterprise hybrid; Stanford research legitimacy + Fortune 100 sales motions.
- Mascot/logo system with animated logo lockup.
- Emphasis on **confidence/uncertainty quantification** (“confidence model”) — a likely moat claim.
- Positioning: not just synthetic respondents, but an infrastructure layer for decision-making in an agentic world.

**Competitive Angle vs. Haga**
- **Different stack layer:** Simile = **digital/behavioral simulation**; Haga = **physical-world verification + adversarial policy stress.**
- Overlap is narrative, not product: both are “simulation infrastructure” plays attracting major capital.
- Market signal value: validates the simulation-infra thesis; can be used as a market-education analogy for investors.
- No direct threat to Haga’s physics-consistency scoring or robotics benchmark claims.

---

## 5. Sources

- Haga vault: `/Users/mushood/Documents/code/personal/coeus/02_PROJECTS/haga/haga_index.md`
- Haga vault: `/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Codebases/Haga_Ecosystem.md`
- Haga live site: `https://haga.mushoodhanif.com` and `/lab`
- Antioch: `https://antioch.com`, FinSMEs (Apr 20 2026), Citybiz (Apr 16 2026), UCapital (Apr 16 2026)
- Bifrost: `https://www.bifrost.ai`, PR Newswire (Oct 31 2024), TechCrunch (Oct 30 2024), Bifrost blog
- Patronus: `https://patronus.ai`, Patronus blog (Jun 25 2026)
- Instance: `https://www.ycombinator.com/companies/instance`, YC launch post, DuckDuckGo snippets
- Robocurve: `https://robocurve.org`, GitHub `robocurve/*` repos

---

## 6. Implications for Haga

1. **Instance is the near-term competitive watch.** Two MIT founders, YC backing, and a clear success-detector product could expand quickly into world-model QA.
2. **Antioch and Bifrost are upstream partners or acquirers, not pure competitors.** Haga should explore integration/partnership (e.g., “verified by Haga” badge on Antioch/Bifrost outputs).
3. **Robocurve’s PBC + open-source model** gives it credibility in academia and policy circles; Haga can differentiate with commercial SLAs and investor-grade reports.
4. **Patronus is a different plane** but validates the world-model infrastructure narrative; useful for market education and fund-raising analogies.
5. **Haga’s unique claim:** “No competitor spans both world-model and policy verification with calibrated physics detectors.” Keep this sharp and evidence-backed.
