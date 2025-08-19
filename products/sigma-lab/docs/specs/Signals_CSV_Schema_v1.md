# Signals CSV Schema v1 — Log and Summaries

## Status
Draft — sample schemas for CSV/XLSX files used by Signals Log and Analytics

## signals_log.csv
- Purpose: Raw or normalized log of signals with fills
- Columns (ordered)
  1) ts (ISO8601)
  2) model_id (string)
  3) risk_profile (conservative|balanced|aggressive)
  4) ticker (string)
  5) side (long|short)
  6) entry_ref_px (number)
  7) fill_px (number|empty)
  8) slippage (number|empty)
  9) status (filled|pending|canceled|error)
  10) rr (number|empty)
  11) pnl (number|empty)
  12) tag (string|empty)

- Sample
```
2025-08-16T09:30:00Z,spy_opt_0dte_hourly,balanced,SPY,long,447.35,447.37,0.02,filled,1.8,12.50,live
2025-08-16T10:15:00Z,spy_eq_swing_daily,balanced,SPY,long,447.35,,,,pending,,,
```

## signals_daily_summary.csv (optional)
- Purpose: Pre-aggregated daily metrics for faster charts
- Columns
  - date (YYYY-MM-DD)
  - model_id (string)
  - risk_profile (string)
  - trades (int)
  - wins (int)
  - losses (int)
  - win_rate (float)
  - cum_return (float)
  - sharpe (float)
  - sortino (float)
  - fill_rate (float)
  - avg_slippage (float)

- Sample
```
2025-08-16,spy_opt_0dte_hourly,balanced,12,7,5,0.58,0.021,1.12,1.35,0.87,0.03
```

## Notes
- Missing fields: use empty string for CSV; N/A in UI.
- Cost-adjustments should be applied before writing summary metrics.
- For XLSX, sheet names: `log`, `daily_summary`.
