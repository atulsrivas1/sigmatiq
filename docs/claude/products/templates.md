# Templates

## Pre-Built Strategies Ready to Use

Templates are complete trading strategies that you can use immediately or customize to your needs.

## What It Is

A template is a pre-configured model that includes:
- Tested indicator combinations
- Proven trading rules
- Appropriate risk settings
- Historical performance data
- Documentation

Think of templates like recipe cards - follow them exactly or adjust to taste.

## Why It Matters

Templates help you:
- Start trading faster
- Learn from proven strategies
- Avoid beginner mistakes
- Save development time
- Build on success

## Key Concepts

### Template Categories

Templates are organized by:
- **Pack Type**: Which trading style (ZeroSigma, SwingSigma, etc.)
- **Complexity**: Simple, Medium, Advanced
- **Asset Type**: Stocks, ETFs, Options
- **Market Condition**: Trending, Ranging, Volatile

### Template Quality

Each template shows:
- **Success Rate**: Historical win percentage
- **Complexity Badge**: Difficulty level
- **Trade Frequency**: How often it trades
- **Tested Period**: How long backtested
- **Live Performance**: Real results if available

## Main Screen Tour

### Templates Gallery

#### Filter Bar
Top of page:
- Pack selector dropdown
- Complexity filter
- Asset type filter
- Sort options (popularity, performance, newest)

#### Template Cards Grid
Visual cards displaying:
- **Template name**: Descriptive title
- **Pack badge**: Color-coded pack type
- **Preview chart**: Mini performance graph
- **Key metrics**: Sharpe, return, trades
- **Complexity**: Simple/Medium/Advanced
- **Use Template button**: One-click start

### Template Detail View

Click any template to see:

#### Overview Section
- Full description
- Strategy explanation
- Best market conditions
- Risk warnings

#### Performance Section
- Historical backtest results
- Equity curve chart
- Monthly returns table
- Key statistics

#### Configuration Section
- Indicators used
- Entry rules
- Exit rules
- Risk parameters

#### Quick Actions
- **Use Template**: Create model from this
- **Preview**: See without creating
- **Clone**: Make editable copy
- **Documentation**: Detailed guide

## Popular Templates

### Beginner Templates

| Template | Pack | Description | Win Rate |
|----------|------|-------------|----------|
| **SPY Simple Swing** | SwingSigma | Basic trend following | 62% |
| **Buy the Dip** | SwingSigma | Mean reversion on drops | 65% |
| **Steady Growth** | LongSigma | Long-term investing | 68% |
| **Momentum Starter** | MomentumSigma | Follow strong trends | 58% |

### Intermediate Templates

| Template | Pack | Description | Win Rate |
|----------|------|-------------|----------|
| **Breakout Hunter** | SwingSigma | Trade new highs | 55% |
| **Gap Trader** | OvernightSigma | Overnight opportunities | 56% |
| **Sector Rotation** | MomentumSigma | Best performing sectors | 60% |
| **Value Momentum** | LongSigma | Quality plus growth | 64% |

### Advanced Templates

| Template | Pack | Description | Win Rate |
|----------|------|-------------|----------|
| **0DTE Lightning** | ZeroSigma | Same-day options | 52% |
| **Iron Condor** | ZeroSigma | Options premium | 68% |
| **Pairs Trading** | SwingSigma | Market neutral | 61% |
| **Vol Harvester** | MomentumSigma | Volatility strategies | 54% |

## Template Components

### Indicator Sets

Common indicators in templates:

**Trend Indicators**
- Moving averages (20, 50, 200)
- MACD for momentum
- ADX for trend strength

**Oscillators**
- RSI for overbought/oversold
- Stochastic for reversals
- Williams %R for extremes

**Volume Indicators**
- Volume moving average
- On-balance volume
- Accumulation/distribution

**Volatility Indicators**
- Bollinger Bands
- ATR for stops
- Keltner Channels

### Entry Rules

Common entry conditions:

**Trend Following**
```
BUY when:
- Price > 20-day MA
- RSI > 50
- Volume > average
```

**Mean Reversion**
```
BUY when:
- RSI < 30
- Price at lower Bollinger Band
- Positive divergence
```

**Breakout**
```
BUY when:
- Price > 20-day high
- Volume > 150% average
- ADX > 25
```

### Exit Rules

Common exit conditions:

**Profit Target**
- Fixed percentage (5%, 10%)
- ATR multiple (2x ATR)
- Resistance level

**Stop Loss**
- Fixed percentage (2%, 3%)
- Below support
- ATR-based

**Time Exit**
- After X days
- End of week
- Before earnings

## Using Templates

### Quick Start Process

