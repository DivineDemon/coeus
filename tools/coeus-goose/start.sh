#!/usr/bin/env bash
# Launch Goose agent for Coeus: Ollama + MemPalace + vault filesystem
set -euo pipefail

GOOSE_BIN="/Applications/Goose.app/Contents/Resources/bin/goose"
VAULT="/Users/mushood/Documents/code/coeus"

export GOOSE_PROVIDER="${GOOSE_PROVIDER:-ollama}"
export GOOSE_MODEL="${GOOSE_MODEL:-qwen3:8b}"
export OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"

# Reinforce MemPalace search-first routing every turn (Top Of Mind extension)
export GOOSE_MOIM_MESSAGE_FILE="${VAULT}/tools/coeus-goose/mempalace-routing.md"
export GOOSE_TOOLSHIM="${GOOSE_TOOLSHIM:-true}"
export GOOSE_TOOLSHIM_OLLAMA_MODEL="${GOOSE_TOOLSHIM_OLLAMA_MODEL:-qwen3:8b}"

if [[ ! -x "$GOOSE_BIN" ]]; then
  echo "Goose not found at $GOOSE_BIN"
  echo "Install: brew install --cask block-goose"
  exit 1
fi

if ! curl -sf "${OLLAMA_HOST}/api/tags" >/dev/null; then
  echo "Ollama not reachable at ${OLLAMA_HOST}"
  echo "Start Ollama, then: ollama pull qwen3:8b"
  exit 1
fi

if ! command -v mempalace-mcp >/dev/null; then
  echo "mempalace-mcp not found. Install: uv tool install mempalace"
  exit 1
fi

cd "$VAULT"
exec "$GOOSE_BIN" session "$@"
