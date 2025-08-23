# Multi-Indicator Set Use Cases

Each use case uses 3–7 indicators together to solve a trading problem.

Latency Legend
- RT Ultra: <100 ms
- RT Fast: <1 s
- Near-RT: <5 s
- Batch: minutes–hours

1) Momentum Breakout + Volume Confirmation
- Persona: Momentum swing/day trader
- Components: `donchian(20)`, `macd(12,26,9)`, `vol_zscore(20)`, `obv`
- Workflow: Alert on price breaking Donchian channel with MACD up and volume z-score > 2 to confirm participation.
- Data: 5m/hourly bars
- Latency: RT Fast
- Output: Breakout signal with confidence; chart overlay.

2) Mean Reversion Bands + Oscillator
- Persona: Mean-reversion swing trader
- Components: `bollinger_bands(20,2)`, `rsi(14)`, `stoch_rsi(14,14)`
- Workflow: Enter when price touches lower band AND RSI < 30 with Stoch RSI rising; exit on mid-band.
- Data: 15m/hourly/daily
- Latency: Near-RT
- Output: Entry/exit recommendation with risk bracket suggestion.

3) Multi-Timeframe Trend Alignment
- Persona: Trend follower
- Components: `ema(20)` HTF (daily), `ema(20)` LTF (hourly), `ema_slope(20)` LTF
- Workflow: Trade long only if daily EMA trend up and hourly EMA above/up-slope; filter chop.
- Data: hourly + daily
- Latency: Near-RT
- Output: Gate state and aligned trend signal.

4) 0DTE Options Gate (Intraday)
- Persona: Options scalper
- Components: `momentum_score_total`, `first15m_range_z`, `open_gap_z`, `atr(14)`
- Workflow: Enable entries only when momentum score positive, first 15m normalized range reasonable, and open gap not extreme; ATR calibrates brackets.
- Data: intraday bars, session flags
- Latency: RT Fast
- Output: Gate (green/yellow/red) with reasons.

5) Breakout Pullback Entry
- Persona: Momentum swing trader
- Components: `donchian(20)`, `ema(20)`, `intraday_vwap`, `vol_zscore(20)`
- Workflow: After breakout, wait for pullback to EMA/VWAP with healthy volume; enter on resumption.
- Data: 5m/hourly
- Latency: RT Fast
- Output: Entry window and confirmation badge.

6) Volatility Expansion Regime
- Persona: Risk manager
- Components: `atr(14)`, `rolling_std(close,20)`, `bollinger_bands(20,2)` width
- Workflow: Detect transition to high-vol regime (ATR ↑, width ↑); increase stops and reduce size.
- Data: hourly/daily
- Latency: Near-RT
- Output: Regime label with policy suggestions.

7) Volume Price Analysis (VPA) Scanner
- Persona: Flow/momentum trader
- Components: `vol_zscore(20)`, `obv`, `close_vs_vwap(kind='pct')`
- Workflow: Identify unusual volume moves above/below VWAP with OBV trend alignment.
- Data: 1–5m bars
- Latency: RT Fast
- Output: Ranked scanner results with badges.

8) Regime Detection Hierarchy
- Persona: Portfolio manager
- Components: `vix_level`, `iv_rank_52w`, `momentum(daily, 50)`
- Workflow: Classify regime (calm/trend/choppy) then gate downstream sets.
- Data: daily bars + VIX
- Latency: Batch/Near-RT
- Output: Regime label and recommended risk profile.

9) Options Premium Strategy Selector
- Persona: Options strategist
- Components: `iv_rank_52w`, `iv_term_slope`, `atm_iv_zscore`, `momentum(daily)`
- Workflow: Choose between premium selling vs buying based on IV regime and underlying momentum.
- Data: IV surfaces EOD + daily bars
- Latency: Near-RT
- Output: Strategy suggestion (sell/buy) with rationale.

10) Scalping Set (Ultra-Short TF)
- Persona: Intraday scalper
- Components: `intraday_vwap`, `rsi(7)`, `ema(9)`, `vol_zscore(20)`
- Workflow: Micro pullback to VWAP/EMA with RSI re-cross, avoid low-volume periods.
- Data: 1m bars
- Latency: RT Ultra
- Output: Fast alerts with throttle/debounce.

11) Swing Set With Risk Controls
- Persona: Swing trader
- Components: `macd`, `ema(50)`, `bollinger_bands(20,2)`, `atr(14)`
- Workflow: Longs when MACD up and price above EMA; exits/position sizing informed by ATR and band width.
- Data: hourly/daily
- Latency: Near-RT
- Output: Trade plan (entry/stop/target) suggestion.

12) Fundamental-Technical Hybrid (Awareness)
- Persona: Investor
- Components: `daily_ret(window=20)` trend, `volatility(close,20)`, external fundamental score (placeholder)
- Workflow: Surface candidates where technical trend aligns with fundamentals; defer detailed fundamentals integration.
- Data: daily bars + fundamentals
- Latency: Batch
- Output: Candidate list with composite score.

