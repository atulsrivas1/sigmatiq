# Trading Terms Glossary

## Your Complete Dictionary of Trading and Sigmatiq Terms

This glossary explains trading terms in plain English, helping you understand the language of markets and the Sigmatiq platform.

## A

### ADX (Average Directional Index)
**What it is**: A technical indicator that measures trend strength from 0-100.
**How to read it**: Above 25 = strong trend, below 20 = weak/no trend
**Example**: ADX at 40 means a very strong trend (up or down)

### Algorithm
**What it is**: A set of rules a computer follows to make trading decisions.
**In Sigmatiq**: Your strategy is converted into an algorithm
**Example**: "Buy when RSI < 30 AND price > 20-day average"

### Alpha
**What it is**: Returns above the market average.
**How it's measured**: Your return minus market return
**Example**: You made 15%, market made 10%, alpha = 5%

### API (Application Programming Interface)
**What it is**: A way for Sigmatiq to communicate with your broker.
**Why it matters**: Enables automated trading
**Example**: Sigmatiq sends buy order to broker via API

### Ask Price
**What it is**: The lowest price a seller will accept.
**Also called**: Offer price
**Example**: Bid $100.00, Ask $100.02 (you buy at ask)

### ATR (Average True Range)
**What it is**: Measures how much a stock typically moves per day.
**Use case**: Setting stop losses
**Example**: ATR = $2 means stock moves $2 daily on average

### At The Money (ATM)
**What it is**: An option whose strike price equals the current stock price.
**Example**: Stock at $100, $100 call option is ATM

## B

### Backtest
**What it is**: Testing a strategy on historical data.
**Purpose**: See how strategy would have performed
**In Sigmatiq**: Core feature in BTB pipeline

### Bear Market
**What it is**: Market declining 20% or more from recent highs.
**Duration**: Typically 6-18 months
**Strategy**: Consider defensive positions or cash

### Beta
**What it is**: How much a stock moves relative to the market.
**Reading**: Beta 1.5 = moves 50% more than market
**Example**: Market up 1%, high-beta stock up 1.5%

### Bid Price
**What it is**: The highest price a buyer will pay.
**Trading**: You sell at the bid price
**Example**: Bid $99.98, Ask $100.00

### Bid-Ask Spread
**What it is**: Difference between bid and ask prices.
**Impact**: Your immediate loss when buying
**Example**: Spread of $0.02 = 0.02% instant loss

### Bollinger Bands
**What it is**: Lines showing expected price range.
**Reading**: Price outside bands = extreme move
**Use**: Identify overbought/oversold conditions

### BTB (Build-Train-Backtest)
**What it is**: Sigmatiq's strategy development pipeline.
**Steps**: Build data → Train model → Backtest performance
**Purpose**: Systematic strategy creation

### Bull Market
**What it is**: Market rising 20% or more from recent lows.
**Characteristics**: Optimism, rising prices, economic growth
**Strategy**: More aggressive positions acceptable

### Buy and Hold
**What it is**: Buying stocks and keeping them long-term.
**Timeframe**: Years to decades
**Compare to**: Active trading in Sigmatiq

## C

### Calibration
**What it is**: Adjusting model probability outputs.
**Purpose**: Make predictions more accurate
**In Sigmatiq**: Automatic in training process

### Call Option
**What it is**: Right to buy stock at specific price.
**When to use**: When expecting price to rise
**Example**: $100 call = right to buy at $100

### Candlestick
**What it is**: Chart showing open, high, low, close prices.
**Colors**: Green/white = up, Red/black = down
**Information**: Shows price action in time period

### Capital
**What it is**: Money available for trading.
**Types**: Starting capital, working capital, reserve capital
**Management**: Never risk all capital

### Commission
**What it is**: Fee paid to broker per trade.
**Typical**: $0-7 per stock trade, $0.65 per option
**Impact**: Reduces profits, increases losses

### Confidence Threshold
**What it is**: Minimum probability to take a trade.
**In Sigmatiq**: Adjustable per strategy
**Example**: 70% threshold = only high-confidence trades

### Conservative (Risk Profile)
**What it is**: Sigmatiq's safest risk setting.
**Characteristics**: Small positions, tight stops, fewer trades
**For**: Beginners, risk-averse traders

