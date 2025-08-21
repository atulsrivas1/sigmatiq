# EventPack Strategy Pack

## Purpose
Trade binary events including FDA approvals, M&A announcements, and economic releases.

## When to Use
- **Market Regime**: Event-driven opportunities regardless of market direction
- **Asset Class**: Biotech, M&A targets, macro ETFs
- **Horizon**: 1-5 days around events
- **Cadence**: Event calendar driven

## Required Data Sources
- FDA calendar (PDUFA dates)
- M&A rumor and announcement feeds
- Economic calendar with consensus
- Clinical trial databases
- Patent expiration dates
- Legal/regulatory dockets

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `event_proximity` | Days to known event | calendar=all |
| `rumor_intensity` | M&A chatter volume | sources=premium |
| `option_skew_event` | Event-specific skew | dte_bucket=weekly |
| `historical_reaction` | Past event moves | similar_events=10 |
| `insider_activity` | Director/officer trades | window=30d |
| `short_interest` | Short squeeze potential | days_to_cover=true |
| `analyst_revision` | Estimate changes | pre_event=30d |
| `news_sentiment` | Media coverage tone | nlp_model=finbert |
| `peer_correlation` | Sector sympathy plays | min_corr=0.6 |
| `halt_probability` | Trading halt likelihood | volatility_based=true |

## Feature List
- `event_edge`: implied_move - historical_avg_move
- `squeeze_potential`: short_interest * days_to_cover * volume_surge
- `information_leakage`: abnormal_volume + insider_buying
- `binary_risk_score`: event_magnitude * success_probability
- `sympathy_strength`: peer_correlation * sector_momentum
- `catalyst_quality`: rumor_intensity * source_credibility
- `hedge_cost`: put_premium / expected_move
- `risk_reward`: upside_scenario / downside_scenario

## Entry/Exit Logic
- **Entry**: 3-5 days before with hedged structure (spreads, condors)
- **Exit**: Immediately after event or at predetermined levels
- **FDA Strategy**: Long volatility via straddles, hedge with sector ETF
- **M&A Strategy**: Risk arbitrage with deal spread capture
- **Macro Events**: Positioned based on surprise direction probability

## Risk Profile Defaults

| Profile | Position Size | Max Event Risk | Hedge Required | Win Probability |
|---------|--------------|----------------|----------------|-----------------|
| Conservative | 1% | 50% loss | Always | > 60% |
| Balanced | 2% | 75% loss | Usually | > 50% |
| Aggressive | 3% | 100% loss | Sometimes | > 40% |

## Gate Overrides
```yaml
min_trades: 15  # Fewer event opportunities
max_dd_pct: 40  # Binary outcomes create large swings
es95x: 3.0  # Tail risk from binary events
spread_pct: 5.0  # Wide spreads around events
min_volume: 25000
fill_rate_pct: 85
max_slippage_usd: 0.10
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 0.6 | > 0.4 | > 0.2 |
| Win Rate | > 60% | > 50% | > 40% |
| Avg Winner/Loser | > 2.0 | > 3.0 | > 4.0 |
| Max Drawdown | < 25% | < 40% | < 60% |
| Turnover (annual) | < 25x | < 50x | < 100x |

## Risks and Failure Modes
- **Binary Risk**: Total loss possible on wrong outcome
- **Information Risk**: Insider trading, leaks
- **Halt Risk**: Stocks halted, options frozen
- **Liquidity Risk**: No exit during halt/news
- **Legal Risk**: Trading on material non-public info
- **Model Risk**: Historical patterns don't repeat

## Template YAML
```yaml
template:
  name: eventpack_catalyst
  version: 0.1.0
  pack: eventpack
indicators:
  - event_proximity
  - rumor_intensity
  - option_skew_event
  - historical_reaction
  - insider_activity
  - short_interest
  - analyst_revision
  - news_sentiment
  - peer_correlation
  - halt_probability
policy:
  execution:
    wait_for_confirmation: false
    position_sizing: kelly_criterion
    hedge_mandatory: true
  risk:
    max_position_size: 0.03
    stop_loss_pct: 50  # Wide due to binary nature
    event_hedge: true
sweeps_defaults:
  thresholds: [[0.60, 0.65, 0.70], [0.65, 0.70, 0.75]]
  allowed_hours: [[9, 10], [15, 16]]
  top_pct: [0.05, 0.10]
```