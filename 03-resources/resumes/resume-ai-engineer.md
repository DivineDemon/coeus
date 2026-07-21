---
type: resume
status: active
tags: [resume, career, ai]
target_role: AI Engineer
last_synced: 2026-07-21
aliases: [Resume A, AI Resume]
---

# Mushood Mohammed Hanif

**Lahore, Pakistan**  
📧 mohdmushood@yahoo.com  
📞 +92 326 886 0405  
🌐 https://mushoodhanif.com  
🔗 https://linkedin.com/in/mushood-hanif  
💻 https://github.com/DivineDemon

---

# Professional Summary

AI Engineer with 5+ years in Python engineering and 3+ years building production LLM and multi-agent systems for enterprise clients across North America, Europe, and APAC. Skilled in RAG architecture, multi-agent orchestration, LLM fine-tuning, MCP-based tool integration, and AI/MLOps on Azure, AWS, and GCP.

---

# Technical Skills

## RAG & Retrieval
- Embeddings
- Semantic search
- Reranking
- Chunking
- GraphRAG

## Languages / Backend
- Python
- FastAPI
- Flask
- REST APIs
- Microservices
- asyncio

## Agentic Frameworks
- LangGraph
- LangChain
- AutoGen
- CrewAI
- Semantic Kernel
- LlamaIndex
- MCP

## Vector Databases
- Pinecone
- Chroma
- FAISS
- Weaviate
- Milvus
- OpenSearch
- Azure AI Search
- pgvector

## Cloud & DevOps
- Docker
- Kubernetes
- GitHub Actions
- Azure AI Foundry
- AWS SageMaker
- GCP Vertex AI

## AI/MLOps
- LangSmith
- MLflow
- Phoenix
- Ragas
- TruLens
- Arize
- OpenTelemetry
- CI/CD for model deployment

## LLM Providers
- OpenAI
- Azure OpenAI
- AWS Bedrock
- Anthropic Claude
- Google Gemini
- Meta Llama
- Mistral

## Governance
- Neo4j
- Knowledge graphs
- Entity extraction
- PII masking
- Prompt-injection prevention
- Responsible AI

## Fine-Tuning
- PEFT
- Instruction-tuning
- RLHF/DPO
- Dataset curation
- Synthetic data
- Distillation
- Embedding adaptation

---

# Experience

## Senior AI Engineer
**Prodago (prodago.com)** — Lahore, Pakistan · Hybrid  
**Jan 2024 – June 2026**

- Deployed a multi-agent support platform (LangGraph, CrewAI, AutoGen), cutting case handling time by 42%.
- Built RAG pipelines over 500K+ documents (Azure AI Search, OpenSearch, pgvector), lifting answer relevance by 35% (Ragas).
- Ran an AI/MLOps stack (LangSmith, MLflow, Phoenix, OpenTelemetry) for versioning, registry, and cost tracking across 3 agent workflows.
- Fine-tuned a Llama-3-8B triage classifier (QLoRA/PEFT, DPO tuning, synthetic data, AWS SageMaker), raising accuracy from 81% to 94% and cutting cost by 35%.
- Built an internal MCP server standardizing CRM, ticketing, and knowledge-base tool access for agents across teams.
- Integrated Claude and Azure OpenAI via tool-calling; added PII masking and prompt-injection guardrails for regulated clients.
- Shipped asyncio-based FastAPI services on Docker/Kubernetes (Azure AI Foundry, CI/CD), supporting 99.9% uptime.

---

## GenAI Developer
**PureLogics (purelogics.net)** — Lahore, Pakistan  
**Apr 2022 – Dec 2023**

- Built ingestion/embedding pipelines (LlamaIndex, FAISS, piloted Pinecone) for a legal-tech client, cutting review time by 60%.
- Shipped FastAPI microservices for LLM summarization and semantic search, integrated with client CRM.
- Fine-tuned Mistral-7B (LoRA) and a domain-adapted embedding model on legal clauses, cutting correction rate by 22%.
- Benchmarked OpenAI, Bedrock, and Llama models; distilled a smaller model from GPT-4 outputs, saving 20% on inference.
- Migrated legacy synchronous Flask services to async FastAPI, cutting p95 API latency by 45% under peak load.

---

## Python / Backend Developer
**SoftSquare (softsquare.io)** — Lahore, Pakistan  
**Nov 2020 – Mar 2022**

