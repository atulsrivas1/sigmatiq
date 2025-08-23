# The Build-Train-Backtest (BTB) Pipeline

## Your Complete Guide to Strategy Development

The BTB Pipeline is the heart of Sigmatiq - a systematic approach to creating, validating, and deploying trading strategies. Think of it as your strategy factory, turning ideas into validated, tradeable models.

## Understanding the Pipeline

### Why BTB?

Traditional trading often relies on:
- Gut feelings and hunches
- Incomplete testing
- Emotional decision-making
- Anecdotal evidence

The BTB Pipeline replaces this with:
- Data-driven decisions
- Comprehensive validation
- Systematic execution
- Statistical confidence

### The Three Stages Explained

#### 1. BUILD - Prepare Your Data 🔨

**What Happens**: Sigmatiq collects and organizes historical market data into a training matrix.

**Think of it like**: Gathering ingredients before cooking
- Stock prices (the main ingredient)
- Technical indicators (the spices)
- Market conditions (the cooking temperature)

**What You Control**:
- Date range for historical data
- Which indicators to include
- Data quality thresholds

**Output**: A training matrix (structured dataset)

#### 2. TRAIN - Create Your Model 🎯

**What Happens**: Machine learning algorithms learn patterns from your training data.

**Think of it like**: Teaching someone to recognize patterns
- Show examples of good trades
- Show examples of bad trades
- Let them learn the differences

**What You Control**:
- Algorithm type (usually XGBoost)
- Training parameters
- Validation splits

**Output**: A trained model (pattern recognizer)

#### 3. BACKTEST - Validate Performance 📈

**What Happens**: Test your model on historical data to see how it would have performed.

**Think of it like**: Taking practice exams before the real test
- Apply model to past data
- Simulate trades
- Calculate performance

**What You Control**:
- Test period
- Trading costs/slippage
- Position sizing

**Output**: Performance report with metrics

## Detailed Walkthrough

### Stage 1: BUILD - Data Preparation

#### Step 1: Select Your Model
Navigate to Models → Select your model → Click Composer → Build tab

#### Step 2: Configure Date Range

**Training Period Selection**:
- **Minimum**: 1 year (250 trading days)
- **Recommended**: 2-3 years
- **Maximum**: 5 years

**Considerations**:
- **Recent data** (1-2 years): Captures current market regime
- **Longer data** (3-5 years): Includes various market conditions
- **Very old data** (5+ years): May not reflect current markets

**Example Settings**:
```
Start Date: 2022-01-01
End Date: 2023-12-31
Result: 2 years, ~500 trading days
```

#### Step 3: Review Indicators

Your model template includes pre-selected indicators. Common ones:

**Trend Indicators**:
- Moving Averages (20, 50, 200-day)
- MACD (trend strength)
- ADX (trend quality)

**Momentum Indicators**:
- RSI (overbought/oversold)
- Stochastic (momentum shifts)
- Rate of Change

**Volatility Indicators**:
- ATR (average true range)
- Bollinger Bands
- Standard Deviation

**Volume Indicators**:
- Volume Moving Average
- On-Balance Volume
- Volume Rate of Change

#### Step 4: Build the Matrix

Click "Build Matrix" and monitor:

**Progress Indicators**:
- Data fetching (30 seconds)
- Indicator calculation (1 minute)
- Matrix construction (30 seconds)
- Quality validation (instant)

**Quality Metrics**:
```
Rows: 504 (trading days)
Features: 23 (indicators + price)
Missing Data: 0.1% (excellent)
Matrix SHA: 7f3a2b1 (unique identifier)
```

#### Step 5: Verify Matrix Quality

**Green Flags** ✅:
- Complete data (>99%)
- Sufficient rows (>250)
- Balanced features (10-50)
- No corrupted values

**Red Flags** ❌:
- Missing data (>5%)
- Too few rows (<100)
- Too many features (>100, overfitting risk)
- Data errors

### Stage 2: TRAIN - Model Creation

#### Step 1: Configure Training Parameters

**Algorithm Selection** (usually automatic):
- **XGBoost**: Best for most strategies (default)
- **Random Forest**: Good for simple patterns
- **Neural Network**: Complex patterns (advanced)

**Training/Validation Split**:
- **80/20 Split**: Standard approach
- 80% data for learning
- 20% for validation

**Cross-Validation**:
- **5-Fold**: Recommended
- Tests model robustness
- Prevents overfitting

