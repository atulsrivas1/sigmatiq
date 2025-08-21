# Trading Strategies and Models Guide

## Understanding Sigmatiq's Strategy Types

This comprehensive guide explains all available trading strategies in Sigmatiq, helping you choose the right approach for your goals, experience level, and market conditions.

## What Are Trading Models?

Trading models are systematic strategies that:
- Analyze market data using technical indicators
- Generate buy/sell signals based on patterns
- Execute trades according to predefined rules
- Remove emotion from trading decisions

Think of them as recipes - they specify exactly what ingredients (indicators) to use and how to combine them to create profitable trades.

## Strategy Packs Overview

Sigmatiq organizes strategies into five specialized "packs", each designed for different market approaches and time horizons:

### Quick Comparison

| Pack | Holding Period | Risk Level | Time Commitment | Best For |
|------|---------------|------------|-----------------|----------|
| **ZeroSigma** | Same day | Very High | Full-time | Options experts |
| **SwingSigma** | 2-10 days | Moderate | 30 min/day | Active traders |
| **LongSigma** | 2-12 months | Low | Weekly | Investors |
| **OvernightSigma** | Overnight | High | End of day | Gap traders |
| **MomentumSigma** | Variable | Moderate | Daily | Trend followers |

## Detailed Strategy Pack Descriptions

### ⚡ ZeroSigma - Zero Days to Expiration (0DTE)

**What It Is**: Ultra-short-term options trading using options that expire the same day.

#### How It Works

ZeroSigma strategies capitalize on intraday price movements using options with hours left until expiration:

1. **Morning Analysis** (9:00-9:30 AM):
   - Check overnight gaps
   - Identify support/resistance
   - Review option flow data

2. **Signal Generation** (9:30 AM-3:00 PM):
   - Monitor price action
   - Track unusual options activity
   - Calculate probability zones

3. **Execution** (When signals trigger):
   - Buy calls for bullish signals
   - Buy puts for bearish signals
   - Quick exits (minutes to hours)

#### Key Indicators Used

**Options Flow Indicators**:
- **DIX (Dark Pool Index)**: Institutional activity
- **GEX (Gamma Exposure)**: Market maker positioning
- **Put/Call Ratio**: Sentiment gauge
- **IV Rank**: Volatility opportunities

**Technical Indicators**:
- **VWAP**: Volume-weighted average price
- **9/21 EMA**: Short-term trend
- **RSI (5-minute)**: Overbought/oversold

#### Example Strategies

**SPY 0DTE Momentum**:
- Trades: SPY options expiring same day
- Signals: When price breaks VWAP with volume
- Target: 30-50% option gain
- Stop: 25% option loss
- Frequency: 2-3 trades per day

**QQQ 0DTE Reversal**:
- Trades: QQQ options at extremes
- Signals: RSI < 20 or > 80 on 5-min chart
- Target: Quick 20-30% reversals
- Stop: 20% option loss
- Frequency: 1-2 trades per day

#### Risk Considerations

**High Risk Factors** ⚠️:
- Options can expire worthless
- Time decay accelerates
- Requires constant monitoring
- High stress environment
- Pattern day trader rules apply

**Who Should Use**:
- Experienced options traders
- Full-time traders
- High risk tolerance
- Understanding of Greeks
- $25,000+ account (PDT rules)

**Who Should Avoid**:
- Beginners
- Part-time traders
- Risk-averse investors
- Small accounts
- Emotional traders

### 🎯 SwingSigma - Multi-Day Trading

**What It Is**: Capturing price swings over 2-10 days using stocks and options.

#### How It Works

SwingSigma identifies short-term trends and rides them for days:

1. **Daily Scan** (After market close):
   - Screen for setups
   - Check earnings calendar
   - Review sector rotation

2. **Entry Criteria**:
   - Technical setup complete
   - Volume confirmation
   - Risk/reward favorable

3. **Position Management**:
   - Hold 2-10 days average
   - Trail stops as price moves
   - Take partial profits

#### Key Indicators Used

**Trend Indicators**:
- **20/50 EMA**: Trend direction
- **MACD**: Momentum shifts
- **ADX**: Trend strength

