# All Packs Runbook — Preview, Build, Train, Backtest, Alerts

This runbook shows a consistent way to preview and run pipelines for all packs. Commands assume POLYGON_API_KEY in .env or the environment. DB is optional (used for /leaderboard).

## Prerequisites
- Start the API (Windows-friendly):
  - `python products/edge-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`
- Set env vars in `products/edge-lab/.env` or the environment as needed:
  - `POLYGON_API_KEY=...`
  - Optional: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SCHEMA`

---

## ZeroEdge (0DTE, options)
- Models:
  - spy_opt_0dte_hourly_headfake_1030 (indicator_set: zeroedge_headfake_reversal_v2)
  - spy_opt_0dte_hourly_pin_1500 (indicator_set: zeroedge_pin_drift_v2)
- Preview (v2 gates apply for v2 features):
  - make preview MODEL_ID=spy_opt_0dte_hourly_headfake_1030 PACK_ID=zeroedge START=2024-07-01 END=2024-07-03
- Build -> Train -> Backtest:
  - make build MODEL_ID=spy_opt_0dte_hourly_headfake_1030 PACK_ID=zeroedge TICKER=SPY START=2024-07-01 END=2024-07-12
  - make train MODEL_ID=spy_opt_0dte_hourly_headfake_1030 ALLOWED_HOURS=13,14,15
  - make backtest MODEL_ID=spy_opt_0dte_hourly_headfake_1030 THRESHOLDS=0.55,0.60,0.65 SPLITS=5
- Live alerts (scores latest rows; for true intraday, rebuild today first):
  - make alerts MODEL_ID=spy_opt_0dte_hourly_headfake_1030 ALLOWED_HOURS=13,14,15

---

## SwingEdge (equities/options)
- Models:
  - spy_eq_swing_daily (indicator_set: swing_eq_default, labels: fwd_ret_20d)
  - spy_opt_swing_daily (indicator_set: swing_opt_default, labels: fwd_ret_20d)
- Preview (stocks path):
  - python scripts/preview_stock_model.py --model_id spy_eq_swing_daily --pack_id swingedge --start 2023-01-01 --end 2023-06-30 --label_kind fwd_ret_20d --out reports/preview_spy_eq_swing_daily.json
- Build (API alternative):
  - curl -sS -X POST http://localhost:8001/build_stock_matrix -H "Content-Type: application/json" -d '{"ticker":"SPY","pack_id":"swingedge","model_id":"spy_eq_swing_daily","start":"2023-01-01","end":"2023-12-31","label_kind":"fwd_ret_20d"}'
- Train -> Backtest:
  - make train MODEL_ID=spy_eq_swing_daily
  - make backtest MODEL_ID=spy_eq_swing_daily THRESHOLDS=0.55,0.60,0.65 SPLITS=5

### Scanners Quickstart (equities)
- Predefined templates (indicator sets):
  - breakout: `swing_eq_breakout_scanner`
  - mean-revert: `swing_eq_meanrevert_scanner`
  - trend-follow: `swing_eq_trend_follow_scanner`
  - vol-contraction: `swing_eq_vol_contraction_scanner`
  - relative-strength: `swing_eq_rel_strength_scanner`
  - high-momentum: `swing_eq_high_momentum_scanner`

- One-liners (CLI): provide a universe list or CSV, plus a short date window:
```
make scan-breakout     UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
make scan-meanrevert   UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
make scan-trend        UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
make scan-squeeze      UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
make scan-rs           UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
make scan-highmomo     UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
```
- Or with a CSV universe:
```
make scan-breakout UNIVERSE_CSV=data/universe/sample10.csv START=2025-08-01 END=2025-08-06
```
- Outputs: `products/edge-lab/live_data/<model_id>/signals.csv` and Top picks echoed in the console.

---

## LongEdge (equities/options)
- Models:
  - spy_eq_long_daily (indicator_set: long_eq_default, labels: fwd_ret_63d)
  - spy_opt_long_daily (indicator_set: long_opt_default, labels: fwd_ret_63d)
- Preview (use a long window for lookahead):
  - python scripts/preview_stock_model.py --model_id spy_eq_long_daily --pack_id longedge --start 2022-01-01 --end 2023-12-31 --label_kind fwd_ret_63d --out reports/preview_spy_eq_long_daily.json
- Build -> Train -> Backtest (equities example):
  - curl -sS -X POST http://localhost:8001/build_stock_matrix -H "Content-Type: application/json" -d '{"ticker":"SPY","pack_id":"longedge","model_id":"spy_eq_long_daily","start":"2022-01-01","end":"2023-12-31","label_kind":"fwd_ret_63d"}'
  - make train MODEL_ID=spy_eq_long_daily
  - make backtest MODEL_ID=spy_eq_long_daily THRESHOLDS=0.55,0.60,0.65 SPLITS=5

---

## OvernightEdge (equities/options)
- Models:
  - spy_eq_intraday_daily (indicator_set: overnight_eq_default, labels: close_to_open supported via stocks builder)
  - spy_opt_intraday_daily (indicator_set: overnight_opt_default)
- Preview (equities):
  - curl -sS -X POST http://localhost:8001/build_stock_matrix -H "Content-Type: application/json" -d '{"ticker":"SPY","pack_id":"overnightedge","model_id":"spy_eq_intraday_daily","start":"2024-07-01","end":"2024-07-05","label_kind":"close_to_open"}'
- Train -> Backtest:
  - make train MODEL_ID=spy_eq_intraday_daily
  - make backtest MODEL_ID=spy_eq_intraday_daily THRESHOLDS=0.55,0.60,0.65 SPLITS=5

---

## MomentumEdge (equities/options)
- Models:
  - spy_eq_intraday_hourly (indicator_set: momo_eq_default, next-bar labels)
  - spy_opt_intraday_hourly (indicator_set: momo_opt_default)
- Preview (equities):
  - python scripts/preview_stock_model.py --model_id spy_eq_intraday_hourly --pack_id momentumedge --start 2024-06-01 --end 2024-06-30 --out products/edge-lab/reports/preview_spy_eq_intraday_hourly.json
- Build -> Train -> Backtest (equities):
  - curl -sS -X POST http://localhost:8001/build_stock_matrix -H "Content-Type: application/json" -d '{"ticker":"SPY","pack_id":"momentumedge","model_id":"spy_eq_intraday_hourly","start":"2024-06-01","end":"2024-06-30"}'
  - make train MODEL_ID=spy_eq_intraday_hourly
- make backtest MODEL_ID=spy_eq_intraday_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5

---

## Options Overlay (single-leg and vertical)

Use the options overlay to turn stock signals into options contracts with bracket estimates. It can read signals from the DB (preferred) or fall back to the CSV produced by scans.

- Single-leg overlay (DB signals):
```
curl -sS -X POST http://localhost:8001/options_overlay \
 -H 'Content-Type: application/json' \
 -d '{
   "model_id": "universe_eq_swing_daily_breakout_scanner",
   "date": "2025-08-06",
   "expiry": "2025-08-16",
   "target_delta": 0.35,
   "min_oi": 1000,
   "limit": 50
  }'
