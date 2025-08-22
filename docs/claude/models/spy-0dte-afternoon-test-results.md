# SPY 0DTE Model - Afternoon Hours (14:00-15:00) Test Results

**Model**: spy_opt_0dte_hourly  
**Test Date**: 2025-01-22  
**Focus**: Hours 14:00-15:00 (2-3 PM ET)  
**Data Period**: January 2024 - January 2025

---

## Executive Summary

Testing with afternoon hours only (14:00-15:00) revealed a critical issue with the 2024-2025 dataset: **insufficient signal diversity**. All backtest attempts failed with class imbalance errors, indicating that the cross-validation folds contain only one class (likely all FLAT).

---

## Data Analysis for Afternoon Hours

### Label Distribution (Hours 14-15)
```
DOWN:  42 (5.2%)
FLAT: 714 (88.1%)
UP:    54 (6.7%)
```

### Key Statistics
- **Total afternoon samples**: 810 rows
- **Actionable signals**: 96 (11.9%)
- **Non-actionable (FLAT)**: 714 (88.1%)
- **Training rows used**: 405 (hour 14 only) or 810 (both hours)

---

## Tests Attempted

### 1. Model Training Results

| Configuration | Rows Used | Status |
|--------------|-----------|---------|
| Hours 14,15 | 810 | ✅ Success |
| Hour 14 only | 405 | ✅ Success |

### 2. Backtest Attempts

| Test Type | Parameters | Result |
|-----------|------------|--------|
| Baseline (14,15) | top_pct=0.10, splits=5 | ❌ Class error |
| Baseline retrained | top_pct=0.10, splits=5 | ❌ Class error |
| Hour 14 only | top_pct=0.15, splits=3 | ❌ Class error |
| High percentage | top_pct=0.30, splits=2 | ❌ Class error |
| Parameter sweep | 18 configurations | ❌ Server error |

### 3. Test Commands Used

```bash
# Train model for afternoon hours
curl -sS -X POST http://localhost:8001/train \
  -H "Content-Type: application/json" \
  -d '{
    "model_id":"spy_opt_0dte_hourly",
    "pack_id":"zerosigma",
    "allowed_hours":"14,15"
  }'

# Baseline backtest
curl -sS -X POST http://localhost:8001/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "model_id":"spy_opt_0dte_hourly",
    "pack_id":"zerosigma",
    "top_pct":0.10,
    "splits":5,
    "allowed_hours":"14,15"
  }'

# High percentage attempt
curl -sS -X POST http://localhost:8001/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "model_id":"spy_opt_0dte_hourly",
    "pack_id":"zerosigma",
    "top_pct":0.30,
    "splits":2,
    "allowed_hours":"14,15"
  }'
```

---

## Error Analysis

### Consistent Error Message
```json
{"ok":false,"error":"Invalid classes inferred from unique values of `y`. Expected: [0], got [1]"}
```

### Root Cause
The backtest's cross-validation splits are creating folds where:
1. All samples belong to the FLAT class (88.1% of data)
2. The classifier cannot train/test on single-class data
3. Even with only 2 splits, the imbalance persists

### Why Afternoon Hours?
Hours 14-15 were chosen because:
- Previous analysis showed them as top performers
- Mid-afternoon typically has good liquidity
- Avoids opening volatility and closing chaos

However, even these "optimal" hours suffer from extreme class imbalance in the expanded dataset.

---

## Comparison with Previous Results

### Q4 2024 Data (Previous)
- Hours 14,15 were part of best config
- Achieved 0.3333 Sharpe ratio
- 6 trades per fold

### Full 2024-2025 Data (Current)
- Cannot complete backtests
- 88.1% FLAT signals
- Suggests Q4 2024 was anomalous

---

## Key Insights

### 1. Signal Scarcity
- Only 11.9% of afternoon hours present tradeable opportunities
- This aligns with 0DTE nature - most hours don't offer edge
- The strategy is correctly selective but perhaps too selective

### 2. Data Requirements
- Need stratified sampling to ensure class balance
- May need to aggregate multiple hours or days
- Consider different label generation thresholds

### 3. Model Limitations
- Classification approach may not suit this imbalanced data
- Regression or ranking models might work better
- Need custom cross-validation strategy

---

## Recommendations

### Immediate Solutions

1. **Modify Cross-Validation**
   - Use StratifiedKFold instead of TimeSeriesSplit
   - Ensure minimum samples per class per fold
   - Consider leave-one-out or custom splitting

2. **Adjust Label Generation**
   - Lower threshold for UP/DOWN classification
   - Use percentile-based labels instead of fixed thresholds
   - Consider binary classification (TRADE/NO_TRADE)

3. **Data Filtering**
   - Focus on high-volatility days only (VIX > 15)
   - Filter for days with known catalysts (Fed, earnings)
   - Use only days with sufficient price movement

### Alternative Approaches

1. **Change Model Type**
   - Switch from classification to regression
   - Predict magnitude instead of direction
   - Use anomaly detection for rare opportunities

2. **Ensemble Approach**
   - Train separate models for different market regimes
   - Combine predictions from multiple timeframes
   - Use meta-learning to select when to trade

3. **Reduce Selectivity**
   - Increase top_pct to 40-50% for testing
   - Trade every signal above minimal threshold
   - Use position sizing to manage risk instead

---

## Files Generated

### Test Results
- `results_2025_afternoon/baseline_14_15.json`
- `results_2025_afternoon/baseline_retrained.json`
- `results_2025_afternoon/hour_14_only.json`
- `results_2025_afternoon/high_pct_test.json`
- `results_2025_afternoon/sweep_afternoon.json`

### Model Artifacts
- Retrained model saved to standard location
- 810 rows used for afternoon training
- 405 rows for hour 14 only

---

## Conclusion

The afternoon-only tests (14:00-15:00) confirm that the 2024-2025 dataset has fundamental challenges:

1. **Extreme class imbalance** (88% FLAT) makes standard backtesting impossible
2. **Signal scarcity** is inherent to 0DTE strategies but exceeds system capabilities
3. **Infrastructure limitations** - the backtest API cannot handle single-class folds

The good performance seen with Q4 2024 data appears to have been an anomaly or the result of overfitting to a particularly favorable period. The expanded dataset reveals the true challenge of 0DTE trading: finding the rare moments when same-day options offer a tradeable edge.

### Next Steps
1. Work with engineering to fix the backtest API's handling of imbalanced data
2. Consider alternative labeling or modeling approaches
3. Focus on identifying the specific conditions that create tradeable opportunities
4. Test with even more selective filters (VIX levels, event days, etc.)