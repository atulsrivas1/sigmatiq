# Pipeline Runbook (UI, API, Makefile)

This runbook shows how to execute the modeling pipeline end‑to‑end — build → train → backtest → sweeps — using the UI, the HTTP API, and Make targets.

## Prerequisites
- API server: `python products/sigma-lab/api/run_api.py --reload` (defaults to `http://localhost:8001`).
- Database: set `DATABASE_URL` or `DB_*`/`PG*` env vars; apply migrations: `make db-migrate`.
- Environment: copy `.env.example` to `.env` and fill required keys (e.g., data providers).
- Pack/model naming: examples below use `PACK_ID=zerosigma` and `MODEL_ID=spy_opt_0dte_hourly`.

## UI Flow (Sigma Lab)
- Start the UI dev server (if configured) pointing to the API at `:8001`.
- From Dashboard:
  - Create: click `Create Model` and follow prompts (ticker, asset, horizon, cadence).
  - Build: open the model panel → `• Build` and provide `Start/End` window.
  - Train: click `• Train` (optionally set `Allowed Hours`, `Calibration`).
  - Backtest: click `• Backtest` → set thresholds or `Top %` options.
  - Sweeps: open `Sweeps` to run thresholds/hours variants and compare.
  - Review: open `Leaderboard` to view best runs and metrics.

## API Flow (curl)
- Create model
  - `curl -sS -X POST http://localhost:8001/models -H 'Content-Type: application/json' -d '{"ticker":"SPY","asset_type":"opt","horizon":"0dte","cadence":"hourly","algo":"gbm","pack_id":"zerosigma"}' | jq .`
- Build matrix
  - `curl -sS -X POST http://localhost:8001/build_matrix -H 'Content-Type: application/json' -d '{"model_id":"spy_opt_0dte_hourly","pack_id":"zerosigma","start":"2024-01-01","end":"2024-06-30","ticker":"SPY","distance_max":7}' | jq .`
- Train
  - `curl -sS -X POST http://localhost:8001/train -H 'Content-Type: application/json' -d '{"model_id":"spy_opt_0dte_hourly","pack_id":"zerosigma","allowed_hours":"13,14,15","calibration":"sigmoid"}' | jq .`
- Backtest
  - `curl -sS -X POST http://localhost:8001/backtest -H 'Content-Type: application/json' -d '{"model_id":"spy_opt_0dte_hourly","pack_id":"zerosigma","thresholds":"0.55,0.60,0.65","splits":5,"allowed_hours":"13,14,15"}' | jq .`
- Sweeps (optional)
  - `curl -sS -X POST http://localhost:8001/backtest_sweep -H 'Content-Type: application/json' -d '{"model_id":"spy_opt_0dte_hourly","pack_id":"zerosigma","thresholds_variants":["0.50,0.52,0.54","0.55,0.60,0.65"],"allowed_hours_variants":["13,14,15"],"splits":5,"embargo":0.0,"save":true,"tag":"sweep"}' | jq .`
- Readouts
  - Leaderboard: `curl -sS 'http://localhost:8001/leaderboard?pack_id=zerosigma&model_id=spy_opt_0dte_hourly&limit=20' | jq .`
  - Runs: `curl -sS 'http://localhost:8001/build_runs?pack_id=zerosigma&model_id=spy_opt_0dte_hourly' | jq .` and `.../training_runs` and `.../sweeps`.

## Makefile Flow
- Configure vars (override per command):
  - `PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly TICKER=SPY START=2024-01-01 END=2024-06-30`
- Build → Train → Backtest
  - `make build PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly TICKER=SPY START=2024-01-01 END=2024-06-30`
  - `make train PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15`
  - `make backtest PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5 ALLOWED_HOURS=13,14,15`
- One-shot pipelines
  - `make pipeline PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly TICKER=SPY START=2024-01-01 END=2024-06-30`
  - `make pipeline-gated PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15 MOMENTUM_MIN=0.1`
- Lists and leaderboard
  - `make leaderboard PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly`
  - `make runs-build PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly`
  - `make runs-train PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly`
  - `make sweeps PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly`

## Persistence and artifacts
- The API persists `build_runs`, `training_runs`, `backtest_runs`, `backtest_folds`, `backtest_sweeps`, and `sweep_results` when DB is configured.
- Artifacts table records `matrix` CSVs and `plot` directories for traceability.

## Troubleshooting
- 404s on endpoints: ensure API is running: `python products/sigma-lab/api/run_api.py --reload`.
- DB errors: set `DATABASE_URL` or `DB_*` envs and run `make db-migrate`.
- Matrix not found during backtest: make sure you ran Build first and paths are under the model’s workspace.
- Policy missing: use `GET /validate_policy?model_id=...&pack_id=...` and ensure policy file exists.

Links
- [[Modeling Pipeline Guide|MODELING_PIPELINE_GUIDE]] — narrative guide.
- [[API Map|codex-api-endpoints]] — endpoint reference.
- [[Makefile Guide|MAKEFILE_GUIDE]] — all targets and variables.

