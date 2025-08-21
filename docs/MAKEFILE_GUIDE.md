# Makefile Pipeline Guide

This guide shows how to use the root `Makefile` to run the full modeling pipeline: discover packs, create a model, build data, create sweeps, backtest, inspect leaderboard, and train based on results. It also covers DB-backed run history and troubleshooting.

## Prerequisites
- API server reachable at `BASE_URL` (default `http://localhost:8001`). Start with:
  - `uvicorn products.sigma-lab.api.app:app --host 0.0.0.0 --port 8001`
- `.env` configured (see `.env.example` for keys):
  - Polygon: `POLYGON_API_KEY`
  - Database: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- Apply migrations once: `make db-migrate`
- Tools: `curl`, `jq` in PATH

## Core Variables
- `PACK_ID` (default `zeroedge`), `MODEL_ID`, `TICKER`, `START`, `END`
- `ALLOWED_HOURS`, `THRESHOLDS` (CSV `0.55,0.60,0.65`), `SPLITS` (default `5`)
- `DISTANCE_MAX` (default `7`), `BASE_URL` (default `http://localhost:8001`)
- Listing/paging: `LIMIT` (default `20`), `OFFSET` (default `0`)

## 1) Discover Packs and Templates
- List packs: `make packs`
- Pack detail: `make pack-detail PACK_ID=zerosigma`
- Pack templates: `make pack-templates PACK_ID=zerosigma`
- Pack indicator sets: `make pack-indicators PACK_ID=zerosigma`
- Pack models: `make pack-models PACK_ID=zerosigma` (alias of `make models PACK_ID=...`)

Tip: pick a `PACK_ID` (e.g., `zerosigma`) and the `TICKER` you want to work with (e.g., `SPY`).

## 2) Create a Model
- Manual: `make init MODEL_ID=spy_opt_0dte_hourly TICKER=SPY PACK_ID=zeroedge`
- Auto: `make init-auto TICKER=SPY ASSET=opt HORIZON=0dte CADENCE=hourly PACK_ID=zeroedge`

Creates `models/<PACK_ID>/<MODEL_ID>/README.md` and `policy.yaml`.

## 3) Build the Dataset (Matrix)
`make build MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31 TICKER=SPY PACK_ID=zerosigma`

Result: a CSV under `products/sigma-lab/matrices/<MODEL_ID>/training_matrix_built.csv`

DB: a row is written to `build_runs` and an artifact row (kind=matrix) is created.

History: `make runs-build PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly`

## 4) Generate a Sweep Configuration (editable)
`make sweep-config MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31`
→ writes `sweeps/<MODEL_ID>_sweep.yaml` with grids for build/train/backtest.

You can pass this YAML into your own sweep runner or call the API’s sweep endpoint (see “Sweeps” below).

## 5) Backtest the Model
- Standard: `make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5`
- Gated: `make backtest-gated MODEL_ID=spy_opt_0dte_hourly MOMENTUM_MIN=0.1 MOMENTUM_COLUMN=momentum_score_total`

DB: a row is written to `backtest_runs` (and folds to `backtest_folds`), plus an artifact row (kind=plot).

Leaderboard: `make leaderboard PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly`

## 6) Train the Model (Baseline)
`make train MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15`

Output: model bundle under `products/sigma-lab/artifacts/<MODEL_ID>/gbm.pkl`

DB: a row is written to `training_runs` and an artifact row (kind=model) is created.

History: `make runs-train PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly`

## 7) Train Based on Leaderboard Findings
- Use leaderboard or sweep results to pick params (e.g., the best hours or top thresholds):
  - `make leaderboard MODEL_ID=spy_opt_0dte_hourly` and inspect for highest `best_sharpe_hourly`.
  - If sweeps are used (see next section), query the best entries and choose `allowed_hours`/threshold strategy accordingly.
- Retrain with selected hours or calibration:
  - `make train MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15`

## 8) Sweeps (optional, but recommended)
- Use a client (or curl) against the sweep endpoint to explore multiple variants in one shot.
- History and detail:
  - `make sweeps PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly STATUS=completed`
  - `make sweep SWEEP_ID=123`
- Use the best performing variants to guide training and backtesting.

## 9) Run History (DB)
- Build runs: `make runs-build PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly LIMIT=20 OFFSET=0`
- Training runs: `make runs-train PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly LIMIT=20 OFFSET=0`
- Sweeps list/detail: `make sweeps ...` / `make sweep SWEEP_ID=...`

## End-to-End Smoke Test
Use a single command to validate the real backend end-to-end:
```
make check-backend \
  BASE_URL=http://localhost:8001 \
  TICKER=SPY PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly \
  START=2024-01-01 END=2024-03-31
```
This runs: health → build → train → backtest → leaderboard.

## Tips & Troubleshooting
- Health: `make health TICKER=SPY` (checks Polygon/data/DB wiring)
- Migrations: `make db-migrate` (reads DB_* from `.env`)
- DB rows not appearing? Ensure `.env` contains DB credentials and restart the API.
- Matrix empty or NaNs high? Adjust date ranges or indicator sets under `packs/<PACK_ID>/indicator_sets`.
- Missing models? Use `make models PACK_ID=zerosigma` to list model configs discovered in packs.
- More help: `make help`

## Model discovery and policy validation
- List models (by pack): `make models PACK_ID=zerosigma` or `make pack-models PACK_ID=zerosigma` (GET `/models?pack_id=$(PACK_ID)`).
- Validate policy (alias to policy explain): `make validate-policy MODEL_ID=spy_opt_0dte_hourly PACK_ID=zerosigma` (GET `/validate_policy`).

## Backend smoke test
End-to-end against the real API:
`make check-backend BASE_URL=http://<api> TICKER=SPY PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31`
Runs: health → build → train → backtest → leaderboard.
