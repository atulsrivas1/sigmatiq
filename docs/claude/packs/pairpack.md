# PairPack Strategy Pack

## Purpose
Execute market-neutral pairs trading using statistical arbitrage and mean reversion between correlated assets.

## When to Use
- **Market Regime**: All markets (market-neutral approach)
- **Asset Class**: Equity pairs, sector ETFs, futures spreads
- **Horizon**: 5-20 days (mean reversion cycle)
- **Cadence**: Daily signals with continuous monitoring

## Required Data Sources
- Historical price correlations (90-day rolling)
- Cointegration test results
- Sector/industry classifications
- Fundamental ratios (P/E, P/B comparisons)
- Corporate actions calendar

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `correlation` | Pair correlation strength | window=60 |
| `cointegration` | Statistical relationship | lookback=90 |
| `zscore` | Spread standardization | window=20 |
| `half_life` | Mean reversion speed | method=ornstein |
| `beta_hedge` | Hedge ratio calculation | window=30 |
| `spread_bb` | Bollinger bands on spread | period=20, std=2 |
| `rsi_spread` | Spread momentum | period=14 |
| `volume_ratio` | Relative volume | window=10 |
| `hurst_exponent` | Mean reversion tendency | window=100 |
| `kalman_spread` | Dynamic hedge ratio | adaptive=true |

## Feature List
- `spread_zscore`: (spread - spread_mean) / spread_std
- `reversion_probability`: 1 - hurst_exponent
- `spread_acceleration`: d2(spread) / dt2
- `volume_divergence`: volume_ratio_leg1 / volume_ratio_leg2
- `correlation_stability`: rolling_corr_std
- `cointegration_pvalue`: johansen_test_result
- `time_in_spread`: bars_since_entry
- `spread_percentile`: rank(spread) / window

## Entry/Exit Logic
- **Entry**: |Z-score| > 2.0 + correlation > 0.7 + cointegration p < 0.05
- **Exit**: Z-score crosses 0 or |Z-score| < 0.5 or correlation breaks
- **Position**: Long underperformer, short outperformer with beta-neutral weights
- **Risk**: Exit if spread widens beyond 3 standard deviations

## Risk Profile Defaults

| Profile | Position Size | Max Pairs | Stop Loss | Min Correlation |
|---------|--------------|-----------|-----------|-----------------|
| Conservative | 2% per leg | 5 | 3σ | 0.80 |
| Balanced | 3% per leg | 10 | 4σ | 0.70 |
| Aggressive | 5% per leg | 15 | 5σ | 0.60 |

## Gate Overrides
```yaml
min_trades: 40  # Need sufficient samples
max_dd_pct: 20  # Lower due to market neutrality
es95x: 1.5
spread_pct: 1.0  # Two-leg execution
min_volume: 50000  # Both legs
fill_rate_pct: 92
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 1.5 | > 1.2 | > 1.0 |
| Win Rate | > 65% | > 60% | > 55% |
| Avg Winner/Loser | > 1.0 | > 1.2 | > 1.5 |
| Max Drawdown | < 10% | < 15% | < 20% |
| Turnover (annual) | < 50x | < 100x | < 150x |

## Risks and Failure Modes
- **Correlation Breakdown**: Pairs decouple permanently
- **Fundamental Divergence**: Company-specific events
- **Execution Risk**: Leg risk from partial fills
- **Borrow Costs**: Short leg expenses
- **Dividend Risk**: Ex-dividend date mismatches
- **Delisting/Halts**: One leg becomes untradeable

## Template YAML
```yaml
template:
  name: pairpack_stat_arb
  version: 0.1.0
  pack: pairpack
indicators:
  - correlation
  - cointegration
  - zscore
  - half_life
  - beta_hedge
  - spread_bb
  - rsi_spread
  - volume_ratio
  - hurst_exponent
  - kalman_spread
policy:
  execution:
    wait_for_confirmation: true
    position_sizing: equal_weight
    market_neutral: true
  risk:
    max_position_size: 0.06  # 3% per leg
    stop_loss_pct: 15  # On spread
    correlation_min: 0.60
sweeps_defaults:
  thresholds: [[0.50, 0.55, 0.60], [0.55, 0.60, 0.65]]
  allowed_hours: [[9, 10, 11, 14, 15]]
  top_pct: [0.10, 0.15]
```