**Entry/Exit Indicators**:
- **RSI (14)**: Oversold/overbought
- **Bollinger Bands**: Volatility breakouts
- **Volume**: Confirmation

#### Example Strategies

**Classic Swing Trade**:
```
Entry Conditions:
- Price above 20 EMA
- RSI between 40-60
- MACD bullish cross
- Above-average volume

Exit Conditions:
- 8% profit target OR
- RSI > 70 OR
- Break below 20 EMA OR
- 5 days elapsed
```

**Breakout Swing**:
```
Entry Conditions:
- Break above 20-day high
- Volume 150% of average
- ADX > 25 (trending)

Exit Conditions:
- 10% profit target OR
- Break below 10 EMA OR
- 10 days elapsed
```

#### Typical Performance

**Expected Metrics**:
- Win Rate: 55-65%
- Average Win: +6-8%
- Average Loss: -3-4%
- Risk/Reward: 1:2
- Monthly Trades: 10-20

#### Best Practices

**Do's** ✅:
- Set stops at entry
- Take partial profits
- Trade liquid stocks
- Follow the trend
- Review nightly

**Don'ts** ❌:
- Hold through earnings
- Average down
- Ignore stops
- Trade pre/post market
- Over-leverage

### 📈 LongSigma - Investment Strategies

**What It Is**: Long-term position trading over 2-12 months.

#### How It Works

LongSigma identifies major trends and holds positions for months:

1. **Weekly Analysis**:
   - Review weekly charts
   - Check fundamentals
   - Assess sector trends

2. **Position Building**:
   - Scale in over weeks
   - Average into positions
   - Reinvest dividends

3. **Portfolio Management**:
   - Rebalance quarterly
   - Adjust for market conditions
   - Tax-loss harvesting

#### Key Indicators Used

**Long-Term Indicators**:
- **200 EMA**: Major trend
- **52-week highs/lows**: Strength gauge
- **Monthly RSI**: Long-term momentum

**Fundamental Overlays**:
- **P/E Ratio**: Valuation
- **Revenue Growth**: Quality
- **Sector Rotation**: Timing

#### Example Strategies

**Trend Following Investment**:
```
Entry:
- Weekly close above 40-week MA
- Monthly RSI > 50
- Positive sector momentum

Position Management:
- 25% initial position
- Add 25% on pullbacks
- Full position within 4 weeks

Exit:
- Weekly close below 40-week MA
- OR 12 months elapsed
- OR 50% profit achieved
```

**Value Momentum Hybrid**:
```
Entry:
- P/E below sector average
- Price above 200-day MA
- Improving fundamentals

Exit:
- P/E above sector average
- OR Price below 200-day MA
- OR Fundamentals deteriorate
```

#### Portfolio Construction

**Typical Allocation**:
- 5-10 positions maximum
- 10-20% per position
- Sector diversification
- Gradual entry/exit

### 🌙 OvernightSigma - Gap Trading

**What It Is**: Trading the gap between market close and next open.

#### How It Works

OvernightSigma exploits price gaps that occur overnight:

1. **3:30 PM Analysis**:
   - Identify gap candidates
   - Check news catalysts
   - Calculate gap probability

2. **3:55 PM Execution**:
   - Enter positions before close
   - Set overnight stops
   - Define exit targets

3. **9:30 AM Next Day**:
   - Exit at open
   - Or manage if trending

#### Key Indicators Used

**Gap Indicators**:
- **ATR (Average True Range)**: Gap size expectation
- **Relative Volume**: Unusual activity
- **News Catalyst**: Gap driver

**Confirmation Indicators**:
- **After-hours price action**
- **Futures correlation**
- **Sector momentum**

#### Example Strategies

**Earnings Gap Trade**:
```
Setup:
- Earnings after close
- Historical gap tendency
- Options IV elevated

Execution:
- Buy/short 3:55 PM
- Exit 9:35 AM next day
- 2% stop loss
```

**Momentum Gap Continuation**:
```
Setup:
- Strong close (>1% day)
- Above-average volume
- Sector leadership

Execution:
- Long at 3:55 PM
- Exit at open +0.5%
- Or trail if gapping up
```

### 🚀 MomentumSigma - Trend Following

**What It Is**: Riding strong trends with volatility-adjusted position sizing.

#### How It Works