### Correlation
**What it is**: How similarly two assets move.
**Range**: -1 (opposite) to +1 (identical)
**Use**: Diversification planning

### Cross-Validation
**What it is**: Testing strategy on multiple data segments.
**Purpose**: Ensure strategy isn't lucky
**In Sigmatiq**: Automatic in training

## D

### Day Trading
**What it is**: Buying and selling same day.
**Requirements**: $25,000 minimum (PDT rule)
**In Sigmatiq**: ZeroSigma strategies

### Derivative
**What it is**: Financial instrument based on another asset.
**Examples**: Options, futures
**Complexity**: Higher risk than stocks

### Divergence
**What it is**: When indicator disagrees with price.
**Significance**: Potential reversal signal
**Example**: Price up but RSI down

### Diversification
**What it is**: Spreading risk across multiple positions.
**Purpose**: Reduce impact of single loss
**Rule**: Don't put all eggs in one basket

### Dividend
**What it is**: Cash payment to shareholders.
**Frequency**: Usually quarterly
**Impact**: Reduces stock price on ex-dividend date

### Drawdown
**What it is**: Decline from peak to valley.
**Maximum Drawdown**: Largest decline experienced
**Acceptable**: Under 20% for most strategies

### DTE (Days to Expiration)
**What it is**: Days until option expires.
**0DTE**: Expires same day (ZeroSigma)
**Impact**: Less time = faster decay

## E

### EMA (Exponential Moving Average)
**What it is**: Average price giving more weight to recent data.
**Vs SMA**: Reacts faster to price changes
**Common**: 20, 50, 200-day EMAs

### Entry Signal
**What it is**: Conditions triggering a buy.
**In Sigmatiq**: Generated by your model
**Example**: "Buy when RSI < 30"

### Equity Curve
**What it is**: Graph of account value over time.
**Ideal**: Smooth upward slope
**Reality**: Has ups and downs

### ETF (Exchange-Traded Fund)
**What it is**: Basket of stocks trading as one.
**Popular**: SPY (S&P 500), QQQ (Nasdaq)
**Benefits**: Instant diversification

### Exit Signal
**What it is**: Conditions triggering a sell.
**Types**: Profit target, stop loss, time exit
**Importance**: More important than entry

### Expected Value
**What it is**: Average outcome if repeated many times.
**Formula**: (Win% × Win$) - (Loss% × Loss$)
**Positive**: Profitable long-term

## F

### Feature
**What it is**: Input data for machine learning.
**In Sigmatiq**: Technical indicators
**Example**: RSI, Volume, Moving Average

### Fill
**What it is**: Execution of your order.
**Types**: Full fill, partial fill
**Quality**: Affects actual vs expected performance

### Float
**What it is**: Shares available for public trading.
**Impact**: Low float = more volatile
**Consideration**: For liquidity planning

### FOMO (Fear of Missing Out)
**What it is**: Emotional urge to chase trades.
**Danger**: Leads to poor decisions
**Solution**: Stick to strategy rules

### Futures
**What it is**: Contract to buy/sell asset at future date.
**Leverage**: High (use caution)
**In Sigmatiq**: Coming soon

## G

### Gap
**What it is**: Price jump between close and next open.
**Types**: Gap up (higher), Gap down (lower)
**Strategy**: OvernightSigma trades gaps

### Gate System
**What it is**: Sigmatiq's quality control for strategies.
**Purpose**: Prevent trading poor strategies
**Criteria**: Sharpe, drawdown, trade count

### Greeks (Options)
**What they are**: Risk measures for options.
- **Delta**: Price sensitivity
- **Gamma**: Delta change rate
- **Theta**: Time decay
- **Vega**: Volatility sensitivity

## H

### Hedge
**What it is**: Position protecting against losses.
**Example**: Own stocks, buy puts for protection
**Cost**: Reduces profits but limits losses

### High-Frequency Trading (HFT)
**What it is**: Very fast automated trading.
**Speed**: Milliseconds
**In Sigmatiq**: Not HFT, but fast execution

### Historical Volatility
**What it is**: Past price movement magnitude.
**Calculation**: Standard deviation of returns
**Use**: Position sizing, risk management

