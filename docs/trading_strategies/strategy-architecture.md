# Strategy Architecture

```mermaid
graph LR
  MD[(Market Data)] --> SIG[Signal Layer]
  IND[Indicator Sets] --> SIG
  SIG --> POL[Execution Policy]
  POL --> SIZ[Position Sizing]
  SIZ --> ORD[Order Manager]
  ORD --> EXC[Broker/Exchange]
  EXC --> FILL[Fills]
  FILL --> PNL[PnL & Risk]
  PNL --> MON[Monitoring]
  SIG --> BK[Backtest Engine]
  POL --> BK
  SIZ --> BK
```

Components
- Signal Layer: transforms indicator-set outputs into entry/exit events (rules or ML).
- Execution Policy: slippage, brackets (ATR/time), momentum gates, hours, liquidity rules.
- Position Sizing: fixed-fractional, volatility targeting, Kelly cap, max exposure/heat.
- Order Manager: child orders (limit/market), time-in-force, partial fills, retries.
- Risk Engine: drawdown monitors, exposure caps, circuit breakers, compliance rules.
- Backtest Engine: event-driven or vectorized sim with TX costs, splits, embargo.
- Monitoring: metrics, alerts, dashboards, logs, audit lineage.

State & Lineage
- Persist strategy config, policy version, indicator-set version, and git sha.
- Store run history: trades, orders, fills, PnL, and artifacts (plots/reports).

