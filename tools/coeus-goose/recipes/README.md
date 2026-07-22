# Coeus Secretary Recipes

Goose YAML recipes for headless secretary workflows. Designed for local Ollama
(`qwen3-coeus-agent` / `qwen3-coder:8b`) with minimal tool surface per recipe.

## Recipes

| File | Purpose | Model | Extensions |
|------|---------|-------|------------|
| `secretary.yaml` | Interactive router → sub-recipes | qwen3-coeus-agent | global core |
| `morning-brief.yaml` | Queue/cap digest (no sends) | qwen3-coeus-agent | global core |
| `daily-job-hunt.yaml` | Search, score, apply | qwen3-coder:8b | global core |
| `investor-cold-email.yaml` | Investor research + send | qwen3-coder:8b | core + PDF Reader |
| `lead-pipeline.yaml` | B2B discover → outreach | qwen3-coder:8b | global core |
| `social-publish.yaml` | LinkedIn draft + publish | qwen3-coeus-agent | global core |
| `smoke-test.yaml` | E2E self-send + audit verification | qwen3-coder:8b | global core |

Recipes without an `extensions` block inherit enabled extensions from
`~/.config/goose/config.yaml` (secretary core stack).

## Validate

```bash
GOOSE=/Applications/Goose.app/Contents/Resources/bin/goose
for f in tools/coeus-goose/recipes/*.yaml; do
  "$GOOSE" recipe validate "$f"
done
```

## Run manually (headless)

```bash
export GOOSE_RECIPE_PATH="$(pwd)/tools/coeus-goose/recipes"
export N8N_BASE=https://self8n.sv.mushoodhanif.com

GOOSE=/Applications/Goose.app/Contents/Resources/bin/goose
"$GOOSE" run --recipe morning-brief.yaml --no-session -q
"$GOOSE" run --recipe daily-job-hunt.yaml --no-session -q
"$GOOSE" run --recipe secretary.yaml --params channel=lead-pipeline -q
"$GOOSE" run --recipe smoke-test.yaml --no-session -q
```

E2E smoke (deterministic script — validates recipe, sends to self, writes vault log):

```bash
tools/coeus-goose/scripts/smoke-test.sh
tools/coeus-goose/scripts/smoke-test.sh --skip-send   # audit + vault only
```

## Schedules (UTC)

| Schedule ID | Cron | Recipe |
|-------------|------|--------|
| `secretary-morning-brief` | `0 8 * * *` | morning-brief |
| `secretary-daily-job-hunt` | `0 9 * * *` | daily-job-hunt |
| `secretary-investor-cold-email` | `0 10 * * 1,3,5` | investor-cold-email |
| `secretary-lead-pipeline` | `0 11 * * *` | lead-pipeline |
| `secretary-social-publish` | `0 14 * * *` | social-publish |

Install:

```bash
chmod +x tools/coeus-goose/recipes/install-schedules.sh
tools/coeus-goose/recipes/install-schedules.sh
```

Dry run (validate only):

```bash
tools/coeus-goose/recipes/install-schedules.sh --dry-run
```

List / run now / remove:

```bash
goose schedule list
goose schedule run-now secretary-morning-brief
goose schedule remove secretary-morning-brief
```

## Skills

Each recipe instructs the agent to load skills from `tools/coeus-goose/skills/`
via the Goose skills extension. See [[../skills/README|skills README]].

## Related

- [[../n8n/secretary-webhooks|n8n webhook contracts]]
- [[../../../02-areas/secretary/secretary-overview|Secretary overview]]
- [[../README|Coeus + Goose setup]]
