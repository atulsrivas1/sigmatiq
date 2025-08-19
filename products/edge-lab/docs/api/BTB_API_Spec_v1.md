# BTB API Spec v1 — Build → Sweeps → Leaderboard → Train

## Status
Draft — documentation-only; aligns with ADR 0005 and Matrix Contract v1

## Principles
- Simple, composable endpoints; stateless requests with explicit lineage.
- First-class risk profiles and gates; transparent “why” for pass/fail.
- Reproducibility via shas: `matrix_sha`, `config_sha`, `policy_sha`, `risk_sha`.
- Pagination, idempotency where practical, and predictable error shapes.

## Types
```jsonc
// Common types (abbreviated)
Lineage: {
  matrix_sha: string,
  config_sha?: string,
  policy_sha?: string,
  risk_profile: "conservative"|"balanced"|"aggressive",
  risk_sha: string
}

Gate: { pass: boolean, reasons: string[] }

ConfigTuple: {
  kind: "thr"|"top_pct",
  value: string,              // e.g., "0.55,0.60,0.65" or "0.15"
  allowed_hours?: string,     // e.g., "13,14,15"
  splits?: number,
  tag?: string
}

Metrics: {
  sharpe?: number,
  sortino?: number,
  cum_return?: number,
  trades?: number,
  win_rate?: number,
  max_dd?: number,
  es95?: number
}
```

## Endpoints

### 1) Matrix — Build/Preview
- POST `/matrix/build`
  - body: `{ model_id, date_window: { start, end }, features?: string[], hours_filter?, label_def?, preview?: boolean }`
  - resp: `{ matrix_sha, preview?: { features, rows, label_balance, nan_pct, leakage_flags[], coverage_by_hour[], drift_summary } }`
- GET `/matrix/{matrix_sha}` → metadata only

Notes: Label/hours rules as per Matrix Contract v1. Preview is optional, fast path.

### 2) Sweeps — Run and Inspect
- POST `/sweeps/run`
  - body: `{ model_id, matrix_sha?, risk_profile, sweep: { threshold_variants: string[], hours_variants?: string[], top_pct_variants?: string[], splits?: number }, risk_budget_overrides?: object, tag?: string }`
  - resp: `{ sweep_id }`

- GET `/sweeps/{sweep_id}/status`
  - resp: `{ status: "queued"|"running"|"completed"|"failed", progress?: { completed:int, total:int }, results?: SweepRow[] }`

- GET `/sweeps/{sweep_id}/results?limit=&offset=`
  - resp: `{ rows: SweepRow[], total:int }`

Type `SweepRow`
```jsonc
{
  id: string,
  model_id: string,
  pack_id: string,
  config: ConfigTuple,
  metrics: Metrics,
  lineage: Lineage,
  gate: Gate,
  created_at: string
}
```

### 3) Leaderboard — Aggregate Best Results
- GET `/leaderboard?model_id=&pack_id=&risk_profile=&pass_gate=&start=&end=&limit=&offset=`
  - resp: `{ rows: LeaderboardRow[], total:int }`

Type `LeaderboardRow`
```jsonc
{
  id: string,
  started_at: string,
  model_id: string,
  pack_id: string,
  metrics: Metrics,
  config: ConfigTuple,
  lineage: Lineage,
  gate: Gate,
  tag?: string
}
```

### 4) Selection — Persisted Cart (optional server-side)
- POST `/selections` body: `{ items: SelectionItem[] }` → `{ selection_id }`
- GET `/selections/{id}` → `{ items: SelectionItem[] }`

Type `SelectionItem`
```jsonc
{
  model_id: string,
  config: ConfigTuple,
  lineage: Lineage
}
```

### 5) Train — Batch Queue
- POST `/train/batch`
  - body: `{ jobs: TrainJob[] }`
  - resp: `{ job_ids: string[] }`

- GET `/train/jobs?model_id=&risk_profile=&status=&limit=&offset=`
  - resp: `{ rows: TrainJobStatus[], total:int }`

Types
```jsonc
TrainJob: {
  model_id: string,
  config: ConfigTuple,
  lineage: Lineage,
  algorithm?: string,    // default per pack
  seed?: number,
  tag?: string
}

TrainJobStatus: TrainJob & {
  job_id: string,
  status: "queued"|"running"|"completed"|"failed",
  progress?: number,
  started_at?: string,
  completed_at?: string,
  metrics?: { accuracy?: number, f1_score?: number, duration?: string }
}
```

## Gate Evaluation (summary)
- Inputs: `metrics` + parity/capacity checks + profile budgets.
- Output: `Gate`: `{ pass, reasons[] }`. Reasons examples: `"min_trades_not_met"`, `"max_dd_exceeded"`, `"spread_above_limit"`, `"fill_rate_below_min"`.
- Pack‑aware evaluation per ADR 0005; details in Gate & Scoring spec.

## Idempotency & Caching
- Sweeps: identical requests (normalized) return prior `sweep_id` or short‑circuit to existing results.
- Train: duplicate `jobs` (same normalized key) are ignored unless `force=true`.

## Errors (shape)
```jsonc
{
  error: {
    code: string,            // e.g., "INVALID_PARAM", "NOT_FOUND", "GATE_FAILED"
    message: string,
    details?: object
  }
}
```

## Security / Limits
- Per‑user quotas on sweep concurrency and train jobs; profile‑specific caps optional.
- Max limits for list endpoints (`limit<=200`), sane defaults (`limit=50`).

## Examples
```http
POST /sweeps/run
{
  "model_id": "spy_opt_0dte_hourly",
  "risk_profile": "balanced",
  "sweep": {
    "threshold_variants": ["0.50,0.52,0.54", "0.55,0.60,0.65"],
    "hours_variants": ["13,14,15"],
    "splits": 5
  },
  "tag": "demo"
}
```

