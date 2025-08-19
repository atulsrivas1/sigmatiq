# Predefined Scanner Templates (Roadmap)

These scanner templates mirror common discretionary playbooks. Each lists its feature set and gating ideas. We ship the indicator sets now; gates/weights can be calibrated later.

- ID: `swing_eq_breakout_scanner` (exists)
  - Edge: donchian/band breakout + momentum + trend quality
  - Indicators: EMA 20/50, RSI 14, ADX 14, Momentum 20/63, LR_R2 126, Bollinger 20/2, StdDev 20, ATR 14, OBV, CMF 20, Donchian 20
  - Gates (example): close > upper band or > donchian high * (1 + epsilon); RSI >= 55; ADX >= 18

- ID: `swing_eq_meanrevert_scanner`
  - Edge: pullback to value with oversold confirmation
  - Indicators: SMA 20/50, RSI 14, Bollinger 20/2, Keltner 20/1.5, CMF 20, ATR 14
  - Gates: close < lower band and RSI <= 35; prefer CMF >= 0 (no heavy outflows)

- ID: `swing_eq_trend_follow_scanner`
  - Edge: sustained trend and alignment; buy dips above trend
  - Indicators: EMA 20/50/100, ADX 14, Aroon 25, LR_R2 126, Momentum 63, ATR 14
  - Gates: EMA20 > EMA50 > EMA100; ADX >= 20; Aroon up > down; positive momentum

- ID: `swing_eq_vol_contraction_scanner`
  - Edge: squeeze and expansion potential
  - Indicators: Bollinger 20/2, Keltner 20/1.5, Rolling Std 20, OBV, CMF 20
  - Gates: BB width < Keltner width * x; recent rising OBV; breakout watch
  - Example: `make scan-squeeze UNIVERSE=SHOP,ROKU,SE START=YYYY-MM-DD END=YYYY-MM-DD`

- ID: `swing_eq_rel_strength_scanner`
  - Edge: RS + momentum leadership
  - Indicators: Momentum 20/63, EMA 20/50, RSI 14, LR_R2 126, CMF 20
  - Gates: rank by composite RS (momo/r2), confirm EMA20 > EMA50 and RSI >= 55

- ID: `swing_eq_high_momentum_scanner`
  - Edge: pure momentum burst with trend filter
  - Indicators: Momentum 10/20/63, EMA 20/50, ADX 14, ATR 14
  - Gates: momentum ranks top decile; ADX >= 20; above EMA20

How to use
- Each template has a matching indicator set YAML under `products/edge-lab/packs/swingedge/indicator_sets/`.
- Create a logical model via `POST /models` or `scripts/create_model.py` (set labels.kind: none).
- Run scans via Make targets or the `/scan` endpoint.

Calibration & policy
- Use `/calibrate_thresholds` to target Topâ€‘N or a score threshold per template.
- Policy gating (cooldown, max trades/day, size_by_conf) via per-scanner policy YAML.