### Hold Time
**What it is**: Duration position is kept.
**Varies by strategy**:
- ZeroSigma: Hours
- SwingSigma: Days
- LongSigma: Months

## I

### Implied Volatility (IV)
**What it is**: Market's expectation of future movement.
**High IV**: Expensive options
**Use**: Option strategy selection

### Indicator
**What it is**: Mathematical calculation from price/volume.
**Purpose**: Identify patterns and signals
**In Sigmatiq**: 70+ built-in indicators

### In The Money (ITM)
**What it is**: Option with intrinsic value.
**Call**: Strike below stock price
**Put**: Strike above stock price

## L

### Leverage
**What it is**: Using borrowed money to trade.
**Risk**: Amplifies gains AND losses
**Recommendation**: Avoid until experienced

### Limit Order
**What it is**: Order at specific price or better.
**Pro**: Control execution price
**Con**: May not fill

### Liquidity
**What it is**: Ease of buying/selling without moving price.
**High liquidity**: SPY, AAPL
**Low liquidity**: Small caps, penny stocks

### Long Position
**What it is**: Buying expecting price rise.
**Profit**: When price goes up
**Risk**: Limited to investment

## M

### MACD (Moving Average Convergence Divergence)
**What it is**: Trend-following momentum indicator.
**Signals**: Crossovers, divergences
**Components**: MACD line, signal line, histogram

### Margin
**What it is**: Borrowed money from broker.
**Requirements**: Typically 50% down
**Risk**: Margin calls if position drops

### Margin Call
**What it is**: Broker demand for more money.
**Trigger**: Account value below minimum
**Response required**: Add funds or close positions

### Market Cap
**What it is**: Total value of company's shares.
**Calculation**: Share price × shares outstanding
**Categories**: Large, mid, small cap

### Market Maker
**What it is**: Firm providing liquidity by quoting bid/ask.
**Role**: Enables smooth trading
**Profit**: From spread

### Market Order
**What it is**: Order to buy/sell immediately.
**Pro**: Guaranteed execution
**Con**: No price control

### Matrix (Training)
**What it is**: Historical data table for model training.
**Contains**: Prices, indicators, labels
**In Sigmatiq**: Built in BTB pipeline

### Maximum Drawdown
**What it is**: Largest peak-to-valley decline.
**Importance**: Key risk metric
**Acceptable**: Depends on risk tolerance

### Mean Reversion
**What it is**: Tendency for prices to return to average.
**Strategy**: Buy low, sell high
**Indicators**: Bollinger Bands, RSI

### Model
**What it is**: In Sigmatiq, your trading strategy.
**Components**: Indicators, rules, risk settings
**Output**: Buy/sell signals

### Model Card
**What it is**: Documentation of strategy details.
**Includes**: Logic, performance, assumptions
**Purpose**: Transparency and tracking

### Momentum
**What it is**: Speed of price change.
**Strategy**: Buy strength, sell weakness
**Opposite of**: Mean reversion

### Monte Carlo Simulation
**What it is**: Testing thousands of random scenarios.
**Purpose**: Understand strategy robustness
**Output**: Confidence intervals

### Moving Average
**What it is**: Average price over specific period.
**Types**: Simple (SMA), Exponential (EMA)
**Use**: Trend identification

## O

### Option
**What it is**: Contract to buy/sell at specific price.
**Types**: Calls (bullish), Puts (bearish)
**Complexity**: Higher than stocks

### Order Flow
**What it is**: Stream of buy/sell orders.
**Analysis**: Identifies institutional activity
**In Sigmatiq**: Part of ZeroSigma

### Out of The Money (OTM)
**What it is**: Option with no intrinsic value.
**Call**: Strike above stock price
**Put**: Strike below stock price

### Overfitting
**What it is**: Model memorizing instead of learning.
**Problem**: Great backtest, poor live performance
**Prevention**: Cross-validation, simplicity

## P

### P&L (Profit and Loss)
**What it is**: Money made or lost.
**Types**: Realized (closed), Unrealized (open)
**Tracking**: Essential for improvement

### Paper Trading
**What it is**: Simulated trading without real money.
**Purpose**: Practice and validation
**In Sigmatiq**: Always recommended first

