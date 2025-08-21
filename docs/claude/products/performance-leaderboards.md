# Performance Leaderboards

## Compare and Rank Trading Strategies

The Leaderboard shows how all your strategies perform compared to each other, helping you identify winners and losers.

## What It Is

The Leaderboard is a ranking system that:
- Compares all your models
- Shows performance metrics
- Identifies best strategies
- Tracks improvement over time
- Helps selection decisions

Think of it like a scoreboard showing which strategies are winning.

## Why It Matters

Leaderboards help you:
- Find your best strategies
- Stop using poor ones
- Allocate capital wisely
- Learn what works
- Make data-driven decisions

## Key Concepts

### Ranking Metrics

Strategies are ranked by:
- **Sharpe Ratio**: Risk-adjusted returns (primary)
- **Total Return**: Raw profit percentage
- **Win Rate**: Success percentage
- **Drawdown**: Risk taken
- **Trade Count**: Activity level

### Time Periods

View performance over:
- **Today**: Intraday results
- **Week**: 5 trading days
- **Month**: 30 days
- **Quarter**: 3 months
- **Year**: 12 months
- **All Time**: Since inception

### Filter Options

Show only:
- **Pass Gate**: Quality strategies only
- **By Pack**: Specific strategy types
- **By Risk**: Conservative/Balanced/Aggressive
- **Active Only**: Currently trading
- **Your Models**: Hide marketplace

## Main Screen Tour

### Leaderboard Table

Main table with columns:

#### Identity Columns
- **Rank**: Position (1, 2, 3...)
- **Model**: Strategy name with link
- **Pack**: Color-coded badge
- **Risk**: Profile indicator

#### Performance Columns
- **Sharpe**: Risk-adjusted score
- **Return**: Total percentage
- **Win Rate**: Success percentage
- **Trades**: Number completed
- **Drawdown**: Maximum loss

#### Status Columns
- **Gate**: Pass/Fail badge
- **Status**: Active/Inactive dot
- **Updated**: Last activity

#### Action Columns
- **View**: See details
- **Clone**: Copy strategy
- **Select**: Add to comparison

### Filter Bar

Top controls:

#### Quick Filters
- **Pass Gate Only**: Toggle switch
- **Active Only**: Toggle switch
- **My Models**: Toggle switch

#### Dropdowns
- **Pack Type**: All or specific
- **Risk Profile**: All or specific
- **Time Period**: Various ranges

#### Search
- Model name search
- Tag search
- ID search

### Summary Cards

Top of page cards showing:

#### Overall Stats
- **Total Models**: Count
- **Average Sharpe**: Portfolio score
- **Total Return**: Combined performance
- **Win Rate**: Overall success

#### Best Performer
- Model name
- Key metrics
- Mini chart
- View button

#### Worst Performer
- Model name
- Key metrics
- What went wrong
- Action suggestions

## Typical Workflow

### Daily Review

1. **Check Top Performers**
   - See what's working
   - Note patterns
   - Consider increasing allocation

2. **Review Bottom Performers**
   - Identify problems
   - Decide on action
   - Stop or fix

3. **Compare to Yesterday**
   - See rank changes
   - Spot trends
   - Adjust if needed

### Weekly Analysis

1. **Filter by Time Period**
   - Set to "Week"
   - Sort by return
   - See weekly winners

2. **Check Consistency**
   - Look for stable performers
   - Avoid one-hit wonders
   - Find reliable strategies

3. **Make Decisions**
   - Promote good strategies
   - Demote poor ones
   - Adjust allocations

## Understanding Rankings

### Sharpe Ratio Focus

Why Sharpe is #1:
- Measures risk vs reward
- Better than just returns
- Accounts for volatility
- Industry standard

**Interpretation:**
- **< 0**: Losing money
- **0-0.5**: Poor
- **0.5-1.0**: Acceptable
- **1.0-2.0**: Good
- **> 2.0**: Excellent

### Return vs Risk

High returns aren't everything:

| Model A | Model B | Better? |
|---------|---------|---------|
| Return: 50% | Return: 30% | |
| Drawdown: 40% | Drawdown: 10% | |
| Sharpe: 0.8 | Sharpe: 2.1 | B wins! |

Model B is better despite lower returns because risk is much lower.

### Gate System Impact

**Pass Gate models:**
- Highlighted in green
- Shown at top when filtered
- Safe for real trading

**Fail Gate models:**
- Shown in red
- Warning indicators
- Need improvement

## Comparison Features

### Select and Compare

