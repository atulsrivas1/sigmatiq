# Getting Started with Sigmatiq

Welcome to Sigmatiq! This guide will help you set up your account and create your first trading model in just a few minutes.

## What You'll Learn

By the end of this guide, you'll have:
- Set up your Sigmatiq account
- Created your first trading model
- Run a backtest to see how it performs
- Understood the basic workflow of the platform

## Step 1: Access the Platform

1. **Open Sigma Lab**: Navigate to the Sigma Lab interface (typically at `http://localhost:5173` for local development)
2. **Explore the Dashboard**: You'll see your dashboard with quick actions, recent models, and system health

## Step 2: Create Your First Model

Let's create a simple swing trading model for SPY (S&P 500 ETF):

### 2.1 Start the Model Creation Wizard
1. Click the **"Create Model"** button on your dashboard
2. You'll see template options organized by strategy type (packs)

### 2.2 Choose a Template
1. Select **"SwingSigma"** - this pack focuses on 2-10 day trades
2. Choose the **"SPY Equity Swing Daily"** template
3. This template uses proven swing trading indicators and settings

### 2.3 Configure Your Model
1. **Name**: Give your model a descriptive name like "My First Swing Model"
2. **Risk Profile**: Start with **"Conservative"** to learn with safe settings
   - Conservative: Lower position sizes, strict risk controls
   - Balanced: Moderate risk and return targets
   - Aggressive: Higher risk, higher potential returns

### 2.4 Create the Model
1. Click **"Create Model"**
2. Choose **"Go to Composer"** to start the Build-Train-Backtest process

## Step 3: Build Your Training Data

The Composer uses a three-step process: Build → Train → Backtest

### 3.1 Build Training Matrix
1. In the **Build** tab, you'll see date range selection
2. **Start Date**: Choose a date 6-12 months ago (e.g., if today is August 2025, choose February 2024)
3. **End Date**: Choose a more recent date (e.g., July 2025)
4. Click **"Build Matrix"**

**What's happening**: The system downloads historical price data and calculates technical indicators like moving averages, RSI, and momentum signals.

### 3.2 Review Matrix Profile
After building completes, you'll see:
- **Rows**: Number of data points (typically 100-500 for daily data)
- **Features**: Number of indicators (usually 20-50)
- **Quality Metrics**: Data completeness and balance

## Step 4: Run Your First Backtest

Skip the Training step for now and go directly to backtesting:

### 4.1 Navigate to Backtest Tab
1. Click the **"Backtest"** tab
2. You'll see configuration options

### 4.2 Run Single Backtest
1. Keep the default settings (threshold around 0.55)
2. Click **"Run Backtest"**
3. Wait 30-60 seconds for results

### 4.3 Interpret Results
Your backtest results will show:
- **Sharpe Ratio**: Risk-adjusted returns (>1.0 is good, >2.0 is excellent)
- **Total Return**: Cumulative percentage gain/loss
- **Number of Trades**: How often the model traded
- **Win Rate**: Percentage of profitable trades
- **Maximum Drawdown**: Worst losing streak

**Example Good Results:**
- Sharpe: 1.5
- Return: 15%
- Trades: 25
- Win Rate: 65%
- Max Drawdown: -5%

## Step 5: Understand What You Built

### Your Model Includes:
1. **Technical Indicators**: Mathematical calculations based on price and volume
   - Moving averages to identify trends
   - RSI to measure momentum
   - Volume indicators to confirm moves
   
2. **Risk Controls**: Automatic safety features
   - Position size limits
   - Stop-loss protections
   - Sector diversification rules

3. **Selection Logic**: How the model decides when to trade
   - Entry signals (when to buy)
   - Exit signals (when to sell)
   - Risk thresholds

## Step 6: Next Steps

### Option A: Improve Your Model
1. **Try Different Settings**: Go back to Build and try different date ranges
2. **Test Multiple Configurations**: Use the Sweeps feature to test many variations
3. **Compare Results**: Use the Leaderboard to compare different model versions

### Option B: Practice with Paper Trading
1. **Go to Sigma Sim**: Test your model in a realistic simulation
2. **Paper Trade**: Practice without risking real money
3. **Monitor Performance**: See how your model performs in current market conditions

### Option C: Explore Other Strategy Types
1. **ZeroSigma**: Try same-day options trading
2. **LongSigma**: Build long-term investment strategies
3. **OvernightSigma**: Explore gap trading strategies

## Common Questions

### "My model has poor performance - is this normal?"
Yes! Most initial models need refinement. Try:
- Different date ranges for training
- Alternative risk profiles
- Different strategy packs

### "What makes a good Sharpe ratio?"
- 0.5-1.0: Decent but improvable
- 1.0-2.0: Good risk-adjusted returns
- 2.0+: Excellent performance (rare but achievable)

### "How much data should I use for training?"
- **Minimum**: 3-6 months of data
- **Recommended**: 6-12 months
- **Maximum**: 2-3 years (more data isn't always better)

### "Should I start with Conservative or Aggressive risk?"
Always start with Conservative. You can increase risk later once you understand:
- How the model behaves
- Your personal risk tolerance
- The platform's safety features

## Safety Reminders

1. **Start with Paper Trading**: Never risk real money until you're comfortable
2. **Use Conservative Settings**: Begin with the safest options
3. **Understand Before You Trade**: Make sure you understand what your model does
4. **Check Gate Status**: Models with failing "gates" shouldn't be used for live trading

## Getting Help

- **AI Assistant**: Use the built-in AI helper for questions
- **Tooltips**: Hover over any feature for explanations
- **Documentation**: Return to this guide and the User Guide
- **Support**: Contact support for technical issues

## Quick Checklist

- [ ] Created your first model using a template
- [ ] Built a training matrix with historical data
- [ ] Run a backtest and interpreted results
- [ ] Understand basic performance metrics
- [ ] Know your next steps for improvement or paper trading

**Congratulations!** You've successfully created and tested your first trading model. You're now ready to explore more advanced features or start paper trading.

---

**Next**: Read the [Complete User Guide](user-guide.md) for in-depth explanations of all platform features.