### Pattern Day Trader (PDT)
**What it is**: Makes 4+ day trades in 5 days.
**Requirement**: $25,000 minimum account
**Applies to**: Margin accounts

### Penny Stocks
**What it is**: Stocks under $5.
**Risk**: High volatility, low liquidity
**Recommendation**: Avoid

### Pipeline (BTB)
**What it is**: Sigmatiq's Build-Train-Backtest process.
**Purpose**: Systematic strategy development
**Steps**: Data → Model → Validation

### Portfolio
**What it is**: Collection of all positions.
**Management**: Diversification, risk control
**In Sigmatiq**: Multiple strategy management

### Position
**What it is**: Investment in specific asset.
**Size**: Amount invested
**Management**: Entry, monitoring, exit

### Position Sizing
**What it is**: How much to invest per trade.
**Factors**: Risk tolerance, confidence, volatility
**Rule**: Never risk more than affordable loss

### Profit Factor
**What it is**: Gross profits divided by gross losses.
**Good**: Above 1.5
**Calculation**: Total wins / Total losses

### Profit Target
**What it is**: Predetermined exit price for gains.
**Purpose**: Lock in profits
**Setting**: Based on risk/reward ratio

### Put Option
**What it is**: Right to sell at specific price.
**When to use**: Expecting price decline
**Protection**: Can hedge long positions

## Q

### Quantitative Trading
**What it is**: Using math and data for trading.
**In Sigmatiq**: All strategies are quantitative
**Opposite**: Discretionary/gut trading

## R

### Rally
**What it is**: Strong upward price movement.
**Duration**: Days to months
**Trading**: Momentum strategies work well

### Resistance
**What it is**: Price level where selling increases.
**Behavior**: Price struggles to break above
**Trading**: Potential sell point

### Return
**What it is**: Profit or loss percentage.
**Calculation**: (End - Start) / Start × 100
**Annualized**: Adjusted to yearly basis

### Reversal
**What it is**: Change in price direction.
**Types**: Bullish (up), Bearish (down)
**Indicators**: Divergence, support/resistance

### Risk Management
**What it is**: Controlling potential losses.
**Tools**: Stop losses, position sizing, diversification
**Priority**: More important than returns

### Risk Profile
**What it is**: Sigmatiq's safety settings.
**Options**: Conservative, Balanced, Aggressive
**Impact**: Position size, stops, trade frequency

### Risk/Reward Ratio
**What it is**: Potential profit vs potential loss.
**Good ratio**: 2:1 or better
**Example**: Risk $100 to make $200

### RSI (Relative Strength Index)
**What it is**: Momentum oscillator 0-100.
**Overbought**: Above 70
**Oversold**: Below 30

## S

### Scalping
**What it is**: Very short-term trading for small profits.
**Hold time**: Seconds to minutes
**Not in Sigmatiq**: Too short-term

### Sharpe Ratio
**What it is**: Risk-adjusted return measure.
**Good**: Above 1.0
**Formula**: Return / Volatility

### Short Position
**What it is**: Selling borrowed shares, buy back later.
**Profit**: When price falls
**Risk**: Unlimited (price can rise infinitely)

### Signal
**What it is**: Trade recommendation from model.
**Types**: Buy, sell, hold
**In Sigmatiq**: Generated automatically

### Slippage
**What it is**: Difference between expected and actual price.
**Cause**: Market movement during execution
**Typical**: 0.1-0.5%

### SMA (Simple Moving Average)
**What it is**: Average price over period.
**Calculation**: Sum prices / period
**Use**: Trend identification

### Spread
**What it is**: Difference between bid and ask.
**Impact**: Transaction cost
**Tighter**: Better for trading

### Standard Deviation
**What it is**: Measure of price variability.
**Use**: Volatility calculation
**In strategies**: Position sizing

### Stochastic
**What it is**: Momentum indicator 0-100.
**Overbought**: Above 80
**Oversold**: Below 20

### Stop Loss
**What it is**: Order to sell at specific loss.
**Purpose**: Limit downside
**Essential**: Always use stops

### Strike Price
**What it is**: Price at which option can be exercised.
**Example**: $100 strike call = buy at $100
**Selection**: Based on strategy

