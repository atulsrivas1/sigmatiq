# SeasonPack Strategy Pack

## Purpose
Trade predictable seasonal patterns in commodities, indices, and sector rotations.

## When to Use
- **Market Regime**: Specific calendar periods with historical edge
- **Asset Class**: Commodities, sector ETFs, indices
- **Horizon**: 15-60 days (seasonal windows)
- **Cadence**: Monthly positioning with daily monitoring

## Required Data Sources
- 10+ years historical seasonal data
- Weather patterns and forecasts
- Economic calendar (harvests, holidays)
- Fund flow seasonality
- Tax calendar events

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `seasonal_avg` | Historical average return | years=10, period=month |
| `seasonal_prob` | Win rate by period | lookback=15_years |
| `calendar_day` | Day of month/year | trading_days_only=true |
| `seasonal_strength` | Consistency score | min_years=5 |
| `weather_impact` | Weather correlation | relevant_only=true |
| `roll_yield` | Futures roll return | front_months=2 |
| `seasonal_volume` | Volume patterns | normalize=true |
| `tax_loss_harvest` | Tax selling pressure | december_focus=true |
| `window_momentum` | In-season momentum | adaptive=true |
| `analog_years` | Similar year patterns | correlation=0.7 |

## Feature List
- `seasonal_edge`: current_period_avg_return - baseline_return
- `consistency_score`: wins_in_period / total_years
- `days_to_peak`: optimal_exit_day - current_day
- `strength_rank`: percentile(seasonal_strength)
- `entry_timing_score`: days_from_optimal_entry / window_size
- `weather_alignment`: correlation(weather_forecast, favorable_pattern)
- `roll_adjusted_return`: spot_return + roll_yield
- `seasonal_sharpe`: seasonal_return / seasonal_volatility

## Entry/Exit Logic
- **Entry**: 5 days before historical seasonal window + consistency > 70%
- **Exit**: At historical peak date or momentum reversal
- **Position Size**: Scale by seasonal strength and historical Sharpe
- **Hedging**: Opposite season trades for portfolio balance

## Risk Profile Defaults

| Profile | Position Size | Min Win Rate | Stop Loss | Min Years Data |
|---------|--------------|--------------|-----------|----------------|
| Conservative | 3% | 70% | 10% | 15 |
| Balanced | 5% | 60% | 15% | 10 |
| Aggressive | 8% | 50% | 20% | 7 |

## Gate Overrides
```yaml
min_trades: 12  # Monthly opportunities
max_dd_pct: 20
es95x: 1.8
spread_pct: 1.0
min_volume: 25000
fill_rate_pct: 95
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 1.0 | > 0.8 | > 0.6 |
| Win Rate | > 70% | > 60% | > 50% |
| Avg Winner/Loser | > 1.5 | > 2.0 | > 2.5 |
| Max Drawdown | < 12% | < 18% | < 25% |
| Turnover (annual) | < 12x | < 24x | < 36x |

## Risks and Failure Modes
- **Pattern Change**: Seasonal patterns evolve or break
- **Crowding**: Well-known seasonals get arbitraged away
- **Weather Shocks**: Unexpected weather disrupts patterns
- **Economic Shifts**: Structural changes invalidate history
- **Calendar Changes**: Holiday shifts, leap years
- **Black Swans**: Override seasonal tendencies

## Template YAML
```yaml
template:
  name: seasonpack_calendar
  version: 0.1.0
  pack: seasonpack
indicators:
  - seasonal_avg
  - seasonal_prob
  - calendar_day
  - seasonal_strength
  - weather_impact
  - roll_yield
  - seasonal_volume
  - tax_loss_harvest
  - window_momentum
  - analog_years
policy:
  execution:
    wait_for_confirmation: true
    position_sizing: seasonal_scaled
    enter_early: true
  risk:
    max_position_size: 0.08
    stop_loss_pct: 15
    time_exit: true
sweeps_defaults:
  thresholds: [[0.60, 0.65, 0.70], [0.65, 0.70, 0.75]]
  allowed_hours: [[9, 10], [14, 15]]
  top_pct: [0.20, 0.25]  # Fewer opportunities
```