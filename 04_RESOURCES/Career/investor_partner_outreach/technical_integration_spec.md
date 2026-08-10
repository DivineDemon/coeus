# Haga Technical Integration Specification
## For Simulation Platform Partners (NVIDIA Omniverse, ANSYS, Unity, Siemens, Dassault)

---

## Overview
This document specifies how Haga's physics verification capabilities can be embedded into simulation platforms as a native plugin, service, or API integration.

**Goal:** Enable simulation platform customers to run independent physics verification on their models with one click — "Simulate in [Platform], Verify with Haga."

---

## Integration Patterns

### Pattern 1: Native Plugin (Deepest Integration)
**Best for:** NVIDIA Omniverse, Unity, Unreal Engine

**Architecture:**
```
┌─────────────────────────────────────────────────────────────┐
│                    SIMULATION PLATFORM                       │
├─────────────────────────────────────────────────────────────┤
│  User Workflow:                                              │
│  1. Build scene in platform                                  │
│  2. Click "Haga Verify" button in toolbar/menu              │
│  3. Platform exports scene + physics params to Haga format  │
│  4. Haga runs verification (cloud or local)                 │
│  5. Results appear in platform UI (panel, overlay, report)  │
└─────────────────────────────────────────────────────────────┘
```

**Technical Requirements:**
- Platform SDK/API for scene export (USD for Omniverse, UXML for Unity, etc.)
- Physics parameter extraction (mass, friction, restitution, contact params per body)
- UI extension point for "Verify" action and results panel
- Async job handling (verification takes minutes to hours)

---

### Pattern 2: REST API / Webhook (Standard Integration)
**Best for:** ANSYS, Siemens, Dassault, COMSOL, Altair

**Architecture:**
```
┌─────────────────────┐     HTTPS/JSON      ┌─────────────────────┐
│  SIMULATION PLATFORM│◄───────────────────►│     HAGA API        │
├─────────────────────┤                     ├─────────────────────┤
│  POST /verify       │  Request:           │  POST /verify       │
│  GET /verify/{id}   │  - scene_id         │  Returns: job_id    │
│  Webhook: complete  │  - physics_params   │  GET /verify/{id}   │
└─────────────────────┘  - tasks[]          │  Returns: results   │
                        - config{}          │  Webhook: done      │
                        └─────────────────────┘
```

**API Specification:**

#### POST /api/v1/verify
```json
{
  "scene_id": "ansys_project_12345",
  "platform": "ansys",
  "physics_parameters": {
    "bodies": [
      {
        "name": "robot_link_1",
        "mass": 2.5,
        "inertia": [0.1, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1],
        "contact": {
          "friction": 0.8,
          "restitution": 0.1,
          "contact_stiffness": 1e6,
          "contact_damping": 1e3
        }
      }
    ],
    "global": {
      "gravity": [0, 0, -9.81],
      "timestep": 0.001,
      "solver_iterations": 50
    }
  },
  "tasks": [
    {
      "type": "pillar1_stress_test",
      "task_name": "pickplacecan",
      "stress_tiers": ["mild", "moderate"],
      "episodes_per_tier": 20,
      "baseline_policy": "osc_pose"
    },
    {
      "type": "pillar2_video_check",
      "video_url": "https://platform.com/sim_output/video.mp4",
      "tracker": "cotrack3",
      "profile": "video_checks"
    }
  ],
  "config": {
    "held_out_protocol": "v1",
    "output_format": "json",
    "notify_webhook": "https://platform.com/webhooks/haga/complete"
  }
}
```

#### Response
```json
{
  "job_id": "haga_verify_abc123",
  "status": "queued",
  "estimated_completion": "2026-08-10T14:30:00Z",
  "poll_url": "https://api.haga.ai/api/v1/verify/haga_verify_abc123"
}
```

#### GET /api/v1/verify/{job_id}
```json
{
  "job_id": "haga_verify_abc123",
  "status": "completed",
  "completed_at": "2026-08-10T14:25:00Z",
  "results": {
    "pillar1_stress_test": {
      "pickplacecan": {
        "mild": {
          "episodes": 20,
          "success_rate": 0.85,
          "grasp_failure_rate": 0.10,
          "gate_passed": true,
          "failure_modes": [
            {"type": "light_object_slip", "count": 2, "mass_range": "[0.05, 0.15]"}
          ]
        },
        "moderate": {
          "episodes": 20,
          "success_rate": 0.62,
          "grasp_failure_rate": 0.28,
          "gate_passed": false,
          "failure_modes": [
            {"type": "light_object_slip", "count": 8, "mass_range": "[0.02, 0.2]"},
            {"type": "high_friction_stall", "count": 5, "friction_range": "[1.2, 2.0]"}
          ]
        }
      }
    },
    "pillar2_video_check": {
      "detectors": {
        "permanence": {"score": 0.98, "violations": 0},
        "ballistic": {"score": 0.94, "violations": 2},
        "contact": {"score": 0.99, "violations": 0},
        "static_hover": {"score": 0.96, "violations": 1}
      },
      "overall_physics_iq": 0.967,
      "held_out_protocol": "v1"
    }
  },
  "report_url": "https://reports.haga.ai/haga_verify_abc123.pdf",
  "deployment_readiness": "conditional",
  "recommendations": [
    "Increase sim friction noise floor for light objects (<0.2kg)",
    "Add contact damping for high-friction scenarios"
  ]
}
```

