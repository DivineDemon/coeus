#!/usr/bin/env bash
# End-to-end smoke: recipe validation → n8n email → audit log → vault rollup
#
# Usage:
#   tools/coeus-goose/scripts/smoke-test.sh
#   SECRETARY_SMOKE_EMAIL=you@gmail.com tools/coeus-goose/scripts/smoke-test.sh
#   tools/coeus-goose/scripts/smoke-test.sh --skip-send   # audit + vault only
set -euo pipefail

VAULT="/Users/mushood/Documents/code/coeus"
GOOSE_BIN="/Applications/Goose.app/Contents/Resources/bin/goose"
RECIPE="${VAULT}/tools/coeus-goose/recipes/smoke-test.yaml"
N8N_BASE="${N8N_BASE:-https://self8n.sv.mushoodhanif.com}"
SMOKE_TO="${SECRETARY_SMOKE_EMAIL:-supame123@gmail.com}"
DATE_UTC="$(date -u +%Y-%m-%d)"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
LOG_DIR="${VAULT}/03-resources/secretary-log"
LOG_FILE="${LOG_DIR}/${DATE_UTC}-log.md"
SKIP_SEND=false

for arg in "$@"; do
  case "$arg" in
    --skip-send) SKIP_SEND=true ;;
    -h|--help)
      echo "Usage: $0 [--skip-send]"
      echo "  SECRETARY_SMOKE_EMAIL  recipient (default: supame123@gmail.com)"
      echo "  N8N_BASE               n8n instance (default: https://self8n.sv.mushoodhanif.com)"
      exit 0
      ;;
  esac
done

die() { echo "ERROR: $*" >&2; exit 1; }
ok()  { echo "✓ $*"; }

echo "=== Coeus Secretary E2E Smoke Test ==="
echo "Date (UTC): ${DATE_UTC}"
echo "Recipient:  ${SMOKE_TO}"
echo "N8N_BASE:   ${N8N_BASE}"
echo

# 1. Validate recipe
if [[ -x "$GOOSE_BIN" ]]; then
  "$GOOSE_BIN" recipe validate "$RECIPE" || die "Recipe validation failed"
  ok "Recipe valid: smoke-test.yaml"
else
  echo "WARN: Goose not found — skipping recipe validate"
fi

# 2. Send via n8n (the hands step the recipe would invoke)
SEND_RESPONSE=""
SEND_HTTP=""
if [[ "$SKIP_SEND" == "false" ]]; then
  SUBJECT="[Coeus Secretary Smoke Test] ${TIMESTAMP}"
  BODY="<p>Automated e2e smoke test from Coeus Secretary.</p><p>Pipeline: recipe → n8n → Gmail → audit log.</p><p>Timestamp (UTC): ${TIMESTAMP}</p>"

  SEND_RESPONSE="$(curl -s -w "\n__HTTP__:%{http_code}" -X POST "${N8N_BASE}/webhook/secretary-email" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"${SMOKE_TO}\",
      \"subject\": \"${SUBJECT}\",
      \"body\": \"${BODY}\",
      \"campaign\": \"smoke-test\",
      \"channel\": \"email\",
      \"personalization_hooks\": [\"e2e smoke test\", \"secretary stack verification\"]
    }")"

  SEND_HTTP="${SEND_RESPONSE##*__HTTP__:}"
  SEND_RESPONSE="${SEND_RESPONSE%__HTTP__:*}"

  echo "Email response (HTTP ${SEND_HTTP}):"
  echo "${SEND_RESPONSE}" | python3 -m json.tool 2>/dev/null || echo "${SEND_RESPONSE}"

  if [[ "$SEND_HTTP" != "200" ]]; then
    die "secretary-email returned HTTP ${SEND_HTTP}"
  fi

  if ! echo "${SEND_RESPONSE}" | python3 -c "import sys,json; d=json.load(sys.stdin); assert d.get('ok') and d.get('sent')" 2>/dev/null; then
    die "secretary-email did not confirm send"
  fi
  ok "Email sent to ${SMOKE_TO}"
else
  echo "Skipping send (--skip-send)"
  SUBJECT="[Coeus Secretary Smoke Test] ${TIMESTAMP} (dry run)"
fi

# 3. Verify audit via secretary-log (idempotent check row)
AUDIT_RESPONSE="$(curl -s -X POST "${N8N_BASE}/webhook/secretary-log" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"email\",
    \"recipient\": \"${SMOKE_TO}\",
    \"campaign\": \"smoke-test\",
    \"subject_or_title\": \"${SUBJECT}\",
    \"personalization_hooks\": [\"e2e smoke test\", \"secretary stack verification\"],
    \"status\": \"sent\",
    \"metadata\": {\"source\": \"smoke-test.sh\", \"timestamp\": \"${TIMESTAMP}\"}
  }")"

echo "Audit log response:"
echo "${AUDIT_RESPONSE}" | python3 -m json.tool 2>/dev/null || echo "${AUDIT_RESPONSE}"

if ! echo "${AUDIT_RESPONSE}" | python3 -c "import sys,json; d=json.load(sys.stdin); assert d.get('ok') and d.get('logged')" 2>/dev/null; then
  die "secretary-log audit failed"
fi
ok "Audit logged (Sheets/Neon data table)"

# 4. Vault daily rollup
mkdir -p "$LOG_DIR"
if [[ ! -f "$LOG_FILE" ]]; then
  cat > "$LOG_FILE" <<EOF
---
type: secretary-log
date: ${DATE_UTC}
tags: [secretary, log]
---

# Secretary log — ${DATE_UTC}

| Time (UTC) | Channel | Recipient | Campaign | Status |
|------------|---------|-----------|----------|--------|
EOF
fi

# Avoid duplicate smoke-test rows on re-run (match timestamp in table body)
if ! grep -q "${TIMESTAMP}" "$LOG_FILE" 2>/dev/null; then
  echo "" >> "$LOG_FILE"
  echo "| ${TIMESTAMP} | email | ${SMOKE_TO} | smoke-test | sent |" >> "$LOG_FILE"
fi
ok "Vault log updated: ${LOG_FILE#${VAULT}/}"

echo
echo "=== Smoke test PASSED ==="
echo "Check inbox: ${SMOKE_TO}"
echo "Vault log:   03-resources/secretary-log/${DATE_UTC}-log.md"
echo "n8n audit:   Secretary Audit Log data table (campaign=smoke-test)"
