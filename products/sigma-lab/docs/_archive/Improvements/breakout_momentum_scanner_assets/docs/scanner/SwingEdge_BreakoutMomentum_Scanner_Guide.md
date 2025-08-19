
# SwingSigma — Breakout & Momentum Scanner (Implementation Guide)
*Generated: 2025-08-15 04:10 UTC*

This document specifies a **programmatic scanner** that finds tickers breaking out **with momentum** on daily bars. It plugs directly into your **Sigmatiq Sigma Core** pipeline and **Sigma Packs** structure, and can be run from the CLI or a cron. The same indicator set can be used for training a SwingSigma model later.

- Platform pipeline: Sigma Core `define → build dataset → train → backtest → policy → deploy → live alerts`. fileciteturn0file0  
- Strategy packaging: ship the scanner as a **pack indicator set** under `swingedge`; reproducible, versioned. fileciteturn0file1  
- UI flow: the **Custom Model Builder** already reads indicator sets, writes per‑model overrides, and can run a **Preview** build before a full job. fileciteturn0file2

---

## 0) Scope & prerequisites

- **Universe**: symbols with `price ≥ $5` and `ADV_20 ≥ 500k–1M`. (Optionable subset if trading via options overlay.)
- **Data**: daily OHLCV; indicators from your **registry** (RSI/EMA/returns/ATR/ADX/OBV/CMF/Bollinger, etc.) are already implemented. fileciteturn0file5
- **Outputs**: CSV (and optional DB table) with ranked candidates and diagnostics per day.
- **No look‑ahead**: rolling highs/lows must exclude the current bar used for the decision.

---

## 1) Signals (definitions)

### Breakout (choose one or combine)

**Donchian breakout (N):** close today above the *max high of the prior N sessions* by a small buffer `ε`:
[ Donchian_N = 1{ Close_t > max(High_{t-1..t-N}) * (1+ε) } ]

**ATR‑normalized strength (BoS):**
[ BoS_N = (Close_t - max(High_{t-1..t-N})) / ATR_14,t ]

Use `N ∈ {20, 55}`, `ε ∈ [0.001, 0.003]`, `BoS_20 ≥ 0.25` as a starting gate.

**Squeeze → Breakout (optional):** Bollinger bandwidth in bottom 30% of 252‑day history, then Donchian trigger. (Reduces whipsaws.)

### Momentum (filters)

- Absolute momentum ladder: `RET_5 > 0`, `RET_20 > 0`, `RET_63 > 0` (or z‑scored).  
- Trend quality: `ADX_14 ≥ 20` and/or `LR_R2_126 ≥ 0.3`.  
- Trend alignment: `Close > EMA20 > EMA50`.  
- RSI regime: `RSI_14 ≥ 55–60` (avoid too‑extended unless aiming for continuation).

### Volume confirmation (optional)
- `Volume_today ≥ 1.5 × ADV_20`, or **CMF_20 > 0**, or rising **OBV**.

All ingredients are in your **built‑in indicator families**, surfaced in `/indicators` and consumable via pack indicator sets. fileciteturn0file5 fileciteturn0file2

---

## 2) Composite ranking score

Compute a 0–100 **BreakoutMomentumScore** per ticker:

```
BreakoutScore   = clip01( BoS_20 / 0.50 ) * 40         # 0–40
MomentumScore   = clip01( 0.5*z(RET_20) + 0.5*z(RET_63) ) * 30
TrendQuality    = clip01( (ADX_14 - 20) / 15 ) * 15     # 0 at 20, full at 35
AlignmentScore  = 15 if (Close>EMA20>EMA50) else 0
Total           = BreakoutScore + MomentumScore + TrendQuality + AlignmentScore
```

Apply **hard gates** (e.g., `Donchian_20` or `BoS_20 ≥ 0.25`, `ADX_14 ≥ 18`, `RSI_14 ≥ 55`) and **rank** by `Total`.

---

## 3) Pack assets (drop-in files)

A pack‑level indicator set is provided (download below) that computes the necessary features. The UI can reference it directly, or you can run a CLI scanner.

- Indicator set YAML: `packs/swingedge/indicator_sets/swing_eq_breakout_scanner.yaml` (included). fileciteturn0file1  
- The Model Builder wizard will present these indicators in Step 3; it can save per‑model overrides and run a **Preview** build. fileciteturn0file2

---

## 4) Running the scanner

### Option A — Via API (loop tickers)

1. For each ticker in the universe, call `POST /build_matrix` (daily cadence) using the indicator set `swing_eq_breakout_scanner`.  
2. On the **latest date**, compute gates and the composite score; keep rows passing gates.  
3. Write the top **N** by `Total` to CSV/DB.

This uses your standard pipeline and artifacts. fileciteturn0file0

### Option B — CLI helper (provided skeleton)

Use `scripts/scanner_breakout_momentum.py` (included) to:
- Load a universe (CSV or DB).  
- Build features via your dataset builder or API.  
- Score, gate, and rank.  
- Write `scans/breakout_momentum/YYYY-MM-DD.csv`.

---

## 5) Example thresholds & weights (config)

`scanner_config.json` (included) lets you change `N`, `ε`, gates, and score weights without editing code.

```json
{
  "donchian_N": 20,
  "epsilon": 0.002,
  "bos_min": 0.25,
  "rsi_min": 55,
  "adx_min": 18,
  "top_n": 50,
  "weights": {
    "breakout": 40,
    "momentum": 30,
    "trend_quality": 15,
    "alignment": 15
  }
}
```

---

## 6) Turning a scan into a model (optional)

If you want to **train** with these features (e.g., predict `fwd_ret_10d`):  
- Use the same indicator set; set labels in the model config.  
- Name the model with your auto-naming convention (`<ticker>_<asset>_<horizon>_<cadence>[_<algo>|_<variant>]`). fileciteturn0file3  
- Provide a policy file; `/validate_policy` must pass before backtests. fileciteturn0file4

---

## 7) Best practices

- **No look‑ahead**: rolling highs/lows must exclude today.  
- **Universe hygiene**: avoid penny/illiquid; reconstitute monthly.  
- **Earnings proximity**: optional filter ±3 trading days.  
- **Regime**: add VIX percentile gates if needed.  
- **Reproducibility**: keep configs & outputs versioned via packs and store scan results next to model artifacts. fileciteturn0file1

---

## 8) Files included (download links below)

- `packs/swingedge/indicator_sets/swing_eq_breakout_scanner.yaml` — indicator set used by both the scanner and SwingSigma training.  
- `scripts/scanner_breakout_momentum.py` — CLI skeleton (API or local builder).  
- `scanner_config.json` — tunable thresholds/weights.  
- Output path suggestion: `scans/breakout_momentum/YYYY-MM-DD.csv`.

---

## 9) Appendix: Indicator list (scanner set)

- Trend & momentum: `EMA(20/50)`, `RSI(14)`, `RET(5/20/63)`, `LR_R2(126)`.  
- Volatility & breakout helpers: `ATR(14)`, `STDDEV(20)`, `Bollinger(20, 2.0)`.  
- Volume confirmation: `OBV`, `CMF(20)`.

These indicators come from your existing registry and are discoverable in the UI’s grouped indicator catalog. fileciteturn0file2 fileciteturn0file5

---

**End of guide**
