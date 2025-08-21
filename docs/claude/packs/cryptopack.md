# CryptoPack Strategy Pack

## Purpose
Trade cryptocurrency markets using on-chain metrics, DeFi flows, and 24/7 market dynamics.

## When to Use
- **Market Regime**: Crypto bull/bear cycles, DeFi seasons
- **Asset Class**: BTC, ETH, major altcoins, DeFi tokens
- **Horizon**: 1-14 days (crypto cycles are faster)
- **Cadence**: 24/7 monitoring with 4-hour candles

## Required Data Sources
- On-chain metrics (Glassnode, Santiment)
- Exchange flows and reserves
- DeFi TVL and yields
- Social sentiment (Twitter, Reddit)
- Funding rates and open interest
- Whale wallet tracking

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `nvt_ratio` | Network value to transactions | window=30 |
| `exchange_flow` | Exchange in/outflows | timeframe=24h |
| `funding_rate` | Perpetual funding | exchanges=[binance, ftx] |
| `hash_ribbons` | Miner capitulation | ma_short=30, ma_long=60 |
| `sopr` | Spent output profit ratio | adjusted=true |
| `whale_accumulation` | Large wallet changes | min_size=1000_btc |
| `defi_tvl` | Total value locked | protocols=top_20 |
| `social_volume` | Mention frequency | sources=[twitter, reddit] |
| `long_short_ratio` | Positioning sentiment | aggregate=true |
| `mvrv_zscore` | Market value to realized | window=365 |

## Feature List
- `on_chain_momentum`: nvt_trend * exchange_outflow
- `sentiment_composite`: social_volume * (long_short_ratio - 1)
- `smart_money_flow`: whale_accumulation - retail_selling
- `defi_rotation`: tvl_change_7d / tvl_change_30d
- `funding_divergence`: spot_price_change - funding_rate
- `capitulation_score`: hash_ribbons * sopr
- `alt_season_index`: alt_dominance / btc_dominance
- `volatility_regime`: realized_vol_7d / realized_vol_30d

## Entry/Exit Logic
- **Entry**: Exchange outflows + negative funding + MVRV < 1 + whale accumulation
- **Exit**: Exchange inflows + extreme funding + MVRV > 3 or stop loss
- **DeFi Entry**: TVL expansion + yield compression + governance token momentum
- **Risk**: Position size inverse to volatility, mandatory stops

## Risk Profile Defaults

| Profile | Position Size | Leverage | Stop Loss | Min Volume |
|---------|--------------|----------|-----------|------------|
| Conservative | 2% | None | 15% | $10M |
| Balanced | 5% | 2x | 20% | $5M |
| Aggressive | 8% | 3x | 25% | $1M |

## Gate Overrides
```yaml
min_trades: 30
max_dd_pct: 40  # Crypto is volatile
es95x: 3.0  # Higher tail risk
spread_pct: 0.3  # Major pairs only
min_volume: 1000000  # USD daily volume
fill_rate_pct: 95
max_slippage_usd: 0.005  # 50 bps
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 1.0 | > 0.8 | > 0.6 |
| Win Rate | > 50% | > 45% | > 40% |
| Avg Winner/Loser | > 2.0 | > 2.5 | > 3.0 |
| Max Drawdown | < 30% | < 40% | < 50% |
| Turnover (annual) | < 50x | < 100x | < 200x |

## Risks and Failure Modes
- **Regulatory Risk**: Sudden bans or restrictions
- **Exchange Risk**: Hacks, insolvency (FTX, Mt. Gox)
- **Smart Contract Risk**: DeFi protocol exploits
- **Liquidity Risk**: Thin order books, withdrawal freezes
- **Correlation Risk**: Everything correlates in crashes
- **24/7 Risk**: Markets never close, gaps common
- **Stablecoin Risk**: Depeg events (USDT, USDC)

## Template YAML
```yaml
template:
  name: cryptopack_onchain
  version: 0.1.0
  pack: cryptopack
indicators:
  - nvt_ratio
  - exchange_flow
  - funding_rate
  - hash_ribbons
  - sopr
  - whale_accumulation
  - defi_tvl
  - social_volume
  - long_short_ratio
  - mvrv_zscore
policy:
  execution:
    wait_for_confirmation: false
    position_sizing: vol_adjusted
    rebalance_frequency: daily
  risk:
    max_position_size: 0.08
    stop_loss_pct: 20
    correlation_limit: 0.7
sweeps_defaults:
  thresholds: [[0.55, 0.60, 0.65], [0.60, 0.65, 0.70]]
  allowed_hours: []  # 24/7 market
  top_pct: [0.10, 0.15]
```