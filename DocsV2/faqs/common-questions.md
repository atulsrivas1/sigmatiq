# Frequently Asked Questions

## Complete FAQ Guide for Sigmatiq Users

Find answers to the most common questions about using Sigmatiq, organized by category for easy navigation.

## Getting Started Questions

### What is Sigmatiq?

Sigmatiq is a comprehensive trading platform that brings institutional-grade tools to individual investors. It helps you create, test, and automate trading strategies using advanced machine learning and technical analysis.

**Key Features**:
- Build trading strategies without coding
- Test strategies on historical data
- Paper trade before risking real money
- Automate execution with safety controls
- Track performance in real-time

### Do I need programming knowledge?

**No!** Sigmatiq is designed for traders, not programmers. 

You can:
- Use pre-built templates
- Modify strategies with dropdowns and sliders
- Create complex strategies visually
- Get AI assistance in plain English

No coding required at any step.

### How much money do I need to start?

**For Learning**: $0 (use paper trading)
**For Real Trading**: 
- Minimum recommended: $1,000
- Comfortable start: $5,000
- Full features: $10,000+

Start with paper trading to learn risk-free, then begin with small amounts.

### How long does it take to learn?

**Timeline**:
- **Day 1**: Create first strategy
- **Week 1**: Understand backtesting
- **Month 1**: Comfortable with platform
- **Month 3**: Developing profitable strategies
- **Month 6**: Considering automation

Everyone learns at their own pace. Take your time.

### Is my money safe?

**Platform Safety**:
- Sigmatiq never holds your funds
- You trade through your own broker
- Bank-level encryption
- Read-only API access available
- Two-factor authentication

**Trading Safety**:
- Built-in risk controls
- Automatic stop losses
- Position size limits
- Daily loss limits
- Paper trading for practice

## Account and Setup

### How do I create an account?

1. Visit sigmatiq.com
2. Click "Sign Up"
3. Enter email and create password
4. Verify email address
5. Complete profile
6. Choose subscription plan
7. Start with tutorial

Takes about 5 minutes total.

### What subscription plans are available?

**Free Trial**:
- 14 days full access
- No credit card required
- All features included
- Paper trading only

**Basic** ($49/month):
- 5 strategies
- 100 backtests/month
- Email support
- Paper trading

**Pro** ($149/month):
- Unlimited strategies
- Unlimited backtests
- Priority support
- Real trading
- Advanced features

**Enterprise** (Custom):
- Custom features
- Dedicated support
- API access
- White label options

### Can I connect my broker?

**Supported Brokers**:
- Interactive Brokers ✅
- TD Ameritrade ✅
- E*TRADE ✅
- Charles Schwab ✅
- Alpaca ✅
- Robinhood (coming soon)

Connection is optional and uses secure, read-only API by default.

### How do I cancel my subscription?

1. Go to Account Settings
2. Click Subscription
3. Select "Cancel Subscription"
4. Choose reason (optional)
5. Confirm cancellation

You keep access until the end of your billing period.

## Trading Strategy Questions

### What's the best strategy for beginners?

**Recommended Starting Strategy**:
- **Type**: SwingSigma (2-10 day trades)
- **Asset**: SPY (S&P 500 ETF)
- **Template**: "SPY Swing Classic"
- **Risk Profile**: Conservative

This strategy is:
- Easy to understand
- Well-tested
- Moderate risk
- Good for learning

### How many strategies should I run?

**Guidelines by Experience**:
- **Beginners**: 1-2 strategies
- **Intermediate**: 3-5 strategies
- **Advanced**: 5-10 strategies

Quality over quantity. Master one before adding more.

### Can I create my own strategies?

Yes! Three ways:
1. **Modify Templates**: Easiest, adjust existing strategies
2. **Visual Builder**: Drag-and-drop interface
3. **Custom Indicators**: Advanced users can add custom logic

Most users find templates sufficient.

### Why did my strategy fail the gate?

Common reasons and solutions:

**Too Few Trades** (< 30):
- Solution: Lower confidence threshold or extend time period

**High Drawdown** (> 25%):
- Solution: Tighten stop losses or reduce position size

**Poor Sharpe Ratio** (< 0.5):
- Solution: Review strategy logic or try different market

**Negative Returns**:
- Solution: Opposite signals might work better

### How do I know if a strategy is good?

**Good Strategy Metrics**:
- Sharpe Ratio > 1.0
- Win Rate > 50%
- Maximum Drawdown < 15%
- 50+ trades in backtest
- Consistent monthly returns
- Works in different market conditions

