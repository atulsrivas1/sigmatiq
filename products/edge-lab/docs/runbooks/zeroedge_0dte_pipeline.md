# Edge Lab 0DTE Runbook — Build, Train, Backtest, Alerts

This runbook describes a repeatable, end-to-end flow for a 0DTE model in the `zeroedge` pack: preview → build → train → backtest → generate live alerts.

## Prerequisites
- Polygon API key exported or in `products/edge-lab/.env`: `POLYGON_API_KEY=...`
- Optional DB env vars if you want leaderboard persistence (Postgres): `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SCHEMA` (default `app`).
- Start the API (Windows-friendly): `python products/edge-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`

## Pick a Model + Indicator Set
- Pack: `zeroedge`
- Model ID: `spy_opt_0dte_hourly`
- Indicator set (choose one):
  - v1: `zeroedge_pin_drift_v1` (stable)
  - v2: `zeroedge_headfake_reversal_v2` (adds open/range/IV-delta/gamma density v2 features)

Create a model with the selected set (API):
```
curl -sS -X POST http://localhost:8001/models -H "Content-Type: application/json" -d '{
  "pack_id":"zeroedge",
  "ticker":"SPY",
  "asset_type":"opt",
  "horizon":"0dte",
  "cadence":"hourly",
  "indicator_set_name":"zeroedge_pin_drift_v1"
}'
```

(Alternatively, use `scripts/create_model.py` or place a per-model indicator set at `packs/zeroedge/indicator_sets/<model_id>.yaml`.)

## Step 1 — Preview (sanity check)
- Purpose: small-range build to validate data coverage and catch NaNs early.
- v2 thresholds: warn ≥10% NaN; fail ≥30% NaN for v2 features (`open_gap_z`, `first15m_range_z*`, `atm_iv_open_delta`, `gamma_density_peak_strike`, `gamma_skew_left_right`).

Make:
```
make preview MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge START=2024-07-01 END=2024-07-03
```
Output: `products/edge-lab/reports/preview_spy_opt_0dte_hourly.json` with `ok | warnings | v2_nan_summary`.

API (alternative):
```
curl -sS -X POST http://localhost:8001/preview_matrix \
 -H 'Content-Type: application/json' \
 -d '{"model_id":"spy_opt_0dte_hourly","pack_id":"zeroedge","start":"2024-07-01","end":"2024-07-03"}' | jq .
```

## Step 2 — Build Matrix
```
make build MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge TICKER=SPY START=2024-07-01 END=2024-07-12
```
Output: `products/edge-lab/matrices/spy_opt_0dte_hourly/training_matrix_built.csv`

## Step 3 — Train
```
make train MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
```
Output: `products/edge-lab/artifacts/spy_opt_0dte_hourly/gbm.pkl` (stores model + features + label encoder)

## Step 4 — Backtest
```
make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5
```
Outputs:
- Plots: `products/edge-lab/static/backtest_plots/spy_opt_0dte_hourly/`
- Leaderboard persistence (if DB configured) visible via `GET /leaderboard`

## Step 5 — Generate “Live Alerts”
Scores latest rows in the built matrix with the trained model, writing high-confidence signals.
```
make alerts MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
```
Output: `products/edge-lab/live_data/spy_opt_0dte_hourly/signals.csv`

For intraday usage, do a short “today build” first (e.g., `START=today END=today`) so features reflect current data; then rerun alerts.

## Optional — Backtest Sweep and Smoke Pipeline
- Run a sweep (grid across thresholds/hours or top_pct):
```
make sweep MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14 THRESHOLDS=0.55,0.60,0.65 TOP_PCT=0.10,0.15 TAG=demo
```
Returns a report path under `products/edge-lab/reports/` and persists runs when DB is configured. Also available via `POST /backtest_sweep`.

- Quick smoke pipeline with summary + conditional train:
```
make smoke MODEL_ID=spy_opt_0dte_hourly START=2024-07-01 END=2024-07-12 \
  SMOKE_MIN_SHARPE=0.30 SMOKE_MIN_TRADES=5 SMOKE_TOP_PCT=0.10
```
Prints a summary, backtests, and trains only when guardrails pass.

## BTB v1 — Alternate Path (Recommended)
For configuration discovery and safer training, prefer this order:

1) Build Matrix (Step 2 above) — capture `matrix_sha` and inspect Matrix Profile (NaN%, label balance, leakage flags, coverage).
2) Run Sweeps — vary thresholds/hours/top%; choose a Risk Profile preset (Conservative/Balanced/Aggressive) or override budgets.
3) Review Leaderboard — enable "Pass Gate only"; inspect Gate badges and compare top rows (equity/drawdown/hour-wise performance). Add promising rows to Selection.
4) Train — queue only Gate‑passing selections by default (override requires confirmation + tag). Artifacts are stored under `artifacts/<model_id>/<risk_profile>/...` with lineage (`matrix_sha`, `config_sha`, `policy_sha`, `risk_sha`).

Notes
- Risk budgets and profiles are documented in `specs/Risk_Profile_Schema.md`.
- Gate and ranking logic live in `specs/Gate_and_Scoring_Spec_v1.md`. Leaderboard should reflect pass/fail with reasons.
- Matrix Contract v1 (`specs/Matrix_Contract_v1.md`) defines pre‑labeling hours and hygiene rules for intraday packs.

## Common Issues & Tips
- Missing IV/gamma/PCR/OI → NaNs in preview. Use recent full sessions and ensure same-day chains exist for 0DTE.
- Ensure `POLYGON_API_KEY` is loaded (Preview and v2 features use Polygon adapters).
- v2 features that rely on 5m bars (`first15m_range_z`) only become meaningful after the window ends (e.g., 09:45). If modeling earlier rows, mask or allow NaNs.
- `/healthz` confirms basic data adapters and DB. Use `make health TICKER=SPY`.

## Quick Examples
- Pin Drift v1:
```
# Create
curl -sS -X POST http://localhost:8001/models -H 'Content-Type: application/json' \
 -d '{"pack_id":"zeroedge","ticker":"SPY","asset_type":"opt","horizon":"0dte","cadence":"hourly","indicator_set_name":"zeroedge_pin_drift_v1"}'
# Pipeline
make preview MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge START=2024-07-01 END=2024-07-03
make build   MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge TICKER=SPY START=2024-07-01 END=2024-07-12
make train   MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5
make alerts  MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
```
- Head‑Fake Reversal v2:
```
curl -sS -X POST http://localhost:8001/models -H 'Content-Type: application/json' \
 -d '{"pack_id":"zeroedge","ticker":"SPY","asset_type":"opt","horizon":"0dte","cadence":"hourly","indicator_set_name":"zeroedge_headfake_reversal_v2"}'
make preview MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge START=2024-07-01 END=2024-07-03
# if ok, continue with build/train/backtest/alerts as above
```

## References
- Indicator sets:
  - `packs/zeroedge/indicator_sets/zeroedge_pin_drift_v1.yaml`
  - `packs/zeroedge/indicator_sets/zeroedge_headfake_reversal_v2.yaml`
- Scripts:
  - API runner: `products/edge-lab/api/run_api.py`
- API endpoints: `/models`, `/preview_matrix`, `/build_matrix`, `/train`, `/backtest`, `/leaderboard`
