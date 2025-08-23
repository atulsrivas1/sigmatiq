# Creating Your First Trading Strategy

## A Step-by-Step Tutorial

This tutorial will walk you through creating, testing, and evaluating your first trading strategy in Sigmatiq. We'll build a simple but effective swing trading strategy for the S&P 500 (SPY).

## What We're Building

**Strategy Name**: SPY Swing Trader
**Type**: Swing Trading (2-10 day holds)
**Asset**: SPY (S&P 500 ETF)
**Risk Level**: Conservative
**Time Required**: 15 minutes

## Why Start with SPY?

SPY is perfect for beginners because it:
- Has high liquidity (easy to buy/sell)
- Represents 500 companies (built-in diversification)
- Moves predictably (fewer surprises)
- Has extensive historical data

## Step 1: Navigate to Models

1. Click **Models** in the left sidebar
2. Click the **Create Model** button (usually green or blue)
3. You'll see the template selection screen

## Step 2: Select a Template

### Available Templates

You'll see template cards like:

#### 📊 SPY Swing Classic
- **Indicators**: RSI, Moving Averages
- **Holding Period**: 2-10 days
- **Signals per Month**: 3-5
- **Best Market**: All conditions

#### 🎯 SPY Momentum
- **Indicators**: MACD, ADX
- **Holding Period**: 5-15 days
- **Signals per Month**: 2-4
- **Best Market**: Trending

#### 🔄 SPY Mean Reversion
- **Indicators**: Bollinger Bands, RSI
- **Holding Period**: 1-5 days
- **Signals per Month**: 5-8
- **Best Market**: Ranging

**For this tutorial**, select **SPY Swing Classic**

## Step 3: Configure Your Model

### Name Your Model
Enter: "My First SPY Strategy" (or choose your own name)

### Select Risk Profile

Choose **Conservative** for your first model:
- ✅ Maximum 5% position size
- ✅ Stop loss at 2%
- ✅ Strict trade quality requirements

### Review Indicators

The template includes these indicators (pre-configured):

#### RSI (Relative Strength Index)
- **What it does**: Measures if stock is overbought/oversold
- **Setting**: 14-period
- **Signal**: Buy when RSI < 30, Sell when RSI > 70

#### EMA (Exponential Moving Average)
- **What it does**: Shows trend direction
- **Settings**: 20-day and 50-day
- **Signal**: Buy when price crosses above, sell below

#### Volume
- **What it does**: Confirms price movements
- **Setting**: 20-day average
- **Signal**: Higher volume = stronger signal

You don't need to change these - they're optimized for SPY.

### Click "Create Model"

Your model is now created! You'll see a confirmation message.

## Step 4: Build the Training Data

### Navigate to Composer
1. Click on your new model in the list
2. Select the **Composer** tab
3. You'll see three sub-tabs: Build, Train, Backtest

### Build Tab Settings

#### Date Range
Select your training period:
- **Start Date**: January 1, 2022
- **End Date**: December 31, 2023
- **Why these dates**: Includes bull, bear, and sideways markets

#### Data Quality Check
The system will show:
- ✅ Data availability: 100%
- ✅ Trading days: ~500
- ✅ Market conditions: Varied

#### Click "Build Matrix"

This creates your training dataset. You'll see:
- Progress bar showing data collection
- Row count (expect ~500)
- Feature count (expect ~15-20)

**Wait time**: 1-2 minutes

## Step 5: Train Your Model

### Switch to Train Tab

Once building completes, click the **Train** tab.

### Training Configuration

#### Allowed Trading Hours
Default is market hours (9:30 AM - 4:00 PM ET)
- Keep default for stocks
- Can customize for futures/crypto

#### Model Type
Template selects **XGBoost** (advanced machine learning)
- Don't worry about technical details
- Think of it as pattern recognition

#### Click "Start Training"

You'll see:
- Training progress (0% to 100%)
- Validation metrics appearing
- Model artifacts being saved

**Wait time**: 2-3 minutes

## Step 6: Run Your First Backtest

### Switch to Backtest Tab

After training completes, click **Backtest**.

### Backtest Settings

#### Test Period
Automatically set to out-of-sample data:
- Uses recent 6 months not seen in training
- Prevents overfitting (memorizing vs learning)

#### Capital Allocation
- **Starting Capital**: $10,000 (simulation)
- **Position Sizing**: According to risk profile
- **Commission**: $1 per trade (realistic)

#### Click "Run Backtest"

Watch the simulation:
- Trade entries and exits plotting
- Equity curve building
- Metrics calculating

**Wait time**: 1-2 minutes

## Step 7: Understand Your Results

### Performance Dashboard

Your results appear in several sections:

#### Summary Metrics

**Example Results** (yours will vary):
- **Total Return**: +12.3%
- **Sharpe Ratio**: 1.45
- **Win Rate**: 58%
- **Total Trades**: 42
- **Max Drawdown**: -4.2%

#### What These Mean

**Total Return: +12.3%**
- Your $10,000 became $11,230
- Better than S&P 500 average (~10% annually)
- Remember: Past performance ≠ future results