#### Step 2: Set Trading Constraints

**Allowed Trading Hours**:
```
Market Hours: 9:30 AM - 4:00 PM ET
Pre-Market: 4:00 AM - 9:30 AM ET (optional)
After-Hours: 4:00 PM - 8:00 PM ET (optional)
```

**Position Constraints**:
- Maximum positions: 5-10
- Position size: 10-20% each
- Stop loss: 2-5%

#### Step 3: Start Training

Click "Train Model" and observe:

**Training Phases**:
1. **Data Loading** (10 seconds)
2. **Feature Engineering** (30 seconds)
3. **Model Training** (1-2 minutes)
4. **Validation** (30 seconds)
5. **Artifact Save** (instant)

**Training Metrics**:
```
Training Accuracy: 68%
Validation Accuracy: 65%
Feature Importance: RSI (18%), MA_20 (15%), Volume (12%)
Training Time: 2:34
```

#### Step 4: Understand Training Results

**Good Training Results**:
- Train/Validation accuracy similar (within 5%)
- Accuracy 55-75% (realistic)
- Clear feature importance
- Stable learning curve

**Warning Signs**:
- Train accuracy much higher than validation (overfitting)
- Accuracy >85% (too good to be true)
- Single dominant feature (over-reliance)
- Erratic learning curve

### Stage 3: BACKTEST - Performance Validation

#### Step 1: Configure Backtest

**Test Period**:
- **Out-of-Sample**: Data not used in training
- **Recent Period**: Last 6-12 months
- **Special Events**: Include market stress periods

**Trading Assumptions**:
```
Starting Capital: $10,000
Commission: $1 per trade
Slippage: 0.1% (realistic)
Spread: Bid-Ask included
```

#### Step 2: Run Backtest

Click "Run Backtest" and watch:

**Simulation Steps**:
1. **Initialize Portfolio** (instant)
2. **Generate Signals** (30 seconds)
3. **Execute Trades** (1 minute)
4. **Calculate Metrics** (30 seconds)
5. **Generate Report** (instant)

**Real-Time Display**:
- Trade entries (green arrows)
- Trade exits (red arrows)
- Equity curve building
- Drawdown periods

#### Step 3: Analyze Results

**Core Metrics**:

**Sharpe Ratio** (Risk-Adjusted Return):
- Below 0.5: Poor
- 0.5-1.0: Acceptable
- 1.0-2.0: Good
- Above 2.0: Excellent

**Total Return**:
- Annualized for comparison
- Compare to S&P 500 benchmark
- Account for inflation

**Win Rate**:
- 45-55%: Typical trend following
- 55-65%: Good balance
- 65-75%: Mean reversion
- Above 75%: Verify for realism

**Maximum Drawdown**:
- Under 10%: Conservative
- 10-20%: Moderate
- 20-30%: Aggressive
- Over 30%: High risk

**Trade Statistics**:
```
Total Trades: 52
Winning Trades: 31 (59.6%)
Losing Trades: 21 (40.4%)
Average Win: +2.3%
Average Loss: -1.1%
Largest Win: +5.8%
Largest Loss: -2.2% (stopped out)
Average Hold Time: 4.2 days
```

#### Step 4: Review Detailed Reports

**Equity Curve Analysis**:
- Smooth upward trend (ideal)
- Volatile but profitable (acceptable)
- Flat or declining (needs work)

**Monthly Returns Table**:
```
       Jan   Feb   Mar   Apr   May   Jun
2023  +2.1% -0.5% +3.2% +1.8% -1.2% +2.5%
2024  +1.5% +2.8% -0.3% +1.9% +0.7% +1.1%
```

**Trade Distribution**:
- Bell curve centered above zero (good)
- Long tail of winners (trend following)
- Tight distribution (consistent)

## Advanced BTB Techniques

### Optimization Through Sweeps

**What is a Sweep?**:
Run multiple BTB cycles with different parameters automatically.

**Parameters to Sweep**:
- Confidence thresholds (0.5, 0.6, 0.7)
- Trading hours (morning, afternoon, full day)
- Indicator periods (fast, medium, slow)

**Sweep Results**:
```
Config #1: Threshold=0.5, Hours=Full, Sharpe=1.2
Config #2: Threshold=0.6, Hours=Morning, Sharpe=1.8 ⭐
Config #3: Threshold=0.7, Hours=Full, Sharpe=0.9
```

