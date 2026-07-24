# Antioch — Postmortem / Forensic Analysis

## 1. Identity and origin
- **Company:** Antioch Inc.
- **Focus:** Cloud simulation platform for robotics and physical autonomy.
- **Headquarters:** New York, NY.
- **Founding:** Early 2025.
- **Founders:**
  - Harry Mellsop — previously Tesla Autopilot vision.
  - Alex Langshur — previously head of product at Deep Grey Research.
  - Colton Swingle — previously Google DeepMind, large-scale model validation.
  - Collin Schlager — previously Meta Reality Labs.
- **Previous exit:** Mellsop + Langshur + Calvey founded Transpose, sold to Chainalysis in 2023.
- **Customer-facing narrative:** “Cursor for physical AI.”

## 2. Problem framing and narrative
Antioch’s narrative is strongest because it is easy to understand:
- most robotics teams test in the real world: expensive, slow, dangerous;
- the few who simulate use academic/fragmented tools that require orthogonal expertise;
- Tesla/Waymo/Anduril spend hundreds of millions a year on simulation infra, but smaller players cannot.
- “Sim-to-real gap” is the industry shorthand they are exploiting.
- They position themselves as a **platform layer** above simulators/world models, not a world model themselves.

This is almost identical to Haga’s problem framing, except Antioch sells the *simulation environment* while Haga sells the *independent evaluation of that environment/model*.

## 3. Product / delivery model
- Digital twins of robots in cloud simulation.
- Parallel execution of thousands of tests.
- Deterministic test environments.
- CI/CD integration and telemetry streaming.
- Uses Nvidia/World Labs models under the hood, plus domain-specific libraries.
- Integrations with Foxglove for observability.
- Self-described as making physical autonomy software-first within 2–3 years.

Operational model:
- heavy usage of “pilot sales” early on;
- later scale via usage-based cloud delivery.

## 4. GTM / marketing mechanics
- **Media narrative:** Locked the “Cursor for physical AI” frame, which is repeatable and investor-friendly.
- **Press:** TechCrunch, SiliconANGLE, Robotics and Automation News, Dealroom, The Robot Report.
- **Events/speakers:** Ride AI, MACHINA; Harry Mellsop on stage with industry investors.
- **Content evidence:** LinkedIn sneak-peeks of the platform UI.
- **Customer categories cited:** construction robotics, smart security, foundation model AI developers, Fortune 500s.
- **Lead-gen pattern:** identify a well-capitalized customer class, publish the benchmark comparison, let press/VCs validate.

This is a cold-start playbook well-suited to deep-tech: credibility first, product second, pipeline third.

## 5. Business model and revenue
No public pricing table. Based on quotes and comparisons:
- modeled after cloud compute/usage, not seats;
- pilots -> enterprise contracts;
- long-term lock-in through data and CI/CD integration.

Risk: revenue is not visible; they are still burning runway. They have announced pilot deals, not ARR.

## 6. Investors and backers
- **Pre-seed Dec 2025:** $4.25M
  - Lead: A*
  - Participants: Abstract Ventures, MaC Venture Capital, BoxGroup, Icehouse Ventures
  - Angels: Adrian Macneil (Foxglove), Shyam Sankar (Palantir)
- **Seed April 2026:** $8.5M at $60M valuation
  - Leads: A* and Category Ventures
  - Participants: MaC Venture Capital, Abstract, BoxGroup, Icehouse
- **Thematic cluster:** A* + Category are clearly building a physical-AI/dev-tools thesis across multiple bets; MaC is a repeat robotics/simulation backer.

## 7. Market structure and competition
- **Antioch** = simulation platform.
- **Lightwheel AI** = synthetic simulation data + simulation evaluation + embodied data engine; already global enterprise revenue, RoboFinals eval platform.
- **Genesis AI** = foundation robotics model + its own Genesis World simulator. $105M seed from Eclipse/Khosla.
- **Foxglove** = observability/data pipeline for physical AI; angel investor in Antioch, but not a benchmarker.
- **OpenAI/NVIDIA/Cosmos, NVIDIA Omniverse** = infrastructure, not neutral eval.
- **World Labs / Google DeepMind** = world-model builders, not independent validators.
- **Haga** = independent benchmarking/trust layer; explicitly not a simulator.

## 8. What this means for Haga
- The market is validating simulation fast; proof: $4.25M then $8.5M within 4 months.
- The “Cursor for physical AI” frame works because it promises speed and developer trust.
- Antioch’s “platform above simulators” is different from Haga’s “independent eval layer above simulators” — but the end user has trouble distinguishing them.
- Haga can differentiate by proving failure modes and falsifying world models, rather than generating simulations.

## 9. Likely Antioch weaknesses and opportunities against them
- **Vertical depth:** Antioch cites many verticals; likely none fully penetrated.
- **Claim breadth:** claiming construction + security + foundation models is hard to execute.
- **Customers:** no public named logos beyond comments; enterprise demand is implied, not evidenced.
- **Repeat use case:** if evaluation is the bottleneck, Antioch’s simulators matter less than the eval layer.
- **Trust layer gap:** they are the judge of their own sims’ quality; Haga is the external verifier.

## 10. Haga positioning implication
- Compete in public evidence, not product breadth.
- Publish reproducible failure cases; that is the only defensible moat against simulation platforms.
- Target investors who want “trust” rather than “more sims.”
- Ideal partners/customers are teams that need to prove safety to regulators, insurers, or OEMs.

## Sources
- TechCrunch: https://techcrunch.com/2026/04/16/this-simulation-startup-wants-to-be-the-cursor-for-physical-ai/
- Antioch blog seed announcement: https://antioch.com/blog/seed
- SiliconANGLE: https://siliconangle.com/2026/04/16/antioch-prepares-accelerate-simulated-testing-autonomous-robots-raising-8-5m/
- Robotics and Automation News pre-seed: https://roboticsandautomationnews.com/2025/12/04/us-startup-antioch-raises-4-25-million-to-build-simulation-infrastructure-to-the-robotics-industry/97336/
- Genesis AI seed coverage: https://techcrunch.com/2025/07/01/genesis-ai-launches-with-105m-seed-funding-from-eclipse-khosla-to-build-ai-models-for-robots/
- Lightwheel funding references via public reports.
