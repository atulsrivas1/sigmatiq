# Indicators Backlog

This is the working backlog of indicators/features to add. We’ll keep it current as we implement.

## Completed (implemented in edge_core)
- open_gap_z: opening gap normalized by ATR or 5m stddev
- first15m_range_z: first N minutes range normalized (15/30)
- atm_iv_open_delta: ATM IV delta from prior close to open
- gamma_density_peak_strike: strike with max Σ(|Γ|×OI)
- gamma_skew_left_right: density skew left vs right of spot
- dist_to_gamma_peak: distance from spot to gamma peak

## Regime (Polygon indices)
- vix_level: spot VIX.
- vix_delta: day-over-day change in VIX.
- vix_term_slope: VIX3M − VIX (or 1m vs 3m slope).

## Options Structure & Flow (Polygon options)
- pcr_volume: put/call volume ratio (per day, per expiry or aggregate).
- pcr_oi: put/call open interest ratio.
- oi_change_1d: day-over-day OI change.
- oi_trend: rolling trend/EMA of OI.
- iv_rank_52w: rank of ATM IV vs past year.
- iv_percentile_52w: percentile of ATM IV vs past year.
- atm_iv_zscore: z-score of ATM IV on rolling window (e.g., 20/60/252d).
- iv_smile_wings: IV wings minus ATM (e.g., ±10/20 strikes or 25Δ wings).
 - oi_peak_strike: strike with max OI (same-day expiry).
 - dist_to_oi_peak: distance from spot to OI peak strike.
 - oi_concentration_hhi: Herfindahl over top-N OI strikes.
 - gamma_density_peak_strike: strike with max |Gamma|×OI (Done)
 - dist_to_gamma_peak: distance from spot to gamma peak strike (Done)
 - gamma_skew_left_right: skew of |Gamma|×OI density (Done)
 - gamma_concentration: concentration metric over top-N gamma strikes.

## Intraday-Derived (equities context)
- rsi_last_hour: RSI computed over last hour of intraday bars.
- returns_last_30m: last 30 minutes return.
- close_vs_vwap: normalized distance to session VWAP.
- day_range_pos: (close − day_low)/(day_high − day_low).
- vol_zscore: rolling z-score of volume.
 - open_gap_z: opening gap normalized by ATR or 5m stddev (Done)
 - first15m_range_z: first N minutes range normalized (Done)

## Time/Calendar
- calendar_flags: EOM, EOQ, OPEX (3rd Fri), holiday-eve; encode as binary features.

## Quality/Trend Diagnostics
- lr_r2: rolling linear-regression R² for `close` over window.
- ulcer_index: drawdown-based volatility metric (optional).

## Aliases (loader mapping)
- Map idea-set names to existing implementations:
  - returns→ret
  - stddev→rolling_std
  - bollinger→bollinger_bands
  - iv_skew_25d_rr→iv_skew_25d

## Priorities
- P0: alias mapping, vix_level/vix_delta/vix_term_slope, pcr_volume/pcr_oi, rsi_last_hour, close_vs_vwap.
- P1: iv_rank_52w/iv_percentile_52w/atm_iv_zscore (requires daily ATM IV store), oi_change_1d/oi_trend, returns_last_30m, day_range_pos, vol_zscore, lr_r2.
- P2: iv_smile_wings, ulcer_index, calendar_flags.
