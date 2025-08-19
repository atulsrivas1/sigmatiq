# Indicator Reference (Built-ins)

This document lists the built-in indicators, grouped by category, with a short description, constructor parameters, and primary data sources (Polygon-first).

Notes
- Column refers to the input series (usually `close`) on the working DataFrame.
- Daily indicators fetch Polygon daily bars and are shifted one day to avoid leakage.
- Options indicators rely on Polygon option chain snapshots (IV/Greeks).
- All indicators are available via `/indicators` (flat) and `/indicators?group=true` (grouped).

## New in v2 (Sigma Lab)
- open_gap_z: opening gap normalized by ATR or prior 5m stddev.
- first15m_range_z: first N minutes range normalized by ATR or 5m stddev.
- atm_iv_open_delta: ATM IV delta from prior close to today’s open window.
- gamma_density_peak_strike: strike with max Σ(|Gamma|×OI) per day.
- gamma_skew_left_right: density skew of Σ(|Gamma|×OI) left vs right of spot.
- dist_to_gamma_peak: distance from spot to gamma-density peak strike.

## Price Trend

- momentum
  - Params: `column: str='close'`, `window: int`
  - Output: `close_mom_<window>` (pct change over window)
  - Source: Polygon hourly/daily bars
- ret
  - Params: `column: str='close'`, `window: int`
  - Output: `ret_<window>h` (pct change over window)
  - Source: Polygon hourly/daily bars

## Trend Strength / Directional Movement

- adx
  - Params: `period: int=14`
  - Output: `plus_di_<period>`, `minus_di_<period>`, `adx_<period>`
  - Source: Polygon hourly/daily bars (requires `high`, `low`, `close`)

## Volatility

- volatility (realized)
  - Params: `column: str='close'`, `window: int`
  - Output: `close_vol_<window>` (rolling std of returns)
  - Source: Polygon hourly/daily bars
- rolling_std
  - Params: `column: str='close'`, `window: int=20`
  - Output: `roll_std_<window>` (rolling std of returns)
  - Source: Polygon hourly/daily bars
- atr
  - Params: `period: int=14`
  - Output: `atr_<period>` (Average True Range via Wilder smoothing)
  - Source: Polygon hourly/daily bars (requires `high`, `low`, `close`)

## Intraday Open

- open_gap_z
  - Params: `ticker: str='SPY'`, `atr_period: int=14`, `norm: 'atr'|'stddev5m'='atr'`
  - Output: `open_gap_z` (open − prev close, normalized)
  - Source: Polygon daily bars (ATR) and optional 5m bars for stddev
- first15m_range_z
  - Params: `ticker: str='SPY'`, `window_mins: int=15`, `norm: 'atr'|'stddev5m'='atr'`
  - Output: `first15m_range_z_<window_mins>` (range 09:30→09:30+N, normalized)
  - Source: Polygon 5m bars + daily bars (ATR)

## Moving Average

- ema
  - Params: `column: str='close'`, `window: int`
  - Output: `ema_<window>`
  - Source: Polygon hourly/daily bars
- ema_slope
  - Params: `column: str='close'`, `window: int`, `period: int=1`
  - Output: `ema<window>_slope<period>h` (difference over period)
  - Source: Polygon hourly/daily bars
- dist_to_ema
  - Params: `column: str='close'`, `window: int`, `normalize: str='price'|'ema'`
  - Output: `dist_ema<window>_norm`
  - Source: Polygon hourly/daily bars

## Bands

- bollinger_bands
  - Params: `column: str='close'`, `window: int=20`, `num_std: float=2.0`
  - Output: `bb_mid_<window>`, `bb_upper_<window>`, `bb_lower_<window>`
  - Source: Polygon hourly/daily bars

## Oscillator

- rsi
  - Params: `column: str='close'`, `period: int=14`
  - Output: `rsi_<period>`
  - Source: Polygon hourly/daily bars
- macd
  - Params: `column: str='close'`, `fast: int=12`, `slow: int=26`, `signal: int=9`
  - Output: `macd_line`, `macd_signal`, `macd_hist`
  - Source: Polygon hourly/daily bars
- stochastic
  - Params: `period_k: int=14`, `period_d: int=3`
  - Output: `stoch_k`, `stoch_d`
  - Source: Polygon hourly/daily bars (requires `high`, `low`, `close`)
- cci
  - Params: `period: int=20`
  - Output: `cci_<period>`
  - Source: Polygon hourly/daily bars (requires `high`, `low`, `close`)
- williams_r
  - Params: `period: int=14`
  - Output: `williams_r_<period>`
  - Source: Polygon hourly/daily bars (requires `high`, `low`, `close`)

## Options Flow

