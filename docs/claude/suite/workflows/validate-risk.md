# Validate Risk Workflow

## How to Check Your Strategy Is Safe

This guide helps you validate that your trading strategy has appropriate risk controls before using real money.

## What You'll Need

- A model with backtest results
- 5 minutes to review
- Understanding of your risk tolerance

## Risk Validation Steps

### Step 1: Check Gate Status

Look for the gate badge on your model:

| Badge | Meaning | Action |
|-------|---------|--------|
| **✓ Pass Gate** | Basic safety met | Continue validation |
| **✗ Fail Gate** | Safety issues | Must fix first |

### Step 2: Review Risk Metrics

Go to your backtest results and check:

#### Maximum Drawdown

The biggest loss from peak to valley:

| Drawdown | Risk Level | Suitable For |
|----------|------------|--------------|
| **< 5%** | Very Low | Conservative investors |
| **5-10%** | Low | Most investors |
| **10-20%** | Medium | Active traders |
| **20-30%** | High | Aggressive traders |
| **> 30%** | Very High | Experts only |

**Your comfort zone?** Most people can't handle > 20% losses.

#### Sharpe Ratio

Risk-adjusted returns:

| Sharpe | Quality | Meaning |
|--------|---------|---------|
| **< 0.5** | Poor | Too much risk for returns |
| **0.5-1.0** | Acceptable | Reasonable balance |
| **1.0-1.5** | Good | Well-balanced |
| **> 1.5** | Excellent | Great risk/reward |

#### Win Rate vs. Risk/Reward

Check the balance:

| Win Rate | Avg Win/Loss | Assessment |
|----------|--------------|------------|
| **40%** | Need 2:1 | Trend following |
| **50%** | Need 1.5:1 | Balanced |
| **60%** | Need 1:1 | Mean reversion |

### Step 3: Verify Position Sizing

Check your model's position rules:

#### Per-Trade Risk

| Risk Profile | Max Per Trade | On $10,000 |
|--------------|---------------|------------|
| **Conservative** | 2% | $200 |
| **Balanced** | 5% | $500 |
| **Aggressive** | 10% | $1,000 |

#### Total Exposure

Maximum invested at once:

| Risk Profile | Max Exposure | Positions |
|--------------|--------------|-----------|
| **Conservative** | 30% | 3-5 |
| **Balanced** | 60% | 5-10 |
| **Aggressive** | 90% | 10-15 |

### Step 4: Check Stop Losses

Every model needs stop losses:

#### Stop Loss Types

| Type | Description | Best For |
|------|-------------|----------|
| **Fixed %** | Same percentage always | Simple strategies |
| **ATR-based** | Adjusts to volatility | Adaptive strategies |
| **Time-based** | Exit after X days | Mean reversion |

#### Recommended Levels

| Strategy | Stop Loss | Example |
|----------|-----------|---------|
| **Day trading** | 1-2% | Tight control |
| **Swing trading** | 3-5% | Room to breathe |
| **Position trading** | 7-10% | Wider swings |

### Step 5: Stress Test

Test extreme scenarios:

#### Historical Stress Periods

Run backtests during:
- March 2020 (COVID crash)
- 2008 Financial Crisis
- 2000 Dot-com bubble
- Black Monday 1987

#### Check Performance

| Metric | Acceptable | Concerning |
|--------|------------|------------|
| **Drawdown** | < 2x normal | > 3x normal |
| **Recovery time** | < 6 months | > 1 year |
| **Correlation** | Some hedging | 100% correlated |

### Step 6: Review Trade Frequency

How often does it trade?

| Frequency | Trades/Month | Considerations |
|-----------|--------------|----------------|
| **Low** | < 5 | Less opportunity, lower costs |
| **Medium** | 5-20 | Balanced approach |
| **High** | > 20 | More opportunity, higher costs |

### Step 7: Calculate Costs

Include all trading costs:

#### Cost Components

