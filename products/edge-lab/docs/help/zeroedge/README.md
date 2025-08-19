# ZeroEdge Pack — Quick Help

This pack contains 0DTE options models and indicator sets mixing intraday momentum, options IV/term-structure, and flow features.

## Common Indicator Sets
- zeroedge_default
- zeroedge_headfake_reversal_v1
- zeroedge_headfake_reversal_v2
- zeroedge_pin_drift_v1
- zeroedge_pin_drift_v2

See `products/edge-lab/packs/zeroedge/indicator_sets/` for the full list.

## Create a Model (API)
```
curl -sS -X POST http://localhost:8001/models \
 -H 'Content-Type: application/json' \
 -d '{
   "pack_id":"zeroedge",
   "ticker":"SPY",
   "asset_type":"opt",
   "horizon":"0dte",
   "cadence":"hourly",
   "indicator_set_name":"zeroedge_pin_drift_v1"
 }'
```

## Preview (sanity)
```
make preview MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge START=2024-07-01 END=2024-07-03
```
- v2 features warn >=10% NaN; fail >=30% NaN.

## Build → Train → Backtest → Alerts
```
make build    MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge TICKER=SPY START=2024-07-01 END=2024-07-12
make train    MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5
make alerts   MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
```
- Alerts append to `products/edge-lab/live_data/spy_opt_0dte_hourly/signals.csv`.

## Notes
- Set `POLYGON_API_KEY` (and DB envs if you want `/leaderboard`).
- For intraday alerts, run a short “today build” first, then `make alerts`.

## Sweeps & Smoke
- Sweep backtests and persist tagged runs: `make sweep MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 ALLOWED_HOURS=13,14 TOP_PCT=0.10,0.15 TAG=demo`
- Smoke pipeline with summary + conditional train: `make smoke MODEL_ID=spy_opt_0dte_hourly START=2024-07-01 END=2024-07-12 SMOKE_MIN_SHARPE=0.30 SMOKE_MIN_TRADES=5 SMOKE_TOP_PCT=0.10`

## Runbook
- See the consolidated steps in: `products/edge-lab/docs/runbooks/all_packs_pipeline.md`
