# Use Case Matrix — Indicator Sets

| Use Case | User Type | Components | Data Needs | Latency | Priority | Complexity |
|----------|-----------|------------|------------|---------|----------|------------|
| Momentum Breakout + Volume | Day/Swing | Donchian, MACD, Vol Z, OBV | 5m/hourly | <1s | High | Medium |
| Mean Reversion Bands + Osc | Swing | BB, RSI, Stoch RSI | 15m/hourly/daily | <5s | High | Medium |
| Multi-TF Trend Alignment | Trend | EMA(HTF/LTF), EMA Slope | hourly+daily | <5s | High | Medium |
| 0DTE Gate | Options | Momentum Score, First15m Z, Open Gap Z, ATR | intraday | <1s | High | Medium |
| Breakout Pullback Entry | Swing | Donchian, EMA, VWAP, Vol Z | 5m/hourly | <1s | High | Medium |
| Volatility Expansion | Risk | ATR, Rolling Std, BB Width | hourly/daily | <5s | Medium | Medium |
| VPA Scanner | Flow | Vol Z, OBV, VWAP Deviation | 1–5m | <1s | Medium | High |
| Regime Detection | PM | VIX Level, IV Rank, Momentum | daily | Batch | Medium | Low |
| Options Premium Selector | Options | IV Rank, IV Term Slope, ATM IV Z, Momentum | daily/EOD | <5s | High | High |
| Scalping Set | Day | VWAP, RSI(7), EMA(9), Vol Z | 1m | <100ms | Medium | High |
| Swing + Risk Controls | Swing | MACD, EMA(50), BB, ATR | hourly/daily | <5s | Medium | Medium |
| Fundamental-Tech Hybrid | Investor | Daily Ret, Volatility, Fundamental Score | daily | Batch | Medium | High |

Notes
- Complexity accounts for multi-timeframe alignment, IV data availability, and streaming constraints.

