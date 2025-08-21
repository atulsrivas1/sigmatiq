# SwingSigma — Complete Example Workflow (v1.1)

**Purpose:** Concrete end‑to‑end example from pack to live alerts. Mirrors the v1.1 Spec.  
**Pack:** swingsigma (Swing Sigma)  
**Inspiration:** v1.0 example, reconciled with Spec updates. 【8†source】【10†source】

---

## A) Pack definition — SwingSigma
```yaml
# packs/swingsigma/pack.yaml
pack:
  id: "swingsigma"
  name: "Swing Sigma"
  version: "1.1.0"
  description: "2–10 day swing strategies for stocks and options"
  author: "Sigmatiq Team"
  created_at: "2024-01-01"

metadata:
  vibe:
    time_horizon: "days"
    risk_appetite: "balanced"
    decision_style: "technical"
    market_preference: "trending"
    execution_character: "patient"

tags: ["swing","technical","intermediate","stocks","options","2-10_days"]

supported_instruments: ["stocks","options"]
default_instrument: "stocks"
```
Indicators, features, strategies, gates, and policies match the v1.0 example with unchanged defaults. 【8†source】

---

## B) Model creation
```yaml
# models/user_12345/spy_swing_momentum_v1/config.yaml
model:
  id: "spy_swing_momentum_v1"
  pack_id: "swingsigma"
  user_id: "user_12345"
  created_at: "2024-01-15T10:00:00Z"

instrument:
  type: "stocks"
  ticker: "SPY"

strategy:
  id: "momentum_swing"
  entry_rules:
    - "rsi > 50 AND rsi < 70"
    - "macd_cross == true"
    - "adx > 25"
    - "price > ema_20"
  exit_rules:
    - "rsi > 70 OR rsi < 30"
    - "macd_cross == false"
    - "price < ema_20"

indicators:
  - rsi: { period: 21 }
  - macd: { fast_period: 12, slow_period: 26, signal_period: 9 }
  - adx: { period: 14, threshold: 25 }
  - ema_20: { period: 20 }
  - ema_50: { period: 50 }
  - bollinger_bands: { period: 20, std_dev: 2 }
  - volume_ma: { period: 20 }

features: [rsi_divergence, macd_cross, trend_strength, volume_surge, momentum_composite]

risk_management:
  stop_loss_pct: 6
  take_profit_pct: 16
  max_position_pct: 3
  trailing_stop: true
  trailing_stop_pct: 5
```
【8†source】

---

## C) Sweep configuration

### Simple sweep (Swing packs)
```json
{
  "model_id": "spy_swing_momentum_v1",
  "sweep_type": "simple",
  "date_range": {"start": "2022-01-01", "end": "2023-12-31"},
  "parameters": {
    "thresholds": [0.50, 0.55, 0.60, 0.65, 0.70],
    "allowed_hours": ["all_day", "morning_only", "afternoon_only"],
    "position_size_pct": [1, 2, 3]
  },
  "tag": "initial_sweep_jan2024"
}
```

### Custom sweep (Pro)
```json
{
  "model_id": "spy_swing_momentum_v1",
  "sweep_type": "custom",
  "date_range": {"start": "2022-01-01", "end": "2023-12-31"},
  "parameters": {
    "thresholds": [0.45,0.50,0.55,0.60,0.65,0.70,0.75],
    "allowed_hours": [[9,10],[9,10,11],[13,14,15],[14,15,16],"all_day"],
    "position_size_pct": [1,2,3,4,5],
    "rsi_period": [14,21,28],
    "stop_loss_pct": [4,6,8,10],
    "take_profit_pct": [12,16,20],
    "trailing_stop_pct": [3,5,7]
  },
  "quality_gates": {"min_trades": 30, "min_sharpe": 0.7, "max_drawdown_pct": 25},
  "tag": "advanced_optimization_jan2024"
}
```
Caps and parameter naming align with Spec v1.1. 【10†source】

---

## D) Backtests and leaderboard

### Example backtest run
```json
{
  "combo_id": 15,
  "model_id": "spy_swing_momentum_v1",
  "config": {
    "threshold": 0.60,
    "allowed_hours": [9, 10, 11],
    "position_size_pct": 2,
    "rsi_period": 21,
    "stop_loss_pct": 6,
    "take_profit_pct": 16
  },
  "metrics": {
    "total_return": 0.287,
    "annualized_return": 0.143,
    "sharpe_ratio": 1.85,
    "sortino_ratio": 2.24,
    "max_drawdown": -0.118,
    "win_rate": 0.58,
    "profit_factor": 2.1,
    "total_trades": 87,
    "avg_trade_duration_days": 4.2,
    "best_trade": 0.089,
    "worst_trade": -0.061,
    "avg_winner": 0.028,
    "avg_loser": -0.013
  },
  "gate_results": {
    "pass": true,
    "checks": {
      "min_trades": {"required": 30, "actual": 87, "pass": true},
      "min_sharpe": {"required": 0.7, "actual": 1.85, "pass": true},
      "max_drawdown": {"required": 0.25, "actual": 0.118, "pass": true},
      "min_win_rate": {"required": 0.40, "actual": 0.58, "pass": true}
    }
  },
  "config_hash": "abc123"
}
```