### Support
**What it is**: Price level where buying increases.
**Behavior**: Price bounces up
**Trading**: Potential buy point

### Sweep (Sigmatiq)
**What it is**: Testing multiple strategy variations.
**Purpose**: Find optimal parameters
**Output**: Performance comparison

### Swing Trading
**What it is**: Holding positions 2-10 days.
**In Sigmatiq**: SwingSigma strategies
**Balance**: Between day trading and investing

## T

### Technical Analysis
**What it is**: Using charts and indicators to trade.
**Basis**: Price patterns repeat
**In Sigmatiq**: Foundation of strategies

### Theta (Time Decay)
**What it is**: Daily option value loss.
**Impact**: Accelerates near expiration
**ZeroSigma**: High theta risk

### Ticker
**What it is**: Stock symbol.
**Examples**: AAPL (Apple), SPY (S&P 500)
**In Sigmatiq**: Asset selection

### Time Stop
**What it is**: Exit after specific duration.
**Purpose**: Avoid dead money
**Example**: Exit after 10 days

### Trailing Stop
**What it is**: Stop that follows price up.
**Purpose**: Lock in profits
**Example**: 5% below highest price

### Trend
**What it is**: General price direction.
**Types**: Uptrend, downtrend, sideways
**Trading**: "Trend is your friend"

## U

### Underlying
**What it is**: Asset an option is based on.
**Example**: AAPL stock for AAPL options
**Importance**: Drives option value

## V

### VIX
**What it is**: Volatility Index, "fear gauge".
**Reading**: High = fear, Low = complacency
**Trading**: Above 30 = high volatility

### Volatility
**What it is**: How much price moves.
**Types**: Historical, Implied
**Impact**: Position sizing, option pricing

### Volume
**What it is**: Number of shares traded.
**Significance**: Confirms price moves
**High volume**: Strong conviction

### VWAP (Volume-Weighted Average Price)
**What it is**: Average price weighted by volume.
**Use**: Institutional benchmark
**Trading**: Support/resistance level

## W

### Whipsaw
**What it is**: Quick reversal causing losses.
**Cause**: Volatile, choppy markets
**Prevention**: Wider stops, fewer trades

### Win Rate
**What it is**: Percentage of profitable trades.
**Good**: Above 50%
**Note**: Not everything - size matters

## X

### XGBoost
**What it is**: Machine learning algorithm.
**In Sigmatiq**: Default model type
**Strength**: Handles complex patterns

## Y

### Yield
**What it is**: Income return on investment.
**Dividend Yield**: Annual dividend / price
**Different from**: Capital gains

## Z

### Zero-Sum
**What it is**: One trader's gain = another's loss.
**Options**: Zero-sum game
**Stocks**: Not zero-sum (can all win)

### ZeroSigma
**What it is**: Sigmatiq's 0DTE options strategy pack.
**Risk**: Very high
**For**: Experienced traders only

---

## Common Phrases

### "Buy the dip"
**Meaning**: Purchase during price decline.
**Strategy**: Mean reversion
**Risk**: Catching falling knife

### "Catching a falling knife"
**Meaning**: Buying something dropping fast.
**Danger**: Can keep falling
**Better**: Wait for stabilization

### "Dead cat bounce"
**Meaning**: Brief recovery in downtrend.
**Warning**: Not real reversal
**Action**: Don't chase

### "Diamond hands"
**Meaning**: Holding despite volatility.
**Pro**: Conviction in thesis
**Con**: Ignoring stop losses

### "HODL"
**Meaning**: Hold on for dear life.
**Origin**: Crypto community
**In Sigmatiq**: Use stops instead

### "Paper hands"
**Meaning**: Selling too quickly.
**Problem**: Missing bigger moves
**Solution**: Follow strategy rules

### "Pump and dump"
**Meaning**: Artificial price inflation then sell.
**Illegal**: Market manipulation
**Avoid**: Suspicious promotions

### "The trend is your friend"
**Meaning**: Trade with market direction.
**Strategy**: Momentum trading
**Until**: "The bend at the end"

---

**Need more definitions?** Use the AI Assistant or check the documentation for detailed explanations.