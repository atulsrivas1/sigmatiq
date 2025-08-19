
# SwingSigma — Breakout & Momentum Scanner (Implementation Guide)
*Generated: 2025-08-15 20:56 UTC*

**Signals**
- **Donchian breakout (N):** `Close_t > max(High_{t-1..t-N}) * (1+ε)`
- **ATR‑normalized strength:** `BoS_N = (Close_t − max(High_{t-1..t-N})) / ATR_14`
- **Momentum filters:** RET(5/20/63) > 0, ADX(14) ≥ 20, Close > EMA20 > EMA50, RSI(14) ≥ 55
- **Volume confirms:** Volume ≥ 1.5×ADV_20, CMF(20) > 0, OBV rising

**Composite score (0–100)**
```
BreakoutScore = clip01(BoS_20/0.50)*40
MomentumScore = clip01(0.5*z(RET_20)+0.5*z(RET_63))*30
TrendQuality  = clip01((ADX_14-20)/15)*15
Alignment     = 15 if Close>EMA20>EMA50 else 0
Total         = sum(...)
```

**Gates**: BoS_20 ≥ 0.25 or Donchian_20, ADX_14 ≥ 18, RSI_14 ≥ 55; price ≥ $5; ADV_20 ≥ 500k.  
**Outputs**: ranked CSV Top‑N per day; optional DB table.

**Run**
- API: loop universe → `/build_matrix` (daily) using indicator set, then score & rank
- CLI: see `scripts/scanner_breakout_momentum.py`