MomentumSigma identifies and follows strong market trends:

1. **Trend Identification**:
   - Multiple timeframe analysis
   - Momentum confirmation
   - Volume validation

2. **Position Sizing**:
   - Adjust for volatility
   - Scale with trend strength
   - Reduce in uncertainty

3. **Trend Management**:
   - Trail stops with trend
   - Add on pullbacks
   - Exit on reversal

#### Key Indicators Used

**Momentum Indicators**:
- **Rate of Change (ROC)**: Momentum speed
- **Relative Strength**: Versus market
- **52-week highs**: Breakout confirmation

**Risk Management**:
- **ATR-based stops**: Volatility-adjusted
- **Position sizing**: Inverse to volatility
- **Correlation matrix**: Diversification

#### Example Strategies

**Pure Momentum**:
```
Entry:
- 20-day high breakout
- ROC(20) > 10%
- RS vs SPY > 1.1

Position Size:
- Base size / (ATR/Price)
- Max 5% of portfolio

Exit:
- 20-day low break
- OR ROC(20) < 0
- OR RS < 0.9
```

## Choosing the Right Strategy

### By Experience Level

**Beginners** (0-6 months):
1. Start: SwingSigma basic templates
2. Learn: LongSigma for investing
3. Avoid: ZeroSigma, OvernightSigma

**Intermediate** (6-24 months):
1. Master: SwingSigma variations
2. Try: MomentumSigma
3. Explore: OvernightSigma carefully

**Advanced** (2+ years):
1. All strategies available
2. Combine multiple approaches
3. Consider ZeroSigma if appropriate

### By Time Availability

**Minimal** (< 30 min/day):
- LongSigma only
- Weekly reviews
- Set and forget

**Moderate** (30-60 min/day):
- SwingSigma primary
- MomentumSigma secondary
- Daily reviews

**Full-Time** (2+ hours/day):
- All strategies available
- ZeroSigma possible
- Active management

### By Account Size

**Small** ($1,000 - $10,000):
- SwingSigma: Best option
- LongSigma: Good for growth
- Avoid: ZeroSigma (PDT rules)

**Medium** ($10,000 - $50,000):
- All except ZeroSigma
- Diversify across strategies
- Focus on consistency

**Large** ($50,000+):
- All strategies available
- Multi-strategy allocation
- Advanced techniques

### By Market Conditions

**Bull Market** 📈:
- Best: MomentumSigma, LongSigma
- Good: SwingSigma (long bias)
- Careful: ZeroSigma (calls)

**Bear Market** 📉:
- Best: Cash, defensive SwingSigma
- Good: ZeroSigma (puts)
- Avoid: LongSigma (long only)

**Sideways Market** ➡️:
- Best: SwingSigma, OvernightSigma
- Good: ZeroSigma (both directions)
- Avoid: MomentumSigma

**High Volatility** 📊:
- Best: ZeroSigma (if experienced)
- Good: Reduced SwingSigma
- Avoid: Large positions

## Strategy Performance Expectations

### Realistic Returns by Strategy

| Strategy | Conservative | Balanced | Aggressive |
|----------|-------------|----------|------------|
| **ZeroSigma** | N/A | 30-50% | 50-100%+ |
| **SwingSigma** | 10-15% | 20-30% | 30-50% |
| **LongSigma** | 8-12% | 12-20% | 20-30% |
| **OvernightSigma** | 5-10% | 15-25% | 25-40% |
| **MomentumSigma** | 10-15% | 20-35% | 35-60% |

*Annual returns, not guaranteed, historical approximations*

### Risk Metrics by Strategy

| Strategy | Max Drawdown | Win Rate | Avg Hold Time |
|----------|-------------|----------|---------------|
| **ZeroSigma** | -30% | 45-55% | 2-4 hours |
| **SwingSigma** | -15% | 55-65% | 5 days |
| **LongSigma** | -20% | 60-70% | 4 months |
| **OvernightSigma** | -20% | 50-60% | 1 night |
| **MomentumSigma** | -25% | 45-55% | 3 weeks |

## Creating Custom Strategies

### Template Modification

Start with a template and adjust:

**Parameters to Modify**:
- Indicator periods (fast/slow)
- Confidence thresholds
- Stop loss distances
- Profit targets
- Holding periods

