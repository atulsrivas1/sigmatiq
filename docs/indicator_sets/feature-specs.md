# Feature Specs — Top 5 Set Features

Format
- User Story, Acceptance Criteria, Technical Design, Dependencies, Effort

1) Momentum Breakout + Volume Scanner
- Story: As a trader, I can run a breakout-with-volume screen and see ranked candidates quickly.
- Acceptance
  - Configure components/params; save as a reusable set
  - Evaluate on watchlist/universe ≤ 1 s (U≤200)
  - Inline chart with Donchian/MACD/volume overlays
- Technical
  - Set evaluate endpoint; compute plan dedup across users
  - Cached EMAs; last-window compute
- Deps: Registry, charts
- Effort: 3 sprints

2) 0DTE Gate with Rationale
- Story: As an options trader, I get a clear green/yellow/red gate with explainability.
- Acceptance
  - Composite gate from momentum/first15m/open_gap/atr; rationale badges
  - Session-aware; throttle updates; persist events
- Technical
  - Rules engine; QA session alignment; WS streaming
- Deps: Intraday data, policy layer
- Effort: 3 sprints

3) Multi-Timeframe Trend Filter
- Story: As a trend trader, I only take signals when HTF and LTF trends align.
- Acceptance
  - Daily/hourly EMA alignment; configurable windows
  - Gate output consumable by other workflows
- Technical
  - Explicit resampling; alignment QA; cached HTF
- Deps: Data fetcher, cache
- Effort: 2 sprints

4) Mean Reversion Bands + Oscillator
- Story: As a swing trader, I find band-touch + oscillator oversold candidates.
- Acceptance
  - BB touch + RSI/Stoch threshold logic
  - Debounce controls at alert layer
- Technical
  - Rolling stats; event detection
- Deps: Charts, alert center
- Effort: 2 sprints

5) Options Premium Strategy Selector
- Story: As a strategist, I get a suggestion to sell/buy premium with reasons.
- Acceptance
  - IV rank/term slope/ATM z + momentum combine into classification
  - Daily refresh; audit lineage
- Technical
  - EOD IV ingestion; composite scoring; artifacts
- Deps: IV data, artifacts store
- Effort: 3–4 sprints