### Walk-Forward Analysis

**What It Is**:
Continuously retrain your model with recent data.

**Process**:
1. Train on Year 1
2. Test on Month 13
3. Add Month 13 to training
4. Test on Month 14
5. Repeat...

**Benefits**:
- Adapts to changing markets
- More realistic testing
- Identifies strategy decay

### Monte Carlo Simulation

**What It Is**:
Run thousands of random variations to understand strategy robustness.

**Variations Include**:
- Random trade order
- Different start dates
- Variable slippage
- Position size changes

**Results Show**:
- Confidence intervals
- Worst-case scenarios
- Best-case scenarios
- Most likely outcome

## Common BTB Patterns

### Pattern 1: The Overfit Model

**Symptoms**:
- Amazing backtest results
- Poor live performance
- High training accuracy

**Solution**:
- Use more data
- Simplify model
- Add regularization

### Pattern 2: The Underfit Model

**Symptoms**:
- Poor backtest results
- Similar train/test accuracy
- Few trades

**Solution**:
- Add more indicators
- Adjust thresholds
- Extend time period

### Pattern 3: The Market-Dependent Model

**Symptoms**:
- Great in trends, fails in ranges
- Period-specific performance
- Inconsistent results

**Solution**:
- Add market regime filter
- Create multiple models
- Use adaptive parameters

## BTB Best Practices

### Data Quality

**Do's** ✅:
- Use adjusted price data
- Include dividends/splits
- Verify data sources
- Check for gaps/errors

**Don'ts** ❌:
- Use unadjusted prices
- Ignore corporate actions
- Mix data sources
- Include lookahead bias

### Training Discipline

**Do's** ✅:
- Reserve test data
- Use cross-validation
- Document parameters
- Track model versions

**Don'ts** ❌:
- Test on training data
- Skip validation
- Change parameters randomly
- Forget what you tested

### Backtesting Realism

**Do's** ✅:
- Include all costs
- Account for slippage
- Use realistic position sizes
- Consider market impact

**Don'ts** ❌:
- Ignore trading costs
- Assume perfect fills
- Use unrealistic leverage
- Trade illiquid assets

## Troubleshooting BTB Issues

### Issue: "Build Failed"

**Causes**:
- Data unavailable
- Invalid date range
- Network issues

**Solutions**:
- Check date range
- Verify ticker symbol
- Retry operation

### Issue: "Training Stuck"

**Causes**:
- Large dataset
- Complex model
- System resources

**Solutions**:
- Reduce date range
- Simplify model
- Close other apps

### Issue: "Poor Backtest Results"

**Causes**:
- Bad strategy logic
- Wrong market conditions
- Overtrading

**Solutions**:
- Review indicators
- Test different periods
- Adjust thresholds

## Interpreting Gate Results

### Pass Gate ✅

Your strategy passed if:
- Sharpe Ratio > 0.5
- Maximum Drawdown < 25%
- Number of Trades > 30
- Positive returns

**Next Steps**:
- Run sweeps for optimization
- Paper trade for validation
- Consider live trading

### Fail Gate ❌

Common failure reasons:

**"Insufficient Trades"** (< 30):
- Lower confidence threshold
- Extend test period
- Add more signals

**"Excessive Drawdown"** (> 25%):
- Tighten stop losses
- Reduce position size
- Add risk filters

**"Poor Risk-Adjusted Returns"**:
- Review strategy logic
- Test different markets
- Adjust parameters

## Moving from BTB to Live Trading

### The Graduation Process

1. **BTB Success** (You are here)
2. **Sweep Optimization** (Next step)
3. **Paper Trading** (2-4 weeks)
4. **Small Live Trading** ($1,000)
5. **Scale Up** (Gradually)

### Reality Check

**Backtest vs Reality**:
- Backtests are optimistic
- Expect 20-30% performance degradation
- Slippage impacts small accounts more
- Psychology affects execution

**Risk Management**:
- Start with 1/10th intended size
- Never risk more than 2% per trade
- Keep maximum 5 positions
- Use stop losses always

## Summary

The BTB Pipeline transforms trading from gambling to science:

**BUILD** → Organize historical data
**TRAIN** → Learn patterns
**BACKTEST** → Validate performance

Master this process and you'll:
- Create strategies systematically
- Validate before risking money
- Understand what works and why
- Trade with confidence

---

**Next**: Learn about [Sweeps and Optimization](sweeps.md) →