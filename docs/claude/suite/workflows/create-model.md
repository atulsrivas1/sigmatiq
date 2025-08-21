# Create a Model Workflow

## How to Build Your First Trading Strategy

This guide walks you through creating a trading model from start to finish.

## What You'll Need

- A Sigmatiq account
- 10 minutes
- An idea of what you want to trade (or just use our suggestions)

## Step-by-Step Process

### Step 1: Go to Models

1. Click **Models** in the left sidebar
2. Click the green **Create Model** button (top right)

### Step 2: Choose a Template

You'll see template cards. Each shows:
- **Pack name** (like SwingSigma)
- **Hold time** (how long trades last)
- **Complexity** (Simple, Medium, Advanced)
- **Success rate** (historical performance)

**For beginners, choose:**
- SwingSigma Simple SPY
- Hold time: 2-10 days
- Complexity: Simple

Click the template card to select it.

### Step 3: Name Your Model

Enter a name that helps you remember what it does:

**Good names:**
- "My First SPY Swing"
- "Tech Stocks Momentum"
- "Safe Dividend Strategy"

**Avoid:**
- "Test1"
- "Model_final_v2"
- Random letters

### Step 4: Select Risk Profile

Choose your safety level:

| Profile | Description | Best For |
|---------|-------------|----------|
| **Conservative** | Smallest risks, fewer trades | Beginners, retirement accounts |
| **Balanced** | Medium risk and reward | Most users |
| **Aggressive** | Higher risk for higher returns | Experienced only |

**Tip:** Start with Conservative. You can change later.

### Step 5: Review Settings

The template fills in these automatically:

**Indicators** (signals to watch):
- RSI (finds oversold/overbought)
- Moving averages (shows trends)
- Volume (confirms moves)

**Trading Rules**:
- When to buy
- When to sell
- Stop loss levels

**You don't need to change these yet.**

### Step 6: Create the Model

1. Check everything looks right
2. Click the blue **Create Model** button
3. Wait 2-3 seconds

You'll see "Model created successfully!"

## What Happens Next

### Automatic Steps

Sigmatiq automatically:
1. Saves your model
2. Assigns a unique ID
3. Sets up the calculation engine
4. Prepares for backtesting

### Your Model Page

You're taken to your model's page showing:
- Model name and ID
- Current status (Active/Inactive)
- Performance metrics (empty at first)
- Action buttons

### Available Actions

From your model page, you can:

| Action | What It Does | When To Use |
|--------|--------------|-------------|
| **Edit** | Change settings | Adjust indicators or rules |
| **Composer** | Build, train, test | Run backtests |
| **Clone** | Make a copy | Create variations |
| **Delete** | Remove model | Clean up mistakes |

## Next: Run a Backtest

Your model needs testing. Click **Composer** to:

1. **Build** - Prepare historical data
2. **Train** - Teach the model patterns
3. **Backtest** - See how it would have performed

This takes 5-10 minutes total.

## Understanding the Model Designer

If you click **Edit**, you'll see:

### Indicators Section
Lists all technical indicators your model uses:
- Each has settings (like period length)
- Green check = active
- Gray = inactive

### Policy Section  
Trading rules in plain English:
- Entry conditions (when to buy)
- Exit conditions (when to sell)
- Risk controls (stop losses)

### Don't change these until you understand them.

## Tips for Success

### Do's ✓
- Start with templates
- Use descriptive names
- Begin with Conservative risk
- Test before trading
- Keep notes on changes

### Don'ts ✗
- Create too many models at once
- Use Aggressive risk as beginner
- Trade without backtesting
- Ignore the gate warnings
- Copy others blindly

## Common Issues

### "Template not loading"
- Refresh the page
- Check internet connection
- Try a different template

### "Name already exists"
- Add a number or date
- Make it more specific
- Check your existing models

### "Creation failed"
- Check all fields are filled
- Try a simpler template
- Contact support if continues

## Model Management

### Organizing Models

**Use naming patterns:**
- By asset: "SPY_swing_v1"
- By strategy: "momentum_tech_stocks"
- By date: "2024_q1_test"

### Model Limits

| Plan | Max Models | Active Models |
|------|------------|---------------|
| Free Trial | 3 | 1 |
| Basic | 10 | 3 |
| Premium | 100 | 20 |

### Deleting Models

To remove a model:
1. Go to Models list
2. Click the trash icon
3. Confirm deletion

**Warning:** This cannot be undone.

## Advanced Options

### Custom Indicators

After creating, you can add:
- More technical indicators
- Custom parameters
- Combined signals

### Multiple Assets

Modify your model to trade:
- Different stocks
- ETFs
- Options (advanced)

### Strategy Variations

Create variations by:
1. Cloning the original
2. Changing one thing
3. Comparing results

## What Success Looks Like

A good model shows:
- ✓ Passes the gate
- ✓ Positive returns in backtest
- ✓ Reasonable number of trades
- ✓ Controlled drawdowns
- ✓ Works in different markets

## Getting Help

### Built-in Help
- Hover over any field for tooltips
- Click ? icons for explanations
- Check the docs section

### Support Options
- In-app chat
- Email support
- Video tutorials
- Community forum

## Assumptions & Open Questions

**Assumptions:**
- You have market data access
- Templates are pre-validated
- Risk profiles are properly configured

**Open Questions:**
- Custom indicator upload process
- Model sharing between users
- Version control for models

---

## Related Reading

- [Run a Backtest](./run-backtest.md)
- [Models](../../products/models.md)
- [Risk Profiles](../../products/risk-profiles.md)
- [Templates](../../products/templates.md)
- [Dashboard](../../products/dashboard.md)