---
type: repo
status: active
tags: [repo, ai, research]
url: https://github.com/DivineDemon/research
stack: [Python, PyTorch, LaTeX]
deployed: false
private: false
last_synced: 2026-07-21
aliases: [Research Monorepo]
---

# Research

A monorepo of independent research projects spanning **neural inductive learning**, **computational geometry**, and **structural solvability theory**. Each top-level directory is a self-contained line of work with its own artifacts (code, LaTeX, or notes).

| Project | Status | Type |
|---------|--------|------|
| [`ion/`](ion/) | Active — full experiment suite | Python / PyTorch |
| [`polygon-inference/`](polygon-inference/) | In progress — formulation & notes | Theory / geometry |
| [`unsolvability/`](unsolvability/) | In progress — draft paper | LaTeX |

---

## Table of contents

- [Overview](#overview)
- [Repository structure](#repository-structure)
- [Projects](#projects)
  - [ION — Inductive invariant for Ordered Networks](#ion--inductive-invariant-for-ordered-networks)
  - [Polygon inference](#polygon-inference)
  - [Structural solvability](#structural-solvability)
- [Getting started (ION)](#getting-started-ion)
- [Reproducing ION experiments](#reproducing-ion-experiments)
- [Building papers](#building-papers)
- [License](#license)

---

## Overview

This repository collects research on three related themes:

1. **Learning with inductive structure (ION).** Neural networks trained with an auxiliary *inductive consistency* loss that ties consecutive hidden states via a learned invariant \(P\) and update rule \(F\), so that \(P(h_{t+1}) \approx F(P(h_t), x_t)\). Inspired by the Principle of Mathematical Induction (PMI), ION targets **length generalization** (train on short sequences, test on long ones) and **depth stability** (consistent behavior across many layers).

2. **Polygon inference from unordered points.** Given a finite set of 2D points with no prescribed order or adjacency, infer a simple polygon whose edges are approximately equilateral, optionally adding Steiner vertices. Includes feasibility analysis (reachability bounds, equilateral constraints) and cost-function design.

3. **Structural solvability.** A meta-level framework for recognizing when a problem has *no* admissible solution before committing resources. Problems are tuples \(P = (S, G, C, K)\) (state, goal, constraints, knowledge); the *dead region* \(\mathcal{D}\) is the set of instances with empty solution sets.

---

## Repository structure

```
research/
├── README.md                 # This file
├── LICENSE                   # GPL-3.0 (repo root)
│
├── ion/                      # PMI-inspired neural network training (ION)
│   ├── README.md             # Detailed ION setup & usage
│   ├── requirements.txt
│   ├── configs/              # YAML experiment configs
│   ├── src/                  # Models, training, analysis, runners
│   ├── scripts/              # Batch experiment & data scripts
│   ├── results/              # Experiment outputs (JSON, CSV)
│   └── overleaf/             # LaTeX source for the ION paper
│
├── polygon-inference/          # Polygon reconstruction from point sets
│   ├── formulation.md        # Formal problem statement & feasibility
│   └── Polygon_Inference_Study_Summary.docx
│
└── unsolvability/              # Structural solvability framework (draft)
    ├── main.tex
    └── refs.bib
```

---

## Projects

### ION — Inductive invariant for Ordered Networks

**Location:** [`ion/`](ion/)  
**Paper:** [`ion/overleaf/`](ion/overleaf/)

ION adds two learned modules to standard architectures (GRU, MLP, Transformer):

- **\(P\)** — maps hidden state \(h\) to an invariant summary \(p\)
- **\(F\)** — predicts the next invariant from the current one and input: \(p_{t+1} \approx F(p_t, x_t)\)

Training minimizes:

\[
\mathcal{L} = \mathcal{L}_{\text{task}} + \lambda \, \mathcal{L}_{\text{ind}}, \quad
\mathcal{L}_{\text{ind}} = \sum_t \big\| P(h_{t+1}) - F(P(h_t), x_t) \big\|^2
\]

Two variants are implemented:

| Variant | Index | Architecture | Module |
|---------|-------|--------------|--------|
| Recurrent ION | Time step | GRU backbone | `IONRecurrent` |
| Universal ION | Layer depth | MLP backbone | `IONUniversal` |
| Transformer ION | Sequence position | Transformer backbone | `IONTransformer` |

**Experiments** compare ION against parameter-matched baselines (GRU, LSTM, MLP, Transformer) on:

- **Length generalization** — cumulative sum, parity, Dyck-1, Dyck-2, last-token (failure case)
- **MNIST classification**
- **Depth stability** — MNIST and CIFAR-10 at depths 4, 8, 16, 32
- **LRA ListOps** and image-sequence tasks
- **Ablations** — \(\lambda\), \(p_{\text{dim}}\), mechanistic ablations (P-only, F-only, random P)
- **Invariant drift** — how the learned invariant changes across depth

Results are stored under `ion/results/` and can be aggregated into paper figures via `python -m src.run_figures_tables`.

For full setup, CLI reference, and parameter-matching guidance, see **[`ion/README.md`](ion/README.md)**.

---

### Polygon inference

**Location:** [`polygon-inference/`](polygon-inference/)

**Problem.** Given a finite point set \(V = \{v_1, \ldots, v_n\} \subset \mathbb{R}^2\) in general position, with **no given order or adjacency**, find a simple polygon \(Q\) whose vertex set is \(V \cup S\) (observed points plus optional inferred Steiner vertices \(S\)), such that edges are approximately equal to a dominant length \(L^*\) estimated from pairwise distances.

**Objective** (model-selection framing):

\[
\text{Cost}(Q) = \lambda_1 \sum_{e \in Q} \mathbb{1}[\,| \text{len}(e) - L^* | > \varepsilon\,]
  + \lambda_2 \, |S|
  + \lambda_3 \sum_{e \in Q} (\text{len}(e) - L^*)^2
\]

**Key results documented in [`formulation.md`](polygon-inference/formulation.md):**

- **Layer A (combinatorial feasibility)** — any point set admits a simple polygon (possibly with added vertices).
- **Layer B (equilateral feasibility)** — the binding constraint: bridging two points \(v_i, v_j\) with a chain of \(k\) edges of length \(L^*\) requires:
  - \(k = 1\): \(d(v_i, v_j) \approx L^*\) (exact match)
  - \(k \geq 2\): \(d(v_i, v_j) \leq k L^*\) (full disk reachable; verified by Monte Carlo)
- **Minimum Steiner count** for a gap of distance \(d\): \(k_{\min}(d) = \lceil d / L^* \rceil\) (with adjustments for the \(k=1\) exact-match case).

The open problem is **simplicity under routing** — reachability alone does not guarantee a non-self-intersecting polygon; fragment pairing and cyclic ordering remain the hard combinatorial core.

**Artifacts:**

| File | Description |
|------|-------------|
| [`formulation.md`](polygon-inference/formulation.md) | Formal problem, feasibility layers, reachability bounds |
| `Polygon_Inference_Study_Summary.docx` | Extended study summary |

No executable code yet; this directory is theory and notes.

---

### Structural solvability

**Location:** [`unsolvability/`](unsolvability/)

Draft paper: *Structural Solvability and Resource-Aware Problem Analysis: A Framework for Recognizing Unsolvability Across Domains*.

**Core idea.** Before choosing an algorithm or allocating effort, determine whether a problem is **structurally unsolvable** — i.e., no admissible resolution exists under the stated goal and constraints.

| Concept | Definition |
|---------|------------|
| Problem | \(P = (S, G, C, K)\) — state, goal, constraints, knowledge |
| Solution mapping | \(\Sigma(P)\) — set of admissible resolutions |
| Dead region | \(\mathcal{D} = \{ P : \Sigma(P) = \emptyset \}\) |
| Reducibility | Preorder \(\le_R\) on problem instances |

**Contributions (draft):**

1. Structural solvability framework with precise definitions and fibres over goal–constraint pairs
2. Sufficient conditions for unsolvability (goal–constraint inconsistency, unreachability, knowledge gaps)
3. Structural theorems (dead-region projection, monotonicity)
4. Practical methodology — decompose real situations into \((S, G, C, K)\) and apply an unsolvability checklist

This work is **meta-level**: it does not compete with computability theory or universal agency (e.g. AIXI); it addresses when to redirect effort *before* formalizing or solving.

**Build the draft:**

```bash
cd unsolvability
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or upload `unsolvability/` to [Overleaf](https://www.overleaf.com).

---

## Getting started (ION)

The only project with runnable code is **ION**. All commands below assume you are in the `ion/` directory.

### Requirements

- Python 3.9+
- CPU works for smoke tests; **GPU (CUDA) recommended** for full experiments
- Optional: Bash (for `scripts/run_all_experiments.sh`; on Windows use WSL or run Python commands directly)

### Setup

```bash
cd ion

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .\.venv\Scripts\Activate.ps1     # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# (Optional) GPU-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

### Verify installation

```bash
python -m src.run_unit_check
```

Checks forward-pass shapes, inductive loss computation, and parameter-count helpers.

### Quick smoke test

```bash
python -m src.run_length_gen --task cumsum --model ion --epochs 2 --seeds 42
python -m src.run_mnist --epochs 5 --seeds 42
```

---

## Reproducing ION experiments

All experiment runners live in `ion/src/` and are invoked as Python modules from `ion/`.

| Experiment | Command |
|------------|---------|
| Length-gen (single) | `python -m src.run_length_gen --task cumsum --model ion` |
| Length-gen (all tasks × models) | `python -m src.run_length_gen --all` |
| MNIST | `python -m src.run_mnist --seeds 42,123,456,789,1024` |
| Depth (CIFAR) | `python -m src.run_depth --dataset cifar` |
| LRA ListOps | `python -m src.run_lra --task listops --model ion` |
| Ablations (\(\lambda\), \(p_{\text{dim}}\)) | `python -m src.run_ablations --sweep both` |
| Mechanistic ablations | `python -m src.run_mechanistic_ablations` |
| Invariant drift | `python -m src.run_drift` |
| Figures & tables | `python -m src.run_figures_tables` |

**Full suite** (several hours; GPU recommended):

```bash
./scripts/run_all_experiments.sh
```

Quick run with fewer epochs:

```bash
QUICK=1 ./scripts/run_all_experiments.sh
```

**Default seeds:** `42, 123, 456, 789, 1024` (override with `--seeds` or `SEEDS=...`).

**Config hierarchy:** `configs/base.yaml` → task config (e.g. `configs/length_gen/cumsum_ion.yaml`) → CLI overrides.

**Results layout:**

```
ion/results/
├── length_gen/<task>/<model>/     # accuracy_vs_length.csv, summary.json
├── mnist/
├── depth/
├── lra/listops/<model>/
├── ablations/
├── mechanistic_ablations/
└── drift/
```

---

## Building papers

| Paper | Source | Build |
|-------|--------|-------|
| ION (PMI-NN) | [`ion/overleaf/main.tex`](ion/overleaf/main.tex) | Upload `ion/overleaf/` to Overleaf, or compile locally |
| Structural solvability | [`unsolvability/main.tex`](unsolvability/main.tex) | Same |

**ION paper (local build):**

```bash
cd ion/overleaf
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

To regenerate figures and tables from experiment results before compiling:

```bash
cd ion
python -m src.run_figures_tables
python scripts/build_overleaf.py   # assembles overleaf/ from results + paper sources
```

---

## License

This repository is licensed under the [GNU General Public License v3.0](LICENSE). The `ion/` subdirectory carries its own [LICENSE](ion/LICENSE) (also GPL-3.0).

---

## Author

**Mushood Hanif** — [mohdmushood@yahoo.com](mailto:mohdmushood@yahoo.com)

## Related

- Skills: [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- Resume: [[03-resources/resumes/resume-ai-engineer|Resume — AI Engineer]]
- Profile: [[03-resources/social-profiles/GitHub|GitHub]]
- Index: [[03-resources/github-repos/github-overview|GitHub Repos]]