---

### Pattern 3: Batch/CLI (CI/CD Integration)
**Best for:** All platforms — automated regression verification

**Usage:**
```bash
# Platform CI pipeline step
haga-cli verify \
  --scene-id ansys_project_12345 \
  --platform ansys \
  --physics-params physics_params.json \
  --tasks pillar1_stress_test,pillar2_video_check \
  --config config.yaml \
  --output results.json \
  --fail-on-gate-failure
```

**Exit codes:**
- `0`: All gates passed
- `1`: Gate failure (configurable per task)
- `2`: Error (API, auth, validation)

---

## Data Exchange Formats

### Physics Parameters Schema (Haga Physics Parameter Format - HPPF)
```yaml
# Standardized format for physics parameters across platforms
version: "1.0"
platform: "ansys"  # | omniverse | unity | unreal | mujoco | drake | isaac_sim
exported_at: "2026-08-10T12:00:00Z"
scene:
  name: "pickplace_task"
  bodies:
    - name: "panda_link0"
      type: "fixed"
      mass: 0
    - name: "panda_hand"
      type: "dynamic"
      mass: 0.5
      inertia: [0.01, 0, 0, 0, 0.01, 0, 0, 0, 0.01]
      contact:
        friction: 1.0
        restitution: 0.0
        contact_stiffness: 1e6
        contact_damping: 1e3
        geom_priority: 1  # Critical for Pillar 1
  gravity: [0, 0, -9.81]
  timestep: 0.002
  solver: "cgs"  # | newton | pgs | tgs
  solver_iterations: 100
```

### Task Configuration Schema
```yaml
tasks:
  - type: "pillar1_stress_test"
    task_name: "pickplacecan"  # | lift | stack | door
    stress_tiers: ["mild", "moderate", "severe"]
    episodes_per_tier: 50
    baseline_policy: "osc_pose"  # | user_policy_path
    gate_thresholds:
      success_ratio_min: 0.80
      grasp_fail_delta_max: 0.15
    rng:
      base_seed: 42
      independent_per_tier: true
  
  - type: "pillar2_video_check"
    video_source: "sim_output"  # | platform_generated | user_uploaded
    tracker: "cotrack3"  # | cotrack2 | tapir
    profile: "video_checks"  # | strict | custom
    detectors:
      - permanence
      - ballistic
      - contact
      - static_hover
    calibration:
      protocol: "v1"
      recall_target: 0.95
      false_positive_max: 0.02
```

---

## Authentication & Security

### API Authentication
- **API Keys:** Per-platform, per-environment (dev/staging/prod)
- **JWT Tokens:** For user-delegated actions (OAuth2 integration)
- **mTLS:** Optional for enterprise customers

### Data Privacy
- **Scene data:** Processed in-memory, not persisted after job completion
- **Results:** Encrypted at rest, customer-controlled retention
- **Compliance:** SOC2 Type II (target), GDPR ready

### Deployment Options
1. **Haga Cloud (SaaS):** API at `api.haga.ai` — lowest friction
2. **VPC Deployment:** Haga runs in customer's cloud account (AWS/GCP/Azure)
3. **On-Premise:** Air-gapped deployment for defense/regulated customers
4. **Hybrid:** Control plane in Haga Cloud, workers in customer VPC

---

## Platform-Specific Integration Details

### NVIDIA Omniverse (Isaac Sim)
- **Extension:** Omniverse Kit extension (Python + Carbonite)
- **Scene Export:** USD → HPPF converter
- **UI:** Toolbar button + Results panel in Isaac Sim viewport
- **Video Capture:** Built-in RTX renderer → MP4 for Pillar 2
- **Auth:** NVIDIA NGC API key integration

### Unity (Unity Physics / Havok)
- **Package:** Unity Package Manager (UPM) package
- **Scene Export:** UXML/EntityComponentSystem → HPPF
- **UI:** Editor window + Runtime verification component
- **Video Capture:** Unity Recorder integration
- **Auth:** Unity Services authentication

