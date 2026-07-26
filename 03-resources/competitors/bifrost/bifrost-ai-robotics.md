# Robot policy evaluation and synthetic data | Bifrost

> Source: https://bifrost.ai/robotics/

MANIFOLD + STARDUST

# Improve your robot policies, faster

Manifold runs any policy on any benchmark and ranks it on a shared leaderboard, so you see exactly what improved and what regressed, run over run. Stardust generates the photorealistic, multi-modal data that trains the perception underneath. One pipeline, from training data to reproducible evaluation.

[BOOK A DEMO](https://www.bifrost.ai/contact) [READ THE DOCS](https://docs.app.bifrost.ai/)

Open source. 1,000 rollouts per run. Any simulator.

## Robots pass in the lab and fail in the field

A policy that clears 90% in the lab can still fail in the field, because real test sets are small, static, and impossible to stage at scale. You cannot evaluate against the long tail of objects, grasps, lighting, and clutter that actually breaks a policy.

Bifrost closes both ends of that loop. Train perception on Stardust synthetic data that covers the long tail, then evaluate the trained policy on Manifold across every benchmark, at thousands of rollouts, with failure analysis you can act on. Evaluation leads, because you cannot improve what you cannot measure.

## Evaluation is the bottleneck

// evaluating robots today

- ✕A single sim eval rollout still takes 24 hours or more, and every benchmark needs a hand-built harness
- ✕Every policy and every benchmark has a different shape, so every lab rebuilds the harness from scratch and the work never compounds
- ✕Reproducibility is informal: no shared leaderboard, no CI, no citable run
- ✕Real-world test sets are broken, and there is no systematic way to evaluate robots at scale

MANIFOLD · POLICY EVALUATION

## Drop in your policy, run millions of evaluations, see exactly where it fails

Manifold is the open-source orchestration layer for robot evaluation. Any policy should run on any benchmark, scaled to a thousand rollouts, without re-engineering the harness.

manifold-cli

$ manifold run pi0.5 L█

**One click, any benchmark** LIBERO, RoboCasa, Isaac Lab, MuJoCo, Genesis, or your own scenarios. Same flow for every policy and embodiment.

**Scale on demand** Parallelize rollouts across thousands of GPU instances. An overnight job becomes a lunch break.

**Live error analysis** Success rate and failure modes per task and per step, as the run progresses, not in a doc at the end.

**Living leaderboard** Rank policies on shared benchmarks. Every run is reproducible and gets a citable manifold:// URI.

**CI for policies** Hook Manifold into training. Every checkpoint is evaluated automatically, so regressions surface before they ship.

**Open source** The standards layer can't be proprietary. Runner, harness, and leaderboard schema are all open.

![Manifold run detail: overall score, per-task pass rates, and clustered failure analysis](https://www.bifrost.ai/manifold/app.png)

GET EARLY ACCESS [EXPLORE MANIFOLD](https://manifold.bifrost.ai/)

## And the perception data behind the policy

**Pixel-perfect labels** Segmentation, depth, 6-DoF pose, and grasp annotations on every frame. No manual labeling.

**Every object and layout** Randomize objects, materials, clutter, and lighting to cover the long tail before deployment.

**Factory and household scenes** Configurable production lines and diverse home environments, so models see the chaos before the real world does.

**Sim-to-real ready** Photorealistic rendering and domain randomization close the gap from simulation to the real cell.

SENSOR COVERAGE

RGBDEPTHSEGMENTATION6-DOF POSEGRASPBBOXES

## Manifold and Stardust, in action

![Manifold run detail](https://www.bifrost.ai/manifold/app.png)

Manifold run detailPer-task pass rates and clustered failure analysis

Auto-docking perceptionRandomized trailer and ramp detection, with Honda Research Institute

Scenarios as codeBuild and vary embodied scenes programmatically

## What teams build with it

**VLA policy evaluation** Run vision-language-action policies on LIBERO, RoboCasa, or your own scenarios.

**Manipulation and grasping** Evaluate pick-and-place, assembly, and grasp policies across objects and clutter.

**Bimanual and dexterity** Score dexterous, two-arm policies on shared benchmarks.

**Humanoid evaluation** Stand up reproducible evaluation for humanoid policies as embodiments scale.

**Sim-to-real transfer** Quantify the gap between simulation and hardware before you deploy.

**Regression testing** Catch policy regressions automatically on every training checkpoint.

**A/B policy comparison** Compare two policies on identical benchmarks and conditions.

**Manipulation perception** Train detection, segmentation, and 6-DoF pose on Stardust synthetic data.

1,000rollouts per run, no harness rebuild

24h → minfrom an overnight eval to a lunch break

95.9%F1 from synthetic-trained perception vs 48.7% on real data, in one detection benchmark

20hand-picked VLA and manipulation design-partner labs

## Speaks your domain

The vocabulary, sensors, and benchmarks robotics teams actually use.

VLAmanipulation policyimitation learningworld modeldomain randomizationsim-to-real6-DoF posegraspbimanualdexterityhumanoidLIBERORoboCasaIsaac LabMuJoCoGenesisrolloutsuccess rateleaderboardCI for policies

Built with the teams setting the bar in robotics and mobility.

![Honda](https://www.bifrost.ai/logos/logo-honda.png)![Mitsubishi](https://www.bifrost.ai/logos/logo-mitsubishi.png)

## Questions teams ask

### How do you evaluate a VLA policy?

Drop the policy into Manifold and run it at thousands of rollouts across any benchmark: LIBERO, RoboCasa, Isaac Lab, MuJoCo. You get success rate plus per-task and per-step failure modes live, and a reproducible run you can cite.

### What is sim-to-real for manipulation?

It is the test of whether a policy that works in simulation holds up on real hardware. Manifold quantifies the gap, and Stardust narrows it with photorealistic synthetic training data.

### How do you run thousands of robot eval rollouts?

Manifold parallelizes rollouts across thousands of GPU instances in one line, turning an overnight job into a lunch break.

### Can I add CI to my robot policy training?

Yes. Hook Manifold into your pipeline and every checkpoint is evaluated automatically, so regressions surface before they ship.

### Why use synthetic data if you already have real data?

Real data gives you more of the same distribution. Synthetic data stress-tests the conditions you never captured and shows which real data to collect next. In one detection benchmark, synthetic-trained models hit 95.9% F1 versus 48.7% for real.

## Put your policy on the board

Tell us what you are building and the scenarios you need. We will get you access.

[BOOK A DEMO](https://www.bifrost.ai/contact) [EXPLORE MANIFOLD](https://manifold.bifrost.ai/)

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