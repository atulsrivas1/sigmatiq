# Run a Backtest Workflow

## How to Test Your Strategy with Historical Data

This guide shows you how to backtest your model - testing it on past market data to see how it would have performed.

## What You'll Need

- A created model
- 5-10 minutes
- Understanding of basic results

## The Three-Step Process

Backtesting follows the BTB pipeline:
1. **Build** - Gather historical data
2. **Train** - Teach the model patterns
3. **Backtest** - Test performance

## Step-by-Step Guide

### Step 1: Open Your Model

1. Click **Models** in sidebar
2. Find your model in the list
3. Click the model name

### Step 2: Go to Composer

Click the **Composer** tab. You'll see three sub-tabs:
- Build
- Train  
- Backtest

### Step 3: Build the Matrix

Click **Build** tab if not already there.

#### Set Date Range

Choose your training period:

| Period | Good For | Data Points |
|--------|----------|-------------|
| **6 months** | Quick test | ~125 days |
| **1 year** | Basic validation | ~250 days |
| **2 years** | Recommended | ~500 days |
| **5 years** | Thorough test | ~1250 days |

**Recommended dates:**
- Start: 2 years ago
- End: 1 month ago

#### Click Build Matrix

Press the **Build Matrix** button. You'll see:
- Progress bar filling up
- "Fetching data..." message
- Row count increasing
- "Matrix built!" when done

**This takes 1-2 minutes.**

### Step 4: Train the Model

Click **Train** tab.

#### Review Settings

Default settings work well:
- **Algorithm**: XGBoost (leave as is)
- **Validation**: 80/20 split (good default)
- **Cross-validation**: 5-fold (recommended)

#### Set Trading Hours

Choose when model can trade:

| Option | Hours | Best For |
|--------|-------|----------|
| **Market Hours** | 9:30 AM - 4:00 PM ET | Stocks |
| **Extended** | 7:00 AM - 8:00 PM ET | Active traders |
| **Custom** | You choose | Special strategies |

#### Click Train

Press **Start Training**. You'll see:
- "Training model..." message
- Progress percentage
- "Training complete!" when done

**This takes 2-3 minutes.**

### Step 5: Run Backtest

Click **Backtest** tab.

#### Configure Test

Settings appear:
- **Test Period**: Auto-set to recent months
- **Starting Capital**: $10,000 (simulation)
- **Commission**: $1 per trade
- **Slippage**: 0.1% (realistic)

#### Start Backtest

Click **Run Backtest**. Watch:
- Trades plotting on chart
- Equity curve building
- Metrics calculating
- "Backtest complete!" when done

**This takes 1-2 minutes.**

## Understanding Results

### Key Metrics

Your results show important numbers:

| Metric | What It Means | Good Value |
|--------|---------------|------------|
| **Total Return** | Money made/lost | > 10% yearly |
| **Sharpe Ratio** | Risk-adjusted return | > 1.0 |
| **Max Drawdown** | Biggest loss | < 15% |
| **Win Rate** | Winning trades % | > 50% |
| **Trade Count** | Number of trades | > 30 |

### The Equity Curve

The main chart shows:
- **Green line**: Your strategy's value
- **Gray line**: Buy-and-hold comparison
- **Red areas**: Losing periods

**Good curve:**
- Goes up over time
- Smooth, not choppy
- Above gray line

### Gate Status

Look for the gate badge:

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **✓ Pass Gate** | Strategy is good | Can trade it |
| **✗ Fail Gate** | Needs work | Check why it failed |

### Why Gates Fail

Common reasons:
- Too few trades (< 30)
- Large drawdown (> 25%)
- Poor Sharpe (< 0.5)
- Negative returns

## Detailed Reports

### Trade List

Click **Trades** tab to see:
- Entry/exit dates
- Buy/sell prices
- Profit/loss per trade
- Hold time

### Monthly Breakdown

Click **Monthly** tab for:
- Returns by month
- Win/loss patterns
- Seasonal trends

### Statistics

Click **Stats** tab for:
- Average trade metrics
- Risk measurements
- Performance ratios

## Optimizing Results

### If Results Are Poor

Try these fixes:

| Problem | Solution |
|---------|----------|
| **Few trades** | Lower confidence threshold |
| **Big losses** | Tighten stop losses |
| **Low returns** | Adjust entry rules |
| **High drawdown** | Reduce position size |

### Running Sweeps

Test multiple variations:
1. Click **Sweeps** in sidebar
2. Select your model
3. Choose variations to test
4. Compare results

### Adjusting Parameters

In Model Designer:
- Change indicator periods
- Adjust thresholds
- Modify rules

Then re-run backtest.

## Export and Save

### Download Results

Click **Export** button for:
- CSV of all trades
- PDF report
- Performance charts

### Save Configuration

Good results? Save them:
1. Click **Save Config**
2. Name this version
3. Can restore later

## Common Issues

### "Insufficient Data"
- Use longer date range
- Check if stock existed then
- Try different asset

### "Training Failed"
- Reduce date range
- Check data quality
- Contact support

### "No Trades Generated"
- Signals too strict
- Wrong market conditions
- Review model logic

### "Results Too Good"
- Check for lookahead bias
- Verify costs included
- Test different period

## Best Practices

### Do's ✓
- Test multiple time periods
- Include transaction costs
- Check different markets
- Save good configurations
- Document changes

### Don'ts ✗
- Trust single backtest
- Ignore drawdowns
- Skip failed gates
- Overtrade
- Forget slippage

## What's Next

### After Good Backtest

1. **Run sweeps** - Find optimal settings
2. **Paper trade** - Test with fake money
3. **Start small** - Use minimal capital
4. **Scale up** - Increase gradually

### After Poor Backtest

1. **Review logic** - Check strategy makes sense
2. **Adjust parameters** - Try different settings
3. **Change template** - Try another approach
4. **Learn more** - Study what works

## Performance Expectations

### Realistic Returns

| Strategy Type | Annual Return | Risk Level |
|---------------|---------------|------------|
| **Conservative** | 5-10% | Low |
| **Balanced** | 10-20% | Medium |
| **Aggressive** | 20-40% | High |

Remember: Past performance doesn't guarantee future results.

## Tips for Better Backtests

1. **Use enough data** - Minimum 1 year
2. **Test bad periods** - Include 2008, 2020
3. **Be realistic** - Include all costs
4. **Stay skeptical** - If too good, probably is
5. **Keep testing** - Markets change

## Assumptions & Open Questions

**Assumptions:**
- Historical data is accurate
- Market conditions repeat somewhat
- Execution at shown prices possible

**Open Questions:**
- Live performance variance
- International market testing
- Options backtesting details

---

## Related Reading

- [Create a Model](./create-model.md)
- [Validate Risk](./validate-risk.md)
- [Models](../../products/models.md)
- [Performance Leaderboards](../../products/performance-leaderboards.md)
- [Troubleshooting](../../help/troubleshooting.md)