# Signals API Spec v1 — Live Leaderboard, Log, Analytics

## Status
Draft — extends BTB surfaces with live performance APIs

## Types (abbreviated)
```jsonc
SignalRow: {
  ts: string,
  model_id: string,
  risk_profile: "conservative"|"balanced"|"aggressive",
  side: "long"|"short",
  entry_ref_px: number,
  fill_px?: number,
  slippage?: number,
  status: "filled"|"pending"|"canceled"|"error",
  rr?: number,
  pnl?: number,
  tag?: string
}

LiveMetrics: {
  sharpe?: number,
  sortino?: number,
  cum_return?: number,
  win_rate?: number,
  trades?: number,
  fill_rate?: number,
  avg_slippage?: number,
  capacity?: "Low"|"Medium"|"High",
  coverage_pct?: number,
  freshness_sec?: number
}

LeaderboardRow: {
  model_id: string,
  risk_profile: string,
  period: { start: string, end: string },
  metrics: LiveMetrics,
  lineage: { matrix_sha?: string, config_sha?: string, policy_sha?: string, risk_sha?: string }
}
```

## Endpoints

### GET `/signals`
- Query: `model_id?`, `start?`, `end?`, `status?`, `limit?`, `offset?`
- Resp: `{ rows: SignalRow[], total: number }`

### GET `/signals/summary`
- Query: `model_id`, `risk_profile?`, `start`, `end`
- Resp: `{ model_id, risk_profile, period: {start,end}, metrics: LiveMetrics }`

### GET `/signals/leaderboard`
- Query: `pack?`, `risk_profile?`, `start`, `end`, `limit?`, `offset?`
- Resp: `{ rows: LeaderboardRow[], total: number }`

### GET `/models/:id/performance`
- Query: `start`, `end`
- Resp: `{ live: { period, metrics: LiveMetrics }, backtest?: { started_at, metrics: {...} } }`

## Notes
- All metrics are cost-adjusted (commission + slippage) where applicable.
- Include `coverage_pct` and `freshness_sec` for transparency on live data quality.
- Lineage is included when available to aid comparisons and debugging.
- Metric definitions and display rules follow `specs/Signals_Metrics_v1.md`.

## Errors & Limits
- Follows Error Catalog v1; paginate with `limit<=200`.
