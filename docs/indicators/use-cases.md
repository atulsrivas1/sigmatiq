# Single-Indicator Use Cases

Each use case below involves exactly one indicator. For combinations, see the separate indicator-sets exercise (to be created later).

Latency Legend
- RT Ultra: <100 ms
- RT Fast: <1 s
- Near-RT: <5 s
- Batch: minutes–hours

1) RSI Oversold/Oscillation Gate
- Persona: Day/Swing trader
- Indicator: `rsi(period=14)`
- Workflow: Screen for RSI < 30 (oversold) or > 70 (overbought) on the chosen timeframe to queue reversals or exhaustion alerts.
- Data: 5m/hourly/daily bars
- Latency: RT Fast
- Output: List of symbols crossing thresholds with timestamps; alert toggle.

2) MACD Signal Cross
- Persona: Momentum trader
- Indicator: `macd(fast=12, slow=26, signal=9)`
- Workflow: Detect MACD line crossing signal line up/down to time entries/exits.
- Data: 5m/hourly/daily bars
- Latency: RT Fast
- Output: Cross events (up/down), last values, histogram snapshot.

3) ATR Expansion Alert
- Persona: Volatility trader
- Indicator: `atr(period=14)`
- Workflow: Alert when ATR rises above a rolling percentile (e.g., 80th) to signal a volatility regime shift.
- Data: hourly/daily bars
- Latency: Near-RT
- Output: Spike flag with current ATR and percentile.

4) Bollinger Band Touch
- Persona: Mean-reversion trader
- Indicator: `bollinger_bands(window=20, num_std=2)`
- Workflow: Flag when close touches upper/lower band; optional middle-band reversion target.
- Data: 15m/hourly/daily bars
- Latency: RT Fast
- Output: Touch event (upper/lower), band widths, z-score.

5) Intraday VWAP Deviation
- Persona: Intraday scalper
- Indicator: `intraday_vwap(price_col=close, volume_col=volume)`
- Workflow: Monitor price distance from VWAP; alert on > x% deviation for reversion plays.
- Data: 1m/5m bars with volume
- Latency: RT Ultra
- Output: Deviation value and side; optional brackets suggestion.

6) Volume Z-Score Spike
- Persona: News/flow trader
- Indicator: `vol_zscore(window=20)`
- Workflow: Trigger when volume z-score > 2.0 to highlight unusual activity.
- Data: 1m/5m/hourly bars
- Latency: RT Fast
- Output: Spike alert with current z and baseline.

7) IV Rank Extreme
- Persona: Options trader
- Indicator: `iv_rank_52w(window_days=252)`
- Workflow: Indicate when IV rank > 80% (premium selling candidates) or < 20% (premium buying candidates).
- Data: EOD IV series, daily
- Latency: Batch/Near-RT
- Output: Rank value and bucket (low/neutral/high).

8) Donchian Channel Break
- Persona: Trend follower
- Indicator: `donchian(window=20)`
- Workflow: Detect price breakout above/below channel extremes.
- Data: 5m/hourly/daily bars
- Latency: RT Fast
- Output: Breakout event (up/down), channel bounds.

9) Supertrend Flip
- Persona: Swing trader
- Indicator: `supertrend(period=10, multiplier=3)`
- Workflow: Capture trend flips when price crosses supertrend line.
- Data: 5m/hourly/daily bars
- Latency: RT Fast
- Output: State change (bullish/bearish), current line value.

10) Stochastic %K Threshold
- Persona: Mean-reversion trader
- Indicator: `stochastic(period_k=14, period_d=3)`
- Workflow: Alert when %K crosses above/below 20/80 thresholds.
- Data: 5m/hourly/daily bars
- Latency: RT Fast
- Output: Cross direction and levels.

11) Distance to EMA
- Persona: Trend trader
- Indicator: `dist_to_ema(column=close, window=20, normalize=true)`
- Workflow: Use normalized distance to gauge stretch from trend; alert when >1.5σ.
- Data: 5m/hourly/daily bars
- Latency: RT Fast
- Output: Distance value and z-normalization.

12) VIX Level Gate
- Persona: Risk manager
- Indicator: `vix_level(index_ticker=^VIX)`
- Workflow: Gate trading when VIX > threshold (e.g., 25) to reduce risk.
- Data: VIX daily/intraday series
- Latency: Near-RT
- Output: Gate state and last VIX value.