**Sharpe Ratio: 1.45**
- Risk-adjusted return measure
- Above 1.0 is good
- Yours shows solid risk/reward balance

**Win Rate: 58%**
- Won 24 trades, lost 18
- Above 50% is positive
- Quality matters more than quantity

**Max Drawdown: -4.2%**
- Largest loss from peak
- Under 5% is conservative
- Shows good risk management

### Equity Curve

The chart shows your account value over time:
- **Green line**: Your strategy
- **Gray line**: Buy and hold comparison
- **Red areas**: Drawdown periods

Look for:
- Steady upward trend
- Shallow drawdowns
- Consistent growth

### Trade Analysis

#### Trade Distribution
- **Long trades**: Buying expecting price rise
- **Short trades**: None (this strategy is long-only)
- **Average hold time**: 4.5 days
- **Best trade**: +3.2%
- **Worst trade**: -2.0% (stopped out)

#### Win/Loss Analysis
- **Average win**: +1.8%
- **Average loss**: -0.9%
- **Win/Loss ratio**: 2:1 (good!)

### Gate Status

Your model shows: ✅ **PASS GATE**

This means:
- Sufficient sample size (30+ trades)
- Acceptable risk metrics
- Positive risk-adjusted returns
- Ready for next steps

## Step 8: Optimize with Sweeps

### What is a Sweep?

A sweep tests multiple variations to find optimal settings:
- Different confidence thresholds
- Various trading hours
- Multiple risk levels

### Running Your First Sweep

1. Click **Sweeps** in the navigation
2. Select your model
3. Choose **Conservative Sweep** preset

#### Sweep Configuration
- **Variations**: 9 (3x3 grid)
- **Parameters**: Threshold and hours
- **Estimated time**: 5-10 minutes

#### What Happens
The system will test combinations like:
- High confidence + morning trading
- Medium confidence + full day trading
- Low confidence + afternoon trading

### Understanding Sweep Results

You'll see a table with all variations:

| Config | Sharpe | Return | Trades | Gate |
|--------|--------|--------|--------|------|
| High/AM | 1.82 | 10.2% | 28 | ❌ |
| Med/Full | 1.45 | 12.3% | 42 | ✅ |
| Low/PM | 0.91 | 8.7% | 61 | ✅ |

**Best performer**: Medium confidence, full day (your original!)

## Step 9: Save and Document

### Create Model Card

Click **Generate Model Card** to document:
- Strategy logic
- Performance metrics
- Risk parameters
- Assumptions

### Add Notes

In the notes section, record:
- Why you created this strategy
- What you learned
- Ideas for improvement

Example:
```
First strategy - SPY swing trading
- Works well in normal markets
- Struggles in high volatility
- Consider adding VIX filter
```

## Step 10: Next Steps

### Immediate Actions

1. **Paper Trade** (Recommended)
   - Test with simulated money
   - Run for 2-4 weeks
   - Compare to backtest

2. **Create Variations**
   - Try different templates
   - Adjust parameters
   - Test other assets

3. **Join Leaderboard**
   - Compare to other strategies
   - Learn from top performers
   - Share insights

### Learning Exercises

#### Exercise 1: Create QQQ Strategy
- Use same template
- Apply to QQQ (tech stocks)
- Compare results to SPY

#### Exercise 2: Adjust Risk Profile
- Clone your model
- Change to "Balanced"
- See how results change

#### Exercise 3: Different Time Period
- Test 2020-2021 (bull market)
- Test 2022 (bear market)
- Understand market dependence

## Common Issues and Solutions

### "My model failed the gate"

**Possible causes**:
- Too few trades (< 30)
- High drawdown (> 10%)
- Negative returns

**Solutions**:
- Extend test period
- Adjust confidence threshold
- Try different template

### "Results seem too good"

**Red flags**:
- Returns over 50% annually
- Win rate over 80%
- No losing months

**What to check**:
- Look for look-ahead bias
- Verify realistic trading costs
- Test different time periods

### "I don't understand the indicators"

**Learning resources**:
- Click indicator names for explanations
- Use AI assistant for plain English
- Start with simpler templates

## Tips for Success

### Do's ✅
- Start with templates
- Test multiple strategies
- Keep risk conservative initially
- Document everything
- Paper trade first

### Don'ts ❌
- Risk real money immediately
- Ignore risk metrics
- Over-optimize (curve fitting)
- Trade without understanding
- Expect immediate profits

## Congratulations!

You've successfully:
- Created your first trading model
- Run a complete backtest
- Understood the results
- Learned optimization basics

### Your Progress

- [x] Account setup
- [x] First model created
- [x] Backtest completed
- [x] Results analyzed
- [ ] Paper trading started
- [ ] Real trading approved

## What's Next?

1. **Read**: [Understanding Risk Profiles](risk-profiles.md)
2. **Try**: Create 2-3 more models this week
3. **Learn**: Watch video tutorials on advanced features
4. **Connect**: Join the community forum

Remember: **Trading is a marathon, not a sprint.** Take time to learn, test thoroughly, and never risk more than you can afford to lose.

---

Questions? Click the **AI Assistant** icon or see our [FAQ](../faqs/common-questions.md)