## Backtesting Questions

### What is backtesting?

Backtesting simulates how your strategy would have performed in the past. It's like a time machine that shows what would have happened if you had traded your strategy historically.

**Purpose**:
- Validate strategy ideas
- Understand risk/reward
- Build confidence
- Identify weaknesses

### Are backtest results reliable?

**Somewhat, with caveats**:

**Backtests assume**:
- Perfect execution
- No market impact
- Historical patterns repeat
- Costs are predictable

**Reality includes**:
- Slippage
- Partial fills
- Changing markets
- Unexpected events

Expect real results to be 20-30% worse than backtests.

### Why are my live results different from backtest?

**Common Reasons**:

1. **Slippage**: Real orders don't fill at exact prices
2. **Market Impact**: Your orders affect prices
3. **Timing**: Backtests assume instant execution
4. **Psychology**: Emotions affect real trading
5. **Market Change**: Conditions evolved

This is normal. Focus on direction, not exact numbers.

### How much historical data do I need?

**Minimum Requirements**:
- **Day Trading**: 6 months
- **Swing Trading**: 2 years
- **Long-term**: 5 years

**Ideal Amounts**:
- Include bull and bear markets
- Cover different volatility regimes
- Multiple economic cycles

More data = more confidence.

### What is out-of-sample testing?

Testing on data NOT used for strategy creation. Like taking a practice test with new questions.

**Example**:
- Build strategy using 2020-2022 data
- Test on 2023 data (out-of-sample)
- More realistic performance estimate

Always use out-of-sample testing.

## Risk Management Questions

### How much should I risk per trade?

**By Risk Profile**:
- **Conservative**: 1-2% of account
- **Balanced**: 2-5% of account  
- **Aggressive**: 5-10% of account

**Example** ($10,000 account):
- Conservative: $100-200 per trade
- Balanced: $200-500 per trade
- Aggressive: $500-1000 per trade

Never risk more than you can afford to lose.

### What is a stop loss?

A stop loss automatically exits a losing trade to limit losses.

**Example**:
- Buy stock at $100
- Set stop loss at $95
- If price drops to $95, automatically sell
- Maximum loss: $5 per share (5%)

Always use stop losses.

### What is maximum drawdown?

The largest peak-to-valley decline in your account value.

**Example**:
- Account peaks at $12,000
- Drops to $10,000
- Drawdown = $2,000 (16.7%)

**Acceptable Drawdowns**:
- Conservative: < 10%
- Balanced: < 20%
- Aggressive: < 30%

### How do I manage multiple positions?

**Best Practices**:
- Limit to 5-10 positions
- Diversify across sectors
- Don't exceed 20% in any position
- Monitor correlation
- Set portfolio stop loss

**Example Allocation**:
- 5 positions × 15% each = 75% invested
- 25% cash reserve
- No sector > 30%

### Should I use leverage?

**For Most Users**: No

**Leverage Risks**:
- Amplifies losses
- Margin calls
- Forced liquidation
- Interest costs
- Emotional stress

Only use leverage if:
- Very experienced
- Fully understand risks
- Have risk controls
- Can afford total loss

## Technical Questions

### What are technical indicators?

Mathematical calculations based on price and volume that help identify trading opportunities.

**Common Categories**:
- **Trend**: Moving averages, MACD
- **Momentum**: RSI, Stochastic
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV, Volume MA

Think of them as gauges on a dashboard.

### What is machine learning in trading?

Sigmatiq uses machine learning to find patterns in market data that humans might miss.

**How it works**:
1. Feed historical data
2. Algorithm learns patterns
3. Identifies similar setups
4. Generates predictions
5. You decide to trade or not

It's like having a very smart assistant.

### What is the Sharpe Ratio?

A measure of risk-adjusted returns. Higher is better.

**Interpretation**:
- < 0: Losing money
- 0-0.5: Poor
- 0.5-1.0: Acceptable
- 1.0-2.0: Good
- > 2.0: Excellent

**Formula** (simplified):
Returns divided by risk taken

### What is paper trading?

Trading with simulated money to practice without risk.

**Benefits**:
- Learn platform
- Test strategies
- Build confidence
- No financial risk
- Realistic experience

Always paper trade before using real money.

### What is slippage?

The difference between expected and actual trade prices.

**Example**:
- Signal says buy at $100.00
- Actual fill at $100.05
- Slippage = $0.05

