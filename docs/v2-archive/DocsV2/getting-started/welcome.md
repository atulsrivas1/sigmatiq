# Welcome to Sigmatiq

## Your Journey to Smarter Trading Starts Here

Welcome to Sigmatiq! Whether you're new to algorithmic trading or an experienced trader looking for better tools, this guide will help you get up and running quickly.

## What You'll Learn

In this guide, we'll cover:
1. Setting up your account
2. Understanding the dashboard
3. Choosing your risk profile
4. Creating your first trading model
5. Running your first backtest
6. Understanding results

## Before You Begin

### What You Need
- A modern web browser (Chrome, Firefox, Safari, or Edge)
- 15-30 minutes for initial setup
- Basic understanding of stock market concepts

### What You Don't Need
- Programming knowledge
- Advanced mathematics
- Large amounts of capital
- Previous algorithmic trading experience

## Understanding Sigmatiq's Approach

Sigmatiq uses a systematic approach to trading that removes emotion and guesswork:

### The Build-Train-Backtest (BTB) Pipeline

Think of it like training an athlete:
1. **Build** - Design the training program (create your trading strategy)
2. **Train** - Practice the techniques (teach the model using historical data)
3. **Backtest** - Measure performance (test how well it would have worked)

This approach ensures every trading decision is based on data, not hunches.

## Your First Login

When you first access Sigmatiq, you'll see:

### The Dashboard
Your command center showing:
- **Recent Models** - Your trading strategies at a glance
- **Last Runs** - Recent backtest results
- **Quick Actions** - One-click access to common tasks
- **System Health** - Platform status indicators

### Navigation Menu
On the left side:
- **Dashboard** - Your home base
- **Models** - Create and manage trading strategies
- **Signals** - Monitor trading opportunities
- **Sweeps** - Run multiple backtests
- **Leaderboard** - Compare strategy performance

## Choosing Your Risk Profile

Before creating your first model, you'll select a risk profile. This is like choosing the difficulty level in a game:

### 🛡️ Conservative (Recommended for Beginners)
- **What it means**: Prioritize capital preservation
- **Trade frequency**: Fewer, higher-confidence trades
- **Drawdown limits**: Strict (max 5-8% loss)
- **Position sizes**: Smaller (1-2% per trade)
- **Best for**: New users, risk-averse investors

### ⚖️ Balanced (Default Setting)
- **What it means**: Balance growth with protection
- **Trade frequency**: Moderate number of trades
- **Drawdown limits**: Moderate (max 10-15% loss)
- **Position sizes**: Standard (2-5% per trade)
- **Best for**: Most users, steady growth seekers

### 🚀 Aggressive (Experienced Users)
- **What it means**: Maximize returns, accept higher risk
- **Trade frequency**: More trades, lower thresholds
- **Drawdown limits**: Flexible (max 20-25% loss)
- **Position sizes**: Larger (5-10% per trade)
- **Best for**: Experienced traders, high risk tolerance

You can change your risk profile anytime, and different models can use different profiles.

## Creating Your First Model

### Step 1: Choose a Template

Click "Create Model" and you'll see strategy templates:

**For Your First Model, We Recommend:**
- **SPY Swing Trading** - Trade the S&P 500 ETF over 2-10 days
- **Simple Momentum** - Follow strong trends in major stocks
- **Mean Reversion** - Buy oversold, sell overbought conditions

Each template includes:
- Pre-selected indicators
- Tested parameters
- Appropriate risk settings

### Step 2: Name Your Model

Choose a descriptive name like:
- "My First Swing Strategy"
- "Test SPY Momentum"
- "Learning Model 1"

The name helps you track multiple strategies later.

### Step 3: Review Settings

The template provides good defaults, but you can see:
- **Indicators** - Technical analysis tools (RSI, Moving Averages, etc.)
- **Time Frame** - How often to check for signals
- **Asset Type** - Stocks or options
- **Risk Controls** - Stop losses and position limits

Don't worry about changing these yet - templates are pre-optimized.

## Running Your First Backtest