```

- Single-leg overlay (CSV fallback):
  - Requires `products/edge-lab/live_data/<model_id>/signals.csv` (e.g., from `make scan-*`).
```
curl -sS -X POST http://localhost:8001/options_overlay \
 -H 'Content-Type: application/json' \
 -d '{
   "model_id": "universe_eq_swing_daily_breakout_scanner",
   "date": "2025-08-06",
   "dte_target": 14,
   "target_delta": 0.35,
   "option_mode": "single",
   "limit": 50
 }'
```
  - Output CSV fallback: `products/edge-lab/live_data/<model_id>/options_signals.csv`

- Debit vertical (call) overlay:
```
curl -sS -X POST http://localhost:8001/options_overlay \
 -H 'Content-Type: application/json' \
 -d '{
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
- Side defaults to calls for buy signals; override with `"side_override": "put"` if needed.
- If `expiry` is omitted, you can supply `dte_target` (days) to approximate an expiry.
- Pricing uses snapshot mid when available; falls back to the last quote mid if missing.
- Premium brackets are first-order delta-mapped from underlying brackets.

---

## Leaderboard & DB
- Optional DB persistence; without DB, backtest returns metrics and plots locally.
- With DB configured, query leaderboard:
  - curl -sS "http://localhost:8001/leaderboard?pack_id=<pack>&model_id=<model_id>&limit=20"
  - Tag filter: add `&tag=<your_tag>` to scope to sweep/smoke runs

## Troubleshooting
- Missing IV/OI/quotes -> NaNs in preview; pick dates with full sessions.
- Use longer windows for long-horizon labels (e.g., 63d lookahead).
- ZeroEdge v2 preview enforces NaN thresholds (warn >=10%, fail >=30%) on v2 features.
- Ensure POLYGON_API_KEY is loaded in the environment or .env.


Helper: list expirations
```
python scripts/list_expirations.py --ticker AAPL --weeks 12 --base_url http://localhost:8001
```
Or via API: `GET /options/expirations?ticker=AAPL&weeks=12`

## Extras
- Backtest sweep:
  - `make sweep MODEL_ID=<id> THRESHOLDS=0.55,0.60,0.65 TOP_PCT=0.10,0.15 ALLOWED_HOURS=13,14 TAG=demo`
- Smoke pipeline with conditional train:
  - `make smoke MODEL_ID=<id> START=<YYYY-MM-DD> END=<YYYY-MM-DD> SMOKE_MIN_SHARPE=0.30 SMOKE_MIN_TRADES=5 SMOKE_TOP_PCT=0.10`
