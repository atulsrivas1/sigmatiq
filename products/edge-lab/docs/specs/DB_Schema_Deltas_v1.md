# DB Schema Deltas v1 — BTB + Assistant

## Status
Draft — documents recommended schema changes; migrations not applied yet

## Goals
- Persist risk-aware lineage and gate results for leaderboard/backtests.
- Track training jobs and selection carts (optional, server-side).
- Support assistant queries with concise, indexed fields.

## Tables (new/changed)

### backtest_runs (existing → extend)
- id: bigserial PK
- model_id: text (indexed)
- pack_id: text
- started_at: timestamptz (indexed desc)
- params: jsonb
- metrics: jsonb
- best_sharpe_hourly: numeric
- best_cum_ret: numeric
- trades_total: int
- tag: text (indexed)
- plot_uri: text
- data_uri: text
- lineage additions:
  - matrix_sha: text (indexed)
  - config_sha: text
  - policy_sha: text
  - risk_profile: text CHECK IN ('conservative','balanced','aggressive') (indexed)
  - risk_sha: text
- gate additions:
  - gate_pass: boolean (indexed)
  - gate_reasons: text[]
- parity/capacity (0DTE/options, nullable):
  - median_spread_pct: numeric
  - fill_rate: numeric
  - oi_min_observed: int
  - volume_min_observed: int

Indexes
- (model_id, started_at desc)
- (risk_profile, gate_pass, started_at desc)
- (tag)

### backtest_folds (existing → extend)
- run_id: FK → backtest_runs.id (indexed)
- fold_idx: int
- metrics: jsonb
- instability helpers (nullable):
  - sharpe: numeric
  - sortino: numeric
  - max_dd: numeric

Index
- (run_id, fold_idx)

### train_jobs (new)
- id: bigserial PK
- submitted_at: timestamptz default now() (indexed desc)
- model_id: text (indexed)
- pack_id: text
- status: text CHECK IN ('queued','running','completed','failed','canceled') (indexed)
- progress: int CHECK (progress BETWEEN 0 AND 100)
- algorithm: text
- seed: int
- lineage: jsonb (must include matrix_sha, config_sha, policy_sha, risk_profile, risk_sha)
- error: text
- metrics: jsonb (accuracy, f1, duration, etc.)
- tag: text
- user_id: text (optional, for multi-user)

### selections (optional, new)
- id: bigserial PK
- created_at: timestamptz default now()
- user_id: text
- items: jsonb[]  // array of { model_id, config, lineage }

### signals (new)
- id: bigserial PK
- ts: timestamptz (indexed desc)
- model_id: text (indexed)
- risk_profile: text CHECK IN ('conservative','balanced','aggressive') (indexed)
- side: text CHECK IN ('long','short')
- entry_ref_px: numeric
- fill_px: numeric NULL
- slippage: numeric NULL
- status: text CHECK IN ('filled','pending','canceled','error') (indexed)
- rr: numeric NULL
- pnl: numeric NULL
- tag: text NULL
- lineage: jsonb (matrix_sha?, config_sha?, policy_sha?, risk_sha?)

Indexes
- (model_id, ts desc)
- (risk_profile, ts desc)
- (status, ts desc)

### signals_daily_summary (optional view/matview)
- date, model_id, risk_profile
- metrics: jsonb (daily aggregates)

### live_metrics (optional matview)
- model_id, risk_profile, period_start, period_end
- sharpe, sortino, cum_return, win_rate, trades, fill_rate, avg_slippage, capacity, coverage_pct, freshness_sec

