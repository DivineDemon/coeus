#!/usr/bin/env bash
# Seed 00-inbox/secretary-queue/ from n8n Serper for Haga investor + B2B client leads.
# Use when Goose headless recipes stall on local 8B (empty model response).
set -euo pipefail

VAULT="/Users/mushood/Documents/code/coeus"
N8N_BASE="${N8N_BASE:-https://self8n.sv.mushoodhanif.com}"
QUEUE="${VAULT}/00-inbox/secretary-queue"
DATE_UTC="$(date -u +%Y-%m-%d)"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

mkdir -p "$QUEUE"

search() {
  local query="$1" gl="${2:-us}"
  curl -sf -X POST "${N8N_BASE}/webhook/secretary-search" \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"${query}\",\"num\":8,\"gl\":\"${gl}\"}"
}

write_queue() {
  local channel="$1" campaign="$2" query="$3" json_file="$4"
  local slug
  slug="$(echo "$query" | tr ' ' '-' | tr -cd '[:alnum:]-' | cut -c1-48)"
  local out="${QUEUE}/${DATE_UTC}-${channel}-${slug}.md"

  OUT="$out" CHANNEL="$channel" CAMPAIGN="$campaign" QUERY="$query" TS="$TS" JSON_FILE="$json_file" \
    python3 <<'PY'
import json, os
out = os.environ["OUT"]
channel = os.environ["CHANNEL"]
campaign = os.environ["CAMPAIGN"]
query = os.environ["QUERY"]
ts = os.environ["TS"]
with open(os.environ["JSON_FILE"]) as f:
    data = json.load(f)
lines = [
    "---",
    "type: secretary-queue",
    f"channel: {channel}",
    f"campaign: {campaign}",
    "status: discovered",
    f"discovered_at: {ts}",
    "venture: Haga",
    "---",
    "",
    f"# Queue — {query}",
    "",
    f"Source: n8n secretary-search ({ts})",
    "",
    "## Results",
    "",
]
for r in data.get("results", [])[:8]:
    title = r.get("title", "").replace("|", "\\|")
    link = r.get("link", "")
    snippet = r.get("snippet", "").replace("\n", " ")
    lines += [f"### [{title}]({link})", "", snippet, "", "- [ ] Score / enrich / draft", ""]
with open(out, "w") as f:
    f.write("\n".join(lines))
print(out)
PY
}

echo "=== Haga leads bootstrap ${TS} ==="
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

search "seed pre-seed robotics physical AI simulation benchmark investors" > "$TMP"
write_queue "investor" "investor-cold-email" "robotics-seed-investors" "$TMP"

search "robotics simulation benchmark startup B2B design partner" > "$TMP"
write_queue "lead-gen" "lead-pipeline" "robotics-b2b-clients" "$TMP"

echo "✓ Queue files in 00-inbox/secretary-queue/"
echo "Next: mempalace mine, then enrich/send via Goose chat or n8n webhooks."
