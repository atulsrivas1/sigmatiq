# Complete BTB Pipeline Workflow

## The Core of Sigmatiq: Build → Train → Backtest → Sweeps → Leaderboard

This guide shows the complete workflow for creating and optimizing trading strategies using Sigmatiq's BTB (Build-Train-Backtest) pipeline through all three interfaces: UI, API, and command line.

## Overview

The BTB pipeline is Sigmatiq's systematic approach to strategy development:

```
Create Pack/Model → Build Matrix → Run Sweeps → Review Leaderboard → Train Best → Generate Signals
```

## The Complete Workflow

### Phase 1: Setup - Create Strategy Pack and Model

#### Via UI
1. Navigate to **Models** → **Create Model**
2. Select a Pack (ZeroSigma, SwingSigma, etc.)
3. Choose a template or create custom
4. Name your model (e.g., `spy_swing_daily`)
5. Set Risk Profile (Conservative/Balanced/Aggressive)
6. Click **Create**

#### Via API
```bash
POST /models
{
  "pack_id": "swingsigma",
  "model_id": "spy_swing_daily",
  "ticker": "SPY",
  "asset": "eq",
  "horizon": "swing",
  "cadence": "daily",
  "risk_profile": "balanced"
}
```

#### Via Makefile
```bash
# Auto-generate model ID and create structure
make init-auto PACK_ID=swingsigma TICKER=SPY ASSET=eq HORIZON=swing CADENCE=daily

# Or with specific model ID
make init MODEL_ID=spy_swing_daily PACK_ID=swingsigma TICKER=SPY
```

### Phase 2: Build - Prepare Training Data

Building creates the training matrix - historical data with all indicators calculated.

#### Via UI
1. Open your model → **Composer** tab → **Build**
2. Set date range:
   - Start: 2 years ago (e.g., `2022-01-01`)
   - End: 1 month ago (e.g., `2024-12-01`)
3. Review indicators (auto-selected from template)
4. Click **Build Matrix**
5. Wait for completion (2-5 minutes)
6. Note the `matrix_sha` (unique identifier)

#### Via API
```bash
POST /build_matrix
{
  "model_id": "spy_swing_daily",
  "pack_id": "swingsigma",
  "start": "2022-01-01",
  "end": "2024-12-01",
  "ticker": "SPY",
  "distance_max": 7
}

# Response includes:
# - matrix_sha: "c7d8e9a"
# - rows: 504
# - features: 73
```

#### Via Makefile
```bash
make build MODEL_ID=spy_swing_daily PACK_ID=swingsigma \
  START=2022-01-01 END=2024-12-01 TICKER=SPY
```

### Phase 3: Sweeps - Test Multiple Variations

Sweeps test your strategy with different parameter combinations to find optimal settings.

#### Via UI
1. Navigate to **Sweeps** page
2. Select your model
3. Choose Risk Profile
4. Configure variations:
   - **Thresholds**: `[0.50, 0.55, 0.60]`, `[0.55, 0.60, 0.65]`
   - **Hours** (if intraday): `[13,14]`, `[13,14,15]`
   - **Top %** (alternative): `[0.10]`, `[0.15]`
5. Set splits: 5 (for cross-validation)
6. Add tag: "initial_sweep"
7. Click **Run Sweep**
8. Monitor progress (10-30 minutes)

#### Via API
```bash
POST /backtest_sweep
{
  "model_id": "spy_swing_daily",
  "pack_id": "swingsigma",
  "thresholds_variants": [
    "0.50,0.55,0.60",
    "0.55,0.60,0.65",
    "0.60,0.65,0.70"
  ],
  "allowed_hours_variants": ["13,14", "13,14,15"],
  "top_pct_variants": [0.10, 0.15],
  "splits": 5,
  "tag": "initial_sweep",
  "min_trades": 30,
  "min_sharpe": 0.5
}
```

#### Via Makefile
```bash
# First, generate sweep config
make sweep-config MODEL_ID=spy_swing_daily

# Edit sweeps/spy_swing_daily_sweep.yaml to customize

# Then run sweep (requires custom runner or API calls)
# Or run single backtest with specific params:
make backtest MODEL_ID=spy_swing_daily THRESHOLDS=0.55,0.60,0.65 \
  ALLOWED_HOURS=13,14,15 SPLITS=5
```

