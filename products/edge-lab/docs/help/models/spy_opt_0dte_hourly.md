# Model Help — spy_opt_0dte_hourly

ZeroEdge 0DTE hourly model for SPY. Use with any `products/edge-lab/packs/zeroedge/indicator_sets/*.yaml`.

## Quick Start
```
# Create (API)
curl -sS -X POST http://localhost:8001/models -H 'Content-Type: application/json' \
 -d '{"pack_id":"zeroedge","ticker":"SPY","asset_type":"opt","horizon":"0dte","cadence":"hourly","indicator_set_name":"zeroedge_pin_drift_v1"}'

# Preview (1–2 days)
make preview MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge START=2024-07-01 END=2024-07-03

# Build → Train → Backtest → Alerts
make build    MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge TICKER=SPY START=2024-07-01 END=2024-07-12
make train    MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5
make alerts   MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
```

## Outputs
- Matrix: `products/edge-lab/matrices/spy_opt_0dte_hourly/training_matrix_built.csv`
- Model: `products/edge-lab/artifacts/spy_opt_0dte_hourly/gbm.pkl`
- Plots: `products/edge-lab/static/backtest_plots/spy_opt_0dte_hourly/`
- Alerts: `products/edge-lab/live_data/spy_opt_0dte_hourly/signals.csv`
