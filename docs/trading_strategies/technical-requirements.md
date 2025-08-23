# Technical Requirements — Strategy Engine

Scope
- End-to-end lifecycle: define, backtest, optimize, deploy, monitor. Strategies consume indicator sets and policies.

Rules & Signals
- Rules DSL or config: entry, exit, filters, time windows; support ML scores as signals.
- Signal debouncing and hysteresis to limit churn.

Position Sizing
- Modes: fixed fractional, fixed risk (ATR stop distance), volatility targeting, cap by heat.
- Per-asset constraints: min lot size, notional caps, leverage.

Risk & Compliance
- Drawdown guards (per-position/strategy), daily loss limits, max concurrent positions.
- Blackouts (earnings/events), liquidity floors, market hours, short/long rules.

Execution
- Order types: market, limit, stop, bracket OCO; time-in-force.
- Slippage model: bps or function of spread/volume; partial fills handling.
- Broker adapters; dry-run for paper trading.

Backtesting
- CV folds and embargo; walk-forward analysis; parameter sweeps.
- TX cost model; borrow fees for shorts; corporate action adjustments.
- Metrics: Sharpe, Sortino, max drawdown, hit rate, profit factor, turnover.

Optimization
- Grid/random/Bayesian over thresholds/weights/sizing params; constraints to avoid overfit.
- Train/validation/test splits; report parity to live.

Lineage & Audit
- Store strategy config JSON + SHA, policy version, indicator-set version, git sha, data ranges.
- Persist trades, orders, fills with timestamps and IDs.

APIs
- See `strategy-api-spec.md` for CRUD, backtest, walk-forward, optimize, deploy, monitor.

