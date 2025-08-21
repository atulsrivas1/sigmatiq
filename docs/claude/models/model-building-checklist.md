# Model Building Checklist & Best Practices

**Purpose**: Standardized checklist for building new models in the Sigmatiq system  
**Based on**: SPY 0DTE model development experience

---

## Pre-Development Checklist

### 1. Strategy Selection
- [ ] **Market Research**: Is there a documented edge in this strategy?
- [ ] **Liquidity Check**: Is there sufficient volume for entries/exits?
- [ ] **Data Availability**: Do we have quality historical data?
- [ ] **Competition Analysis**: How crowded is this trade?
- [ ] **Risk/Reward**: Is the potential return worth the risk?

### 2. Pack Selection
- [ ] Review available packs: `make packs`
- [ ] Check pack details: `make pack-detail PACK_ID=<pack>`
- [ ] Review indicator sets in pack
- [ ] Verify pack matches strategy timeframe
- [ ] Check for pack-specific templates

### 3. Model Parameters
- [ ] **Ticker**: Most liquid instrument for strategy
- [ ] **Asset**: `opt` for options, `eq` for equities
- [ ] **Horizon**: `0dte`, `intraday`, `swing`, `long`
- [ ] **Cadence**: `5m`, `15m`, `hourly`, `daily`
- [ ] **Algorithm**: `xgb` (default), `lgb`, `rf`
- [ ] **Variant**: Version identifier (v1, v2, etc.)

---

## Development Process

### Step 1: Initialize Model
```bash
make init-auto \
  TICKER=<ticker> \
  ASSET=<opt|eq> \
  HORIZON=<horizon> \
  CADENCE=<cadence> \
  PACK_ID=<pack> \
  ALGO=<algo> \
  VARIANT=<version>
```
- [ ] Model created successfully
- [ ] Directory structure verified
- [ ] Policy.yaml created

### Step 2: Configure Policy
Edit `models/<pack>/<model_id>/policy.yaml`:
- [ ] Update description with strategy rationale
- [ ] Select appropriate feature set
- [ ] Configure backtest parameters
- [ ] Set training parameters

### Step 3: Build Feature Matrix
```bash
make build MODEL_ID=<model_id> START=<date> END=<date>
```
- [ ] Date range appropriate for strategy (3-6 months for short-term, 1-2 years for long-term)
- [ ] Build completes without errors
- [ ] Matrix saved with SHA hash
- [ ] Data quality verified

### Step 4: Run Backtest
```bash
make backtest MODEL_ID=<model_id> THRESHOLDS=<list> SPLITS=<n>
```
- [ ] Cross-validation folds appropriate (5 default)
- [ ] Thresholds cover reasonable range (0.50-0.70)
- [ ] Results saved to database
- [ ] Metrics within realistic ranges

### Step 5: Analyze Results
```bash
make leaderboard MODEL_ID=<model_id>
```
- [ ] Review Sharpe ratios (expect 0.3-0.8)
- [ ] Check win rates (expect 45-60%)
- [ ] Verify trade counts (sufficient samples)
- [ ] Analyze drawdowns (acceptable risk)

### Step 6: Parameter Optimization (Optional)
```bash
make sweeps MODEL_ID=<model_id>
```
- [ ] Sweep completes successfully
- [ ] Optimal parameters identified
- [ ] Improvement over baseline verified
- [ ] Not overfit (check validation metrics)

### Step 7: Train Final Model
```bash
make train MODEL_ID=<model_id> ALLOWED_HOURS=<hours>
```
- [ ] Training completes successfully
- [ ] Model artifacts saved
- [ ] Feature importance reviewed
- [ ] Validation metrics acceptable

---

## Indicator Selection Guide

### For 0DTE/Intraday Strategies
**Must Have**:
- Opening dynamics (gaps, initial range)
- Fast technical indicators (RSI < 14, EMA < 20)
- Options flow metrics (put/call ratios)
- Time-based features (hour, day)
- Volatility measures (ATR, realized vol)

**Nice to Have**:
- Greeks (delta, gamma, vega)
- Market microstructure (bid/ask, order flow)
- Correlated assets (VIX, bonds)

### For Swing Strategies (2-10 days)
**Must Have**:
- Standard technical indicators (RSI 14, MACD)
- Moving averages (20, 50, 200)
- Volume indicators (OBV, CMF)
- Daily/weekly timeframe features
- Trend strength (ADX)

**Nice to Have**:
- Sector relative strength
- Fundamental data
- Sentiment indicators

