# Start Here (Curated Quick Links)

This page is a short, friendly jumping‑off point for non‑technical users. Follow these items in order to get to useful, repeatable alerts quickly.

## 5‑Minute Setup
- Configure `.env` (copy `.env.example` and fill DB_* and `POLYGON_API_KEY`).
- Run DB migrations: `make db-migrate`.
- Start the API: `uvicorn products.sigma-lab.api.app:app --host 0.0.0.0 --port 8001`.
- Sanity check (copy/paste, change caps):
  - `make check-backend BASE_URL=http://localhost:8001 TICKER=SPY PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31`

## Learn by Doing (First Model)
1) Create: `make init-auto TICKER=SPY ASSET=opt HORIZON=0dte CADENCE=hourly PACK_ID=zerosigma`
2) Build: `make build MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31 TICKER=SPY PACK_ID=zerosigma`
3) Backtest: `make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5`
4) Scoreboard: `make leaderboard MODEL_ID=spy_opt_0dte_hourly`
5) Train (lock in): `make train MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15`

## Choose Your Strategy (Packs)
- List available packs: `make packs`
- See a pack’s details (templates, indicators, models): `make pack-detail PACK_ID=zerosigma`
- Models in a pack: `make pack-models PACK_ID=zerosigma`

## What “Good” Looks Like
- Backtest: positive Sharpe, reasonable trade count, consistent across folds.
- Leaderboard: multiple strong entries (not just one lucky run).
- Train: live alerts resemble backtest behavior.

## Best Practices (Quick)
- Start narrow: one ticker + one cadence; expand after consistency.
- Use sweeps to discover good hours/thresholds; then retrain with those.
- Turn on momentum gate and ATR brackets for better risk control.
- Keep runs small and frequent; compare changes on the leaderboard.

## Common Pitfalls
- DB errors during migrations → fix `.env` DB_* (or `DATABASE_URL`).
- Empty matrix or many NaNs → adjust dates; verify API key; try fewer indicators.
- Leaderboard empty → run a backtest first and ensure DB is configured.

## Deep Dives
- End‑to‑end workflow: [[Modeling Pipeline Guide|modeling_pipeline_guide]]
- Concepts and allowed values: [[Modeling Reference|modeling_reference]]
- Indicators catalog (auto‑generated): [[INDICATORS_REFERENCE.md|INDICATORS_REFERENCE]]
- Make targets overview: [[Makefile Guide|makefile_guide]]

## Next Steps
- Run history (DB): `make runs-build`, `make runs-train`, `make sweeps`, `make sweep SWEEP_ID=...`
- Explore sweeps to refine hours/thresholds; retrain the winners.
- Wire your trained model into alerts (CSV/API) for daily use.
