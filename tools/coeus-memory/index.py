#!/usr/bin/env python3
"""Index Coeus vault markdown into a local ChromaDB for RAG."""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import chromadb
import httpx

VAULT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = Path(__file__).resolve().parent / ".chroma"
COLLECTION = "coeus"
OLLAMA_URL = "http://127.0.0.1:11434"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120
SKIP_DIRS = {".git", ".obsidian", "node_modules", ".chroma", "__pycache__"}


def iter_markdown_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3 :].lstrip()
    return text


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


def embed_texts(texts: list[str], client: httpx.Client) -> list[list[float]]:
    vectors: list[list[float]] = []
    for text in texts:
        resp = client.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text},
            timeout=120.0,
        )
        resp.raise_for_status()
        vectors.append(resp.json()["embedding"])
    return vectors


def doc_id(path: Path, chunk_index: int) -> str:
    rel = path.relative_to(VAULT_ROOT).as_posix()
    digest = hashlib.sha1(f"{rel}:{chunk_index}".encode()).hexdigest()[:12]
    return f"{rel}#{chunk_index}#{digest}"


def index_vault(reset: bool = False) -> int:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass
    collection = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

    md_files = iter_markdown_files(VAULT_ROOT)
    ids: list[str] = []
    documents: list[str] = []
    metadatas: list[dict] = []

    for path in md_files:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        body = strip_frontmatter(raw)
        chunks = chunk_text(body)
        rel = path.relative_to(VAULT_ROOT).as_posix()
        for i, chunk in enumerate(chunks):
            ids.append(doc_id(path, i))
            documents.append(chunk)
            metadatas.append({"source": rel, "chunk": i})

    if not documents:
        return 0

    with httpx.Client() as http:
        embeddings = embed_texts(documents, http)

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
    return len(documents)


def main() -> None:
    parser = argparse.ArgumentParser(description="Index Coeus vault for local RAG")
    parser.add_argument("--reset", action="store_true", help="Drop and rebuild the index")
    args = parser.parse_args()
    count = index_vault(reset=args.reset)
    print(f"Indexed {count} chunks from {VAULT_ROOT}")


if __name__ == "__main__":
    main()
