# Priority Matrix & Phased Plan — Single Indicator

Axes
- Priority: user value, breadth of applicability, revenue impact
- Complexity: data availability, compute cost, UX effort

Phase 1 (Foundations)
- RSI Threshold screen (High, Low)
- MACD Cross alerts (High, Medium)
- VWAP Deviation (High, High) — intraday MVP
- Registry + Validation + Caching (infra)

Phase 2 (Volatility/Trend)
- ATR Expansion (Medium, Low)
- Bollinger Touch (Medium, Medium)
- Donchian Break (Medium, Medium)
- Supertrend Flip (Medium, Medium)

Phase 3 (Options/Regime)
- Volume Z-Score (Medium, Low)
- IV Rank Extreme (Medium, Medium)
- VIX Level Gate (Medium, Low)
- Distance to EMA (Medium, Low)

Decision Gates
- P95 screen latency ≤ 800 ms for U=200
- Cache hit-rate ≥ 70% on repeated screens
- QA fails = 0 in last 7 days