**Example Customization**:
```
Base: SwingSigma Classic
Modifications:
- RSI period: 14 → 21 (smoother)
- Stop loss: 5% → 3% (tighter)
- Hold time: 5 days → 3 days (quicker)
Result: "SwingSigma Quick"
```

### Combining Strategies

**Portfolio Approach**:
- 40% LongSigma (core holdings)
- 40% SwingSigma (active trading)
- 20% MomentumSigma (growth kicker)

This provides balance between stability and growth.

### Strategy Development Process

1. **Idea Generation**:
   - Observe market patterns
   - Read trading literature
   - Modify existing strategies

2. **Hypothesis Formation**:
   - Define entry/exit rules
   - Set risk parameters
   - Establish expectations

3. **Backtesting**:
   - Test on historical data
   - Verify across markets
   - Check different periods

4. **Paper Trading**:
   - Test in real-time
   - No money at risk
   - Refine rules

5. **Live Trading**:
   - Start small
   - Scale gradually
   - Monitor closely

## Common Strategy Mistakes

### Over-Optimization
**Problem**: Making strategy fit historical data perfectly
**Solution**: Keep it simple, test out-of-sample

### Ignoring Risk
**Problem**: Focusing only on returns
**Solution**: Always consider drawdowns

### Strategy Hopping
**Problem**: Switching strategies after losses
**Solution**: Stick to plan for meaningful period

### Wrong Market Fit
**Problem**: Using trending strategy in ranging market
**Solution**: Match strategy to conditions

### Complexity Creep
**Problem**: Adding too many indicators
**Solution**: Maximum 3-4 indicators

## Strategy Maintenance

### Regular Reviews

**Weekly**:
- Check performance metrics
- Verify signals triggering
- Review trade quality

**Monthly**:
- Compare to expectations
- Analyze losing trades
- Adjust if needed

**Quarterly**:
- Full strategy audit
- Market regime assessment
- Consider modifications

### When to Retire a Strategy

**Red Flags** 🚩:
- 3 consecutive losing months
- Drawdown exceeds limits
- Market structure changed
- Better alternative found
- No longer suits goals

**Process**:
1. Stop new trades
2. Close existing positions
3. Document lessons learned
4. Archive for reference

## Advanced Strategy Concepts

### Market Regime Filters

Add filters to improve strategies:

**Trend Filter**:
- Only trade when SPY > 200 MA
- Reduces whipsaws
- Improves win rate

**Volatility Filter**:
- Skip trades when VIX > 30
- Avoids chaotic periods
- Preserves capital

### Multi-Timeframe Analysis

**Concept**: Confirm signals across timeframes

**Example**:
- Daily: Bullish trend
- 4-hour: Pullback to support
- 1-hour: Reversal signal
- Entry: All align bullish

### Correlation Management

**Why It Matters**: Avoid concentration risk

**Implementation**:
- Maximum 2 tech stocks
- Maximum 3 correlated positions
- Diversify across sectors

## Getting Started Recommendations

### Week 1: Foundation
1. Read all strategy descriptions
2. Choose SwingSigma to start
3. Paper trade one template
4. Track every trade

### Month 1: Exploration
1. Try 3 different templates
2. Compare performance
3. Identify preferences
4. Document lessons

### Month 3: Specialization
1. Focus on best performing
2. Make small customizations
3. Consider real money
4. Develop expertise

### Month 6: Expansion
1. Add second strategy type
2. Allocate appropriately
3. Monitor correlation
4. Continue learning

## Summary

Sigmatiq offers five distinct strategy packs:

- **ZeroSigma**: Expert-level same-day options
- **SwingSigma**: Versatile multi-day trading
- **LongSigma**: Patient investment approach
- **OvernightSigma**: Gap exploitation
- **MomentumSigma**: Trend following

Start with SwingSigma, master the basics, then expand based on your goals, experience, and available time.

Remember: **No strategy works all the time in all markets.** Success comes from matching the right strategy to the right conditions with the right risk management.

---

**Next Steps**:
- Try the [Strategy Selection Quiz](strategy-quiz.md)
- Read about [Technical Indicators](indicators-guide.md)
- Learn [Backtesting Best Practices](backtesting-guide.md)