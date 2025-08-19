# Custom Scanners — How-To

This guide shows how to create, preview, and run a custom equity scanner in Sigmatiq Sigma. Scanners are “signal jobs” that produce ranked picks without training an ML model. They use the same pack structure, naming, and policy validation as models.

## Prerequisites
- Start API: `python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`
- Polygon API key loaded in `products/sigma-lab/.env`
- A target pack (e.g., `swingedge`)

## Scanner = Indicator Set + Logical Model + Policy
- Indicator set: defines features to compute for each ticker
- Logical model: a config file for bookkeeping (ids/paths) with `labels: { kind: none }`
- Policy: risk/execution/alerting; validated by `/validate_policy`

## Create Steps (API-first)
1) Create/update indicator set
- Endpoint: `POST /indicator_sets`
- Body example:
```
{
  "pack_id": "swingedge",
  "scope": "pack",
  "name": "my_eq_breakout_scanner",
  "indicators": [
    { "name": "ema", "window": 20 },
    { "name": "ema", "window": 50 },
    { "name": "rsi", "period": 14 },
    { "name": "donchian", "window": 20 },
    { "name": "lr_r2", "window": 126 }
  ]
}
```
- Writes: `products/sigma-lab/packs/swingedge/indicator_sets/my_eq_breakout_scanner.yaml`

2) Create logical “scanner model”
- Endpoint: `POST /models`
- Body example:
```
{
  "pack_id": "swingedge",
  "ticker": "universe",
  "asset_type": "eq",
  "horizon": "swing",
  "cadence": "daily",
  "algo": "scanner",
  "indicator_set": "my_eq_breakout_scanner"
}
```
- Edit the file at `products/sigma-lab/packs/swingedge/model_configs/<generated>.yaml` to ensure:
```
labels:
  kind: none
```
- Copy/update policy: `products/sigma-lab/packs/swingedge/policy_templates/<generated>.yaml`. Validate:
  - `GET /validate_policy?model_id=<generated>&pack_id=swingedge`

3) Preview (quick sanity)
- Equities path: `make preview-stock PACK_ID=swingedge MODEL_ID=<generated> START=YYYY-MM-DD END=YYYY-MM-DD`
- Check `products/sigma-lab/reports/preview_stock_<model>.json` for NaN stats

4) Run scan
- CLI: `make scan PACK_ID=swingedge MODEL_ID=<generated> UNIVERSE=AAPL,MSFT,SPY START=YYYY-MM-DD END=YYYY-MM-DD`
- Or: `make scan PACK_ID=swingedge MODEL_ID=<generated> UNIVERSE_CSV=path/to/universe.csv START=... END=...`
- API: `make scan-api ...` (same params via `/scan`)
- Output: `products/sigma-lab/live_data/<model_id>/signals.csv`

## Universe Options
- `--tickers AAPL,MSFT,SPY` or `--universe_csv path/to/universe.csv` with a `ticker` column
- See `products/sigma-lab/api/scripts/universe_resolver.py` (if present) to filter/print ticker lists
- Named universes (sp500, sp100) — tracked in `products/sigma-lab/docs/BACKLOG.md`

## Calibration (optional)
- Count-based threshold fit:
```
curl -sS -X POST localhost:8001/calibrate_thresholds \
 -H 'Content-Type: application/json' \
 -d '{"model_id":"<model>","pack_id":"swingedge","top_n":50,"grid":"0.5,0.55,0.6,0.65"}'
```
- Returns a recommended threshold for `score_total` that yields ~Top‑N names

## Reference Guides
- Breakout+Momentum: see `products/sigma-lab/packs/swingedge/indicator_sets/swing_eq_breakout_scanner.yaml` for the current feature set and use the Scanners how-to above.

## Tips
- Reuse `products/sigma-lab/packs/swingedge/indicator_sets/swing_eq_breakout_scanner.yaml` as a template
- Keep `model_id` naming consistent: `<ticker>_<asset>_<horizon>_<cadence>_scanner`
- For large universes, prefer CSV and consider batching later

## Troubleshooting
- `/healthz` fails: verify Polygon key, DB, and bars coverage
- Missing columns/NaNs: check your indicator set and preview report; tighten the date range
- Policy errors: use `/validate_policy` and ensure required sections exist
