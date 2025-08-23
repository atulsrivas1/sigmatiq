# Performance Analysis — Indicator Sets

Cost Drivers
- Compute duplication across components and symbols; mitigate via cache reuse.
- Multi-timeframe resampling/alignment overhead.
- IV data access for options-related sets.

Use Case Notes
- Momentum Breakout + Volume: Donchian + MACD + volume metrics are cheap; IO dominates on cold path. Cache EMA states.
- Mean Reversion Bands + Osc: Rolling mean/std + RSI/Stoch are inexpensive; debounce alerts to reduce churn.
- Multi-TF Trend: Requires daily + hourly fetch; align once and cache. Avoid re-resampling.
- 0DTE Gate: Session-aware and composite; heavier, but components are individually cheap. Throttle to 1–5s.
- Options Premium Selector: IV rank/term slope/ATM z require EOD/near-RT IV; schedule refreshes and limit universes.

Optimizations
- Build a cross-set compute plan; deduplicate identical indicator requests.
- Maintain rolling state per symbol/timeframe; incremental updates only.
- Batch universe fetches; columnar payloads; pre-materialize hot features.

Guardrails
- Universe and frequency caps; quotas per user; WS backpressure.
- SLA targets: P95 evaluate ≤ 1s for U=200 on common sets; batch for heavy IV sets.