1. **Check boxes** next to models
2. **Click Compare** button
3. See side-by-side view:
   - Performance charts
   - Metric comparison
   - Trade analysis
   - Risk profiles

### Export Comparison

Download comparison as:
- CSV spreadsheet
- PDF report
- PNG charts
- API JSON

### Share Results

Share leaderboard via:
- Read-only link
- Email report
- Team workspace
- Social media

## Performance Analysis

### Metric Deep Dive

Click any metric to see:

**Sharpe Ratio Details**
- Daily calculation
- Rolling average
- Volatility component
- Excess return

**Return Analysis**
- Monthly breakdown
- Compound growth
- Fees impact
- Real vs nominal

**Win Rate Breakdown**
- By time period
- By market condition
- By day of week
- By position size

### Time-Based Views

#### Heatmap Calendar
Visual calendar showing:
- Green days (profitable)
- Red days (losses)
- Intensity (size of move)
- Patterns visible

#### Performance Chart
Line chart displaying:
- Individual model curves
- Portfolio aggregate
- Benchmark comparison
- Drawdown periods

## Filtering and Sorting

### Advanced Filters

Combine multiple filters:
```
Pack: SwingSigma
AND Risk: Conservative
AND Sharpe > 1.0
AND Trades > 30
```

### Custom Sorts

Sort by combinations:
- Primary: Sharpe Ratio
- Secondary: Total Return
- Tertiary: Trade Count

### Saved Views

Save filter combinations:
- "My Best Strategies"
- "Needs Attention"
- "Ready to Scale"
- "Testing Phase"

## Common Patterns

### Success Patterns

Look for models with:
- Consistent ranking
- Steady improvement
- Low drawdowns
- Regular trades
- Pass gate status

### Warning Signs

Watch for models with:
- Dropping ranks
- Increasing drawdowns
- Fewer trades
- Gate failures
- Erratic performance

### Seasonal Patterns

Some strategies work better in:
- Bull markets
- Bear markets
- High volatility
- Low volatility
- Specific months

## Using Leaderboard Data

### Capital Allocation

Use rankings to decide:

| Rank | Action | Allocation |
|------|--------|------------|
| Top 20% | Increase | 40% of capital |
| Middle 60% | Maintain | 50% of capital |
| Bottom 20% | Reduce | 10% of capital |

### Model Lifecycle

Track progression:
1. **Testing**: Bottom tier, learning
2. **Improving**: Moving up ranks
3. **Proven**: Top tier, consistent
4. **Declining**: Dropping ranks
5. **Retired**: Remove from active

### Performance Attribution

Understand why models rank where they do:
- Market conditions
- Strategy type
- Risk taken
- Trade timing
- Asset selection

## Common Issues

### "Models not showing"
- Check filters
- Verify active status
- Refresh page
- Clear search

### "Rankings seem wrong"
- Check time period
- Verify metric selected
- Understand calculation
- Check for updates

### "Can't compare models"
- Maximum 5 at once
- Must have data
- Same time period
- Check selection

## Best Practices

### Do's ✓
- Review daily
- Compare similar strategies
- Track rank changes
- Document decisions
- Use multiple metrics

### Don'ts ✗
- Chase yesterday's winner
- Ignore risk metrics
- Compare different packs
- React to one day
- Forget costs

## Leaderboard Insights

### What to Look For

**Consistency**: Same models usually on top
**Improvement**: Models climbing ranks
**Correlation**: Models moving together
**Divergence**: Unusual rank changes

### Red Flags

- Sudden rank drops
- All models declining
- High correlation
- No gate passes
- Extreme volatility

## Export and Reports

### Available Exports

**Daily Snapshot**
- PDF summary
- Top 10 models
- Key changes
- Action items

**Full Analysis**
- All models
- All metrics
- Time series
- Statistics

### Scheduling

Set up automatic reports:
- Daily email
- Weekly summary
- Monthly deep dive
- Alert on changes

## Next Steps

Use leaderboard to:
1. Identify best models
2. Allocate capital accordingly
3. Stop poor performers
4. Clone and modify winners
5. Track improvements

## Assumptions & Open Questions

**Assumptions:**
- Rankings update real-time
- All models comparable
- Historical data accurate

**Open Questions:**
- Custom ranking formulas
- Team leaderboards
- Public rankings
- Prize competitions

---

## Related Reading

- [Models](./models.md)
- [Signals](./signals.md)
- [Dashboard](./dashboard.md)
- [Risk Profiles](./risk-profiles.md)
- [Run a Backtest](../suite/workflows/run-backtest.md)