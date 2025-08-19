# Model Help — aapl_stock_hourly

Example equities model (hourly) for AAPL. Use with an equities-focused indicator set (e.g., `swingedge`).

## Quick Start
```
# Create (API)
curl -sS -X POST http://localhost:8001/models -H 'Content-Type: application/json' \
 -d '{"pack_id":"swingedge","ticker":"AAPL","asset_type":"eq","horizon":"intraday","cadence":"hourly","indicator_set_name":"swing_eq_default"}'

# Preview (1–2 days)
make preview MODEL_ID=aapl_eq_intraday_hourly PACK_ID=swingedge START=2024-07-01 END=2024-07-03

# Build → Train → Backtest
make build    MODEL_ID=aapl_eq_intraday_hourly PACK_ID=swingedge TICKER=AAPL START=2024-07-01 END=2024-07-12
make train    MODEL_ID=aapl_eq_intraday_hourly
make backtest MODEL_ID=aapl_eq_intraday_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5
```

## Outputs
- Matrix: `products/edge-lab/matrices/aapl_eq_intraday_hourly/training_matrix_built.csv`
- Model: `products/edge-lab/artifacts/aapl_eq_intraday_hourly/gbm.pkl`
- Plots: `products/edge-lab/static/backtest_plots/aapl_eq_intraday_hourly/`
