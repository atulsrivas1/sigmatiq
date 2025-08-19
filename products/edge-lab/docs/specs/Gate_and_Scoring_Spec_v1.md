# Gate & Scoring Spec v1

## Status
Draft — complements ADR 0005

## Purpose
Define pass/fail gate logic (hard guards) and ranking scores (post‑gate) per pack to drive the leaderboard and training eligibility.

## Gate (pass/fail)
- Inputs: backtest metrics (Sharpe, Sortino, return, max_dd, trades, win_rate), parity/capacity checks (spread, OI, volume, fill), and profile `risk_budget`.
- Output: `{ pass: boolean, reasons: string[] }`.
- Examples of reasons: `min_trades_not_met`, `max_dd_exceeded`, `es95_exceeded`, `spread_above_limit`, `oi_below_min`, `fill_rate_below_min`.

Pack defaults (profile‑aware)
- ZeroEdge/Overlay: trades≥min, max_dd≤budget, ES95 within budget, spread≤limit, OI/volume≥min, fill_rate≥min.
- Swing/Momentum: trades/year≥min, max_dd≤budget, cost‑adjusted metrics computed, capacity vs ADV≤limit, turnover≤cap.
- LongEdge: sample length≥min, max_dd≤budget, Calmar≥min.

## Ranking (post‑gate)
- ZeroEdge/Overlay: `score = sortino * sqrt(trades/100) - 0.5*max_dd - 0.2*std_sharpe_folds`.
- Swing/Momentum: `score = sharpe_cost_adj * sqrt(trades/N) - λ_turnover - 0.3*max_dd`.
- LongEdge: `score = calmar`, tie by sortino then CAGR.

Notes
- All metrics cost‑adjusted where applicable (slippage/fees model).
- Fold instability penalty uses std across walk‑forward or k‑fold splits.
- Ties resolved by return, win_rate, then capacity index.

## UI Signals
- Gate Badges: green/red chips with tooltip (reason codes → short human text).
- "Pass Gate only" filter hides failing rows.
- Compare modal includes budget usage bars (e.g., 70% of MaxDD budget).

## Normalization / Caching Key
`(model_id, matrix_sha, config.kind, config.value, config.allowed_hours, config.splits, tag, risk_profile)`.

## Rationale
- Hard gates eliminate unstable/unfillable configs and prevent wasted training runs.
- Ranking favors robust, risk‑adjusted returns and sample size, penalizing tail risk and instability.

