# Sigma Lab API — Plain-English Endpoint Map

This document lists the public FastAPI routes exposed under `products/sigma-lab/api/routers`, grouped by domain. It summarizes purpose, key parameters, and typical responses. Field names are paraphrased for clarity; see routers for exact schemas.

## Health
- GET `/health`: Liveness/readiness check. Returns `{ ok: true, version?, ... }`.
- GET `/healthz`: Minimal liveness probe.

## Packs
- GET `/packs`: List packs. Returns `{ ok, packs: [...] }`.
- GET `/packs/{pack_id}`: Pack detail. Returns `{ ok, pack }`.
- GET `/packs/{pack_id}/templates`: Model templates available in pack. Returns `{ ok, templates }`.
- GET `/packs/{pack_id}/indicator_sets`: Indicator set definitions for pack. Returns `{ ok, indicator_sets }`.

## Models
- POST `/models`: Create a model scaffold. Params (JSON): `ticker` (e.g., "SPY"), `asset_type` ("opt"|"eq"), `horizon` (e.g., "0dte"), `cadence` (e.g., "hourly"), `algo` (e.g., "gbm"), optional `variant`, `pack_id`, `indicator_set_name`. Returns `{ ok, model_id, paths: { config, policy }, message }`.
- PATCH `/models/{model_id}`: Shallow-merge partial config into existing YAML. Params: `pack_id`, `config` (object). Returns `{ ok, path, config }`.
- GET `/models`: List model configs. Query: `pack_id?`. Returns `{ ok, models: [{ id, pack_id, path }], count }`.
- GET `/model_templates`: List available model templates. Query: `pack?`. Returns `{ ok, templates: [{ pack, template_id, name, horizon, cadence, template_version }] }`.
- POST `/preview_matrix`: Build small matrix sample and run QA checks. Body: `{ model_id, start, end, pack_id?, max_rows? }`. Returns `{ ok, rows, qa: { monotonic_time, non_negative_vol, session_alignment, iv_sanity, nan }, warn, fail }`.

## Datasets
- POST `/build_matrix`: Build a training matrix CSV for a model. Body: `{ model_id, start, end, out_csv?, pack_id?, k_sigma, fixed_bp?, distance_max, dump_raw, raw_out?, ticker? }`. Returns `{ ok, out_csv }`. Also persists a `build_runs` row + `artifacts(kind='matrix')` when DB available.
- POST `/build_stock_matrix`: Build a stock-only matrix. Body: `{ ticker, start, end, out_csv?, pack_id?, model_id?, label_kind? }`. Returns `{ ok, out_csv }`.

## Training
- POST `/train`: Train the model based on config and built matrix. Body includes `model_id`, `pack_id`, ranges, and training options (see router). Returns `{ ok, model_out_uri, metrics, features }`. Persists a `training_runs` row + `artifacts(kind='model')` when DB available.

## Backtest & Leaderboard
- POST `/backtest`: Cross-validated backtest over a matrix CSV. Body: `{ model_id, csv?, target?, thresholds? (list or "0.55,0.60"), splits, embargo, top_pct?, allowed_hours? (list or "13,14"), slippage_bps, size_by_conf, conf_cap, per_hour_thresholds, per_hour_select_by ('sharpe'|'cum_ret'|'trades'), calibration ('none'|'sigmoid'|'isotonic'|null), pack_id?, momentum_gate?, momentum_min?, momentum_column?, save?, tag? }`. Returns `{ ok, result, best_sharpe_hourly, best_cum_ret, parity? }`. When `save=true`, persists a backtest run, folds, and a `plot` artifact.
- GET `/leaderboard`: Ranked backtest runs. Query: `pack_id?`, `model_id?`, `limit=20`, `order_by='sharpe_hourly'`, `offset=0`, `tag?`. Returns `{ ok, rows, limit, offset, next_offset, tag }`.

## Sweeps
- POST `/backtest_sweep`: Grid-search style backtests over variants. Body: `{ model_id, pack_id?, start?, end?, thresholds_variants? ["0.50,0.52"...], allowed_hours_variants? ["13,14,15"...], top_pct_variants? [0.01, ...], splits, embargo, allowed_hours?, save=true, tag='sweep', min_trades=0, min_sharpe? }`. Returns `{ ok, runs: top10_by_sharpe, count, filtered, report_path?, sweep_id? }` and stores `backtest_sweeps` + `sweep_results` when DB available.
- GET `/sweeps`: List sweeps. Query: `pack_id?`, `model_id?`, `tag?`, `status?`, `limit`, `offset`. Returns `{ ok, rows, limit, offset, next_offset }`.
- GET `/sweeps/{sweep_id}`: Sweep detail plus results. Returns `{ ok, sweep, results }`.

## Indicators
- GET `/indicators`: List available indicators from registry. Returns `{ ok, indicators: [...] }`.
- GET `/indicators/status`: System readiness for indicators. Returns `{ ok, status }`.

## Signals & Performance
- GET `/signals`: Signal stream/query (see router for filters). Returns `{ ok, rows }`.
- GET `/signals/summary`: Aggregate signal stats. Returns `{ ok, summary }`.
- GET `/signals/leaderboard`: Signal-level leaderboard. Returns `{ ok, rows }`.
- GET `/models/{model_id}/performance`: Model performance series. Returns `{ ok, series }`.

## Options
- POST `/options_overlay`: Compute options overlays for policy/rendering. Body: symbol and overlay options (see router). Returns `{ ok, overlays }`.
- GET `/option_signals`: Point-in-time option-derived signals. Query defines symbol and window. Returns `{ ok, rows }`.
- GET `/options/expirations`: Available expirations for symbol. Query `{ ticker }`. Returns `{ ok, expirations }`.

## Policy
- GET `/policy/explain`: Human-readable policy expansion for a model. Query: `model_id`, `pack_id?`. Returns `{ ok, policy, notes }`.
- GET `/validate_policy`: Alias of `/policy/explain` for convenience.

## Model Cards
- GET `/model_cards`: List model cards (if available). Returns `{ ok, cards }`.
- GET `/model_card`: Fetch a single model card by id/ref. Returns `{ ok, card }`.

## Calibration
- POST `/calibrate_thresholds`: Fit score-to-probability calibration (e.g., sigmoid/isotonic). Returns `{ ok, params, plot_uri? }`.
- POST `/calibrate_brackets`: Calibrate ATR/time-based brackets for parity stock backtest. Returns `{ ok, params, parity }`.

## Admin (internal)
- Jobs: `GET /jobs`, `POST /jobs/{job_id}/retry`, `POST /jobs/{job_id}/cancel`
- Quotas: `GET /quotas`, `PATCH /quotas`
- Risk Profiles: `GET /risk-profiles`, `PATCH /risk-profiles`
- Packs meta: `GET /packs` (admin view)
- Indicator sets: `GET /indicator_sets` (admin view)
- Templates: `GET /templates`, `POST /templates`, `PATCH /templates/{template_id}`, `POST /templates/{template_id}/publish`
- Flags: `GET /flags`, `PATCH /flags`
- Health: `GET /health` (admin scope)
- Audit: `GET /audit`
- Users: `GET /users`, `PATCH /users/{user_id}`, `POST /users/{user_id}/rotate_token`

Notes
- Some routes have both user-facing and admin duplicates (e.g., leaderboard, audit) to serve different contexts. Prefer the non-admin paths documented above unless you are building admin tooling.
- All list endpoints accept basic pagination (`limit`, `offset`) where shown; values are clamped server-side to safe ranges.

