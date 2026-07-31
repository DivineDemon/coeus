# Master Codebase Registry & Map of Content (MOC)

This note indexes all repositories housed within the main code vault directory: `/Users/mushood/Documents/code/`.

---

## 1. Haga Ecosystem (`/Documents/code/haga/`)
> **Focus**: Independent trust and verification layer for robot learning policies & generative world models.

- **[haga-core](file:///Users/mushood/Documents/code/haga/haga-core)**
  - **Path**: `/Users/mushood/Documents/code/haga/haga-core`
  - **Stack**: Python 3.12, MuJoCo, MJX, JAX, Robosuite, CoTracker, CogVideoX
  - **Role**: Core physics benchmark engine, policy stress-testing, world-model consistency checker, metrics publisher (`artifacts/public/`).
  - **Status**: Live benchmark active; publication contract versioned via GitHub Releases (`metrics-latest`).

- **[haga-web](file:///Users/mushood/Documents/code/haga/haga-web)**
  - **Path**: `/Users/mushood/Documents/code/haga/haga-web`
  - **Stack**: Next.js / TypeScript monorepo (`apps/site`, `apps/dataroom`, `packages/brand`)
  - **Role**: Public site ([haga.mushoodhanif.com](https://haga.mushoodhanif.com)), Lab evidence browser, Data Room for investor diligence.
  - **Status**: Consumes sanitized metrics JSON published by `haga-core`.

---

## 2. AI Services & Freelance (`/Documents/code/freelance/`)
> **Focus**: Client deliverables, AI tools, and enterprise automation software.

- **[ezra-bid-assistant](file:///Users/mushood/Documents/code/freelance/ezra-bid-assistant)**
  - **Path**: `/Users/mushood/Documents/code/freelance/ezra-bid-assistant`
  - **Stack**: Python / AI Agent framework
  - **Role**: Automated proposal generation & bid scoring assistant.

- **[ezra-global](file:///Users/mushood/Documents/code/freelance/ezra-global)**
  - **Path**: `/Users/mushood/Documents/code/freelance/ezra-global`
  - **Role**: Platform infrastructure & web services for Ezra client suite.

- **[salon-pos](file:///Users/mushood/Documents/code/freelance/salon-pos)**
  - **Path**: `/Users/mushood/Documents/code/freelance/salon-pos`
  - **Role**: Point of sale & management web system for salon client.

---

## 3. Work Repositories (`/Documents/code/work/`)
> **Focus**: Production engineering projects and enterprise client work.

| Repository Name | Path | Description / Scope |
| :--- | :--- | :--- |
| **adcp** | `/Users/mushood/Documents/code/work/adcp` | Autonomous Data & Content Processing service |
| **agbsim** | `/Users/mushood/Documents/code/work/agbsim` | Simulation engine / agent modeling harness |
| **brsc** | `/Users/mushood/Documents/code/work/brsc` | Business rule & analytics service |
| **faq-srp** | `/Users/mushood/Documents/code/work/faq-srp` | FAQ Search & Retrieval Pipeline |
| **fbf-re** | `/Users/mushood/Documents/code/work/fbf-re` | Rule engine & data pipeline |
| **oplftsf** | `/Users/mushood/Documents/code/work/oplftsf` | Time-series forecasting & optimization pipeline |
| **rtfsp** | `/Users/mushood/Documents/code/work/rtfsp` | Real-time stream processor |
| **ue-sc** | `/Users/mushood/Documents/code/work/ue-sc` | Unified enterprise sync connector |

---

## 4. Personal Projects (`/Documents/code/personal/`)
> **Focus**: Personal knowledge systems, portfolio, and research.

- **[coeus](file:///Users/mushood/Documents/code/personal/coeus)**
  - **Path**: `/Users/mushood/Documents/code/personal/coeus`
  - **Role**: The 2nd Brain Obsidian Vault & Hermes Agent control tower.

- **[portfolio](file:///Users/mushood/Documents/code/personal/portfolio)**
  - **Path**: `/Users/mushood/Documents/code/personal/portfolio`
  - **Role**: Personal founder/consultant showcase website ([mushoodhanif.com](https://mushoodhanif.com)).

- **[research](file:///Users/mushood/Documents/code/personal/research)**
  - **Path**: `/Users/mushood/Documents/code/personal/research`
  - **Role**: Academic paper notes, prototype scripts, AI model evaluations.
