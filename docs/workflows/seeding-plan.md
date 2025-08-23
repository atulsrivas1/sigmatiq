# Seeding Plan — Workflows Library

Phase 1 (Beginner)
- Find Oversold Stocks (RSI)
- Find Breakouts with Volume (uses set: momentum_breakout_v1)
- Gate 0DTE Entries (uses set: zerosigma_0dte_gate)
- Quick Backtest (pack model pipeline)

Phase 2 (Day Trader)
- Intraday VWAP Deviations
- Breakout Pullback Entries
- Gap Fade Setup

Phase 3 (Swing/PM/Options)
- Trend Following Check (SMA200)
- Mean Reversion Bands Finder (BB)
- IV Rank Candidates, Options Wheel, Iron Condor Planner

Sources
- Reuse content from `docs/indicators`, `docs/indicator_sets`, `docs/trading_strategies`.
- Convert to plain‑language steps with concrete example API bodies.

Deliverable
- Draft 8–12 JSON workflows in `docs/workflows/examples/` for review, then promote to `published`.

