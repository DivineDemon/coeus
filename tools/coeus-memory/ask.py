#!/usr/bin/env python3
"""Query Coeus vault via local Ollama RAG."""

from __future__ import annotations

import argparse
from pathlib import Path

import chromadb
import httpx

CHROMA_DIR = Path(__file__).resolve().parent / ".chroma"
COLLECTION = "coeus"
OLLAMA_URL = "http://127.0.0.1:11434"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:8b"
TOP_K = 6

SYSTEM_PROMPT = """You are Coeus, a personal knowledge assistant for Mushood Hanif.
Answer using ONLY the provided context from the Obsidian vault.
If the context is insufficient, say what is missing and suggest which note to check.
Cite sources as [[filepath]] when referencing facts."""


def embed_query(query: str, client: httpx.Client) -> list[float]:
    resp = client.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": query},
        timeout=120.0,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = db.get_collection(COLLECTION)
    with httpx.Client() as http:
        vector = embed_query(query, http)
    results = collection.query(query_embeddings=[vector], n_results=top_k)
    chunks: list[dict] = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"text": doc, "source": meta["source"], "distance": dist})
    return chunks


def build_context(chunks: list[dict]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[{i}] Source: {c['source']}\n{c['text']}")
    return "\n\n".join(parts)


def chat(query: str, context: str, client: httpx.Client) -> str:
    prompt = f"{SYSTEM_PROMPT}\n\n## Context\n{context}\n\n## Question\n{query}"
    resp = client.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": CHAT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_ctx": 8192},
        },
        timeout=300.0,
    )
    resp.raise_for_status()
    return resp.json()["response"].strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask Coeus memory a question")
    parser.add_argument("question", help="Question about your vault")
    parser.add_argument("-k", type=int, default=TOP_K, help="Number of chunks to retrieve")
    parser.add_argument("--show-context", action="store_true", help="Print retrieved chunks")
    args = parser.parse_args()

    chunks = retrieve(args.question, top_k=args.k)
    if not chunks:
        print("No index found. Run: python tools/coeus-memory/index.py")
        return

    if args.show_context:
        print("--- Retrieved context ---")
        for c in chunks:
            print(f"\n[{c['source']}] (dist={c['distance']:.4f})\n{c['text'][:300]}...")
        print("\n--- Answer ---")

    context = build_context(chunks)
    with httpx.Client() as http:
        answer = chat(args.question, context, http)
    print(answer)


if __name__ == "__main__":
    main()
