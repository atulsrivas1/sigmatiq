# Performance Analysis — Strategies

Backtesting Costs
- Vectorized vs event-driven: vectorized faster for simple rules; event-driven needed for order/fill logic.
- Complexity drivers: universe size, bar frequency, parameter grid size, TX cost models.
- Parallelism: per-fold, per-parameter, per-symbol; beware shared-state contention.

Live Execution Costs
- Signal evaluation latency (depends on indicator sets) + policy checks + order routing.
- Broker latencies and throttling; rate limits per venue.

Optimizations
- Cache and reuse indicator-set outputs across runs.
- Pre-materialize features and session flags.
- Efficient portfolio-level updates (incremental PnL, exposure tracking).

SLOs
- Backtest: p95 per-run under 5 min for standard horizons/universe.
- Live: p95 signal-to-order under 300 ms for intraday strategies within venue constraints.