### What is a Backtest?

A backtest is like a time machine - it shows how your strategy would have performed if you had traded it in the past. This helps validate ideas before risking real money.

### Starting the Backtest

1. Click on your new model
2. Go to the "Composer" tab
3. Select "Build" to prepare historical data
4. Choose your date range (we recommend 2 years)
5. Click "Run Backtest"

### Understanding the Progress

You'll see:
- **Building Matrix** - Gathering historical data
- **Training Model** - Learning patterns
- **Running Simulation** - Testing trades
- **Generating Report** - Creating results

This typically takes 2-5 minutes.

## Understanding Your Results

### Key Metrics Explained

When your backtest completes, you'll see:

#### Sharpe Ratio (Risk-Adjusted Returns)
- **What it means**: Return per unit of risk
- **Good**: Above 1.0
- **Excellent**: Above 2.0
- **Poor**: Below 0.5

#### Total Return
- **What it means**: How much money you would have made
- **Example**: 15% means $10,000 becomes $11,500

#### Win Rate
- **What it means**: Percentage of profitable trades
- **Good**: Above 55%
- **Note**: High win rate doesn't always mean profitable

#### Maximum Drawdown
- **What it means**: Largest peak-to-valley loss
- **Acceptable**: Under 15%
- **Concerning**: Over 25%

#### Number of Trades
- **What it means**: How active the strategy is
- **Minimum**: 30+ for statistical significance

### The Gate System

Sigmatiq automatically evaluates results:

✅ **Pass Gate** - Strategy meets quality standards:
- Sufficient trades
- Acceptable risk metrics
- Positive performance

❌ **Fail Gate** - Strategy needs work:
- Too few trades
- Excessive drawdown
- Poor risk-adjusted returns

Only "Pass Gate" strategies should be considered for real trading.

## Next Steps

### Immediate Actions

1. **Run a Sweep** - Test multiple variations automatically
2. **Compare Models** - Use the Leaderboard to rank strategies
3. **Paper Trade** - Test with simulated money (Sigma Sim)

### Learning Path

1. **Week 1** - Create 3-5 models using templates
2. **Week 2** - Customize indicators and parameters
3. **Week 3** - Understand sweep optimization
4. **Week 4** - Begin paper trading best performers

### Resources

- **Help Icon** - Context-sensitive help on every page
- **AI Assistant** - Ask questions in plain English
- **Model Cards** - Detailed explanations of each strategy
- **Video Tutorials** - Step-by-step walkthroughs

## Common Questions

### "How much money do I need?"
Start with paper trading (free). When ready for real trading, $1,000-$5,000 is typical, though you can start smaller.

### "How long before I see results?"
- Backtests: Immediate (2-5 minutes)
- Paper trading: 1-2 weeks for meaningful data
- Real trading: 1-3 months for statistical significance

### "What if my first model fails?"
This is normal and expected! Most professional traders test dozens of strategies. Each "failure" teaches you what doesn't work.

### "Should I trust the backtest results?"
Backtests are helpful but imperfect. They assume:
- You could have executed at shown prices
- Market conditions remain similar
- No significant slippage

Always paper trade before using real money.

## Getting Help

### If You're Stuck

1. **? Button** - Click for page-specific help
2. **AI Assistant** - Describe your problem in plain English
3. **Reset** - You can always delete models and start over
4. **Support** - Contact us via the Help menu

### Warning Signs

Stop and seek help if:
- Results seem too good to be true (300%+ returns)
- You don't understand what a model is doing
- You're tempted to risk more than you can afford to lose
- The platform behaves unexpectedly

## Your Sigmatiq Journey

### Month 1: Learning
- Create multiple models
- Understand backtesting
- Learn risk management

### Month 2: Refining
- Optimize strategies
- Paper trade best models
- Study the market

### Month 3: Graduating
- Consider real trading
- Start small
- Track everything

Remember: **Every expert was once a beginner.** Take your time, learn the platform, and never risk more than you can afford to lose.

---

Ready to create your first model? [Click here to begin →](first-strategy.md)