### ANSYS (Mechanical, Explicit, Twin Builder)
- **ACT Extension:** ANSYS Customization Toolkit (Python)
- **Parameter Extraction:** APDL/Python scripting → HPPF
- **Integration:** Workbench workflow step
- **Results:** Embedded in Workbench project schematic
- **Auth:** ANSYS licensing integration

### Siemens (Simcenter, NX, Solid Edge)
- **CAE Integration:** Simcenter 3D / NX Open API
- **Parameter Extraction:** NX Open / CAE API → HPPF
- **Workflow:** Verification as post-processing step
- **Results:** Embedded in Simcenter dashboard

### Dassault Systèmes (SIMULIA, CATIA, 3DEXPERIENCE)
- **3DEXPERIENCE App:** Web-based app on platform
- **Parameter Extraction:** SIMULIA Abaqus/Isight → HPPF
- **Integration:** 3DEXPERIENCE dashboard widget
- **Results:** Stored in 3DEXPERIENCE collaborative space

---

## Pricing & Licensing for Partners

### Integration Partnership Tiers

| Tier | License Fee | Revenue Share | Support | SLA |
|------|-------------|---------------|---------|-----|
| **Certified Partner** | $0 | 20% of verification revenue | Email, docs | Best effort |
| **Strategic Partner** | $0 | 30% + co-marketing fund | Dedicated Slack, quarterly reviews | 99.9% API uptime |
| **OEM / White-Label** | Annual fee | Custom | Embedded engineering, co-roadmap | 99.95% + custom SLA |

### Customer Pricing (Partner Sets)
- Partner controls end-customer pricing
- Haga provides suggested retail prices
- Volume discounts at partner level

---

## Implementation Roadmap

### Phase 1: MVP Integration (Months 1-2)
- [ ] REST API v1 stable
- [ ] HPPF schema v1.0 finalized
- [ ] Reference implementation: Python SDK
- [ ] Sandbox environment for partners
- [ ] Documentation + Postman collection

### Phase 2: Platform SDKs (Months 2-4)
- [ ] Omniverse Kit extension (alpha)
- [ ] Unity UPM package (alpha)
- [ ] ANSYS ACT extension (alpha)
- [ ] CLI tool v1.0

### Phase 3: Production Hardening (Months 4-6)
- [ ] All SDKs beta
- [ ] Load testing, error handling, retries
- [ ] Partner onboarding program
- [ ] Joint marketing materials

### Phase 4: Scale (Month 6+)
- [ ] GA releases
- [ ] Marketplace listings (Omniverse, Unity Asset Store, ANSYS App Store)
- [ ] Co-selling motions
- [ ] Advanced features: custom detectors, policy import, comparison views

---

## Technical Contacts

**Haga Integration Team:**
- Mushood Hanif, Founder — haga@mushoodhanif.com
- [Engineering Lead — TBD]
- [Partner Engineering — TBD]

**Partner Requirements:**
- Named technical contact
- Access to platform SDK/documentation
- Sandbox environment for testing
- Joint testing / certification process

---

## Appendix: Example Integration Code

### Python SDK Usage
```python
from haga import HagaClient, VerificationJob, Pillar1Config, Pillar2Config

client = HagaClient(api_key="platform_partner_key_123")

# Submit verification job
job = VerificationJob(
    scene_id="ansys_proj_12345",
    platform="ansys",
    physics_params=load_hppf("physics_params.hppf"),
    tasks=[
        Pillar1Config(
            task_name="pickplacecan",
            stress_tiers=["mild", "moderate"],
            episodes_per_tier=20
        ),
        Pillar2Config(
            video_url="https://platform.com/sim/video.mp4",
            profile="video_checks"
        )
    ],
    webhook_url="https://platform.com/webhooks/haga/complete"
)

job_id = client.submit(job)
print(f"Job submitted: {job_id}")

# Poll for results
results = client.wait_for(job_id, timeout=3600)
print(f"Physics IQ: {results.pillar2.overall_physics_iq}")
print(f"Deployment readiness: {results.deployment_readiness}")

# Generate report
report_pdf = client.generate_report(job_id, format="pdf")
```

### Webhook Handler (Platform Side)
```python
# Flask/FastAPI endpoint
@app.post("/webhooks/haga/complete")
async def haga_webhook(payload: HagaWebhookPayload):
    job_id = payload.job_id
    status = payload.status
    results = payload.results
    
    # Update platform UI
    update_verification_status(job_id, status, results)
    
    # Notify user
    notify_user(job_id, "Verification complete!")
    
    return {"status": "received"}
```

---

*Document version: 1.0 | Last updated: 2026-08-10*
*For partner review — confidential*