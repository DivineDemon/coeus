#!/usr/bin/env bash
# Register Goose cron schedules for Coeus secretary recipes.
# Idempotent: removes existing schedule IDs before re-adding.
#
# Usage:
#   tools/coeus-goose/recipes/install-schedules.sh
#   tools/coeus-goose/recipes/install-schedules.sh --dry-run
#
# Requires: Goose CLI (block-goose cask), Ollama reachable for scheduled runs.
set -euo pipefail

GOOSE_BIN="${GOOSE_BIN:-/Applications/Goose.app/Contents/Resources/bin/goose}"
VAULT="${VAULT:-/Users/mushood/Documents/code/coeus}"
RECIPES_DIR="${VAULT}/tools/coeus-goose/recipes"
DRY_RUN=false

if [[ "${1:-}" == "--dry-run" ]]; then
  DRY_RUN=true
fi

if [[ ! -x "$GOOSE_BIN" ]]; then
  echo "Goose not found at $GOOSE_BIN" >&2
  echo "Install: brew install --cask block-goose" >&2
  exit 1
fi

export GOOSE_RECIPE_PATH="${GOOSE_RECIPE_PATH:-$RECIPES_DIR}"
export GOOSE_MOIM_MESSAGE_FILE="${VAULT}/tools/coeus-goose/mempalace-routing.md"
export N8N_BASE="${N8N_BASE:-https://self8n.sv.mushoodhanif.com}"

# schedule_id|cron|recipe_file|description
SCHEDULES=(
  "secretary-morning-brief|0 8 * * *|morning-brief.yaml|Daily digest — queues, caps, plan"
  "secretary-daily-job-hunt|0 9 * * *|daily-job-hunt.yaml|Job discovery, score, apply (cap 10)"
  "secretary-investor-cold-email|0 10 * * 1,3,5|investor-cold-email.yaml|Investor batch Mon/Wed/Fri"
  "secretary-lead-pipeline|0 11 * * *|lead-pipeline.yaml|B2B discover, enrich, outreach"
  "secretary-social-publish|0 14 * * *|social-publish.yaml|LinkedIn publish (Haga Autopilot align)"
)

run_goose() {
  if $DRY_RUN; then
    echo "  [dry-run] $*"
  else
    "$GOOSE_BIN" "$@"
  fi
}

echo "Validating recipes..."
for recipe in "$RECIPES_DIR"/*.yaml; do
  [[ "$(basename "$recipe")" == *.yaml ]] || continue
  run_goose recipe validate "$recipe"
done

echo ""
echo "Installing schedules (GOOSE_RECIPE_PATH=$GOOSE_RECIPE_PATH)..."

for entry in "${SCHEDULES[@]}"; do
  IFS='|' read -r schedule_id cron recipe_file desc <<< "$entry"
  recipe_path="${RECIPES_DIR}/${recipe_file}"

  if [[ ! -f "$recipe_path" ]]; then
    echo "Missing recipe: $recipe_path" >&2
    exit 1
  fi

  echo "→ $schedule_id ($cron) — $desc"

  if ! $DRY_RUN; then
    # Remove stale schedule if present (ignore errors)
    "$GOOSE_BIN" schedule remove "$schedule_id" 2>/dev/null || true
  fi

  run_goose schedule add \
    --schedule-id "$schedule_id" \
    --cron "$cron" \
    --recipe-source "$recipe_path"
done

echo ""
if $DRY_RUN; then
  echo "Dry run complete — no schedules written."
else
  echo "Installed schedules:"
  "$GOOSE_BIN" schedule list
fi
