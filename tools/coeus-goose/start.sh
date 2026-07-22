#!/usr/bin/env bash
# Launch Goose agent for Coeus: Ollama + MemPalace + vault filesystem
#
# Defaults:
#   GOOSE_MODEL=qwen3-coeus-agent  (qwen3:8b + num_ctx 32768; see Modelfile.qwen3-coeus-agent)
#   OLLAMA_CONTEXT_LENGTH=32768   OLLAMA_KEEP_ALIVE=-1
# Tool-heavy / ops recipes: GOOSE_MODEL=qwen3-coder:8b
#   Local alias of qwen2.5-coder:7b (upstream qwen3-coder has no 8B tag; only 30b~/19GB+)
set -euo pipefail

GOOSE_BIN="/Applications/Goose.app/Contents/Resources/bin/goose"
VAULT="/Users/mushood/Documents/code/coeus"
SKILLS_DIR="${VAULT}/tools/coeus-goose/skills"
MODELFILE="${VAULT}/tools/coeus-goose/Modelfile.qwen3-coeus-agent"
DEFAULT_MODEL="qwen3-coeus-agent"

# Wire Goose skills discovery → tools/coeus-goose/skills (canonical source)
ensure_skills_symlink() {
  local link_dir="$1"
  local rel_target="$2"
  mkdir -p "$(dirname "$link_dir")"
  if [[ -L "$link_dir" ]]; then
    local target
    target="$(readlink "$link_dir")"
    [[ "$target" == "$rel_target" ]] && return 0
    rm "$link_dir"
  elif [[ -e "$link_dir" ]]; then
    echo "Cannot link skills: $link_dir exists and is not a symlink" >&2
    exit 1
  fi
  ln -s "$rel_target" "$link_dir"
}

export GOOSE_PROVIDER="${GOOSE_PROVIDER:-ollama}"
export GOOSE_MODEL="${GOOSE_MODEL:-$DEFAULT_MODEL}"
export OLLAMA_HOST="${OLLAMA_HOST:-http://127.0.0.1:11434}"

# Server-side Ollama defaults (effective when this process starts `ollama serve`,
# or when Ollama.app inherits them via launchctl setenv / app restart).
export OLLAMA_CONTEXT_LENGTH="${OLLAMA_CONTEXT_LENGTH:-32768}"
export OLLAMA_KEEP_ALIVE="${OLLAMA_KEEP_ALIVE:--1}"

# Reinforce MemPalace search-first routing every turn (Top Of Mind extension)
export GOOSE_MOIM_MESSAGE_FILE="${VAULT}/tools/coeus-goose/mempalace-routing.md"
export GOOSE_TOOLSHIM="${GOOSE_TOOLSHIM:-true}"
export GOOSE_TOOLSHIM_OLLAMA_MODEL="${GOOSE_TOOLSHIM_OLLAMA_MODEL:-$DEFAULT_MODEL}"
export N8N_BASE="${N8N_BASE:-https://self8n.sv.mushoodhanif.com}"

ollama_has_model() {
  local name="$1"
  ollama list 2>/dev/null | awk '{print $1}' | grep -Eq "^${name}(:|\$)"
}

if [[ ! -x "$GOOSE_BIN" ]]; then
  echo "Goose not found at $GOOSE_BIN"
  echo "Install: brew install --cask block-goose"
  exit 1
fi

if ! curl -sf "${OLLAMA_HOST}/api/tags" >/dev/null; then
  echo "Ollama not reachable at ${OLLAMA_HOST}"
  echo "Start Ollama, then:"
  echo "  ollama pull qwen3:8b"
  echo "  ollama create qwen3-coeus-agent -f ${MODELFILE}"
  echo "  ollama pull qwen2.5-coder:7b && ollama cp qwen2.5-coder:7b qwen3-coder:8b"
  exit 1
fi

# Ensure custom agent model exists (FROM qwen3:8b + num_ctx 32768)
if ! ollama_has_model "qwen3-coeus-agent"; then
  echo "Creating qwen3-coeus-agent from Modelfile..."
  if ! ollama_has_model "qwen3:8b"; then
    echo "Base model qwen3:8b missing — pulling..."
    ollama pull qwen3:8b
  fi
  ollama create qwen3-coeus-agent -f "$MODELFILE"
fi

# Ensure ops coder tag exists (plan name qwen3-coder:8b → local alias of qwen2.5-coder:7b)
if ! ollama_has_model "qwen3-coder:8b"; then
  if ! ollama_has_model "qwen2.5-coder:7b"; then
    echo "Pulling qwen2.5-coder:7b for ops recipes..."
    ollama pull qwen2.5-coder:7b
  fi
  echo "Creating local alias qwen3-coder:8b → qwen2.5-coder:7b..."
  ollama cp qwen2.5-coder:7b qwen3-coder:8b
fi

if ! command -v mempalace-mcp >/dev/null; then
  echo "mempalace-mcp not found. Install: uv tool install mempalace"
  exit 1
fi

cd "$VAULT"
ensure_skills_symlink "${VAULT}/.goose/skills" "../tools/coeus-goose/skills"
ensure_skills_symlink "${VAULT}/.agents/skills" "../tools/coeus-goose/skills"
exec "$GOOSE_BIN" session "$@"
