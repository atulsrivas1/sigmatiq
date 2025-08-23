# Indicators Catalog

This catalog is auto‑generated. It summarizes available indicators with category, subcategory, and constructor parameters.

| Name | Category | Subcategory | Params | Description |
|------|----------|-------------|--------|-------------|
| adx | trend_strength | dmi_adx | period |  |
| aroon | price | trend | period |  |
| atm_iv_eod | options_volatility | eod | underlying, sampling, strike_band |  |
| atm_iv_open_delta | options_volatility | iv_open | underlying, open_sampling, close_sampling_prev, strike_band |  |
| atm_iv_zscore | options_volatility | iv_zscore | underlying, window_days |  |
| atr | volatility | atr | period |  |
| bollinger_bands | band | bollinger | column, window, num_std |  |
| calendar_flags | time | calendar | tz |  |
| cci | oscillator | cci | period |  |
| close_vs_vwap | intraday | vwap | kind |  |
| cmf | volume | money_flow | period |  |
| daily_dist_to_ema | daily_moving_average | distance | underlying, window, normalize |  |
| daily_ema | daily_moving_average | ema | underlying, window |  |
| daily_ret | daily_momentum | returns | underlying, window |  |
| daily_rsi | daily_momentum | rsi | underlying, period, column |  |
| daily_vwap | daily_volume | vwap | underlying, shift_days |  |
| day_range_pos | intraday | session_range | args, kwargs |  |
| dist_to_ema | moving_average | distance | column, window, normalize |  |
| dist_to_gamma_peak | options_structure | gamma_peaks | underlying, spot_col |  |
| dist_to_oi_peak | options_structure | oi_peaks | underlying, spot_col |  |
| div_eod | options_volatility | eod | underlying |  |
| donchian | price | channels | window |  |
| dpo | price | detrended | column, period |  |
| elder_ray | trend_strength | elder_ray | period |  |
| ema | moving_average | ema | column, window |  |
| ema_slope | moving_average | slope | column, window, period |  |
| first15m_range_z | intraday | open | ticker, window_mins, norm |  |
| fisher_transform | oscillator | fisher | period |  |
| gamma_concentration | options_structure | gamma_peaks | underlying, top_n |  |
| gamma_density_peak_strike | options_structure | gamma_density | underlying |  |
| gamma_peak_strike | options_structure | gamma_peaks | underlying |  |
| gamma_skew_left_right | options_structure | gamma_density | underlying, spot_col |  |
| hour_of_day | time | intraday | args, kwargs |  |
| ichimoku | price | trend | tenkan, kijun, senkou, shift_ahead |  |
| intraday_vwap | volume | intraday_vwap | price_col, volume_col |  |
| iv_percentile_52w | options_volatility | iv_rank | underlying, window_days |  |
| iv_rank_52w | options_volatility | iv_rank | underlying, window_days |  |
| iv_realized_spread | options_volatility | iv_rv_spread | underlying, window, freq, contract_type, iv_source, quote_window, strike_band |  |
| iv_skew25_delta | options_volatility | iv_skew | underlying, iv_source, quote_window, strike_band |  |
| iv_smile_wings | options_volatility | smile | underlying, sampling, wing_points, strike_band |  |
| iv_term_slope | options_volatility | term_structure | underlying, days_fwd, iv_source, quote_window, strike_band |  |
| kama | price | moving_average | column, er_period, fast, slow |  |
| keltner | price | channels | window, multiplier |  |
| lr_r2 | trend | quality | column, window |  |
| macd | oscillator | macd | column, fast, slow, signal |  |
| mfi | volume | money_flow | period |  |
| momentum | price_trend | momentum | column, window |  |
| momentum_score_total | composite | momentum_score | w_hourly, w_daily |  |
| obv | volume | obv | price_col, volume_col |  |
| oi_change_1d | options_flow | open_interest | underlying |  |
| oi_concentration_hhi | options_structure | concentration | underlying, top_n |  |
| oi_peak_strike | options_structure | oi_peaks | underlying |  |
| oi_trend | options_flow | open_interest | underlying, window |  |
| open_gap_z | intraday | open | ticker, atr_period, norm |  |
| pcr_eod | options_flow | eod | args, kwargs |  |
| pcr_oi | options_flow | ratios | underlying |  |
| pcr_volume | options_flow | ratios |  |  |
| ppo | oscillator | ppo | column, fast, slow, signal |  |
| psar | price | trend | step, max_step |  |
| qstick | price_trend | qstick | period |  |
| ret | price_trend | returns | column, window |  |
| returns_last_30m | intraday | windowed | args, kwargs |  |
| roc | price | momentum | column, window |  |
| rolling_std | volatility | rolling_std | column, window |  |
| rsi | oscillator | rsi | column, period |  |
| rsi_last_hour | intraday | session_window | period |  |
| sma | price | moving_average | column, window |  |
| sold_flow_ratio | options_flow | ratio | window |  |
| stoch_rsi | oscillator | stoch_rsi | column, rsi_period, stoch_period, smooth_k, smooth_d |  |
| stochastic | oscillator | stochastic | period_k, period_d |  |
| supertrend | price | trend | period, multiplier |  |
| trix | price | momentum | column, period |  |
| tsi | price | momentum | column, r, s |  |
| ultimate_oscillator | price | momentum | short, mid, long |  |
| vix_delta | regime | vix |  |  |
| vix_level | regime | vix | index_ticker |  |
| vix_term_slope | regime | vix_term | near, far |  |
| vol_zscore | volume | zscore | window |  |
| volatility | volatility | realized | column, window |  |
| williams_r | oscillator | williams_r | period |  |