- sold_flow_ratio
  - Params: `window: Optional[int]` (rolling mean window)
  - Output: `sold_flow_ratio` or `sold_flow_ratio_<window>` (puts_sold_total/calls_sold_total)
  - Source: Derived from 0DTE flow builder (uses Polygon options aggregates)

## Options Volatility

- iv_realized_spread
  - Params: `underlying: str='SPY'`, `window: int=20`, `freq: 'hour'|'day'='hour'`, `contract_type: Optional['call'|'put']`
  - Output: `iv_realized_spread_<window>` = ATM IV (snapshot) − realized vol (annualized)
  - Source: Polygon option chain snapshot (IV/Greeks) + Polygon bars
- iv_skew_25d
  - Params: `underlying: str`
  - Output: `iv_skew_25d` = IV(call ~ +0.25 delta) − IV(put ~ −0.25 delta) for the date’s expiry
  - Source: Polygon option chain snapshot (use greeks.delta)
- iv_term_slope
  - Params: `underlying: str`, `days_fwd: int=30`
  - Output: `iv_term_slope` = ATM IV(far expiry) − ATM IV(near/0DTE)
  - Source: Polygon option chain snapshot (two expiries)
- atm_iv_open_delta
  - Params: `underlying: str='SPY'`, `open_sampling: 'HH:MM-HH:MM'='09:30-09:35'`, `close_sampling_prev: 'HH:MM-HH:MM'='15:55-16:00'`
  - Output: `atm_iv_open_delta` (IV at open window − prior close)
  - Source: Polygon option quotes/snapshots + daily bars for prev close

## Options Structure

- gamma_density_peak_strike
  - Params: `underlying: str='SPY'`
  - Output: `gamma_density_peak_strike` (strike with max Σ(|Gamma|×OI))
  - Source: Polygon option chain snapshot (IV/Greeks) with open interest
- gamma_skew_left_right
  - Params: `underlying: str='SPY'`, `spot_col: str='close'`
  - Output: `gamma_skew_left_right` ((right − left)/(right + left)) over Σ(|Gamma|×OI)
  - Source: Polygon option chain snapshot (IV/Greeks) with open interest
- dist_to_gamma_peak
  - Params: `underlying: str='SPY'`, `spot_col: str='close'`
  - Output: `dist_to_gamma_peak` (spot − gamma_density_peak_strike)
  - Source: Derived from `gamma_density_peak_strike`

## Daily Momentum

- daily_rsi
  - Params: `underlying: str`, `period: int=14`
  - Output: `rsi_<period>_d` (shifted 1 day)
  - Source: Polygon daily bars (shifted)
- daily_ret
  - Params: `underlying: str`, `window: int`
  - Output: `ret_<window>d_d` (shifted 1 day)
  - Source: Polygon daily bars (shifted)

## Daily Moving Average

- daily_ema
  - Params: `underlying: str`, `window: int`
  - Output: `ema_<window>_d` (shifted 1 day)
  - Source: Polygon daily bars (shifted)
- daily_dist_to_ema
  - Params: `underlying: str`, `window: int`, `normalize: str='price'|'ema'`
  - Output: `dist_ema<window>_d` (shifted 1 day)
  - Source: Polygon daily bars (shifted)

## Composite

- momentum_score_total
  - Params: `w_hourly: float=0.7`, `w_daily: float=0.3`
  - Output: `momentum_score_total` (blended hourly z-score with daily RSI scale)
  - Source: Derived from computed hourly/daily indicators above

## Daily Volume

- daily_vwap
  - Params: `underlying: str`, `shift_days: int=1`
  - Output: `vwap_d` (previous day’s VWAP)
  - Source: Polygon daily bars (`vw` field from aggregates), shifted by 1 day to avoid leakage

## Volume

- obv
  - Params: `price_col: str='close'`, `volume_col: str='volume'`
  - Output: `obv` (cumulative On-Balance Volume)
  - Source: Polygon hourly/daily bars (requires `close`, `volume`)
- intraday_vwap
  - Params: `price_col: str='vwap'|'close'`, `volume_col: str='volume'`
  - Output: `vwap_intraday` (session-anchored cumulative VWAP)
  - Source: Polygon hourly bars (uses per-hour vwap and volume)

## Data Sources (Polygon)
- Hourly bars: `/v2/aggs/ticker/{ticker}/range/1/hour/{start}/{end}`
- Daily bars: `/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}`
- Options chain snapshot (IV/Greeks): `/v3/snapshot/options/{underlying}` (filtered by `expiration_date`)
- Options aggregates (for 0DTE flow): `/v2/aggs/ticker/{occ}/range/1/minute/{from}/{to}`

## API Browsing
- `GET /indicators` → flat list of registered indicators
- `GET /indicators?group=true` → grouped by category/subcategory
