# EarnPack Strategy Pack

## Purpose
Trade earnings volatility using pre/post-announcement price dislocations and IV crush patterns.

## When to Use
- **Market Regime**: High earnings volatility periods (quarterly earnings seasons)
- **Asset Class**: Equities and equity options with earnings events
- **Horizon**: 1-5 days around earnings
- **Cadence**: Event-driven (earnings calendar)

## Required Data Sources
- Earnings calendar with confirmed dates/times
- Historical earnings surprises and reactions
- Options implied volatility (30-day and weekly)
- Pre/post market price action
- Analyst consensus estimates

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `iv_rank` | Percentile of current IV vs 52-week range | window=252 |
| `iv_skew` | Put/call IV differential | strikes=[0.95, 1.05] |
| `earnings_drift` | Pre-earnings price momentum | lookback=10 |
| `volume_surge` | Unusual volume patterns | threshold=2.0 |
| `rsi` | Overbought/oversold conditions | period=14 |
| `atr` | Expected move sizing | period=20 |
| `historical_move` | Average earnings move | quarters=8 |
| `analyst_dispersion` | Estimate disagreement | min_analysts=3 |
| `put_call_ratio` | Options sentiment | window=5 |
| `gap_history` | Past gap behavior | lookback=4 |

## Feature List
- `iv_crush_expected`: IV30 - IV_post_earnings_estimate
- `earnings_surprise_zscore`: (actual - consensus) / std_dev
- `pre_earnings_drift_pct`: price_change_10d / atr_20
- `volume_acceleration`: volume_5d / volume_20d
- `sentiment_composite`: weighted(iv_skew, put_call_ratio, volume_surge)
- `expected_move_ratio`: iv_implied_move / historical_move
- `time_to_earnings_hours`: hours until announcement
- `post_earnings_decay`: hours since announcement

## Entry/Exit Logic
- **Entry**: 2-3 days before earnings when IV_rank > 70% and volume_surge detected
- **Exit**: Morning after earnings or when IV_crush > 30% realized
- **Alternative**: Straddle/strangle when expected_move_ratio > 1.5

## Risk Profile Defaults

| Profile | Position Size | Max Contracts | Stop Loss | IV Rank Min |
|---------|--------------|---------------|-----------|-------------|
| Conservative | 2% | 5 | 15% | 80% |
| Balanced | 5% | 10 | 25% | 70% |
| Aggressive | 8% | 20 | 35% | 60% |

## Gate Overrides
```yaml
min_trades: 20  # Fewer opportunities due to quarterly events
max_dd_pct: 30  # Higher drawdowns expected around binary events
spread_pct: 3.0  # Wider spreads around earnings
min_volume: 50000  # Ensure liquidity for options
fill_rate_pct: 85  # Lower due to volatility
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 0.8 | > 0.6 | > 0.4 |
| Win Rate | > 55% | > 50% | > 45% |
| Avg Winner/Loser | > 1.5 | > 1.8 | > 2.0 |
| Max Drawdown | < 20% | < 30% | < 40% |
| Turnover (annual) | < 50x | < 100x | < 200x |

## Risks and Failure Modes
- **Binary Risk**: Earnings are win/lose events with gap risk
- **IV Crush Timing**: Volatility can collapse faster than expected
- **Liquidity**: Wide bid/ask spreads around announcements
- **News Leakage**: Information may price in before official release
- **Guidance Risk**: Forward guidance can overshadow earnings results
- **Market Hours**: Many announcements outside regular trading hours

## Template YAML
```yaml
template:
  name: earnpack_quarterly
  version: 0.1.0
  pack: earnpack
indicators:
  - iv_rank
  - iv_skew
  - earnings_drift
  - volume_surge
  - rsi
  - atr
  - historical_move
  - analyst_dispersion
  - put_call_ratio
  - gap_history
policy:
  execution:
    wait_for_confirmation: true
    position_sizing: iv_scaled
    event_driven: true
  risk:
    max_position_size: 0.05
    stop_loss_pct: 25
    time_stop_hours: 48
sweeps_defaults:
  thresholds: [[0.55, 0.60, 0.65], [0.60, 0.65, 0.70]]
  allowed_hours: [[9, 10], [15, 16]]
  top_pct: [0.10, 0.15]
```