# Technical Requirements — Smart Combination Engine

Scope
- Engine to compose multi-indicator sets with redundancy/conflict checks, multi-timeframe alignment, and compute reuse.

Core Functions
- Validate set definition (schema, params, timeframes, aliases).
- Detect redundancy/conflicts and emit warnings with suggested fixes.
- Build compute plan (DAG) across components and symbols; reuse cached results.
- Evaluate rules (boolean/threshold/weighted) to produce signals/scores.
- Support streaming updates with throttling and dedup.

Redundancy/Conflict Detection
- Redundant: overlapping oscillators (RSI/Stoch/Williams %R), duplicate EMA/SMA windows, MACD+PPO duplicates.
- Conflicts: momentum + mean reversion at same TF without gating; multiple opposing signals at equal weight.
- Heuristics + registry metadata guide suggestions; allow override.

Multi-Timeframe Alignment
- Explicit component `timeframe`; align to evaluation clock via resampling utilities.
- Window boundaries and session handling must be deterministic; QA includes alignment checks.

Weights & Scoring
- Normalize weights; compute composite score (0–100) from component states.
- Optional hysteresis/debounce for state changes to reduce churn.

Optimization
- Parameter bounds per component; grid/random/Bayesian optimization via backtest endpoint; persist best as variant.

APIs
- See `set-api-spec.md` for CRUD/evaluate/backtest/subscribe/validate/optimize.

Performance
- Shared cache across sets; micro-batching for universe; vectorized operations; incremental updates.
- Partition streaming by symbol and timeframe; apply backpressure.

Lineage
- Store resolved set JSON + SHA and component versions/timeframes; attach to artifacts and run history.

