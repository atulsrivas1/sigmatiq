# Packs Roadmap

This roadmap tracks pack-scoped work: default indicator sets, dataset/labels, and E2E readiness.

## ZeroEdge (0DTE, options-only)
- Status: baseline indicator set in `products/edge-lab/packs/zeroedge/indicator_sets/zeroedge_default.yaml`.
- Next:
  - Options PCR (`pcr_volume`, `pcr_oi`), `oi_change_1d`, `oi_trend` from Polygon snapshots.
  - IV ranks: `iv_rank_52w`, `iv_percentile_52w`, `atm_iv_zscore` (requires daily ATM IV store).
  - Smile proxy: `iv_smile_wings` from quotes-based IV around ATM.
  - Import idea sets: `zeroedge_opening_drive`, `zeroedge_gamma_unwind`, `zeroedge_headfake_reversal_v1`, `zeroedge_pin_drift_v1`, `zeroedge_pin_drift_v2`.
  - Status: imported
    - `zeroedge_headfake_reversal_v1` → `products/edge-lab/packs/zeroedge/indicator_sets/zeroedge_headfake_reversal_v1.yaml`
    - `zeroedge_pin_drift_v1` → `products/edge-lab/packs/zeroedge/indicator_sets/zeroedge_pin_drift_v1.yaml`
    - `zeroedge_pin_drift_v2` → `products/edge-lab/packs/zeroedge/indicator_sets/zeroedge_pin_drift_v2.yaml`

## SwingEdge (equities/options)
- Status: default sets added for eq/opt; stock pipeline helper present.
- Next:
  - Labels: 5–20 day `fwd_ret` (eq), and options variants (delta-hedged or timing via underlying).^ 
  - Regime: VIX level/Δ and term slope.
  - Import idea sets: breakout/meanrevert (eq/opt) and address missing indicators via alias mapping/backlog.

## LongEdge (equities/options)
- Status: default sets added for eq/opt.
- Next:
  - Indicators: LR R² (`lr_r2`), Ulcer Index (optional), longer-term IV term structure.
  - Labels: 63–252 day returns; calibrate backtests for slower cadence.

## OvernightEdge (equities/options)
- Status: default sets added for eq/opt.
- Next:
  - Intraday-derived signals: `rsi_last_hour`, `returns_last_30m`, `close_vs_vwap`, `day_range_pos`, `vol_zscore`.
  - Options EOD: `atm_iv_eod`, `div_eod`, `pcr_eod`, `oi_change_1d`.
  - Labels: `fwd_ret_close_to_open`.

## MomentumEdge (equities/options)
- Status: default sets added for eq/opt (vol-scaled momentum ladder).
- Next:
  - Add volatility scaling helper; ADX gate wiring; options bias filters (IV–RV, ATM IV z-score).

## Shared Tasks
- Indicator alias mapping for idea sets: returns→ret, stddev→rolling_std, bollinger→bollinger_bands, iv_skew_25d_rr→iv_skew_25d.
- VIX adapter via Polygon indices; common regime features.
- `/preview_matrix` NaN diagnostics for IV- and flow-dependent features.

^ Options labeling approach will be toggled via per-model config: timing via underlying vs option-level P&L proxy.
