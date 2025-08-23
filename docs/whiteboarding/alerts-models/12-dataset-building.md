# Dataset Building — Cohort‑First, Reproducible

Goals
- Cohort models (preset universes) by timeframe/market; per‑ticker only when justified (e.g., SPY 0DTE).
- Reproducible via `training_cfg` on `sc.model_specs`; parity with serving features.
- No leakage; time‑aware splits; safe defaults for novices.

Inputs
- Universe: presets/watchlists; caps + liquidity filters (min dollar volume).
- Bars: Polygon loaders with file cache; never cache “today”. Prefer adjusted=true for daily (record choice in `training_cfg`).
- Features: FeatureBuilder over indicator sets/strategies; add ATR, regime flags, session context.

Labels
- Stock path: TP‑before‑SL within `max_hold_bars`; outcome `tp_hit|sl_hit|max_hold`; realized return.
- Options proxy (optional): ATM estimate with `dte_min`, `delta`; conservative guardrails.

Splits & Calibration
- Forward‑chaining CV grouped by symbol; record `fold` and `cv` in `training_cfg`.
- Calibrate thresholds to alert budgets and precision@K; store calibration alongside artifacts.

Storage & Lineage
- Write Parquet partitioned by timeframe/date; tz‑aware timestamps.
- Compute dataset and feature hashes; insert `sc.model_training_runs` with cfg snapshot, hashes, metrics, git_sha.

Training Config (`training_cfg`) Example
```
{
  "data_window": { "start": "2023-01-01", "end": "2024-08-01" },
  "session": { "hours": "RTH", "timezone": "US/Eastern" },
  "cv": { "method": "rolling", "folds": 5, "gap_bars": 5 },
  "filters": {
    "weekdays": [1,2,3,4,5],
    "time": "09:30-16:00",
    "exclude_dates": [],
    "min_dollar_vol": 1000000
  },
  "cohort_filter": { "presets": ["sp500"] },
  "adjusted_daily": true
}
```

Critic Notes
- Prefer adjusted daily bars; if not, document splits/dividends risk.
- Keep universes capped for intraday datasets; avoid event days if needed.
- Drop last H rows to prevent label leakage; record `gap_bars` when used.
