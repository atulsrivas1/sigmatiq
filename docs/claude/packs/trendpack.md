# TrendPack Strategy Pack

## Purpose
Capture sustained directional moves using trend-following indicators and momentum confirmation.

## When to Use
- **Market Regime**: Trending markets with clear directional bias
- **Asset Class**: Futures, ETFs, large-cap equities
- **Horizon**: 10-30 days (medium-term trends)
- **Cadence**: Daily signals with weekly rebalancing

## Required Data Sources
- Daily OHLCV data (2+ years history)
- Market breadth indicators
- Sector rotation data
- Volume profile
- Moving average ribbons

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `ema_ribbon` | Multiple EMAs for trend strength | periods=[8,13,21,34,55] |
| `adx` | Trend strength measurement | period=14 |
| `macd` | Momentum confirmation | fast=12, slow=26, signal=9 |
| `supertrend` | Dynamic support/resistance | period=10, multiplier=3 |
| `vwap` | Volume-weighted average price | anchor=daily |
| `donchian_channel` | Breakout levels | period=20 |
| `linear_regression` | Trend angle and R² | period=20 |
| `cmf` | Chaikin Money Flow | period=21 |
| `obv` | On-balance volume trend | cumulative=true |
| `parabolic_sar` | Trend reversal points | accel=0.02, max=0.2 |

## Feature List
- `trend_strength`: adx * trend_angle_normalized
- `ribbon_expansion`: (ema_55 - ema_8) / atr
- `momentum_quality`: macd_histogram * volume_ratio
- `trend_consistency`: linear_regression_r2 * days_in_trend
- `volume_confirmation`: cmf * obv_slope
- `breakout_distance`: (price - donchian_high) / atr
- `trend_acceleration`: second_derivative(ema_21)
- `regime_alignment`: correlation(price, market_trend)

## Entry/Exit Logic
- **Entry**: EMA ribbon aligned + ADX > 25 + MACD bullish cross + volume confirmation
- **Exit**: Parabolic SAR flip or ribbon compression or ADX < 20
- **Position Sizing**: Scale with ADX strength and trend consistency

## Risk Profile Defaults

| Profile | Position Size | Leverage | Stop Loss | Min ADX |
|---------|--------------|----------|-----------|---------|
| Conservative | 3% | 1x | 8% | 30 |
| Balanced | 6% | 1.5x | 12% | 25 |
| Aggressive | 10% | 2x | 15% | 20 |

## Gate Overrides
```yaml
min_trades: 30
max_dd_pct: 25
es95x: 2.0
spread_pct: 0.5
min_volume: 100000
fill_rate_pct: 95
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 1.2 | > 1.0 | > 0.8 |
| Win Rate | > 45% | > 40% | > 35% |
| Avg Winner/Loser | > 2.5 | > 3.0 | > 3.5 |
| Max Drawdown | < 15% | < 25% | < 35% |
| Turnover (annual) | < 20x | < 40x | < 60x |

## Risks and Failure Modes
- **Whipsaw Risk**: False breakouts in ranging markets
- **Late Entry**: Joining trends near exhaustion
- **Correlation Risk**: Multiple positions in same trend
- **Gap Risk**: Overnight gaps against position
- **Regime Change**: Trend to range transition losses
- **Slippage**: Large positions in momentum moves

## Template YAML
```yaml
template:
  name: trendpack_momentum
  version: 0.1.0
  pack: trendpack
indicators:
  - ema_ribbon
  - adx
  - macd
  - supertrend
  - vwap
  - donchian_channel
  - linear_regression
  - cmf
  - obv
  - parabolic_sar
policy:
  execution:
    wait_for_confirmation: true
    position_sizing: adx_scaled
    pyramid_allowed: true
  risk:
    max_position_size: 0.10
    stop_loss_pct: 12
    trailing_stop: true
sweeps_defaults:
  thresholds: [[0.50, 0.55, 0.60], [0.55, 0.60, 0.65]]
  allowed_hours: [[9, 10, 11], [14, 15]]
  top_pct: [0.05, 0.10]
```