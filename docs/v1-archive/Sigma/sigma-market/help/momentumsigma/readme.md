# MomentumSigma Pack — Quick Help

MomentumSigma offers intraday/daily momentum models for equities and options.

## Common Indicator Sets
- momo_eq_default
- momo_opt_default

See `products/sigma-lab/packs/momentumsigma/indicator_sets/` for the full list.

## Create a Model (API)
Equities example:
```
curl -sS -X POST http://localhost:8001/models \
 -H 'Content-Type: application/json' \
 -d '{
   "pack_id":"momentumsigma",
   "ticker":"SPY",
   "asset_type":"eq",
   "horizon":"intraday",
   "cadence":"hourly",
   "indicator_set_name":"momo_eq_default"
 }'
```

## Preview → Build → Train → Backtest
```
make preview MODEL_ID=spy_eq_intraday_hourly PACK_ID=momentumsigma START=2024-07-01 END=2024-07-05
make build   MODEL_ID=spy_eq_intraday_hourly PACK_ID=momentumsigma TICKER=SPY START=2024-06-01 END=2024-07-31
make train   MODEL_ID=spy_eq_intraday_hourly
make backtest MODEL_ID=spy_eq_intraday_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5
```

## Notes
- Use `ALLOWED_HOURS` to constrain training to specific ET hours when relevant.

## Runbook
- See consolidated steps in: `products/sigma-lab/docs/runbooks/all_packs_pipeline.md`
