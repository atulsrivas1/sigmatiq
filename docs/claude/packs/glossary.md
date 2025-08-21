# Strategy Pack Glossary

## Common Terms

**ADX (Average Directional Index)**: Measures trend strength regardless of direction. Values above 25 indicate strong trend.

**Alpha**: Excess return above a benchmark. Positive alpha means outperforming the market.

**Backtest**: Testing a strategy on historical data to evaluate performance.

**Beta**: Measure of volatility relative to the market. Beta of 1.0 moves with market.

**Cadence**: Frequency of signal generation (daily, hourly, event-driven).

**Calibration**: Process of adjusting model parameters to match market conditions.

**Cointegration**: Statistical property where two series maintain a stable relationship over time.

**Contango**: Futures trading above spot price. Normal state for VIX futures.

**Drawdown**: Peak-to-trough decline in portfolio value. Maximum drawdown is worst loss.

**DTE (Days to Expiration)**: Number of days until option expires. 0DTE expires same day.

**Edge**: Statistical advantage that produces positive expected returns.

**ES95 (Expected Shortfall 95%)**: Average loss in worst 5% of scenarios.

**Ex-Dividend Date**: Date stock trades without dividend rights. Price typically drops by dividend amount.

**Fill Rate**: Percentage of orders successfully executed at desired price.

**Gate**: Quality control checkpoint that strategy must pass before deployment.

**Hedge Ratio**: Proportion of position offset by opposing position.

**Horizon**: Expected holding period for trades (intraday, swing, long-term).

**Implied Volatility (IV)**: Market's expectation of future volatility derived from option prices.

**Kelly Criterion**: Formula for optimal position sizing based on edge and odds.

**Leverage**: Using borrowed capital to increase position size.

**Lineage**: Complete audit trail of model versions and parameters.

**Market Neutral**: Strategy with no net market exposure (long equals short).

**Matrix**: Historical data table with features calculated for model training.

**Momentum Gate**: Filter requiring minimum momentum score before trade entry.

**NVT Ratio**: Network Value to Transactions ratio. Bitcoin valuation metric.

**OI (Open Interest)**: Total number of outstanding option contracts.

**Parity**: Options pricing relationship to underlying stock.

**PDUFA Date**: FDA drug approval decision deadline.

**Position Sizing**: Method for determining trade size based on risk.

**Realized Volatility (RV)**: Actual historical price volatility.

**Regime**: Current market environment (trending, ranging, volatile).

**Risk Profile**: Conservative, Balanced, or Aggressive settings affecting position size and risk.

**SHA**: Unique identifier hash for configuration versions.

**Sharpe Ratio**: Risk-adjusted return metric. Higher is better, above 1.0 is good.

**Slippage**: Difference between expected and actual execution price.

**Spread**: Difference between bid and ask prices.

**Sweep**: Testing multiple parameter combinations to find optimal settings.

**Term Structure**: Relationship between different maturity futures prices.

**Theta**: Daily option value decay from time passage.

**Threshold**: Confidence level required to trigger trade signal.

**Turnover**: How often portfolio is traded. Annual turnover of 12x means monthly trading.

**VPIN**: Volume-synchronized Probability of Informed Trading. Toxicity measure.

**VaR (Value at Risk)**: Maximum expected loss at given confidence level.

**Vega**: Option price sensitivity to implied volatility changes.

**VVIX**: Volatility of VIX. Measures uncertainty about volatility.

**Whipsaw**: Quick reversal causing losses on both sides.

**XGBoost**: Gradient boosting machine learning algorithm used for predictions.

**Z-Score**: Number of standard deviations from mean. Used for mean reversion signals.

## Pack-Specific Terms

### EarnPack
- **IV Crush**: Rapid decline in implied volatility after earnings announcement
- **Earnings Drift**: Price trend leading into earnings date
- **Analyst Dispersion**: Disagreement among analyst estimates

### TrendPack
- **EMA Ribbon**: Multiple exponential moving averages creating trend channel
- **Supertrend**: Dynamic support/resistance indicator
- **Parabolic SAR**: Stop and reverse points for trend following

### VolPack
- **Backwardation**: VIX futures trading below spot (rare, bearish)
- **GEX (Gamma Exposure)**: Market maker hedging pressure
- **Contango Premium**: Extra cost of futures over spot

### PairPack
- **Half-Life**: Time for spread to revert halfway to mean
- **Hurst Exponent**: Measure of mean reversion tendency
- **Kalman Filter**: Adaptive algorithm for dynamic hedge ratios

### MicroPack
- **Book Imbalance**: Bid vs ask size pressure in order book
- **Microprice**: Volume-weighted price better than mid
- **Kyle Lambda**: Price impact coefficient

### SeasonPack
- **Analog Years**: Historical years with similar patterns
- **Roll Yield**: Return from futures contract rolling
- **Window Momentum**: Strength within seasonal period

### CryptoPack
- **SOPR**: Spent Output Profit Ratio for Bitcoin
- **Hash Ribbons**: Miner capitulation indicator
- **DeFi TVL**: Total Value Locked in protocols

### DividPack
- **Capture Efficiency**: Percentage of dividend retained after ex-date drop
- **Aristocrat**: Company raising dividend 25+ consecutive years
- **Covered Call**: Selling call option against stock position

### EventPack
- **Binary Event**: Win/lose outcome like FDA approval
- **Sympathy Play**: Related stock moving with primary event
- **Halt Probability**: Chance of trading suspension

### RebalPack
- **Inclusion**: Stock added to index
- **Deletion**: Stock removed from index
- **Tracking Funds**: Total AUM following the index

## Risk Metrics

**Maximum Drawdown**: Largest peak-to-trough loss
**Win Rate**: Percentage of profitable trades
**Win/Loss Ratio**: Average winner divided by average loser
**Sortino Ratio**: Sharpe ratio using only downside volatility
**Calmar Ratio**: Annual return divided by maximum drawdown
**Information Ratio**: Active return divided by tracking error
**Tail Ratio**: Right tail divided by left tail size

## Execution Terms

**MOC (Market on Close)**: Order executed at closing price
**VWAP**: Volume-weighted average price benchmark
**TWAP**: Time-weighted average price execution
**Iceberg Order**: Large order split into smaller visible pieces
**Dark Pool**: Private exchange for large block trades
**Smart Routing**: Algorithm finding best execution venue

## Gate Requirements

**Minimum Trades**: Enough samples for statistical significance
**Maximum Drawdown**: Acceptable loss threshold
**ES95 Multiplier**: Tail risk limit
**Spread Percentage**: Maximum acceptable bid-ask spread
**Minimum OI**: Required options liquidity
**Minimum Volume**: Daily trading volume requirement
**Target Fill Rate**: Execution quality standard
**Maximum Slippage**: Acceptable execution cost