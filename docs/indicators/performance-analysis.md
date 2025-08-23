# Performance Analysis — Single Indicator

Cost Drivers
- CPU: windowed ops O(N); multi-output constant factor per indicator.
- IO: market data fetch; dominates cold path.
- Memory: rolling buffers; minimize copies.

Use Case Notes (selected)
- RSI Threshold: cheap rolling calc; cache last state; screening U≤200 fits <1s.
- MACD Cross: two EMAs + signal EMA; incremental update is fast; avoid full recompute.
- ATR Expansion: rolling true range; hourly/daily allows batching.
- VWAP Deviation: intraday cumulative sums; maintain session state to hit <100ms.
- Volume Z-Score: rolling mean/std; cheap; IO-bound on large universes.
- IV Rank: percentile over 252d; batch nightly; store rank to avoid recompute.

Optimizations
- Incremental updates; reuse rolling windows.
- Cache by (id, params, symbol, timeframe); return last-window when possible.
- Batch fetch data for universe screens; columnar payloads.
- Vectorization and optional numba on hot paths.

Guardrails
- Universe caps per request (e.g., 200 symbols) and rate limits.
- P95 latency SLOs per indicator class (intraday vs daily).