1. **Browse Gallery**
   - Filter by your preference
   - Sort by performance
   - Check complexity

2. **Preview Template**
   - Click for details
   - Review performance
   - Understand strategy

3. **Create Model**
   - Click "Use Template"
   - Name your model
   - Select risk profile

4. **Run Backtest**
   - Verify performance
   - Check recent period
   - Confirm gate pass

5. **Start Trading**
   - Paper trade first
   - Monitor closely
   - Adjust if needed

### Customization Options

You can modify:

**Safe to Change:**
- Position size
- Stop loss distance
- Profit targets
- Trading hours
- Specific stocks

**Change Carefully:**
- Indicator periods
- Entry thresholds
- Exit conditions
- Risk profile

**Don't Change (Initially):**
- Core strategy logic
- Indicator combinations
- Risk framework

## Template Selection Guide

### By Experience Level

| Your Level | Start With | Avoid |
|------------|------------|-------|
| **Beginner** | Simple templates, SwingSigma | Advanced, ZeroSigma |
| **Intermediate** | Medium complexity, all packs | Only ZeroSigma |
| **Advanced** | Any template | None |

### By Account Size

| Account | Best Templates |
|---------|---------------|
| **< $5,000** | LongSigma, simple SwingSigma |
| **$5,000-$25,000** | Most templates except ZeroSigma |
| **> $25,000** | All templates available |

### By Time Available

| Time/Day | Recommended Templates |
|----------|---------------------|
| **< 30 minutes** | LongSigma only |
| **30-60 minutes** | SwingSigma, MomentumSigma |
| **2+ hours** | All templates |

### By Market Condition

| Market | Best Templates |
|--------|---------------|
| **Trending Up** | Momentum, breakout |
| **Trending Down** | Short strategies, defensive |
| **Sideways** | Mean reversion, swing |
| **Volatile** | Options strategies |

## Template Performance

### Understanding Metrics

**Sharpe Ratio**: Risk-adjusted returns
- < 0.5: Poor
- 0.5-1.0: Acceptable
- 1.0-2.0: Good
- > 2.0: Excellent

**Win Rate**: Percentage of profitable trades
- Not everything - size matters
- 50-65% typical
- Higher isn't always better

**Maximum Drawdown**: Largest loss
- < 10%: Conservative
- 10-20%: Moderate
- > 20%: Aggressive

### Historical vs Live

**Backtest Performance**: Historical simulation
- Optimistic usually
- Good for comparison
- Not guaranteed

**Live Performance**: Real trading results
- More realistic
- Include slippage
- True test

Expect live to be 20-30% worse than backtest.

## Creating from Templates

### Step-by-Step

1. **Find Template**
   ```
   Gallery → Filter → Select
   ```

2. **Create Model**
   ```
   Use Template → Name → Create
   ```

3. **Verify Settings**
   ```
   Review indicators → Check rules → Confirm risk
   ```

4. **Test First**
   ```
   Run backtest → Check results → Paper trade
   ```

## Template Updates

### Version Control
- Templates updated quarterly
- Previous versions saved
- Changes documented
- Can use old version

### Improvements Include
- Better parameters
- New indicators
- Risk adjustments
- Bug fixes

### Notification
- Email when updated
- In-app notice
- Change summary
- Migration guide

## Common Issues

### "Template not available"
- Check subscription level
- Verify pack access
- May need upgrade

### "Poor performance"
- Check market conditions
- Review customizations
- Try different period
- Use as designed

### "Too complex"
- Start simpler
- Read documentation
- Watch tutorial
- Ask community

## Best Practices

### Do's ✓
- Start with simple templates
- Test before trading
- Understand the strategy
- Follow risk guidelines
- Track performance

### Don'ts ✗
- Use without understanding
- Over-customize initially
- Ignore risk warnings
- Trade immediately
- Combine incompatible templates

## Template Library Growth

### New Templates Added
- Monthly additions
- Community submissions
- Seasonal strategies
- Market-specific

### Request Templates
- Vote on ideas
- Submit suggestions
- Share your own
- Collaborate

## Next Steps

After choosing template:
1. Create model
2. Run comprehensive backtest
3. Paper trade for 2 weeks
4. Start with small capital
5. Scale if successful

## Assumptions & Open Questions

**Assumptions:**
- Templates are maintained
- Historical performance relevant
- Users understand basics

**Open Questions:**
- Custom template creation
- Template marketplace
- Sharing mechanisms
- Version branching

---

## Related Reading

- [Models](./models.md)
- [Packs](./packs.md)
- [Create a Model](../suite/workflows/create-model.md)
- [Risk Profiles](./risk-profiles.md)
- [Getting Started](../getting-started.md)