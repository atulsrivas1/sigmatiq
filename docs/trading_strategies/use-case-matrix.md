# Use Case Matrix — Trading Strategies

| Strategy | User Type | Horizon | Data | Latency | Priority | Complexity |
|----------|-----------|---------|------|---------|----------|------------|
| Momentum Breakout (Eq) | Day/Swing | 5m/hourly | OHLCV | <1s | High | Medium |
| Mean Reversion Swing | Swing | 15m/hourly/daily | OHLCV | <5s | High | Medium |
| Trend Following (SMA200) | PM | daily | OHLC | Batch | High | Low |
| Intraday VWAP Reversion | Day | 1–5m | OHLCV | <100ms | High | High |
| 0DTE Options Scalping | Options | intraday | Bars+IV+Chains | <1s | High | High |
| Options Wheel | Income | multi-day | Daily+IV | Near-RT | Medium | Medium |
| Iron Condor (IV Rank) | Options | multi-day | Daily+IV+Events | Near-RT | High | High |
| Pairs Trading | Quant | 1m–hourly | OHLC | <1s | Medium | High |
| Sector Rotation | PM | monthly | Daily+VIX | Batch | Medium | Low |
| Earnings Drift | Event | days | Events+Bars | <5s | Medium | Medium |
| Gap Fade | Day | 1–5m | OHLCV | <1s | Medium | Medium |
| Crypto Momentum | Crypto | 1m–hourly | OHLCV | <1s | Medium | Medium |
| Futures Trend (CTA) | PM | daily/hourly | Futures+Roll | Near-RT | Medium | High |

Notes
- Complexity includes execution, risk, data freshness, and slippage modeling.