### Phase 4: Leaderboard - Compare Results

The leaderboard shows all sweep results ranked by performance.

#### Via UI
1. Go to **Leaderboard** page
2. Filter:
   - Model: `spy_swing_daily`
   - Risk Profile: Your selected profile
   - Pass Gate Only: ✓ (recommended)
3. Review metrics:
   - **Sharpe Ratio**: Risk-adjusted returns (>1.0 good)
   - **Total Return**: Raw performance
   - **Max Drawdown**: Largest loss
   - **Trade Count**: Must be >30
   - **Gate Status**: Pass/Fail with reasons
4. Select best performers (top 3-5)
5. Add to Selection Cart

#### Via API
```bash
GET /leaderboard?model_id=spy_swing_daily&pack_id=swingsigma&pass_gate=true&limit=10

# Response includes ranked results:
[
  {
    "rank": 1,
    "config": {"kind": "thr", "value": "0.60,0.65,0.70", "allowed_hours": "13,14,15"},
    "metrics": {"sharpe": 1.85, "return": 0.24, "trades": 87, "max_dd": -0.08},
    "gate": {"pass": true, "reasons": []},
    "lineage": {"matrix_sha": "c7d8e9a", "risk_profile": "balanced"}
  }
]
```

#### Via Makefile
```bash
make leaderboard PACK_ID=swingsigma MODEL_ID=spy_swing_daily LIMIT=10
```

### Phase 5: Train - Build Final Models

Train the machine learning models using the best configurations.

#### Via UI
1. Go to **Composer** → **Train** tab
2. Review selected configurations from cart
3. Settings:
   - Algorithm: XGBoost (default)
   - Calibration: Sigmoid
   - Allowed Hours: From best config
4. Click **Start Training**
5. Monitor progress (5-15 minutes per config)

#### Via API
```bash
POST /train
{
  "model_id": "spy_swing_daily",
  "pack_id": "swingsigma",
  "allowed_hours": "13,14,15",
  "calibration": "sigmoid",
  "config": {
    "kind": "thr",
    "value": "0.60,0.65,0.70"
  }
}

# Response:
{
  "ok": true,
  "job_id": "train_123",
  "status": "queued"
}
```

#### Via Makefile
```bash
make train MODEL_ID=spy_swing_daily PACK_ID=swingsigma \
  ALLOWED_HOURS=13,14,15
```

### Phase 6: Backtest - Validate Performance

Run final backtest on the trained model to verify performance.

#### Via UI
1. **Composer** → **Backtest** tab
2. Configuration auto-filled from training
3. Click **Run Backtest**
4. Review results:
   - Equity curve
   - Trade list
   - Performance metrics
   - Gate status

#### Via API
```bash
POST /backtest
{
  "model_id": "spy_swing_daily",
  "pack_id": "swingsigma",
  "thresholds": "0.60,0.65,0.70",
  "splits": 5,
  "allowed_hours": "13,14,15"
}
```

#### Via Makefile
```bash
make backtest MODEL_ID=spy_swing_daily THRESHOLDS=0.60,0.65,0.70 \
  ALLOWED_HOURS=13,14,15 SPLITS=5
```

### Phase 7: Signals - Generate Trading Alerts

Once trained and validated, the model generates live trading signals.

#### Via UI
1. Navigate to **Signals** page
2. Your model appears if active
3. Monitor:
   - Real-time signals as they generate
   - Confidence levels
   - Buy/Sell recommendations

#### Via API
```bash
GET /signals?model_id=spy_swing_daily&limit=10

# Real-time signals:
[
  {
    "timestamp": "2024-01-15T14:30:00Z",
    "model_id": "spy_swing_daily",
    "ticker": "SPY",
    "side": "BUY",
    "confidence": 0.72,
    "status": "NEW"
  }
]
```

#### Via Makefile
```bash
# Generate alerts and write to CSV
make alerts MODEL_ID=spy_swing_daily
```

## Complete Pipeline Commands

### One-Line Pipeline Execution

#### Via Makefile (Full Pipeline)
```bash
# Complete pipeline: build → train → backtest
make pipeline MODEL_ID=spy_swing_daily PACK_ID=swingsigma \
  START=2022-01-01 END=2024-12-01 TICKER=SPY \
  THRESHOLDS=0.60,0.65,0.70 ALLOWED_HOURS=13,14,15

# With momentum gate
make pipeline-gated MODEL_ID=spy_swing_daily PACK_ID=swingsigma \
  START=2022-01-01 END=2024-12-01 TICKER=SPY
```