### For Long-term Strategies (>10 days)
**Must Have**:
- Long moving averages (50, 100, 200)
- Momentum indicators (ROC, Aroon)
- Volatility ratios (IV percentile)
- Fundamental factors
- Regime indicators

**Nice to Have**:
- Macro indicators
- Seasonality features
- Cross-asset correlations

---

## Performance Expectations by Strategy Type

### 0DTE Options
- **Sharpe Ratio**: 0.5-0.8
- **Win Rate**: 55-60%
- **Avg Trade Duration**: 1-4 hours
- **Trades per Day**: 1-3
- **Max Drawdown**: 10-15%

### Swing Trading
- **Sharpe Ratio**: 0.6-1.0
- **Win Rate**: 45-55%
- **Avg Trade Duration**: 3-7 days
- **Trades per Month**: 5-15
- **Max Drawdown**: 15-25%

### Long-term
- **Sharpe Ratio**: 0.8-1.2
- **Win Rate**: 40-50%
- **Avg Trade Duration**: 20-60 days
- **Trades per Year**: 10-30
- **Max Drawdown**: 20-35%

---

## Common Pitfalls to Avoid

### Data Issues
- ❌ Using future information (look-ahead bias)
- ❌ Ignoring survivorship bias
- ❌ Not accounting for splits/dividends
- ❌ Training on insufficient data
- ❌ Ignoring regime changes

### Model Issues
- ❌ Overfitting to historical data
- ❌ Ignoring transaction costs
- ❌ Unrealistic fill assumptions
- ❌ Not using cross-validation
- ❌ Cherry-picking best results

### Risk Issues
- ❌ No position size limits
- ❌ Missing stop losses
- ❌ Ignoring correlation risk
- ❌ No drawdown limits
- ❌ Trading in illiquid instruments

---

## Quality Gates

### Before Moving to Production
- [ ] **Sharpe Ratio > 0.3** (after realistic costs)
- [ ] **Win Rate > 45%** (statistically significant)
- [ ] **Trade Count > 30** (sufficient sample size)
- [ ] **Max Drawdown < 25%** (acceptable risk)
- [ ] **Validation Performance** within 20% of training
- [ ] **Paper Trading** for minimum 2 weeks
- [ ] **Slippage Analysis** completed
- [ ] **Risk Limits** configured

---

## Documentation Requirements

For each model, document:
1. **Strategy Thesis**: Why should this work?
2. **Edge Source**: What inefficiency are we exploiting?
3. **Risk Factors**: What could go wrong?
4. **Feature Rationale**: Why these indicators?
5. **Parameter Choices**: Why these values?
6. **Performance Expectations**: Realistic targets
7. **Monitoring Plan**: How to track degradation
8. **Exit Criteria**: When to stop trading

---

## Post-Development Monitoring

### Daily
- [ ] Check prediction distribution
- [ ] Monitor feature stability
- [ ] Track actual vs expected performance
- [ ] Review any stopped out trades

### Weekly
- [ ] Calculate rolling Sharpe
- [ ] Review feature importance changes
- [ ] Analyze slippage trends
- [ ] Check for regime changes

### Monthly
- [ ] Full performance review
- [ ] Retrain if degraded > 20%
- [ ] Update documentation
- [ ] Review and adjust risk limits

---

## Emergency Procedures

### If Model Degrades
1. **Immediate**: Reduce position size by 50%
2. **Day 1**: Analyze what changed
3. **Day 2**: Retrain with recent data
4. **Day 3**: Paper trade new version
5. **Day 7**: Resume if improved, else pause

### If Drawdown Exceeds Limit
1. **Stop all new trades**
2. **Close losing positions**
3. **Analyze root cause**
4. **Paper trade for 1 week**
5. **Resume at 50% size**

---

## Useful Commands Reference

```bash
# Discovery
make packs                          # List all packs
make pack-detail PACK_ID=<pack>    # Pack details
make models                         # List all models

# Development
make init-auto ...                  # Create model
make build ...                      # Build matrix
make backtest ...                   # Run backtest
make sweeps ...                     # Parameter sweep
make train ...                      # Train model

# Analysis
make leaderboard MODEL_ID=<id>      # View results
make runs-build MODEL_ID=<id>       # Build history
make runs-train MODEL_ID=<id>       # Training history

# Production
make predict MODEL_ID=<id>          # Generate predictions
make performance MODEL_ID=<id>      # Track performance
```

---

**Document Purpose**: Ensure consistent, high-quality model development  
**Last Updated**: January 2025  
**Maintained By**: Sigmatiq Team