- Built REST APIs and microservices (Flask, FastAPI); introduced early NLP automation (spaCy, Hugging Face).
- Wrote unit/integration test suites achieving 80%+ coverage, cutting production bugs by 30%.
- Optimized PostgreSQL queries and added Redis caching, reducing average API response time by 50%.
- Set up Docker-based CI/CD, cutting deployment time from days to hours.

---

# Key Projects

## Enterprise Multi-Agent Support Assistant

### Problem
Multi-system support requiring cross-referencing tickets, contracts, and docs.

### Architecture
LangGraph planner/retriever/executor/validator agents with human-in-the-loop escalation, fronted by an internal MCP server for CRM/ticketing tools.

### Models
Azure OpenAI (GPT-4-class) + Claude fallback; QLoRA fine-tuned Llama-3-8B triage classifier for low-cost routing.

### RAG
Hybrid retrieval over Azure AI Search + pgvector (Weaviate piloted for a data-residency case); cross-encoder reranking.

### Ops
AKS blue-green deploys via GitHub Actions; Ragas/LangSmith/Phoenix eval gates block regressions; MLflow registry.

### Impact
- 42% faster handling
- 30% ticket deflection (CSAT, resolution-time KPIs)

---

## Contract Intelligence & Compliance RAG Platform

### Problem
Legal/procurement teams losing 15+ hrs/week manually searching contracts for obligations and risk.

### Architecture
LlamaIndex retriever + validator agents with a rules-based compliance-checking layer.

### Models
GPT-4-class for extraction; self-hosted LoRA fine-tuned Mistral-7B for low-sensitivity batches.

### RAG
Clause-aware chunking; FAISS (scaled to Milvus) with metadata filters; Neo4j GraphRAG for cross-contract queries.

### Ops
FastAPI on AWS ECS with autoscaling; PII masking at ingestion; SageMaker fine-tuning tracked in MLflow; TruLens/Arize monitoring.

### Impact
- 60% faster review
- $1.2M in missed renewal-fee exposure flagged in Q1

---

## Multi-Model Cost/Quality Routing Framework

### Problem
All LLM traffic routed through one costly frontier model regardless of task complexity.

### Architecture
Semantic Kernel routing agent classifying requests, shared via an MCP interface across internal agents.

### Models
OpenAI, Bedrock (Claude, Llama), Gemini compared; LangChain routing logic; shared Chroma retrieval layer.

### Ops
GCP Vertex AI gateway with request logging and CI cost/quality regression tests; MLflow experiment tracking.

### Impact
- 27% lower monthly inference cost
- No drop in client-rated quality (1–5 rubric)

---

## High-Throughput Order Management Backend

### Problem
Retail client's monolith couldn't handle peak-season traffic, causing checkout timeouts and lost sales.

### Architecture
Decomposed into event-driven FastAPI/Flask microservices over RabbitMQ (inventory, pricing, order-state), with async SQLAlchemy and Redis-cached hot lookups.

### Ops
Kubernetes autoscaling, GitHub Actions CI/CD with load-test gating, circuit breakers/retry queues for payment APIs, Prometheus/Grafana monitoring.

### Impact
- Sustained 10× peak traffic at 99.95% uptime
- Cut checkout latency by 60%

---

# Education

## GIFT University
**Gujranwala, Pakistan**

**B.Sc. Software Engineering (Hons.)**  
Minor: Data Science  
CGPA: **3.0 / 4.0**

**2014 – 2019**

**Award**
- Best Commercial Project — Capstone Project Award (2019)

---

# Recognition

- **Verified n8n Creator** — Recognized automation expert; published production workflows used by global teams.
- **GitHub Arctic Code Vault Contributor** — Open-source code archived for long-term digital preservation.
- **Fractional CTO / Technical Advisor** — Advising founders and executives on SaaS architecture and AI integration.

## Related

- Alternate resume: [[03-resources/resumes/resume-fullstack|Resume — Fullstack]]
- Conflict audit: [[02-areas/career/resume-conflicts|Resume Conflicts]]
- Timeline: [[02-areas/career/master-timeline|Master Timeline]]
- Skills: [[03-resources/skills-matrix/skills-overview|Skills Matrix]]
- Career: [[02-areas/career/career-overview|Career]]