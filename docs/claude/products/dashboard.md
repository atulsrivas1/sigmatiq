# Dashboard

## Your Trading Command Center

The Dashboard is your home screen in Sigmatiq. It shows everything important at a glance.

## What It Is

The Dashboard gives you a quick overview of:
- Your active models and their performance
- Recent trading activity
- System health status
- Quick access to common actions

## Why It Matters

- See everything important without clicking around
- Spot problems before they get worse
- Take quick actions without navigating
- Stay informed about your trading

## Key Concepts

### Information Hierarchy
Most important information is biggest and at the top. Less critical details are smaller and below.

### Real-Time Updates
Numbers and status indicators update automatically. No need to refresh the page.

### Color Coding
- **Green**: Good, profitable, active
- **Red**: Bad, losses, errors
- **Yellow**: Warning, needs attention
- **Gray**: Inactive, neutral

## Main Screen Tour

### Top Section - Header
- **Page title**: "Dashboard"
- **Date/time**: Current market time
- **Refresh button**: Force update

### Recent Models Card
Shows your latest models:
- **Model name**: What you called it
- **Pack badge**: Strategy type (color-coded)
- **Status dot**: Green (active) or gray (inactive)
- **Last updated**: When last changed
- **Performance**: Sharpe ratio if available
- **Quick actions**: Edit, Run, Delete icons

### Last Runs Card
Recent backtest activity:
- **Timestamp**: When it ran
- **Model**: Which model tested
- **Type**: Backtest, sweep, or train
- **Status**: Completed, running, failed
- **Result**: Pass/fail gate badge
- **View link**: See full results

### Quick Actions Card
One-click buttons for:
- **Create Model**: Green button, starts model creation
- **Run Backtest**: Blue button, opens composer
- **Sweeps**: Orange button, parameter testing
- **View Signals**: Purple button, see live signals

### System Health Card
Four status tiles showing:

**API Status**
- Green check: Working normally
- Yellow warning: Slow response
- Red X: Connection issues

**Database** 
- Green check: All systems go
- Yellow warning: High load
- Red X: Database problems

**Market Data**
- Green check: Live feed active
- Yellow warning: Delayed data
- Red X: No data feed

**Jobs Queue**
- Number of pending jobs
- Green: < 10 jobs
- Yellow: 10-50 jobs
- Red: > 50 jobs

### Performance Overview
Bottom section with charts:
- **7-day performance**: Line chart
- **Win/loss ratio**: Pie chart
- **Trade distribution**: Bar chart

## Typical Workflow

1. **Morning Check**
   - Open Dashboard
   - Check System Health (all green?)
   - Review Last Runs (any failures?)
   - Check Recent Models performance

2. **Take Action**
   - Click Quick Action based on needs
   - Or click model name to manage
   - Or click signal count to review

3. **End of Day**
   - Review day's performance
   - Check pending jobs
   - Note any warnings

## Inputs & Outputs

### Inputs
The Dashboard pulls data from:
- Your models database
- Backtest results
- System monitors
- Live market feeds

### Outputs
From Dashboard you can:
- Navigate to any section
- Start common workflows
- Download performance reports
- Access help resources

## Limits & Caveats

### Update Frequency
- Models: Every 30 seconds
- Health: Every 10 seconds
- Performance: Every minute
- Last Runs: Real-time

### Display Limits
- Shows 5 most recent models
- Shows 10 last runs
- Shows 7 days of performance
- More available on dedicated pages

### Performance Impact
Too many models may slow loading. Archive unused models to improve speed.

## Customization

### What You Can Change
- Theme (dark/light/slate/midnight)
- Refresh interval
- Number of items shown
- Chart time period

### What You Cannot Change
- Card layout
- Information displayed
- Color coding system
- Core metrics

## Tips for Use

### Daily Routine
1. Check health first
2. Review overnight runs
3. Check model status
4. Take needed actions

### Warning Signs
Watch for:
- Red health indicators
- Failed runs pattern
- Declining performance
- Queue backlog

### Quick Wins
- Use Quick Actions instead of navigation
- Click model names for details
- Hover over badges for explanations
- Use keyboard shortcuts

## Common Issues

### "Dashboard not loading"
- Check internet connection
- Clear browser cache
- Try different browser
- Contact support

### "Numbers not updating"
- Click refresh button
- Check health status
- Verify market hours
- Check data feed

### "Missing models"
- Check filters
- Verify not archived
- Confirm permissions
- Refresh page

## Mobile Considerations

Dashboard works on mobile but:
- Cards stack vertically
- Charts are simplified
- Some actions need desktop
- Best experienced on tablet+

## Related Features

The Dashboard connects to:
- **Models**: Manage strategies
- **Signals**: Live trading alerts
- **Health**: Detailed diagnostics
- **Reports**: Full analytics

## Next Steps

From the Dashboard, typically users:
1. Create their first model
2. Run backtests
3. Review signals
4. Check detailed reports

## Assumptions & Open Questions

**Assumptions:**
- User has at least one model
- Market data is available
- System has recent activity

**Open Questions:**
- Custom dashboard layouts
- Widget configuration
- Alert preferences
- Export capabilities

---

## Related Reading

- [Models](./models.md)
- [Signals](./signals.md)
- [System Health](./options-health.md)
- [Getting Started](../getting-started.md)
- [Create a Model](../suite/workflows/create-model.md)