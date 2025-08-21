# Sigma Product Suite Overview

## How Our Products Work Together

The Sigma Product Suite is a complete system for trading. Each product has a specific job, and they all work together to help you trade safely and successfully.

## The Five Core Products

### 1. Sigma Lab - The Workshop
**What it is:** Where you build and test trading strategies.

**Why it matters:** You can test ideas with historical data before risking real money.

**Key features:**
- Build models using templates
- Test with past market data  
- Compare different strategies
- See detailed performance reports

**Who uses it:** Anyone with a trading idea to test.

### 2. Sigma Sim - The Practice Field
**What it is:** A safe place to practice with fake money.

**Why it matters:** Learn without losing real money.

**Key features:**
- Realistic market simulation
- Track practice performance
- No financial risk
- Same tools as real trading

**Who uses it:** Beginners and anyone testing new strategies.

### 3. Sigma Market - The Store
**What it is:** A marketplace for proven trading strategies.

**Why it matters:** Get expert strategies without building them yourself.

**Key features:**
- Browse verified strategies
- See real performance history
- Subscribe to signal feeds
- Transparent track records

**Who uses it:** People who want to follow experts.

### 4. Sigma Pilot - The Autopilot
**What it is:** Automated trading with safety controls.

**Why it matters:** Trade 24/7 without watching screens.

**Key features:**
- Automatic order execution
- Risk limits and safeguards
- Works with your broker
- Full audit trail

**Who uses it:** Busy traders who want automation.

### 5. Sigma Core - The Engine
**What it is:** The technology that powers everything.

**Why it matters:** Makes all other products work reliably.

**Key features:**
- Market data processing
- Strategy calculations
- Risk management
- Performance tracking

**Who uses it:** (Works behind the scenes for everyone)

## How Products Connect

```
You Create in LAB → Test in SIM → Get Signals from MARKET → Automate with PILOT
                            ↑                                        ↓
                            └──────── Powered by CORE ──────────────┘
```

### Typical User Journey

1. **Start in Lab**
   - Pick a template
   - Create a model
   - Run backtests

2. **Practice in Sim**
   - Paper trade the model
   - Watch performance
   - Adjust if needed

3. **Explore Market**
   - See what experts use
   - Compare to your models
   - Subscribe to best ones

4. **Activate Pilot**
   - Set risk controls
   - Connect broker
   - Start automation

## Roles and Access Levels

### User Roles

| Role | What They Can Do | Products They Use |
|------|------------------|-------------------|
| **Viewer** | Look but not change | Market (browse only) |
| **Trader** | Create and trade strategies | Lab, Sim, Market |
| **Premium Trader** | Everything plus automation | All products |
| **Admin** | Manage users and settings | All products + Admin tools |

### Access Controls

**Everyone can:**
- View public strategies
- Use paper trading
- See their own performance

**Traders can also:**
- Create models
- Run backtests
- Save strategies

**Premium traders can also:**
- Use automation
- Access all templates
- Priority support

**Admins can also:**
- Manage users
- Set system limits
- View all activity

## Data Flow

### How Information Moves

1. **Market Data** flows into Core
2. **Core** processes and stores it
3. **Lab** uses data for testing
4. **Models** generate signals
5. **Pilot** executes trades
6. **Results** flow back for analysis

### What Gets Shared

**Between Products:**
- Model definitions
- Performance metrics
- Risk settings
- User preferences

**Not Shared:**
- Personal account details
- Actual money amounts
- Private strategies (unless you share)

## Integration Points

### Broker Connections
Pilot connects to your broker to:
- Send orders
- Check positions
- Get account balance
- Track executions

**Supported Brokers:**
- Interactive Brokers
- TD Ameritrade
- E*TRADE
- Charles Schwab
- Alpaca

### Data Sources
Core gets market data from:
- Polygon.io (primary)
- Broker feeds (backup)
- Historical databases

### External Tools
You can export to:
- Excel (CSV files)
- Trading journals
- Tax software
- Performance trackers

## System Architecture

### Simple View

```
Your Computer → Web Browser → Sigmatiq Cloud → Your Broker
                                    ↓
                            Market Data Providers
```

### Components

**Front-End (What you see):**
- Web application
- Real-time updates
- Interactive charts
- Forms and tables

**Back-End (Behind scenes):**
- API servers
- Database storage
- Calculation engines
- Message queues

**Infrastructure:**
- Cloud hosting
- Security systems
- Backup services
- Monitoring tools

## Security and Safety

### Data Protection
- Encrypted connections
- Secure storage
- Regular backups
- Access logging

### Trading Safety
- Risk limits enforced
- Stop losses required
- Position size limits
- Daily loss limits

### Account Safety
- Two-factor authentication
- Session timeouts
- Activity monitoring
- Suspicious activity alerts

## Performance and Limits

### System Capabilities

| Feature | Limit | Note |
|---------|-------|------|
| **Models per user** | 100 | Can request more |
| **Backtests per day** | 50 | Resets at midnight |
| **Signals per minute** | 100 | Rate limited |
| **Data history** | 10 years | For backtesting |
| **Live positions** | 20 | Per account |

### Response Times

| Action | Expected Time |
|--------|--------------|
| **Page load** | < 2 seconds |
| **Backtest** | 1-5 minutes |
| **Signal generation** | < 1 second |
| **Order execution** | < 2 seconds |

## Module Dependencies

### What Needs What

**Lab needs:**
- Core for calculations
- Market data for testing

**Sim needs:**
- Lab for models
- Core for simulation

**Market needs:**
- Lab for strategies
- Core for tracking

**Pilot needs:**
- Everything above
- Broker connection

## Common Workflows

### Create and Test Strategy
1. Lab → Create model
2. Lab → Run backtest
3. Sim → Paper trade
4. Review results

### Subscribe to Signals
1. Market → Browse strategies
2. Market → View performance
3. Market → Subscribe
4. Pilot → Auto-trade

### Optimize Performance
1. Lab → Run sweeps
2. Lab → Compare results
3. Lab → Pick best
4. Sim → Validate

## Getting Support

### Self-Service
- In-app help buttons
- Documentation
- Video tutorials
- FAQ section

### Assisted Support
- Chat support (business hours)
- Email tickets
- Phone (premium only)
- Community forum

## Assumptions & Open Questions

**Assumptions:**
- Users have basic market knowledge
- Desktop/laptop primary (not mobile)
- US markets focus initially

**Open Questions:**
- International market support timeline
- Crypto trading availability
- Mobile app development

---

## Related Reading

- [Getting Started](../getting-started.md)
- [Dashboard](../products/dashboard.md)
- [Models](../products/models.md)
- [Risk Profiles](../products/risk-profiles.md)
- [FAQ](../help/faq.md)