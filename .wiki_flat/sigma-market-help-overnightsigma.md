# OvernightSigma Pack — Quick Help

OvernightSigma targets close→next-open signals for equities and options.

## Common Indicator Sets
- overnight_eq_default
- overnight_opt_default

See `products/sigma-lab/packs/overnightsigma/indicator_sets/` for the full list.

## Create a Model (API)
Equities example:
```
curl -sS -X POST http://localhost:8001/models \
 -H 'Content-Type: application/json' \
 -d '{
   "pack_id":"overnightsigma",
   "ticker":"SPY",
   "asset_type":"eq",
   "horizon":"intraday",
   "cadence":"daily",
   "indicator_set_name":"overnight_eq_default"
 }'
```

## Preview → Build → Train → Backtest
```
make preview MODEL_ID=spy_eq_intraday_daily PACK_ID=overnightsigma START=2024-07-01 END=2024-07-05
make build   MODEL_ID=spy_eq_intraday_daily PACK_ID=overnightsigma TICKER=SPY START=2024-06-01 END=2024-07-31
make train   MODEL_ID=spy_eq_intraday_daily
make backtest MODEL_ID=spy_eq_intraday_daily THRESHOLDS=0.55,0.60,0.65 SPLITS=5
```

## Notes
- Indicators rely on close/open alignment and intraday/VWAP context; pick full sessions.

## Runbook
- See consolidated steps in: `products/sigma-lab/docs/runbooks/all_packs_pipeline.md`
