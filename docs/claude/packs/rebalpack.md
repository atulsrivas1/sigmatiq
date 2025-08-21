# RebalPack Strategy Pack

## Purpose
Profit from index rebalancing, ETF flows, and portfolio reconstitution events.

## When to Use
- **Market Regime**: Around index rebalance dates (quarterly/annually)
- **Asset Class**: Index constituents, ETFs, factor portfolios
- **Horizon**: 5-20 days around rebalance
- **Cadence**: Known rebalance schedule (Russell, S&P, MSCI)

## Required Data Sources
- Index methodology documents
- Rebalance calendars and announcements
- ETF holdings and flows
- Index weight changes
- Free float adjustments
- Corporate action calendar

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `index_weight_delta` | Expected weight change | announcement_date=true |
| `etf_flow` | Passive flow estimates | aum_tracking=true |
| `days_to_rebal` | Countdown to event | include_prelim=true |
| `tracking_funds` | AUM following index | passive_only=true |
| `inclusion_probability` | Add probability | market_cap_rank=true |
| `deletion_probability` | Drop probability | fundamentals=true |
| `flow_imbalance` | Supply/demand mismatch | shares_needed=true |
| `arb_spread` | Current vs fair value | adjust_costs=true |
| `correlation_change` | Basket correlation shift | window=60 |
| `liquidity_score` | Ability to absorb flows | depth_weighted=true |

## Feature List
- `rebal_impact`: weight_delta * tracking_aum / float
- `flow_pressure`: expected_buying - available_liquidity
- `front_run_opportunity`: days_to_rebal * flow_imbalance
- `index_arb_score`: (index_price - nav) / nav
- `inclusion_surprise`: actual_adds - expected_adds
- `passive_demand`: etf_aum * weight_change
- `execution_risk`: spread * expected_volume
- `mean_reversion_time`: historical_reversion_days

## Entry/Exit Logic
- **Entry**: 10-15 days before rebalance for anticipated changes
- **Exit**: On rebalance date or 1-2 days after
- **Additions**: Long expected additions, scale by flow impact
- **Deletions**: Short expected deletions (if borrowable)
- **Risk Management**: Hedge with index futures/options

## Risk Profile Defaults

| Profile | Position Size | Days Early | Hedge Ratio | Min Probability |
|---------|--------------|------------|-------------|-----------------|
| Conservative | 2% | 5 | 80% | 80% |
| Balanced | 4% | 10 | 60% | 70% |
| Aggressive | 6% | 15 | 40% | 60% |

## Gate Overrides
```yaml
min_trades: 20
max_dd_pct: 15
es95x: 1.8
spread_pct: 2.0  # Can be wide near rebalance
min_volume: 100000
fill_rate_pct: 90
max_slippage_usd: 0.05
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 1.5 | > 1.2 | > 1.0 |
| Win Rate | > 70% | > 65% | > 60% |
| Avg Winner/Loser | > 1.3 | > 1.5 | > 1.8 |
| Max Drawdown | < 8% | < 12% | < 18% |
| Turnover (annual) | < 20x | < 40x | < 60x |

## Risks and Failure Modes
- **Announcement Risk**: Changes to methodology
- **Crowding Risk**: Too many arbitrageurs
- **Timing Risk**: Early/late execution
- **Liquidity Risk**: Insufficient float for flows
- **Tracking Error**: ETFs don't follow exactly
- **Market Risk**: Broad selloff overwhelms rebalance

## Template YAML
```yaml
template:
  name: rebalpack_index
  version: 0.1.0
  pack: rebalpack
indicators:
  - index_weight_delta
  - etf_flow
  - days_to_rebal
  - tracking_funds
  - inclusion_probability
  - deletion_probability
  - flow_imbalance
  - arb_spread
  - correlation_change
  - liquidity_score
policy:
  execution:
    wait_for_confirmation: true
    position_sizing: flow_weighted
    portfolio_approach: true
  risk:
    max_position_size: 0.06
    stop_loss_pct: 10
    index_hedge: true
sweeps_defaults:
  thresholds: [[0.60, 0.65, 0.70], [0.65, 0.70, 0.75]]
  allowed_hours: [[14, 15, 16]]  # MOC focus
  top_pct: [0.10, 0.15]
```