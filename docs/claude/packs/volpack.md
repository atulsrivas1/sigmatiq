# VolPack Strategy Pack

## Purpose
Trade volatility regime changes using VIX derivatives and volatility arbitrage strategies.

## When to Use
- **Market Regime**: Volatility transitions (low to high, high to low)
- **Asset Class**: VIX futures, VXX, UVXY, SPY options
- **Horizon**: 2-10 days (volatility cycles)
- **Cadence**: Intraday monitoring with daily signals

## Required Data Sources
- VIX spot and futures term structure
- Options implied volatility surface
- Realized volatility (5, 10, 20, 30-day)
- Put/call ratios and skew
- VVIX (volatility of volatility)

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `vix_term_structure` | Contango/backwardation | months=[1,2,3,6] |
| `rv_iv_spread` | Realized vs implied gap | window=20 |
| `vix_percentile` | Current VIX vs history | lookback=252 |
| `vvix` | Volatility of VIX | real_time=true |
| `put_call_skew` | Demand for protection | strikes=[0.90, 1.10] |
| `gex` | Gamma exposure | net_exposure=true |
| `correlation_index` | Cross-asset correlations | basket=sp500 |
| `volatility_ratio` | Short/long vol ratio | periods=[5, 20] |
| `term_structure_slope` | Futures curve steepness | front_months=2 |
| `vol_of_vol` | Volatility clustering | window=10 |

## Feature List
- `contango_premium`: (vix_m2 - vix_spot) / vix_spot
- `vol_risk_premium`: iv_20d - rv_20d
- `regime_transition_score`: vix_percentile * term_structure_slope
- `mean_reversion_signal`: (vix - vix_ma_20) / vix_std_20
- `volatility_momentum`: rv_5d / rv_20d
- `skew_divergence`: put_skew - call_skew
- `compression_score`: vvix / vix
- `carry_roll`: daily_theta / position_value

## Entry/Exit Logic
- **Entry Long Vol**: VIX < 15th percentile + term structure steep + compression signal
- **Entry Short Vol**: VIX > 85th percentile + backwardation + mean reversion signal
- **Exit**: Target vol level reached or term structure normalizes
- **Risk Management**: Delta hedge with SPY, size by VVIX

## Risk Profile Defaults

| Profile | Position Size | Max VIX Exposure | Stop Loss | Min Contango |
|---------|--------------|------------------|-----------|--------------|
| Conservative | 2% | 10% | 20% | 5% |
| Balanced | 4% | 20% | 30% | 3% |
| Aggressive | 6% | 30% | 40% | 1% |

## Gate Overrides
```yaml
min_trades: 25
max_dd_pct: 35  # Volatility strategies have larger drawdowns
es95x: 2.5
spread_pct: 1.0
min_volume: 10000  # VIX products
fill_rate_pct: 90
max_slippage_usd: 0.10  # Per VIX point
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 0.7 | > 0.5 | > 0.3 |
| Win Rate | > 60% | > 55% | > 50% |
| Avg Winner/Loser | > 1.2 | > 1.5 | > 2.0 |
| Max Drawdown | < 25% | < 35% | < 50% |
| Turnover (annual) | < 100x | < 200x | < 300x |

## Risks and Failure Modes
- **Contango Decay**: Daily roll costs in VIX futures
- **Volatility Spikes**: Sudden VIX explosions (2018, 2020)
- **Correlation Breakdown**: Hedges fail during crisis
- **Liquidity Crunch**: Wide spreads during volatility events
- **Path Dependency**: Timing of volatility matters
- **Basis Risk**: VIX futures vs SPX options divergence

## Template YAML
```yaml
template:
  name: volpack_regime
  version: 0.1.0
  pack: volpack
indicators:
  - vix_term_structure
  - rv_iv_spread
  - vix_percentile
  - vvix
  - put_call_skew
  - gex
  - correlation_index
  - volatility_ratio
  - term_structure_slope
  - vol_of_vol
policy:
  execution:
    wait_for_confirmation: false
    position_sizing: vvix_scaled
    hedge_required: true
  risk:
    max_position_size: 0.04
    stop_loss_pct: 30
    vix_cap: 40
sweeps_defaults:
  thresholds: [[0.60, 0.65, 0.70], [0.65, 0.70, 0.75]]
  allowed_hours: [[9, 10], [15, 16]]
  top_pct: [0.05, 0.10]
```