# Strategy Use Cases (Archetypes)

Each strategy describes entry/exit, risk controls, data/latency, and outputs.

Latency Legend
- RT Ultra: <100 ms (order reacts to bar/tick)
- RT Fast: <1 s (intraday bars)
- Near-RT: <5 s (screen/alerts)
- Batch: minutes–hours (offline backtests)

1) Momentum Breakout (Equities)
- Persona: Momentum swing/day trader
- Entry: Donchian breakout + volume confirm; trade pullbacks to breakout level.
- Exit: Trailing ATR stop or mid-channel reversion; time-stop optional.
- Risk: 1% per trade; ATR-sized stop; max 4 concurrent positions.
- Data: 5m/hourly bars; corporate actions; volume
- Latency: RT Fast
- Output: Signals → orders; daily PnL and trade log.

2) Mean Reversion Swing
- Persona: Swing trader
- Entry: Bollinger lower-band touch with RSI < 30; scale-in optional.
- Exit: Middle band or fixed RR; time-stop 5 bars.
- Risk: 0.5–1% per position; portfolio heat cap.
- Data: 15m/hourly/daily
- Latency: Near-RT

3) Trend Following (Long-Only)
- Persona: ETF investor/PM
- Entry: Close above 200-day SMA; add on pullbacks.
- Exit: Close below 200-day SMA or max drawdown.
- Risk: Volatility parity across symbols; monthly rebalance.
- Data: Daily bars
- Latency: Batch/Near-RT

4) Intraday VWAP Reversion (Scalping)
- Persona: Intraday scalper
- Entry: |price - VWAP| > x% with session liquidity OK.
- Exit: Reversion to VWAP or time-stop (5–15m).
- Risk: Tight stops; max consecutive losses guard.
- Data: 1m/5m bars
- Latency: RT Ultra

5) 0DTE Options Scalping
- Persona: Options scalper
- Entry: Gate green (momentum/first15m/open_gap) then buy options at target delta.
- Exit: ATR/time brackets; parity-calibrated RR; time-stop <120m.
- Risk: Premium-at-risk cap; min OI/volume filters.
- Data: Intraday bars + options chain snapshots/IV
- Latency: RT Fast

6) Options Wheel (Covered Calls/Cash-Secured Puts)
- Persona: Income investor
- Entry: Sell CSP on pullback; roll/assign → sell covered calls.
- Exit: Roll at 21 DTE or 50% profit.
- Risk: Position sizing by equity allocation; earnings blackout.
- Data: Daily bars + options EOD IV
- Latency: Near-RT

7) Iron Condor (IV Rank)
- Persona: Options strategist
- Entry: IV Rank > 70; sell condor around expected move; distance by ATR.
- Exit: 50% profit or 2x loss; early exit pre-event.
- Risk: Portfolio margin limits; per-underlying exposure caps.
- Data: Daily + EOD IV; event calendar
- Latency: Near-RT

8) Pairs Trading (Stat Arb)
- Persona: Quant trader
- Entry: Spread z-score > 2; short rich, long cheap.
- Exit: Mean reversion to z=0; stop at z>3 or time-stop.
- Risk: Dollar/ beta neutrality; max leverage caps.
- Data: 1m/5m/hourly depending on horizon
- Latency: RT Fast

9) Sector Rotation (Regime-Based)
- Persona: PM
- Entry: Allocate among sector ETFs based on momentum/regime labels.
- Exit: Monthly rebalance; volatility-based tilts.
- Risk: Max drawdown guard; volatility targeting.
- Data: Daily bars + VIX
- Latency: Batch

10) Earnings Drift (Post-Announcement)
- Persona: Event trader
- Entry: Long winners (gap+hold) or fade losers based on drift stats.
- Exit: Close after N days or when drift weakens.
- Risk: Per-symbol exposure cap; avoid low liquidity.
- Data: Corporate events; intraday/daily bars
- Latency: Near-RT

11) Gap Fade (Intraday)
- Persona: Intraday mean reversion
- Entry: Large open gap against prior trend; fade towards prior close.
- Exit: Prior close or time-stop; ATR-based stop.
- Risk: First-15m gate; avoid news halts.
- Data: 1m/5m bars; session flags
- Latency: RT Fast

12) Crypto Momentum
- Persona: Crypto trader
- Entry: Breakout + trend filter; 24/7 session logic.
- Exit: Trailing stop; ATR/time targets.
- Risk: Higher volatility sizing; exchange fees.
- Data: 1m/15m/hourly crypto bars
- Latency: RT Fast

13) Futures Trend (Multi-Asset)
- Persona: CTA/PM
- Entry: Donchian breakout across futures; add on continuation.
- Exit: Trailing stop; roll contracts on expiry.
- Risk: Risk parity; per-asset limits; margin utilization.
- Data: Daily/hourly futures bars; contract metadata
- Latency: Near-RT

