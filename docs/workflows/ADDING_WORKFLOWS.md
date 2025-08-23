Workflows — How To Add (for Codex sessions)

Where
- Add JSON files to `docs/workflows/examples/<workflow_id>.json`
- Regenerate SQL seed via `make -C products/sigma-core gen-workflow-seed`

Schema (minimum)
- `workflow_id`, `version`, `status`
- `title`, `subtitle`, `goal`, `persona: 'beginner'`, `difficulty: 'beginner'`, `time_to_complete`
- `prerequisites`: ["API URL", "Data access", ...]
- `dependencies`: `{ indicators:[], indicator_sets:[], strategies:[] }` (at least one ID)
- `steps`: ordered list with objects containing:
  - `description`, `rationale`, `api: { method, path, query?, body? }`, `expects`
- `outputs`: expected artifacts / results
- `best_when`, `avoid_when`, `caveats`
- `links`: e.g., `{ indicator_set: "/catalog/indicator_set/<id>", strategy: "/catalog/strategy/<id>" }`
- `novice_ready: true`, `beginner_summary`: one‑line explainer

Tips
- 1–2 steps max for beginner workflows; keep API examples concrete and safe
- Reflect our Simple Mode actions (screen/alert/subscribe/backtest)
- Use curated top‑20 sets/strategies in `dependencies`

Validate + Seed
- Lint: `make -C products/sigma-core lint-workflows` (Issues: 0 expected)
- Seed: `make -C products/sigma-core gen-workflow-seed` (updates `0005_sc_seed_workflows.sql`)

Naming
- `<purpose>_<timeframe>_v1.json` (e.g., `trend_follow_alignment_hourly_v1.json`)
