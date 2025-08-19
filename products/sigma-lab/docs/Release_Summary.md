# Sigmatiq Sigma — Backend, Scanners, Alerts, and Options Overlay (Summary)


> Backlog: products/sigma-lab/docs/BACKLOG.md

> Go/No-Go & Sigma Sim PRD: products/sigma-lab/docs/Sigmatiq_Execution_Plan_GoNoGo_SigmaSim_PRD_v1_UPDATED_2025-08-16.md

> Vision: products/sigma-lab/docs/Sigmatiq_Vision_and_Product_Ecosystem_v3_2025-08-16.md


## What's New
- Stock Bracketed Alerts: Scanners and ML alerts now emit actionable entries with ATR-based stop/target/time-stop and RR. CSV + optional DB write.
- Options Overlay: Converts stock picks to option contracts (single-leg or debit vertical) with premium estimates; supports DB and CSV fallback.
- Signals DB: Normalized tables for alerts; read/write helpers; APIs to list and summarize signals.
- API Modularization: FastAPI endpoints moved into focused routers with shared services for policy, IO, and brackets; app.py slimmed down.
- Docs & Runbooks: End-to-end quickstarts for scanning, alerts, overlay, and expirations helper; predefined scanner templates include examples.

## Core Capabilities
- Scanners (SwingSigma): Breakout, mean-revert, trend-follow, vol-contraction, relative strength, high-momentum — with ready-to-run indicator sets.
- Stock Alerts: Bracket computation uses ATR (period=14, floor=0.05% of price), default entry_mode=next_session_open, stop=1.2xATR, target=2.0xATR, time_stop=120, optional min_rr.
- Options Overlay: Target delta and min OI selection, expiry via exact date or dte_target, vertical spreads (debit call) with width; quotes fallback when snapshot mid is missing.

## APIs (FastAPI)
- Health: GET /health, GET /healthz?ticker=SPY
- Indicators: GET /indicators, GET /indicators?group=true
- Datasets: POST /build_matrix, POST /build_stock_matrix
- Training: POST /train
- Backtest: POST /backtest, GET /leaderboard
- Models: POST /models, POST /indicator_sets, POST /preview_matrix
- Calibration: POST /calibrate_thresholds (Top-N fit), POST /calibrate_brackets (RR-based ATR stop/target suggestion)
- Signals:
  - List: GET /signals?model_id=<id>&date=YYYY-MM-DD&limit=200
  - Summary vs prior day: GET /signals/summary?model_id=<id>&date=YYYY-MM-DD
- Options:
  - Overlay: POST /options_overlay (single | vertical), DB/CSV fallback
  - Expirations helper: GET /options/expirations?ticker=AAPL&weeks=12

## CLI & Make
- Run API: make ui
- Scan presets:
  - Breakout: make scan-breakout UNIVERSE=AAPL,MSFT,SPY START=YYYY-MM-DD END=YYYY-MM-DD
  - More: scan-meanrevert | scan-trend | scan-squeeze | scan-rs | scan-highmomo
  - Universes: scan-nasdaq100 | scan-nasdaq200 | scan-sp100 | scan-sp500 | scan-russell1000
- Signals:
  - List via API (example): curl -sS "http://localhost:8001/signals?model_id=<id>&date=YYYY-MM-DD&limit=50"
- Options Overlay:
  - Single-leg (DB): POST /options_overlay with { model_id, date, expiry, target_delta, min_oi }
  - Single-leg (CSV fallback): POST with { model_id, date, dte_target, target_delta }
  - Vertical (debit): POST with { model_id, date, expiry, option_mode: "vertical", spread_width, target_delta }
- Expirations:
  - Helper: make expirations TICKER=AAPL [WEEKS=12]
  - CLI: python scripts/list_expirations.py --ticker AAPL --weeks 12
- Calibration:
  - Thresholds: POST /calibrate_thresholds (grid + Top-N)
  - Brackets: POST /calibrate_brackets (suggests ATR stop/target for a desired RR)

## Data & DB
- Signals Table (migrations/0004_create_signals.sql):
  - Keys: (date, model_id, ticker), fields: side, entry_mode, entry_ref_px, stop_px, target_px, time_stop_minutes, rr, plus scores and metadata.
- Option Signals (migrations/0005_create_option_signals.sql):
  - Child rows per signal: occ_symbol | expiry | strike | type | delta | iv_used | entry/stop/target premium estimates | legs_json (future spreads).
- Write Path:
  - /scan and ML alerts write CSV and optionally upsert to DB.
- Overlay stores to DB (when configured) or products/sigma-lab/live_data/<model_id>/options_signals.csv.

## Code Structure
- Routers (edge_api/routers): health.py, indicators.py, datasets.py, training.py, backtest.py, models.py, calibration.py, signals.py, options.py
- Services (edge_api/services): brackets.py (stock brackets), policy.py (load/validate), io.py (paths/config)
- Signals Registry: sigma_core/registry/signals_registry.py (upsert/fetch, option upsert)
- Polygon Adapters: sigma_core/data/sources/polygon.py (bars, chain snapshot, quotes)

## Docs & Help
- Runbook: docs/runbooks/all_packs_pipeline.md (scan -> alerts -> overlay workflow + expirations helper)
- Scanners:
  - How-to: docs/help/scanners/README.md
  - Predefined templates + examples: docs/help/scanners/predefined_scanners.md
  - Stock brackets guide: docs/help/scanners/stock_bracketed_alerts.md
- Packs Help:
  - SwingSigma: docs/help/swingedge/README.md (scan -> signals -> overlay quickstart)
  - Help index: docs/help/README.md (Signals API examples)

## What's Next (TODOs)
- Options Overlay (docs/todos/options_overlay_todos.md):
  - Credit verticals (TP% / loss multiple), put/iron spreads, expirations helper UI/CLI, BS-IV pricing fallback, vega/theta aware mapping.
- Backtests Parity: Entry mode + bracket parity for backtests (stocks first, then options with quotes/BS pricing).
- Data Hygiene: Split heavy dataset flows into sigma_core/data/options_flow.py (no API change).

## Quick Start
- Scan + Signals:
  - make ui
  - make scan-breakout UNIVERSE=AAPL,MSFT,SPY START=2025-08-01 END=2025-08-06
  - Inspect: products/sigma-lab/live_data/universe_eq_swing_daily_breakout_scanner/signals.csv
- Overlay:
  - curl -sS -X POST http://localhost:8001/options_overlay -H 'Content-Type: application/json' -d '{ "model_id": "universe_eq_swing_daily_breakout_scanner", "date": "2025-08-06", "expiry": "2025-08-16", "target_delta": 0.35, "min_oi": 1000 }'
- Expirations:
  - make expirations TICKER=AAPL WEEKS=8