| Cost Type | Typical Amount | Impact |
|-----------|----------------|--------|
| **Commission** | $1-5/trade | Direct cost |
| **Slippage** | 0.1-0.5% | Hidden cost |
| **Spread** | 0.01-0.1% | Immediate loss |
| **Data fees** | $10-100/month | Fixed cost |

#### Break-Even Calculation

```
Monthly costs ÷ Account size = Required return
Example: $50 ÷ $10,000 = 0.5% monthly needed
```

## Risk Profile Alignment

### Match Strategy to Profile

| Your Profile | Max Drawdown | Position Size | Strategies |
|--------------|--------------|---------------|------------|
| **Conservative** | 10% | 2% | SwingSigma, LongSigma |
| **Balanced** | 20% | 5% | All except ZeroSigma |
| **Aggressive** | 30% | 10% | All strategies |

### Warning Signs

**Too Risky If:**
- Drawdown > comfort level
- Can't sleep at night
- Checking constantly
- Emotional decisions
- Breaking rules

## Risk Controls Checklist

### Essential Controls ✓

- [ ] Stop loss on every trade
- [ ] Maximum position size set
- [ ] Daily loss limit defined
- [ ] Maximum positions limited
- [ ] Risk profile selected

### Advanced Controls

- [ ] Correlation limits
- [ ] Sector concentration limits
- [ ] Time-based exits
- [ ] Volatility filters
- [ ] Market regime filters

## Common Risk Mistakes

### Mistake 1: No Stop Loss
**Problem:** Unlimited losses possible
**Solution:** Always use stops, no exceptions

### Mistake 2: Too Big Positions
**Problem:** One loss wipes out many wins
**Solution:** Never risk > 5% per trade

### Mistake 3: Correlated Positions
**Problem:** All lose together
**Solution:** Diversify across sectors

### Mistake 4: Ignoring Costs
**Problem:** Profits eaten by fees
**Solution:** Include all costs in testing

## Risk Monitoring

### Daily Checks

Quick morning review:
- Open positions within limits?
- Stop losses in place?
- Account balance OK?

### Weekly Review

Deeper analysis:
- Win/loss ratio on track?
- Drawdown acceptable?
- Following the rules?

### Monthly Assessment

Full evaluation:
- Performance vs. expectations
- Risk metrics still good?
- Need adjustments?

## When to Stop Trading

### Circuit Breakers

Stop if:

| Trigger | Action | Resume When |
|---------|--------|-------------|
| **Daily loss > 5%** | Stop today | Next day |
| **Weekly loss > 10%** | Stop week | Next week |
| **Drawdown > 20%** | Full stop | Review strategy |
| **3 losses in row** | Pause | Check system |

## Risk Documentation

### Keep Records Of

- Initial risk parameters
- Changes made and why
- Actual vs. expected losses
- Close calls and saves
- Lessons learned

### Risk Report

Monthly report should show:
- Maximum drawdown
- Average position size
- Stop loss effectiveness
- Cost analysis
- Risk-adjusted returns

## Getting Help

### Warning Signs Need Help

Contact support if:
- Losses exceed plans
- Don't understand risks
- System not following rules
- Emotional trading
- Need guidance

### Resources

- Risk calculator in Tools
- Video on risk management
- Support chat for questions
- Community best practices

## Final Risk Check

Before going live, confirm:

1. **Understand maximum loss** - Know worst case
2. **Have emergency plan** - Know when to stop
3. **Can afford loss** - Never risk rent money
4. **Tested thoroughly** - Multiple scenarios checked
5. **Comfortable with risk** - Can sleep at night

## Assumptions & Open Questions

**Assumptions:**
- Stop losses will execute
- Historical risk repeats
- Correlations stay stable

**Open Questions:**
- Gap risk handling
- International market risks
- Options assignment risk

---

## Related Reading

- [Risk Profiles](../../products/risk-profiles.md)
- [Run a Backtest](./run-backtest.md)
- [Create a Model](./create-model.md)
- [Troubleshooting](../../help/troubleshooting.md)
- [FAQ](../../help/faq.md)