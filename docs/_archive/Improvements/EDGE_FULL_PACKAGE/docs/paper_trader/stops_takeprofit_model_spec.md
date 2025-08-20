
# Stop‑Loss & Take‑Profit Model — Specification
*Generated: 2025-08-15 20:56 UTC*

## Rule‑based (default)
- **ATR multiples**: stop = entry − 1.2×ATR(14); target = entry + 2.0×ATR(14) (tunable).  
- **Time stop**: flatten after Δt if neither bracket hits.  
- **Volatility regime**: widen/narrow k based on volatility percentile.

**Policy YAML**
```yaml
policy:
  execution:
    brackets:
      enabled: true
      mode: atr          # atr|range
      atr_mult_stop: 1.2
      atr_mult_target: 2.0
      time_stop_minutes: 120
```

## ML‑based (optional)
- Predict quantiles of forward **max drawdown** and **max run‑up** over horizon H (e.g., 10d).  
- Derive brackets: `stop = entry − Qdd(α)`, `target = entry + Qru(β)`; calibrate α,β on a recent window.

## Features
ATR, stddev(20), gap/range z‑scores, EMA(20/50), ADX(14), RSI(14), LR_R2(126), ADV_20, spreads (if available).

## Backtest alignment
Backtests must simulate the same **fill model** and **bracket logic** as Paper (parity mode).