**Causes**:
- Market movement
- Bid-ask spread
- Order size
- Liquidity

Account for 0.1-0.5% slippage in planning.

## Platform Features

### What is the Gate System?

Automatic quality control that evaluates strategies.

**Gate Checks**:
- Sufficient trades (30+)
- Acceptable drawdown (<25%)
- Positive Sharpe ratio
- Statistical significance

**Pass Gate** ✅ = Ready for next steps
**Fail Gate** ❌ = Needs improvement

Protects you from poor strategies.

### What are Sweeps?

Testing multiple strategy variations simultaneously.

**Example Sweep**:
Test 9 combinations:
- 3 confidence levels (50%, 60%, 70%)
- 3 time windows (morning, afternoon, all day)

Finds optimal parameters automatically.

### What is the Leaderboard?

Ranking of all your strategies by performance.

**Displays**:
- Sharpe ratio
- Total returns
- Win rate
- Drawdown
- Trade count

Helps identify best performers.

### What is a Model Card?

Detailed documentation for each strategy including:
- How it works
- Performance history
- Risk metrics
- Assumptions
- Best use cases

Like a manual for your strategy.

### Can I export my data?

Yes! Export options:
- **CSV**: Trade history, performance
- **PDF**: Reports, model cards
- **API**: JSON data
- **Charts**: PNG images

Your data is always yours.

## Troubleshooting

### My strategy isn't generating signals

**Common Causes**:
1. Thresholds too strict
2. Wrong market conditions
3. Indicators conflicting
4. Data issues

**Solutions**:
- Lower confidence threshold
- Check indicator values
- Review in different time period
- Verify data quality

### Platform is running slowly

**Try**:
1. Clear browser cache
2. Close unused tabs
3. Use Chrome/Firefox
4. Check internet connection
5. Reduce chart complexity

Contact support if issues persist.

### I can't connect my broker

**Checklist**:
- ✓ Broker is supported
- ✓ API enabled in broker account
- ✓ Correct credentials
- ✓ Two-factor authentication handled
- ✓ IP whitelist if required

See broker-specific guides in documentation.

### My backtest failed

**Error Messages and Solutions**:

"Insufficient data":
- Use longer time period
- Check if ticker exists in timeframe

"Matrix build failed":
- Verify all indicators valid
- Check date range
- Retry operation

"Training error":
- Reduce complexity
- Check for data quality
- Contact support

### I forgot my password

1. Click "Forgot Password" on login
2. Enter email address
3. Check email (including spam)
4. Click reset link
5. Create new password
6. Use password manager

## Money and Billing

### When am I charged?

**Billing Cycle**:
- Monthly: Same date each month
- Annual: Same date each year (20% discount)
- Free trial: No charge for 14 days

Charges appear as "Sigmatiq Trading" on statements.

### Can I change plans?

Yes, anytime:
- **Upgrade**: Immediate access, prorated charge
- **Downgrade**: Changes at next billing cycle
- **Cancel**: Access until period ends

No penalties for changes.

### Do you offer refunds?

**Refund Policy**:
- Within 7 days: Full refund
- Within 30 days: Prorated refund
- After 30 days: No refund
- Annual plans: 30-day guarantee

Contact support for refund requests.

### Are there hidden fees?

**No hidden fees**.

You pay:
- Subscription fee
- Your broker's commissions
- Market data (if required by broker)

Sigmatiq charges only subscription.

### Do you offer discounts?

**Available Discounts**:
- Annual billing: 20% off
- Students: 50% off (with .edu email)
- Multiple accounts: 10% off each
- Referrals: 1 month free per referral

## Educational Questions

### How do I learn trading?

**Sigmatiq Learning Path**:
1. Platform tutorials
2. Strategy templates
3. Paper trading
4. Community forums
5. Documentation
6. AI assistant

**External Resources**:
- Books on technical analysis
- YouTube channels
- Trading courses
- Market news sites

Start with platform tutorials.

### What books do you recommend?

**Beginner Books**:
- "A Random Walk Down Wall Street" - Malkiel
- "The Intelligent Investor" - Graham
- "Trading for a Living" - Elder

**Technical Analysis**:
- "Technical Analysis of the Financial Markets" - Murphy
- "Japanese Candlestick Charting" - Nison

**Psychology**:
- "Trading in the Zone" - Douglas
- "Thinking, Fast and Slow" - Kahneman

### Should I follow trading gurus?

**Be Cautious** ⚠️

