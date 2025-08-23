# Model Pipeline — Design

## Overview
A background pipeline that orchestrates dataset building, sweep backtesting, leaderboard generation, and conditional training with novice-first caps and summaries. Exposed via an async-friendly API that returns a `pipeline_run_id` and incremental status.

## Architecture
- API layer (FastAPI): orchestrates phases and records pipeline runs.
- Worker (preferred) or async task: executes build → sweep → train with retries and caps.
- Storage: Postgres (`sc.*`) + Parquet/CSV datasets; object store for artifacts.

## New Table: sc.model_pipeline_runs
- `pipeline_run_id UUID PK`
- `model_id TEXT`, `model_version INT`, `timeframe TEXT`
- `universe JSONB` (preset/watchlist/symbols, cap)
- `sweep JSONB` (preset_id or grid snapshot), `guardrails JSONB`
- `dataset_run_id UUID`, `backtest_run_ids JSONB`, `training_run_id UUID`
- `status TEXT` (`pending|running|success|stopped|error`)
- `summary TEXT`, `errors JSONB`, `created_at TIMESTAMPTZ`, `finished_at TIMESTAMPTZ`

Indexes: `(model_id, created_at DESC)`, `(status)`, GIN on `errors` if needed.

## Endpoint Contracts
### POST /models/{model_id}/pipeline/run
Request (simple):
```json
{
  "universe": {"preset_id": "sp500", "cap": 20},
  "mode": "simple",
  "persist": true
}
```
Request (advanced):
```json
{
  "timeframe": "hour",
  "start_date": "2024-06-01",
  "end_date": "2024-06-30",
  "universe": {"preset_id": "liquid_etfs", "cap": 30},
  "grid": {"thresholds_list": [[0.55,0.6,0.65]], "allowed_hours_list": [[9,10,11,12,13,14,15]]},
  "guardrails": {"min_trades": 50, "min_sharpe": 0.2},
  "persist": true,
  "dry_run": false
}
```
Response:
```json
{
  "pipeline_run_id": "...",
  "status": "pending",
  "summary": "We will build a dataset for 20 symbols (hour) over 30 days..."
}
```

### GET /models/pipeline/runs/{pipeline_run_id}
Response:
```json
{
  "pipeline_run_id": "...",
  "status": "running",
  "dataset": {"run_id": "...", "rows": 123456, "symbols": 20},
  "backtests": {"run_ids": ["...","..."], "leaderboard": [{"run_id":"...","metrics": {"avg_sharpe_hourly":0.28, "trades_total":120}}]},
  "chosen": {"config": {"thresholds":[0.6,0.65]}, "metrics": {"avg_sharpe_hourly":0.31, "trades_total":140}},
  "training": {"run_id": "...", "status": "success"},
  "summary": "Tried 12 safe configurations across 20 symbols; best passed guardrails and trained.",
  "next_steps": ["Review training metrics", "Run Critic Gate", "(Optional) Publish model version"]
}
```

## Orchestration Flow
1) Validate request and enforce caps (≤90 days, ≤50 symbols, ≤50 combos).
2) Resolve model version, timeframe, data window (defaults).
3) Build or reuse dataset (hash match) via `/models/dataset/build`.
4) Sweep/backtest via `/models/{id}/backtest/sweep` (simple uses sweep preset).
5) Compute leaderboard (top N) from persisted runs; store slice in pipeline run.
6) Check guardrails → if pass, build `training_cfg.selection` and train; record `sc.model_training_runs`.
7) Write plain-language `summary` and `next_steps`.

## Guardrails
- Hard: date window, universe, combos, RTH hours default for intraday.
- Quality: `min_trades`, `min_sharpe`, optional `max_position_rate`.
- Preset requirement in simple mode; public presets must have guardrails.

## Error Handling
- Global exception handler maps env/network/DB errors to novice messages.
- Pipeline row captures errors and partial progress; GET endpoint surfaces status and advice.

## Security & Quotas
- Per-user soft budgets for pipeline runs; throttle with friendly 429s + next steps.
- Ownership/visibility respected for sweep presets and watchlists.

## Testing Strategy
- Unit: pipeline orchestrator state machine; guardrail checks; summary generation.
- Integration: dataset build + sweep + leaderboard; dry-run; failure injection (missing API key, empty universe).
- E2E: simple and advanced flows via Postman; ensure caps and messages.

## Rollout Plan
- Phase A: Add DB table + endpoints; implement simple mode only; dry-run default.
- Phase B: Add advanced grid support + training trigger; no auto-publish.
- Phase C: Add UI hooks + CI checks for lints; expand presets and metrics explanations.
