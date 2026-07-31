# Enterprise & Work Repositories Overview

> **Core Focus**: Production engineering, high-throughput microservices, real-time analytics, ML pipelines, and MLOps infrastructure built during enterprise roles (Afiniti, Confiz, etc.). This document captures extreme technical depth and impact metrics for each system.

---

## Repositories Index (`/Documents/code/work/`)

### 1. adcp (Agentic Document Compliance Pipeline)
- **Description**: An enterprise-grade, 6-Agent LangGraph orchestration pipeline for autonomous document extraction, regulatory compliance verification, citation grounding, and HITL review.
- **Tech Stack**: Python 3.10+, LangGraph, MCP (Model Context Protocol), LLaMA-3 QLoRA, FastAPI.
- **Architecture**: 6-agent workflow: Intake Agent, Extraction Agent (fine-tuned LLaMA-3), Verifier Agent, Compliance Agent, Confidence Router, HITL Gate Agent.
- **Resume Metrics**:
  - Cut manual document-processing time by ~92% (from 3 days to under 4 hours).
  - Raised extraction accuracy from 81% to 96.1% F1 by fine-tuning domain-specific LLaMA-3 models with QLoRA on a single on-prem A100 GPU.
  - Cut agent hallucination rate from 11.0% to 1.8% via citation-grounding.
  - False-approval rate slashed from 6.0% to 0.4% using a Confidence Router Agent.
  - Reduced API integration time from ~2 weeks to 2 days using an MCP Tool Routing Layer exposing 9 internal APIs (e.g., `tariff_lookup`, `hs_code_validator`, `incoterms_rules_engine`).
  - Reduced GPU idle time by 35% with a dynamic batching and request-queuing scheduler.

### 2. agbsim (Azure GPU Streaming Inference Migration)
- **Description**: Production-grade MLOps showcase migrating a legacy on-premise batch inference system to a high-throughput GPU-backed streaming microservice on Azure (FastAPI, Redis, PyTorch, Azure AKS).
- **Architecture**: Async FastAPI streaming server (SSE), Redis async broker, PyTorch dynamic tensor batching on Azure Standard_NC6s_v3 / T4 GPUs. Blue-Green deployment orchestrator with automated circuit-breaker rollback.
- **Resume Metrics**:
  - Inference latency slashed from 2.1s (2071ms p50) to 170.3ms p95 (~92% reduction) with Time-To-First-Token < 31ms.
  - Per-transaction compute cost cut by 64% ($1,332/mo savings per 1M daily requests) replacing 24/7 CPU allocation with right-sized Azure GPUs + real-time HPA autoscaling.
  - Deployment rollback time cut from ~40m to <5m (instant automated rollback upon circuit breaker trip).

### 3. brsc (Bilingual RAG Support Chatbot)
- **Description**: Production-grade, highly concurrent conversational assistant and MLOps analytics dashboard for bilingual (Urdu & English) customer support.
- **Tech Stack**: FastAPI, PyTorch, Celery, Redis, FAISS, Docker, `paraphrase-multilingual-MiniLM-L12-v2`.
- **Architecture**: FAISS HNSW-Based Retrieval Engine replacing O(N) brute force cosine similarity with O(log N) flat index for sub-60ms retrieval. Model weight quantization (FP32 to INT8) via ONNX Runtime reducing memory footprint by ~75% (470MB to 117MB).
- **Resume Metrics**: Dual-boundary threshold routing: Vetted Match directly neutralizes LLM hallucinations (~80% reduction), Generative RAG synthesizes localized response, Escalation Gate routes to human support. Sustains 95+ requests/second at p95 latencies < 400ms.

### 4. faq-srp (FAQ Search Reranking Prototype)
- **Description**: Multi-stage search architecture (Legacy Keyword Candidate Retrieval → TF-IDF & Feature-Weighted Reranker) and a Semi-Automated Active Learning Loop.
- **Architecture**: Candidate Retrieval + TF-IDF Feature Reranker (sublinear TF, n-grams, cosine vector spaces). Uncertainty & Margin Sampling pipeline.
- **Resume Metrics**:
  - +18 Point FAQ Accuracy Boost (62% -> 80%+) achieving Top-3 Accuracy of 93.33% and MRR 0.8667.
  - Cut labeling backlog from 3,000 to <200 tickets via an active-learning pseudo-label verification loop (100% backlog reduction simulation auto-accepting 2,824 high confidence tickets).