**Red Flags**:
- Guaranteed returns
- Get rich quick
- Secret methods
- Expensive courses
- No track record

**Better Approach**:
- Learn fundamentals
- Test everything yourself
- Develop your own style
- Use Sigmatiq's tools
- Trust data, not personalities

### How do I stay informed?

**Daily Routine**:
- Check economic calendar
- Review overnight news
- Monitor your positions
- Check Sigmatiq signals

**Resources**:
- Bloomberg/Reuters
- CNBC/Yahoo Finance
- Twitter/FinTwit
- Sigmatiq community

Don't over-consume news.

## Community and Support

### How do I get help?

**Support Channels**:
1. **In-app chat**: Fastest response
2. **Email**: support@sigmatiq.com
3. **Documentation**: Comprehensive guides
4. **AI Assistant**: 24/7 help
5. **Community Forum**: User discussions

**Response Times**:
- Chat: < 5 minutes
- Email: < 24 hours
- Priority: < 2 hours

### Is there a user community?

**Yes! Active community**:
- Forums on platform
- Discord server
- Monthly webinars
- Strategy sharing
- Success stories

Join at community.sigmatiq.com

### Can I share strategies?

**Strategy Sharing**:
- Share read-only links
- Publish to marketplace (coming soon)
- Export configurations
- Community templates

You maintain ownership of your strategies.

### Do you offer training?

**Training Options**:
- **Self-guided**: Tutorials and documentation
- **Webinars**: Monthly live sessions
- **1-on-1**: Premium support plan
- **Videos**: YouTube channel

Most users succeed with self-guided.

## Advanced Questions

### Can I trade crypto?

**Currently**: No
**Planned**: Yes, Q2 2025

Focus now is traditional markets:
- Stocks
- ETFs
- Options
- Futures (coming)

### Can I use custom indicators?

**Options**:
1. Request addition (we add popular ones)
2. Combine existing indicators
3. API access (Enterprise plan)
4. Coming: Custom indicator builder

Most needs met by 70+ built-in indicators.

### Is there an API?

**API Access**:
- Read strategies
- Trigger backtests
- Get signals
- Performance data

Available on Pro and Enterprise plans.

### Can I white-label Sigmatiq?

**Enterprise Option**:
- Custom branding
- Your domain
- Modified features
- Dedicated support

Contact sales for details.

### Do you offer managed accounts?

**No**. Sigmatiq provides tools, not management.

**We do NOT**:
- Manage your money
- Make trades for you
- Provide personal advice
- Guarantee returns

You maintain full control.

## Common Concerns

### "This seems too good to be true"

**Reality Check**:
- Trading is hard
- Most traders lose money
- No guaranteed returns
- Requires discipline
- Tools help but don't guarantee success

Sigmatiq improves odds but doesn't eliminate risk.

### "I'm afraid of losing money"

**Risk Management**:
1. Start with paper trading
2. Use Conservative profile
3. Risk only 1-2% per trade
4. Set stop losses
5. Start small

Never trade with money you can't afford to lose.

### "It's too complicated"

**Simplification Path**:
1. Use one template
2. Don't modify anything
3. Paper trade only
4. Watch tutorials
5. Ask AI assistant

Complexity is optional. Start simple.

### "I don't have time"

**Time Requirements**:
- **Minimum**: 15 minutes/week (LongSigma)
- **Moderate**: 30 minutes/day (SwingSigma)
- **Active**: 2+ hours/day (ZeroSigma)

Choose strategy matching available time.

### "Markets are rigged"

**Our View**:
- Markets are competitive
- Information asymmetry exists
- But patterns exist
- Small traders have advantages (size, flexibility)
- Tools level playing field

Focus on your edge, not disadvantages.

## Contact Information

### Support
- **Email**: support@sigmatiq.com
- **Chat**: In-app bubble
- **Phone**: 1-800-SIGMATIQ (Enterprise only)
- **Hours**: 24/7 chat, 9-5 ET email

### Sales
- **Email**: sales@sigmatiq.com
- **Enterprise**: enterprise@sigmatiq.com

### Community
- **Forum**: community.sigmatiq.com
- **Discord**: discord.gg/sigmatiq
- **Twitter**: @sigmatiq

### Company
- **Website**: sigmatiq.com
- **Address**: 123 Trading Street, New York, NY
- **Blog**: blog.sigmatiq.com

---

**Can't find your answer?** Click the chat bubble for instant help or email support@sigmatiq.com