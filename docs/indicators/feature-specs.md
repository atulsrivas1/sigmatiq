# Feature Specs — Top 5 Single-Indicator Features

Format
- User Story, Acceptance Criteria, Technical Design, Dependencies, Effort

1) RSI Threshold Screen
- Story: As a trader, I can screen my watchlist for RSI crossing 30/70 and receive results in under a second.
- Acceptance
  - Configure threshold and timeframe
  - Run on watchlist or preset universe; results ≤ 1 s for U ≤ 200
  - Save as a screen; export CSV
- Technical
  - API: `POST /screen` with single `rsi` condition
  - Engine: incremental RSI; cached last window
  - UI: simple threshold editor with preview sparkline
- Deps: Registry, market data
- Effort: 1–2 sprints

2) MACD Cross Alerts
- Story: As a momentum trader, I receive alerts when MACD crosses its signal line.
- Acceptance
  - Configure fast/slow/signal; choose cross direction
  - WebSocket and inbox alerts; mute/snooze
- Technical
  - WS `/ws/indicators` subscribe for `macd` cross
  - Incremental EMA updates
- Deps: Quotas, alert center
- Effort: 2 sprints

3) VWAP Deviation Monitor
- Story: As an intraday trader, I see when price deviates more than X% from VWAP.
- Acceptance
  - Session-aware VWAP; configurable deviation
  - Last-bar compute <100 ms per symbol
- Technical
  - Maintain session cumulative sums; efficient update
- Deps: Session utils
- Effort: 2 sprints

4) Bollinger Touch Finder
- Story: As a mean-reversion trader, I can list symbols touching upper/lower Bollinger bands.
- Acceptance
  - Configurable window and std; band touch events
  - Inline chart overlay in results
- Technical
  - Rolling mean/std; cheap vectorized compute
- Deps: Charts
- Effort: 2 sprints

5) IV Rank Extreme Dashboard
- Story: As an options trader, I view symbols with IV rank >80% or <20%.
- Acceptance
  - Daily update; sortable list with rank value
  - CSV export; alert on threshold cross
- Technical
  - Batch compute 252d rank; cache results
- Deps: IV data
- Effort: 2 sprints