## Understanding Lineage and SHAs

The system tracks every step with unique identifiers:

- **matrix_sha**: Identifies the exact training data
- **config_sha**: Identifies the configuration parameters
- **policy_sha**: Identifies the trading rules
- **risk_sha**: Identifies the risk profile settings

This ensures complete reproducibility and audit trail.

## Risk Profiles Impact

Your Risk Profile affects the entire pipeline:

| Profile | Position Size | Sweeps Budget | Min Sharpe | Max Drawdown |
|---------|--------------|---------------|------------|--------------|
| **Conservative** | 2% | 20 configs | 1.0 | 10% |
| **Balanced** | 5% | 50 configs | 0.7 | 20% |
| **Aggressive** | 10% | 100 configs | 0.5 | 30% |

## Gate System

The Gate system automatically validates strategies:

### Pass Gate Requirements
- Minimum 30 trades
- Sharpe ratio > 0.5
- Maximum drawdown < risk limit
- Positive returns
- Sufficient data quality

### Fail Gate Reasons
Common failures and solutions:
- `"min_trades_not_met"` → Lower threshold or extend period
- `"excessive_drawdown"` → Tighten risk controls
- `"poor_sharpe"` → Review strategy logic
- `"insufficient_data"` → Extend date range

## Best Practices

### Do's ✓
- Always run sweeps before training
- Use Pass Gate filter on leaderboard
- Test multiple time periods
- Document your configurations
- Start with Conservative risk profile

### Don'ts ✗
- Skip the sweep phase
- Ignore gate failures
- Train on failing configurations
- Use untested parameters
- Rush to live trading

## Optimization Tips

### Sweep Efficiency
- Start with wide parameter ranges
- Narrow based on initial results
- Cache matrices (reuse matrix_sha)
- Run parallel sweeps for different risk profiles

### Performance Optimization
```bash
# Preview matrix first (quick check)
make preview MODEL_ID=spy_swing_daily START=2024-01-01 END=2024-01-31

# Calibrate thresholds
make calibrate-scanner MODEL_ID=spy_swing_daily TOP_N=50
```

## Troubleshooting

### Common Issues

**"Matrix build failed"**
- Check date range validity
- Verify ticker exists
- Ensure sufficient data

**"Sweep taking too long"**
- Reduce parameter combinations
- Use fewer splits (3 instead of 5)
- Check system load

**"No signals generated"**
- Verify model is active
- Check confidence thresholds
- Ensure market hours

**"Poor backtest results"**
- Review indicator selection
- Adjust thresholds
- Try different time period
- Check market conditions

## Advanced Features

### Custom Indicators
```python
# Add to model configuration
"custom_indicators": [
  {"name": "custom_rsi", "params": {"period": 21}},
  {"name": "volatility_filter", "params": {"threshold": 0.02}}
]
```

### Momentum Gate
```bash
# Add momentum filter to backtests
make backtest-gated MODEL_ID=spy_swing_daily \
  MOMENTUM_MIN=0.0 MOMENTUM_COLUMN=momentum_score_total
```

### Scanner Integration
```bash
# Run scanner to find opportunities
make scan-breakout UNIVERSE=sp500 TOP_N=20
```

## Summary

The BTB pipeline transforms trading ideas into validated, automated strategies:

1. **Create** model with pack and template
2. **Build** training matrix from historical data
3. **Sweep** parameter combinations
4. **Review** leaderboard for best performers
5. **Train** models with optimal settings
6. **Backtest** final validation
7. **Generate** live trading signals

Master this workflow and you'll be able to create, test, and deploy professional trading strategies systematically.

## Next Steps

- Start with a simple SwingSigma model
- Run your first sweep with default parameters
- Review results on the leaderboard
- Train only Pass Gate configurations
- Paper trade before using real money

---

## Related Reading

- [Create a Model](./create-model.md)
- [Run a Backtest](./run-backtest.md)
- [Validate Risk](./validate-risk.md)
- [Models](../../products/models.md)
- [Performance Leaderboards](../../products/performance-leaderboards.md)