### 5. fbf-re (FAISS-Based FAQ Retrieval Engine)
- **Description**: High-performance bilingual semantic support system and MLOps query triage dashboard.
- **Tech Stack**: Python 3.14 (implied future), FastAPI, FAISS-CPU, Celery, SQLite.
- **Architecture**: WebAssembly-powered client-side demo capability. Zero-downtime hot-reloading using `os.path.getmtime` for FAISS index refreshes via a Celery worker.
- **Resume Metrics**:
  - Latency optimized from 340ms to 60ms.
  - Hallucination reduced by ~80% via custom confidence thresholding (default: 0.70).
  - 60% Direct QA Load Reduction via MLOps relevance logging triage dashboard.

### 6. oplftsf (On-Prem LLM Fine-Tuning & Serving Framework)
- **Description**: Enterprise-grade framework for on-premise QLoRA fine-tuning, vLLM-based serving with dynamic adapter-swapping, and self-service CLI tooling ensuring data residency.
- **Tech Stack**: Python 3.10+, QLoRA (4-bit NF4, target modules), vLLM, FastAPI, React/TypeScript.
- **Architecture**: Dynamic scheduler and queue manager. Serves dozens of fine-tuned LoRA adapters dynamically over a shared 4-bit base model (`Meta-Llama-3-8B-Instruct`) with LRU in-memory caching.
- **Resume Metrics**:
  - Reduced Model-to-Production time from 6 weeks to 9 days (~78% faster) across 4 internal product teams.
  - 45% GPU Memory Savings via NF4 quantization and dynamic adapter swapping.
  - 35% reduction in GPU idle time via dynamic batching.
  - Raised extraction F1 accuracy from 81% to 96% on logistics domain datasets.

### 7. rtfsp (Real-Time Fraud Scoring Pipeline)
- **Description**: High-throughput, low-latency streaming fraud detection pipeline combining gradient-boosted trees with a secondary ensemble classifier and real-time feature store.
- **Architecture**: Sub-5ms online feature store sliding windows (Redis). LightGBM primary model + Secondary Ensemble (RF + ExtraTrees) for ambiguous score bands [0.45, 0.80]. Canary auto-rollback framework.
- **Resume Metrics**:
  - Scores 1.2M+ daily transactions at <180ms p95 latency (slashing from 2.1s, a 92% reduction).
  - Slashed False Positive Rate from 14.0% to 3.5% while raising recall by +22% against a 50k-case labeled dataset.
  - Reduced model-drift incidents by 80% using automated Population Stability Index (PSI) monitoring triggering weekly retraining (drift threshold > 0.25).
  - Canary deployment instant auto-rollback reduced MTTR from ~50m to ~8m (error threshold > 2.0%).

### 8. ue-sc (Bilingual Urdu-English Sentiment Classifier)
- **Description**: End-to-end Machine Learning system for Bilingual (Urdu, Roman Urdu, English) Sentiment Analysis for customer support.
- **Architecture**: Fine-tuned `xlm-roberta-base` / `bert-base-multilingual-cased`. Bilingual text normalization (Arabic Unicode normalizations, Roman Urdu standardizations like `bht`->`bohat`). Entropy-based active learning sampler $H(p) = -\sum p_i \log_2(p_i)$.
- **Resume Metrics**:
  - 89% Accuracy on 12,000 Support Tickets across Urdu script, Roman Urdu, and English.
  - Cut Retraining Turnaround by 45% through repeatable preprocessing pipelines.
  - Reduced Feedback-Tagging Effort by 70% with a real-time auto-tagging API (sentiment, priority routing).
  - Cut Backlog from 3,000 to <200 Tickets using Uncertainty sampling (93.3% workload reduction).
