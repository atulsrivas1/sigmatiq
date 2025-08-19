# SwingSigma Pack — Quick Help

SwingSigma provides swing-horizon models for equities and options.

## Common Indicator Sets
- swing_eq_default
- swing_opt_default

See `products/sigma-lab/packs/swingedge/indicator_sets/` for the full list.

## Create a Model (API)
Equities example:
```
curl -sS -X POST http://localhost:8001/models \
 -H 'Content-Type: application/json' \
 -d '{
   "pack_id":"swingedge",
   "ticker":"AAPL",
   "asset_type":"eq",
   "horizon":"swing",
   "cadence":"daily",
   "indicator_set_name":"swing_eq_default"
 }'
```

## Preview → Build → Train → Backtest
```
make preview MODEL_ID=aapl_eq_swing_daily PACK_ID=swingedge START=2024-07-01 END=2024-07-10
make build   MODEL_ID=aapl_eq_swing_daily PACK_ID=swingedge TICKER=AAPL START=2024-07-01 END=2024-07-31
make train   MODEL_ID=aapl_eq_swing_daily
make backtest MODEL_ID=aapl_eq_swing_daily THRESHOLDS=0.55,0.60,0.65 SPLITS=5
```

## Notes
- Ensure `POLYGON_API_KEY` is set.
- Options sets require Polygon option snapshots; start with equities if testing quickly.

## Scanners
- How-to: `products/sigma-lab/docs/help/scanners/README.md`
- Stock brackets: `products/sigma-lab/docs/help/scanners/stock_bracketed_alerts.md`
- Predefined templates (indicator sets ready):
  - `swing_eq_breakout_scanner`
  - `swing_eq_meanrevert_scanner`
  - `swing_eq_trend_follow_scanner`
  - `swing_eq_vol_contraction_scanner`
  - `swing_eq_rel_strength_scanner`
  - `swing_eq_high_momentum_scanner`
Run via CLI: `make scan PACK_ID=swingedge MODEL_ID=universe_eq_swing_daily_scanner UNIVERSE=AAPL,MSFT,SPY START=YYYY-MM-DD END=YYYY-MM-DD`

## Runbook
- See the consolidated steps in: `products/sigma-lab/docs/runbooks/all_packs_pipeline.md`


## Signals + Overlay Quickstart

1) Run a scan and produce signals
```
make scan-breakout UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
# CSV: products/sigma-lab/live_data/universe_eq_swing_daily_breakout_scanner/signals.csv
```

2) Inspect signals or read from API
```
curl -sS "http://localhost:8001/signals?model_id=universe_eq_swing_daily_breakout_scanner&date=2025-08-06&limit=50"
```

3) Turn stock picks into options (overlay)
- Single-leg (DB signals):
```
curl -sS -X POST http://localhost:8001/options_overlay  -H 'Content-Type: application/json'  -d '{
   "model_id": "universe_eq_swing_daily_breakout_scanner",
   "date": "2025-08-06",
   "expiry": "2025-08-16",
   "target_delta": 0.35,
   "min_oi": 1000,
   "limit": 50
 }'
```
- Single-leg (CSV fallback):
```
curl -sS -X POST http://localhost:8001/options_overlay  -H 'Content-Type: application/json'  -d '{
   "model_id": "universe_eq_swing_daily_breakout_scanner",
   "date": "2025-08-06",
   "dte_target": 14,
   "target_delta": 0.35,
   "limit": 50
 }'
```
- Debit vertical (call):
```
curl -sS -X POST http://localhost:8001/options_overlay  -H 'Content-Type: application/json'  -d '{
   "model_id": "universe_eq_swing_daily_breakout_scanner",
   "date": "2025-08-06",
   "expiry": "2025-08-16",
   "target_delta": 0.35,
   "option_mode": "vertical",
   "spread_width": 5,
   "min_oi": 500,
   "limit": 50
 }'
```

Notes
- Side defaults to calls for buy signals; you can override with "side_override": "put".
- If "expiry" is omitted, use "dte_target" (days) to approximate an expiry.
- Pricing uses snapshot mid when available; falls back to last quote mid if needed.
- Premium brackets are first-order, based on delta and underlying brackets.


Tip: list upcoming expirations
```
python products/sigma-lab/api/scripts/list_expirations.py --ticker AAPL --weeks 8 --base_url http://localhost:8001
```
Or via API: `GET /options/expirations?ticker=AAPL&weeks=8`
