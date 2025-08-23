# Interaction Transcript — Engineers A & B (Single Indicator Focus)

Context: Engineers conduct the indicators exercise with the constraint that each use case must involve exactly one indicator. Combinations/sets are deferred.

Round 1 — Presentations

Engineer A
- Proposes top single-indicator screens: RSI threshold, MACD cross, ATR expansion, VWAP deviation, IV rank extremes.
- Rationale: High familiarity, clear thresholds, broad applicability, fast to compute.

Engineer B
- Proposes: Bollinger band touch, Donchian break, Supertrend flip, Volume z-score spike, VIX level gate.
- Rationale: Captures distinct trading intents (mean reversion, trend, volatility, risk gating) without mixing indicators.

Round 2 — Clarifying Questions
- A → B: “For Supertrend, are we ok with single indicator despite its internal ATR dependency?”
  - B: “Yes. Internal math is fine; from the user’s perspective it’s one indicator.”
- B → A: “VWAP deviation: session handling edge cases?”
  - A: “Reset at session open, guard against partial first bar and halts; we’ll QA session flags.”

Round 3 — Critiques
- A on B: “Donchian/BB_TOUCH can be noisy in chop; need debounce.”
  - B: “Agree; but we stay ‘single indicator’. Debounce belongs to alert policy, not indicator.”
- B on A: “MACD cross lags; communicating lag risk?”
  - A: “We’ll surface ‘lagging’ tag in registry metadata and show recent delay stats.”

Round 4 — Roleplay Challenges
- Skeptical CTO: “Prove U=200 screen ≤ 800ms.”
  - A: “Batch fetch, cached last-window states; RSI/MACD/BB are vectorized; show P95 dashboards.”
- Demanding Trader: “Bloomberg feels instant.”
  - B: “We’ll stream incremental updates with throttle; first paint under 1s, then live.”
- Compliance: “Audit?”
  - A: “Persist indicator id/version/params, timeframe, and git sha alongside results.”
- DevOps: “Noisy neighbors?”
  - B: “Per-user quotas, universe caps, and WS backpressure.”

Round 5 — Convergence
- Agreement on Phase 1: RSI, MACD, VWAP as MVP; Bollinger and IV Rank follow.
- Guardrails: Debounce at alert layer; QA checks mandatory; publish metadata tags (lagging/vol-sensitive/live-safe).

Action Items
- Define registry entries with params schema and metadata flags.
- Implement `/indicators/compute`, `/screen` (single condition), and `/ws/indicators` subscriptions.
- Ship dashboards for latency and cache hit rate.

