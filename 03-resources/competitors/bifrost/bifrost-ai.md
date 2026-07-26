# Bifrost · Simulation infrastructure for physical AI

> Source: https://bifrost.ai/

BIFROST\_SIM\_v2.0

```
CONTAINERIZING POLICIES ......... OK
SETTING UP ENVIRONMENT .......... OK
RETICULATING SPLINES ............
```

# Evaluate & Improve  Physical AI

Find your robot's failure modes in 30 minutes with GPU-accelerated simulation.

EvaluateManifold

Robot policy evaluations made easy, fast and insightful.

GET ACCESS [LEARN MORE](https://manifold.bifrost.ai/)

ImproveStardust

Fix failures by generating photorealistic, multi-modal sensor data.

[BOOK A DEMO](https://www.bifrost.ai/contact) [LEARN MORE](https://www.bifrost.ai/stardust)

## We’re getting AI into the physical world

01

### Codifying the hardest tasks in simulation

Turn demanding physical tasks into high-fidelity, multi-modal simulation.

02

### Evaluation Tasks defined by industry experts

To ensure reliability across complex industrial tasks domain experts define scenarios and SOPs

03

### Making simulation accessible to all

Open tools and synthetic data so any team can train, test, and evaluate physical AI.

We started where the stakes are highest, in production with the world’s most demanding teams.

NASA![Saronic](https://www.bifrost.ai/logos/logo-saronic.png)![Seadronix](https://www.bifrost.ai/logos/logo-seadronix.svg)![Honda](https://www.bifrost.ai/logos/logo-honda.png)![Privateer](https://www.bifrost.ai/logos/logo-privateer.png)![ST Engineering](https://www.bifrost.ai/logos/logo-stengineering.png)![NTT Data](https://www.bifrost.ai/logos/logo-nttdata.png)![Havoc](https://www.bifrost.ai/logos/logo-havoc.png)NASA![Saronic](https://www.bifrost.ai/logos/logo-saronic.png)![Seadronix](https://www.bifrost.ai/logos/logo-seadronix.svg)![Honda](https://www.bifrost.ai/logos/logo-honda.png)![Privateer](https://www.bifrost.ai/logos/logo-privateer.png)![ST Engineering](https://www.bifrost.ai/logos/logo-stengineering.png)![NTT Data](https://www.bifrost.ai/logos/logo-nttdata.png)![Havoc](https://www.bifrost.ai/logos/logo-havoc.png)NASA![Saronic](https://www.bifrost.ai/logos/logo-saronic.png)![Seadronix](https://www.bifrost.ai/logos/logo-seadronix.svg)![Honda](https://www.bifrost.ai/logos/logo-honda.png)![Privateer](https://www.bifrost.ai/logos/logo-privateer.png)![ST Engineering](https://www.bifrost.ai/logos/logo-stengineering.png)![NTT Data](https://www.bifrost.ai/logos/logo-nttdata.png)![Havoc](https://www.bifrost.ai/logos/logo-havoc.png)

BACKED BY

![Sequoia](https://www.bifrost.ai/logos/inv-sequoia.png)![Lux Capital](https://www.bifrost.ai/logos/inv-lux.png)![Airbus Ventures](https://www.bifrost.ai/logos/inv-airbus.png)![Wavemaker](https://www.bifrost.ai/logos/inv-wavemaker.png)![Carbide](https://www.bifrost.ai/logos/inv-carbide.png)![Techstars](https://www.bifrost.ai/logos/inv-techstars.png)

## A living library of physical work, across every domain

MARITIME

SPACE

AERIAL

OFF-ROAD

ROBOTICS

OPERATIONS

MANIFOLD

## The evaluation platform for robotics researchers

Run every major simulator benchmark in hours, not days, see exactly where your policy fails, and compare against verified baselines.

manifold-cli

$ manifold run pi0.5 LIBERO-█

GET EARLY ACCESS [LEARN MORE](https://manifold.bifrost.ai/)

Open source release coming soon

One harness for every major simulator

ISAAC LABMUJOCOMANISKILLGENESISSTARDUST

// evaluation today

- ✕A single eval rollout takes 24 hours or more
- ✕Every team reinvents the harness for every policy and every benchmark
- ✕No CI. Reproducibility is nearly impossible

01 **Every benchmark** LIBERO, RoboCasa, or your own scenarios

02 **8× faster** sharded across GPUs by default

03 **Track the SOTA** compare against verified baselines

04 **Find failures** cluster episodes by failure mode

![Manifold run detail: score, per-task pass rates, and clustered failure analysis](https://www.bifrost.ai/manifold/app.png)

STARDUST

## Synthetic data for perception and autonomy

Define a scenario in Python, or just describe it to your coding agent (Claude Code, Codex, any LLM). Stardust renders the rest: diverse, labeled, photorealistic data with rich time-series metadata, no 3D expertise required.

scene.ipynb

```
import bbi world = bbi.World()world.spawn("container_ship", quantity=12)world.spawn("buoy", quantity=30, scatter=True) world.ocean(sea_state=4)world.weather(fog=0.3, time="dusk")cam = world.camera(preset="maritime_eo") imgs = world.render(frames=4000)imgs.download(annotations=["bbox", "segmentation"])
```

[BOOK A DEMO](https://www.bifrost.ai/contact) [READ THE DOCS](https://docs.app.bifrost.ai/)

SENSORS & LABELS

### Multi-domain, photorealistic data matching your operational requirements

One scene, rendered across modalities in perfect registration, with ground-truth labels generated automatically for every frame.

RGBPhotorealistic visible spectrum

IRInfrared and thermal bands

DEPTHPer-pixel depth and range

SEGMENTATION + BBOXESPixel-perfect masks and 2D/3D boxes

NEURAL RENDERING

### Realism and diversity with AI post-processing

A learned post-processing pass closes the domain gap and multiplies diversity. One scene, every condition: weather, lighting, and time of day, all photorealistic, so models transfer cleanly to the real world.

![Synthetic maritime scene, clear conditions](https://www.bifrost.ai/stardust/neural-1.jpg)CLEAR![Synthetic maritime scene, overcast conditions](https://www.bifrost.ai/stardust/neural-2.jpg)OVERCAST![Synthetic maritime scene, fog conditions](https://www.bifrost.ai/stardust/neural-3.jpg)FOG![Synthetic maritime scene, dawn conditions](https://www.bifrost.ai/stardust/neural-4.jpg)DAWN![Synthetic maritime scene, dusk conditions](https://www.bifrost.ai/stardust/neural-5.jpg)DUSK![Synthetic maritime scene, rain conditions](https://www.bifrost.ai/stardust/neural-6.jpg)RAIN

3D ASSETS

### A 1,000+ object 3D asset library, and counting

Drag and drop from over a thousand production-ready, physically-accurate 3D assets, each tagged with real-world dimensions. Need something rare? Generate new assets with AI on demand, or request a custom asset from our 3D team.

![Container ship](https://www.bifrost.ai/stardust/assets/asset-01.webp)

Container ship213 × 43 × 52 m

![Container ship (Maersk)](https://www.bifrost.ai/stardust/assets/asset-02.webp)

Container ship (Maersk)400 × 60 × 73 m

![Cruise ship](https://www.bifrost.ai/stardust/assets/asset-03.webp)

Cruise ship366 × 69 × 78 m

![Response boat](https://www.bifrost.ai/stardust/assets/asset-08.webp)

Response boat14 × 4.7 × 8.1 m

![Kayak](https://www.bifrost.ai/stardust/assets/asset-07.webp)

Kayak5.5 × 2.1 × 0.5 m

![Monitoring buoy](https://www.bifrost.ai/stardust/assets/asset-04.webp)

Monitoring buoy1.0 × 1.0 × 1.1 m

![Special mark buoy](https://www.bifrost.ai/stardust/assets/asset-05.webp)

Special mark buoy2.8 × 2.6 × 6.1 m

![Cardinal mark buoy](https://www.bifrost.ai/stardust/assets/asset-06.webp)

Cardinal mark buoy1.3 × 1.3 × 3.0 m

![Cessna 208 Caravan](https://www.bifrost.ai/stardust/assets/asset-09.webp)

Cessna 208 Caravan13 × 16 × 4.6 m

![Pilatus PC-12](https://www.bifrost.ai/stardust/assets/asset-10.webp)

Pilatus PC-1214 × 16 × 4.2 m

![Harbor crane](https://www.bifrost.ai/stardust/assets/asset-11.webp)

Harbor crane12 × 28 × 29 m

![Shipping port](https://www.bifrost.ai/stardust/assets/asset-12.webp)

Shipping port912 × 1979 × 82 m

![](https://www.bifrost.ai/stardust/assets/asset-01.webp)

Container ship213 × 43 × 52 m

![](https://www.bifrost.ai/stardust/assets/asset-02.webp)

Container ship (Maersk)400 × 60 × 73 m

![](https://www.bifrost.ai/stardust/assets/asset-03.webp)

Cruise ship366 × 69 × 78 m

![](https://www.bifrost.ai/stardust/assets/asset-08.webp)

Response boat14 × 4.7 × 8.1 m

![](https://www.bifrost.ai/stardust/assets/asset-07.webp)

Kayak5.5 × 2.1 × 0.5 m

![](https://www.bifrost.ai/stardust/assets/asset-04.webp)

Monitoring buoy1.0 × 1.0 × 1.1 m

![](https://www.bifrost.ai/stardust/assets/asset-05.webp)

Special mark buoy2.8 × 2.6 × 6.1 m

![](https://www.bifrost.ai/stardust/assets/asset-06.webp)

Cardinal mark buoy1.3 × 1.3 × 3.0 m

![](https://www.bifrost.ai/stardust/assets/asset-09.webp)

Cessna 208 Caravan13 × 16 × 4.6 m

![](https://www.bifrost.ai/stardust/assets/asset-10.webp)

Pilatus PC-1214 × 16 × 4.2 m

![](https://www.bifrost.ai/stardust/assets/asset-11.webp)

Harbor crane12 × 28 × 29 m

![](https://www.bifrost.ai/stardust/assets/asset-12.webp)

Shipping port912 × 1979 × 82 m

## Build physical AI at the speed of compute

From synthetic data to policy evaluation, Bifrost is the infrastructure for AI in the physical world. Tell us what you’re building.

[EXPLORE MANIFOLD](https://manifold.bifrost.ai/) [BOOK A DEMO](https://www.bifrost.ai/contact)

✕

// request access

## Get early access to Manifold

Free for research partners. Tell us a little about your work and we'll be in touch when your spot opens.

NameOrganizationEmailHow many sim evaluations do you run a week?Select…Fewer than 1010 to 5050 to 200More than 200What is your research area?

Specific task performanceCross-embodiment policiesTask generalizationOther

REQUEST ACCESS →

Free for research partners · open-source release coming soon

// request received

Thanks. We read every request and will reach out at the email you provided as spots open up.

CLOSE