### Leaderboard slice
```json
{
  "sweep_id": "sweep_20240115_103000",
  "model_id": "spy_swing_momentum_v1",
  "leaderboard": [
    {"rank": 1, "combo_id": 15, "sharpe": 1.85, "return": 0.287, "trades": 87, "gate": "PASS"},
    {"rank": 2, "combo_id": 23, "sharpe": 1.72, "return": 0.245, "trades": 62, "gate": "PASS"},
    {"rank": 3, "combo_id": 8,  "sharpe": 1.54, "return": 0.312, "trades": 124, "gate": "PASS"}
  ]
}
```
【8†source】

---

## E) Training

### Selection
```json
{
  "model_id": "spy_swing_momentum_v1",
  "selected_configs": [
    {"combo_id": 15, "rank": 1},
    {"combo_id": 23, "rank": 2}
  ],
  "training_params": {
    "algorithm": "xgboost",
    "validation_method": "time_series_split",
    "test_size": 0.2,
    "calibration": "sigmoid"
  }
}
```

### Job and results
```json
{
  "job_id": "train_001",
  "trained_model_id": "spy_swing_momentum_v1_trained_001",
  "status": "completed",
  "metrics": {
    "training": {"accuracy": 0.72, "precision": 0.68, "recall": 0.75, "f1_score": 0.71, "auc_roc": 0.78},
    "validation": {"accuracy": 0.69, "precision": 0.65, "recall": 0.71, "f1_score": 0.68, "auc_roc": 0.74}
  },
  "feature_importance": [
    {"feature": "momentum_composite", "importance": 0.24},
    {"feature": "trend_strength", "importance": 0.18},
    {"feature": "rsi_divergence", "importance": 0.15},
    {"feature": "macd_cross", "importance": 0.12},
    {"feature": "volume_surge", "importance": 0.10}
  ],
  "artifacts": {
    "model_file": "models/spy_swing_momentum_v1_trained_001.pkl",
    "scaler_file": "models/spy_swing_momentum_v1_scaler_001.pkl",
    "metadata_file": "models/spy_swing_momentum_v1_meta_001.json"
  }
}
```
【8†source】【10†source】

---

## F) Publish and paper trade

### Publish trained artifact
```http
POST /trained-models/spy_swing_momentum_v1_trained_001/publish
Content-Type: application/json

{
  "name": "SPY Morning Momentum",
  "description": "Trades SPY momentum in morning hours with 58% win rate",
  "alert_frequency": "5_minutes",
  "max_alerts_per_day": 3,
  "paper_trade_first": true,
  "paper_trade_duration_days": 14
}
```

### Response (paper mode)
```json
{
  "id": "pub_spy_momentum_001",
  "status": "paper_trading",
  "paper_trade_start": "2024-01-16T09:30:00Z",
  "paper_trade_end": "2024-01-30T09:30:00Z",
  "live_date": "2024-01-30T09:30:00Z"
}
```
【8†source】【10†source】

---

## G) Alerts

### Real‑time processing sample
```json
{
  "timestamp": "2024-01-30T10:15:00Z",
  "ticker": "SPY",
  "indicators": {
    "rsi": 61.5,
    "macd": {"macd_line": 1.23, "signal_line": 0.98, "histogram": 0.25},
    "adx": 28.4,
    "ema_20": 451.20,
    "ema_50": 448.75,
    "bollinger_bands": {"upper": 456.80, "middle": 452.10, "lower": 447.40},
    "volume_ma": 2103400
  },
  "features": {"macd_cross": true, "trend_strength": 0.73, "volume_surge": true, "momentum_composite": 0.68}
}
```

### Generated alert (core + optional blocks)
```json
{
  "alert_id": "alert_20240130_101500_001",
  "timestamp": "2024-01-30T10:15:00Z",
  "model_id": "pub_spy_momentum_001",
  "action": "BUY",
  "instrument": "stock",
  "ticker": "SPY",
  "quantity": 22,
  "confidence": 0.72,
  "entry_price": 453.50,
  "stop_loss": 426.29,
  "take_profit": 525.61,
  "urgency": "immediate",
  "valid_until": "2024-01-30T16:00:00Z",

  "metadata": {
    "strategy": "momentum_swing",
    "pack": "swingsigma",
    "features": {"rsi": 61.5, "macd_cross": true, "trend_strength": 0.73, "volume_surge": true},
    "backtest_stats": {"historical_win_rate": 0.58, "avg_return": 0.028, "avg_duration": 4.2}
  },

  "routing": [
    {"service": "sigma_sim", "status": "sent", "timestamp": "2024-01-30T10:15:01Z"},
    {"service": "user_email", "status": "sent", "timestamp": "2024-01-30T10:15:02Z"},
    {"service": "mobile_push", "status": "sent", "timestamp": "2024-01-30T10:15:02Z"}
  ]
}
```
Latency SLO measures generation (T1−T0) separately from delivery. 【8†source】【10†source】

---

## H) Performance tracking and go‑live
```json
{
  "model_id": "pub_spy_momentum_001",
  "period": "2024-01-30 to 2024-02-13",
  "paper_trading_results": {
    "total_trades": 8,
    "winning_trades": 5,
    "losing_trades": 3,
    "win_rate": 0.625,
    "total_return": 0.0425,
    "sharpe_ratio": 1.68,
    "max_drawdown": -0.028,
    "avg_trade_return": 0.0053
  },
  "recommendation": "APPROVE_FOR_LIVE_TRADING"
}
```
If approved, configure Pilot and go live on scheduled date. 【8†source】
