# MicroPack Strategy Pack

## Purpose
Execute high-frequency microstructure strategies using order flow, book dynamics, and tick data.

## When to Use
- **Market Regime**: High liquidity environments with tight spreads
- **Asset Class**: Liquid futures (ES, NQ), major FX pairs, large-cap stocks
- **Horizon**: Seconds to minutes (ultra short-term)
- **Cadence**: Tick-by-tick with microsecond execution

## Required Data Sources
- Level 2 order book (full depth)
- Time and sales (tick data)
- Order flow imbalance
- Market microstructure metrics
- Exchange latency statistics

## Indicator Set

| Indicator | Purpose | Default Params |
|-----------|---------|----------------|
| `book_imbalance` | Bid/ask pressure | levels=10 |
| `order_flow_toxicity` | Adverse selection | window=100_ticks |
| `microprice` | Weighted mid price | weight=size |
| `trade_intensity` | Arrival rate | buckets=1_second |
| `quote_stuffing` | Spoofing detection | threshold=100_msgs |
| `effective_spread` | Execution cost | rolling=true |
| `kyle_lambda` | Price impact | window=500_trades |
| `vpin` | Volume-synchronized PIN | buckets=50 |
| `tick_rule` | Trade direction | aggregate=true |
| `queue_position` | Order book priority | track_cancels=true |

## Feature List
- `book_pressure`: (bid_size_weighted - ask_size_weighted) / total_size
- `flow_imbalance`: buy_volume - sell_volume over window
- `spread_relative`: (ask - bid) / mid
- `trade_velocity`: trades_per_second / avg_trades_per_second
- `toxicity_score`: vpin * kyle_lambda
- `book_stability`: 1 / order_book_update_frequency
- `execution_edge`: microprice - midprice
- `momentum_ticks`: consecutive_upticks - consecutive_downticks

## Entry/Exit Logic
- **Entry**: Book imbalance > threshold + positive order flow + microprice divergence
- **Exit**: Tick profit target or adverse selection signal or book flip
- **Execution**: Passive limit orders with queue priority management
- **Risk**: Cancel if toxicity score spikes or spread widens

## Risk Profile Defaults

| Profile | Position Size | Hold Time | Profit Target | Max Loss |
|---------|--------------|-----------|---------------|----------|
| Conservative | $10K | < 30 sec | 2 ticks | 1 tick |
| Balanced | $25K | < 60 sec | 3 ticks | 2 ticks |
| Aggressive | $50K | < 120 sec | 5 ticks | 3 ticks |

## Gate Overrides
```yaml
min_trades: 100  # High frequency requires many trades
max_dd_pct: 10  # Tight risk control
es95x: 1.2
spread_pct: 0.1  # Must capture tiny edges
min_volume: 1000000  # Need deep liquidity
fill_rate_pct: 98  # Execution quality critical
max_slippage_usd: 0.01  # Per share/contract
```

## Target Metrics

| Metric | Conservative | Balanced | Aggressive |
|--------|-------------|----------|------------|
| Sharpe Ratio | > 3.0 | > 2.5 | > 2.0 |
| Win Rate | > 60% | > 55% | > 52% |
| Avg Winner/Loser | > 1.0 | > 1.1 | > 1.2 |
| Max Drawdown | < 5% | < 8% | < 10% |
| Turnover (annual) | > 1000x | > 2000x | > 5000x |

## Risks and Failure Modes
- **Latency Risk**: Millisecond delays fatal
- **Adverse Selection**: Toxic flow identification
- **Technology Risk**: System outages, disconnections
- **Regulatory Risk**: Spoofing, manipulation rules
- **Competition**: HFT arms race
- **Flash Crashes**: Extreme microsecond moves

## Template YAML
```yaml
template:
  name: micropack_hft
  version: 0.1.0
  pack: micropack
indicators:
  - book_imbalance
  - order_flow_toxicity
  - microprice
  - trade_intensity
  - quote_stuffing
  - effective_spread
  - kyle_lambda
  - vpin
  - tick_rule
  - queue_position
policy:
  execution:
    wait_for_confirmation: false
    position_sizing: fixed_notional
    execution_algo: passive_aggressive
  risk:
    max_position_size: 50000  # Dollars
    stop_loss_pct: 0.1  # Tight stops
    max_hold_seconds: 120
sweeps_defaults:
  thresholds: [[0.52, 0.55, 0.58], [0.55, 0.58, 0.60]]
  allowed_hours: [[9, 10, 11, 14, 15]]  # Most liquid hours
  top_pct: [0.01, 0.02]  # Very selective
```