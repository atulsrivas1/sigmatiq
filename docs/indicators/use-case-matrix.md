# Use Case Matrix

| Use Case | User Type | Indicators | Data Needs | Latency | Priority | Complexity |
|----------|-----------|------------|------------|---------|----------|------------|
| Watchlist Screening | Day/Swing | RSI, MACD, Volume | 1–5m bars | <1s | High | Medium |
| Momentum Entry Timing | Day | momentum, ema_slope, intraday_vwap | 1m bars | <100ms | High | High |
| Mean Reversion Rebound | Swing | rsi, bollinger_bands, stoch_rsi | 15m/hourly | <5s | Medium | Medium |
| Breakout + Volume | Swing | donchian, vol_zscore, obv | 5m/hourly | <1s | High | Medium |
| 0DTE Gate | Options | momentum_score_total, first15m_range_z, open_gap_z | intraday bars | <1s | High | Medium |
| Portfolio Health | PM | iv_rank_52w, vix_term_slope, daily_ret | daily | Batch | Medium | Low |
| Event Vol Guard | Risk | atm_iv_zscore, iv_term_slope | IV surfaces | <5s | Medium | High |
| Real-Time Scanner | Active | rsi, macd, vol_zscore, ema_slope | 1–5m bars | <1s | High | High |
| Backtest Combos | Quant | pack indicators + thresholds | historical | Batch | High | High |
| Indicator Chaining | Power | rolling_std(rsi), ema_slope | derived | <5s | Medium | Medium |
| Brackets Calibration | Systematic | atr, volatility, rolling_std | daily/hourly | Batch | Medium | Medium |
| Regime Detection | PM | vix_level, iv_rank_52w, momentum | daily | Batch | Medium | Low |

Notes
- Priority reflects business value and user demand; Complexity blends compute, data availability, and UX.

