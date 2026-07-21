# Coeus Memory (legacy)

> **Superseded by [MemPalace](https://github.com/MemPalace/mempalace).** See [[03-resources/infrastructure/local-llm-memory|Local LLM Memory]] for the current setup.

Minimal Ollama + ChromaDB RAG harness. Kept as a lightweight fallback only.

## Setup (fallback)

```bash
cd tools/coeus-memory
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3:8b && ollama pull nomic-embed-text
python index.py
python ask.py "your question"
```

## Prefer MemPalace

```bash
uv tool install mempalace
mempalace mine /Users/mushood/Documents/code/coeus
mempalace search "your question" --wing coeus
```
