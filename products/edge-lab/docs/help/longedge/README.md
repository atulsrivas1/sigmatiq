# LongEdge Pack — Quick Help

LongEdge covers longer horizons (63–252 days) for equities and options.

## Common Indicator Sets
- long_eq_default
- long_opt_default

See `products/edge-lab/packs/longedge/indicator_sets/` for the full list.

## Create a Model (API)
Equities example:
```
curl -sS -X POST http://localhost:8001/models \
 -H 'Content-Type: application/json' \
 -d '{
   "pack_id":"longedge",
   "ticker":"SPY",
   "asset_type":"eq",
   "horizon":"long",
   "cadence":"daily",
   "indicator_set_name":"long_eq_default"
 }'
```

## Preview → Build → Train → Backtest
```
make preview MODEL_ID=spy_eq_long_daily PACK_ID=longedge START=2023-06-01 END=2023-06-10
make build   MODEL_ID=spy_eq_long_daily PACK_ID=longedge TICKER=SPY START=2023-01-01 END=2024-06-30
make train   MODEL_ID=spy_eq_long_daily
make backtest MODEL_ID=spy_eq_long_daily THRESHOLDS=0.55,0.60,0.65 SPLITS=5
```

## Notes
- Longer windows benefit from broader date ranges and more stable sessions.

## Runbook
- See consolidated steps in: `products/edge-lab/docs/runbooks/all_packs_pipeline.md`
