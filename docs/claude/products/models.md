# Models

## Your Trading Strategies Hub

Models are the heart of Sigmatiq - they're your trading strategies that decide when to buy and sell.

## What It Is

A model is a set of rules that:
- Watches market indicators
- Identifies trading opportunities  
- Generates buy/sell signals
- Manages risk automatically

Think of it like a recipe for trading - it has ingredients (indicators) and instructions (rules).

## Why It Matters

Models let you:
- Trade without emotions
- Test ideas before risking money
- Trade 24/7 automatically
- Learn what actually works
- Scale successful strategies

## Key Concepts

### Model Components

Every model has:
- **Indicators**: Technical analysis tools (RSI, moving averages)
- **Rules**: When to buy and sell
- **Risk controls**: Stop losses and position sizing
- **Training data**: Historical patterns learned

### Model Types

Based on holding period:
- **ZeroSigma**: Same-day trades
- **SwingSigma**: 2-10 day holds
- **LongSigma**: 2-12 month positions
- **OvernightSigma**: Overnight gaps
- **MomentumSigma**: Trend following

### Model States

| State | Meaning | Can Trade? |
|-------|---------|------------|
| **Active** | Ready to generate signals | Yes |
| **Training** | Being built/updated | No |
| **Paused** | Temporarily stopped | No |
| **Failed** | Has errors | No |
| **Archived** | Stored away | No |

## Main Screen Tour

### Models List Page

#### Search Bar
Top of page:
- Type model names
- Filter by pack type
- Filter by status
- Sort options

#### Models Table
Main content area with columns:
- **Model ID**: Unique identifier
- **Name**: Your chosen name
- **Pack**: Strategy type badge
- **Updated**: Last modification
- **Status**: Active/Inactive dot
- **Sharpe**: Performance metric
- **Gate**: Pass/Fail badge
- **Actions**: Edit, Clone, Delete buttons

#### Create Model Button
Top right, green button:
- Opens template selector
- Starts creation workflow

### Model Detail Page

Click any model to see:

#### Header Section
- Model name (editable)
- Status toggle switch
- Risk profile badge
- Last updated timestamp

#### Performance Metrics
If backtested:
- **Sharpe Ratio**: Risk-adjusted returns
- **Total Return**: Percentage gain/loss
- **Max Drawdown**: Biggest loss
- **Trade Count**: Number of trades
- **Win Rate**: Successful trades percentage

#### Action Tabs
- **Overview**: Summary and recent activity
- **Designer**: Edit indicators and rules
- **Composer**: Build, train, backtest
- **History**: Change log

#### Quick Actions
Right side buttons:
- **Run Backtest**: Test with historical data
- **Clone Model**: Make a copy
- **Export**: Download configuration
- **Archive**: Store away
- **Delete**: Remove permanently

## Typical Workflow

### Creating Models

1. **Choose Approach**
   - Use template (recommended)
   - Clone existing model
   - Start from scratch (advanced)

2. **Configure Basics**
   - Name your model
   - Select pack type
   - Choose risk profile

3. **Set Indicators**
   - Pick technical indicators
   - Adjust parameters
   - Set thresholds

4. **Define Rules**
   - Entry conditions
   - Exit conditions
   - Risk limits

5. **Test and Deploy**
   - Run backtest
   - Review results
   - Activate if good

### Managing Models

Daily tasks:
- Review performance
- Check for signals
- Adjust if needed
- Archive old ones

Weekly tasks:
- Compare models
- Run new backtests
- Optimize parameters
- Document changes

## Inputs & Outputs

### Model Inputs
Models use:
- Price data (open, high, low, close)
- Volume information
- Technical indicators
- Market conditions

### Model Outputs
Models produce:
- Buy signals with confidence
- Sell signals with timing
- Position size recommendations
- Stop loss levels

## Limits & Caveats

### Quantity Limits

| Plan | Max Models | Active Models |
|------|------------|---------------|
| Free | 3 | 1 |
| Basic | 10 | 3 |
| Pro | 50 | 10 |
| Premium | 100 | 20 |

### Performance Limits
- Training: 5 minutes max
- Backtest: 10 minutes max
- Signals: 100 per minute
- Updates: Once per minute

### Data Limits
- Historical data: 10 years
- Tick data: Not available
- International: US markets only
- Real-time: During market hours

## Model Designer

### Indicators Section

Available indicators grouped by type:

**Trend Indicators**
- Moving averages (SMA, EMA)
- MACD
- ADX

**Momentum Indicators**
- RSI
- Stochastic
- Rate of change

**Volatility Indicators**
- Bollinger Bands
- ATR
- Standard deviation

**Volume Indicators**
- Volume moving average
- On-balance volume
- Volume rate of change

### Policy Editor

Define rules in plain English:
```
BUY when:
- RSI < 30 (oversold)
- Price > 20-day moving average
- Volume > average

SELL when:
- RSI > 70 (overbought)
- OR 5% profit reached
- OR 2% stop loss hit
```

## Model Templates

### Popular Templates

| Template | Description | Success Rate |
|----------|-------------|--------------|
| **SPY Swing Classic** | S&P 500 swing trading | 65% |
| **Tech Momentum** | Technology stock trends | 58% |
| **Mean Reversion Daily** | Buy dips, sell rips | 62% |
| **Breakout Scanner** | New highs strategy | 55% |

### Customizing Templates

You can modify:
- Indicator parameters
- Entry/exit thresholds  
- Risk settings
- Asset selection

Don't modify:
- Core logic (until experienced)
- Risk controls (keep safe)
- Multiple things at once

## Common Issues

### "Model not generating signals"
- Check if active
- Verify market hours
- Review thresholds
- Check data feed

### "Poor performance"
- Review backtest
- Check market conditions
- Adjust parameters
- Try different template

### "Training failed"
- Reduce date range
- Check data quality
- Simplify model
- Contact support

## Best Practices

### Do's ✓
- Start with templates
- Test thoroughly
- Document changes
- Keep it simple
- Monitor regularly

### Don'ts ✗
- Over-optimize
- Ignore risks
- Trade untested models
- Make emotional changes
- Use aggressive settings initially

## Advanced Features

### Model Cloning
Create variations:
1. Clone successful model
2. Change one parameter
3. Compare results
4. Keep best version

### Model Versioning
Track changes:
- Auto-saves versions
- Compare versions
- Rollback if needed
- See what changed

### Model Sharing
Share with others:
- Export configuration
- Share read-only link
- Publish to marketplace
- Keep proprietary

## Next Steps

After creating models:
1. Run comprehensive backtests
2. Optimize with sweeps
3. Paper trade first
4. Start small with real money
5. Scale successful models

## Assumptions & Open Questions

**Assumptions:**
- US market focus
- Daily or longer timeframes
- Standard indicators sufficient

**Open Questions:**
- Custom indicator upload
- International markets
- Cryptocurrency support
- Sub-minute timeframes

---

## Related Reading

- [Create a Model](../suite/workflows/create-model.md)
- [Templates](./templates.md)
- [Risk Profiles](./risk-profiles.md)
- [Packs](./packs.md)
- [Performance Leaderboards](./performance-leaderboards.md)