## Migrations (illustrative SQL)
```sql
-- 0004_btb_add_lineage_and_gate.sql
ALTER TABLE backtest_runs
  ADD COLUMN IF NOT EXISTS matrix_sha text,
  ADD COLUMN IF NOT EXISTS config_sha text,
  ADD COLUMN IF NOT EXISTS policy_sha text,
  ADD COLUMN IF NOT EXISTS risk_profile text,
  ADD COLUMN IF NOT EXISTS risk_sha text,
  ADD COLUMN IF NOT EXISTS gate_pass boolean,
  ADD COLUMN IF NOT EXISTS gate_reasons text[],
  ADD COLUMN IF NOT EXISTS median_spread_pct numeric,
  ADD COLUMN IF NOT EXISTS fill_rate numeric,
  ADD COLUMN IF NOT EXISTS oi_min_observed int,
  ADD COLUMN IF NOT EXISTS volume_min_observed int;

CREATE INDEX IF NOT EXISTS idx_backtest_runs_model_time
  ON backtest_runs(model_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_backtest_runs_profile_gate_time
  ON backtest_runs(risk_profile, gate_pass, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_backtest_runs_tag ON backtest_runs(tag);

-- 0005_train_jobs.sql
CREATE TABLE IF NOT EXISTS train_jobs (
  id bigserial PRIMARY KEY,
  submitted_at timestamptz DEFAULT now(),
  model_id text NOT NULL,
  pack_id text,
  status text NOT NULL CHECK (status IN ('queued','running','completed','failed','canceled')),
  progress int CHECK (progress BETWEEN 0 AND 100),
  algorithm text,
  seed int,
  lineage jsonb NOT NULL,
  error text,
  metrics jsonb,
  tag text,
  user_id text
);
CREATE INDEX IF NOT EXISTS idx_train_jobs_time ON train_jobs(submitted_at DESC);
CREATE INDEX IF NOT EXISTS idx_train_jobs_model ON train_jobs(model_id);
CREATE INDEX IF NOT EXISTS idx_train_jobs_status ON train_jobs(status);

-- 0006_selections.sql (optional)
CREATE TABLE IF NOT EXISTS selections (
  id bigserial PRIMARY KEY,
  created_at timestamptz DEFAULT now(),
  user_id text,
  items jsonb[]
);

-- 0007_signals.sql
CREATE TABLE IF NOT EXISTS signals (
  id bigserial PRIMARY KEY,
  ts timestamptz NOT NULL,
  model_id text NOT NULL,
  risk_profile text CHECK (risk_profile IN ('conservative','balanced','aggressive')),
  side text CHECK (side IN ('long','short')),
  entry_ref_px numeric,
  fill_px numeric,
  slippage numeric,
  status text CHECK (status IN ('filled','pending','canceled','error')),
  rr numeric,
  pnl numeric,
  tag text,
  lineage jsonb
);
CREATE INDEX IF NOT EXISTS idx_signals_time ON signals(ts DESC);
CREATE INDEX IF NOT EXISTS idx_signals_model_time ON signals(model_id, ts DESC);
CREATE INDEX IF NOT EXISTS idx_signals_risk_time ON signals(risk_profile, ts DESC);
CREATE INDEX IF NOT EXISTS idx_signals_status_time ON signals(status, ts DESC);
```

## ASCII ERD (simplified)
```
models (?)           backtest_runs                       backtest_folds
   |                  ├─ id (PK)                           ├─ run_id (FK)
   └───────────────┐  ├─ model_id                          ├─ fold_idx
                   │  ├─ metrics (jsonb)                   └─ metrics (jsonb)
                   │  ├─ lineage: matrix_sha, policy_sha, risk_* 
                   │  └─ gate_pass, gate_reasons, tag, started_at
                   │
                   └──────────► train_jobs
                                  ├─ id (PK)
                                  ├─ model_id, status, progress
                                  ├─ algorithm, seed
                                  └─ lineage (jsonb)

selections (optional)
  ├─ id (PK)
  ├─ user_id
  └─ items: [{ model_id, config, lineage }]
```

## Notes
- All lineage fields must be supplied by the backend from request context or computed during the run.
- Gate reasons should use stable reason codes (see Gate & Scoring Spec v1).
- Add minimal covering indexes only; revisit after observing query patterns.
