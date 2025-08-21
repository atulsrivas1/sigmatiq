# DividPack Strategy Pack

## Purpose
Capture dividend income with options enhancement and ex-dividend date arbitrage strategies.

## When to Use
- **Market Regime**: Stable to mildly bullish markets
- **Asset Class**: High-dividend stocks, REITs, dividend ETFs
- **Horizon**: 30-90 days (quarterly dividend cycles)
- **Cadence**: Monthly scanning, weekly adjustments

## Required Data Sources
- Dividend calendar and history
- Ex-dividend dates and amounts
- Options chains (30-90 DTE)
- Dividend growth rates
- Payout ratios and sustainability
- Share buyback announcements

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `dividend_yield` | Annual yield calculation | trailing=true |
| `ex_div_days` | Days to ex-dividend | forward_looking=90 |
| `payout_ratio` | Earnings payout percentage | ttm=true |
| `dividend_growth` | YoY growth rate | periods=5 |
| `option_premium` | Call premium available | dte=[30, 45, 60] |
| `implied_move` | Expected price change | to_ex_div=true |
| `dividend_coverage` | FCF coverage ratio | quarters=4 |
| `aristocrat_score` | Consistency rating | min_years=10 |
| `buyback_yield` | Share reduction rate | trailing_12m=true |
| `capture_spread` | Borrowing cost spread | institutional=true |

## Feature List
- `total_yield`: dividend_yield + option_premium_annualized
- `sustainability_score`: payout_ratio * dividend_coverage
- `capture_efficiency`: (dividend - expected_drop) / dividend
- `risk_adjusted_yield`: total_yield / implied_volatility
- `days_to_capture`: ex_div_days - settlement_days
- `assignment_probability`: delta * days_to_expiry_factor
- `dividend_surprise`: actual_div - expected_div
- `quality_score`: aristocrat_score * dividend_growth

## Entry/Exit Logic
- **Entry**: 30-45 days before ex-div + payout ratio < 70% + covered call setup
- **Exit**: After ex-dividend or if called away at profit
- **Enhancement**: Sell OTM calls 5-10% above for extra income
- **Protection**: Buy protective puts if yield > 8% (dividend cut risk)

## Risk Profile Defaults

| Profile | Position Size | Min Yield | Call Strike | Put Protection |
|---------|--------------|-----------|-------------|----------------|
| Conservative | 5% | 3% | 10% OTM | Yes if yield > 6% |
| Balanced | 8% | 2.5% | 7% OTM | Yes if yield > 8% |
| Aggressive | 12% | 2% | 5% OTM | No |

## Gate Overrides
```yaml
min_trades: 20
max_dd_pct: 15  # Lower volatility strategy
es95x: 1.5
spread_pct: 1.5  # Options spreads
min_volume: 100000
fill_rate_pct: 94
min_oi: 100  # Options liquidity
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 1.2 | > 1.0 | > 0.8 |
| Win Rate | > 75% | > 70% | > 65% |
| Avg Winner/Loser | > 1.0 | > 1.2 | > 1.5 |
| Max Drawdown | < 10% | < 15% | < 20% |
| Turnover (annual) | < 4x | < 6x | < 12x |

## Risks and Failure Modes
- **Dividend Cuts**: Reduction or suspension of dividends
- **Assignment Risk**: Early exercise on ITM calls
- **Ex-Dividend Drop**: Price drops more than dividend
- **Tax Implications**: Qualified vs non-qualified dividends
- **Corporate Actions**: Mergers, spinoffs affect dividends
- **Rate Risk**: Rising rates reduce dividend stock appeal

## Template YAML
```yaml
template:
  name: dividpack_enhanced
  version: 0.1.0
  pack: dividpack
indicators:
  - dividend_yield
  - ex_div_days
  - payout_ratio
  - dividend_growth
  - option_premium
  - implied_move
  - dividend_coverage
  - aristocrat_score
  - buyback_yield
  - capture_spread
policy:
  execution:
    wait_for_confirmation: true
    position_sizing: yield_weighted
    options_required: true
  risk:
    max_position_size: 0.12
    stop_loss_pct: 10
    min_dividend_yield: 0.02
sweeps_defaults:
  thresholds: [[0.55, 0.60, 0.65], [0.60, 0.65, 0.70]]
  allowed_hours: [[9, 10], [15]]
  top_pct: [0.15, 0.20]
```