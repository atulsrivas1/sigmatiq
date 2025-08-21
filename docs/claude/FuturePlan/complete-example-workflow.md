# Complete Example Workflow: SwingSigma Pack

## Overview
This document provides a complete, concrete example of the entire Sigmatiq workflow from Pack definition through to alert generation, using actual configurations and parameters.

---

## Step 1: Pack Definition - SwingSigma

### 1.1 Pack Configuration File
```yaml
# packs/swingsigma/pack.yaml
pack:
  id: "swingsigma"
  name: "Swing Sigma"
  version: "1.0.0"
  description: "2-10 day swing trading strategies for stocks and options"
  author: "Sigmatiq Team"
  created_at: "2024-01-01"
  
metadata:
  vibe:
    time_horizon: "days"  # seconds, minutes, hours, days, weeks, months
    risk_appetite: "balanced"  # conservative, balanced, aggressive
    decision_style: "technical"  # technical, fundamental, sentiment, flow
    market_preference: "trending"  # trending, ranging, volatile, all_weather
    execution_character: "patient"  # aggressive, patient, adaptive
  
  tags:
    - "swing"
    - "technical"
    - "intermediate"
    - "stocks"
    - "options"
    - "2-10_days"
    
supported_instruments:
  - "stocks"
  - "options"
  
default_instrument: "stocks"
```

### 1.2 Available Indicators
```yaml
# packs/swingsigma/indicators.yaml
indicators:
  momentum:
    - id: "rsi"
      name: "Relative Strength Index"
      params:
        period: 14
        overbought: 70
        oversold: 30
      
    - id: "macd"
      name: "MACD"
      params:
        fast_period: 12
        slow_period: 26
        signal_period: 9
        
    - id: "stochastic"
      name: "Stochastic Oscillator"
      params:
        k_period: 14
        d_period: 3
        smooth_k: 3
        
  trend:
    - id: "ema_20"
      name: "20-day EMA"
      params:
        period: 20
        
    - id: "ema_50"
      name: "50-day EMA"
      params:
        period: 50
        
    - id: "adx"
      name: "Average Directional Index"
      params:
        period: 14
        threshold: 25
        
  volatility:
    - id: "bollinger_bands"
      name: "Bollinger Bands"
      params:
        period: 20
        std_dev: 2
        
    - id: "atr"
      name: "Average True Range"
      params:
        period: 14
        
  volume:
    - id: "obv"
      name: "On-Balance Volume"
      params:
        cumulative: true
        
    - id: "volume_ma"
      name: "Volume Moving Average"
      params:
        period: 20
```

### 1.3 Features (Derived from Indicators)
```yaml
# packs/swingsigma/features.yaml
features:
  - id: "rsi_divergence"
    name: "RSI Price Divergence"
    calculation: "detect_divergence(price, rsi)"
    
  - id: "macd_cross"
    name: "MACD Signal Cross"
    calculation: "macd_line > signal_line"
    
  - id: "trend_strength"
    name: "Trend Strength Score"
    calculation: "adx * sign(ema_20 - ema_50)"
    
  - id: "bb_squeeze"
    name: "Bollinger Band Squeeze"
    calculation: "(bb_upper - bb_lower) / bb_middle < 0.04"
    
  - id: "volume_surge"
    name: "Volume Surge"
    calculation: "volume > volume_ma * 1.5"
    
  - id: "momentum_composite"
    name: "Momentum Composite Score"
    calculation: "normalized(rsi) + normalized(macd) + normalized(stochastic)"
```

### 1.4 Strategies
```yaml
# packs/swingsigma/strategies.yaml
strategies:
  - id: "momentum_swing"
    name: "Momentum Swing"
    description: "Trade strong momentum with trend confirmation"
    entry_logic:
      - "rsi > 50 AND rsi < 70"
      - "macd_cross == true"
      - "adx > 25"
      - "price > ema_20"
    exit_logic:
      - "rsi > 70 OR rsi < 30"
      - "macd_cross == false"
      - "price < ema_20"
      
  - id: "mean_reversion_swing"
    name: "Mean Reversion Swing"
    description: "Fade extremes with oversold bounce"
    entry_logic:
      - "rsi < 30"
      - "price < bb_lower"
      - "volume_surge == true"
      - "stochastic < 20"
    exit_logic:
      - "rsi > 50"
      - "price > bb_middle"
      - "stochastic > 80"
      
  - id: "breakout_swing"
    name: "Breakout Swing"
    description: "Trade range breakouts with volume"
    entry_logic:
      - "bb_squeeze == true"
      - "price > bb_upper"
      - "volume_surge == true"
      - "adx increasing"
    exit_logic:
      - "price < ema_20"
      - "volume < volume_ma"
      - "adx < 20"
```

### 1.5 Risk Gates
```yaml
# packs/swingsigma/gates.yaml
gates:
  quality:
    min_trades: 30
    min_sharpe: 0.7
    max_drawdown_pct: 25
    min_win_rate: 40
    
  execution:
    max_slippage_bps: 10
    min_volume: 100000
    max_spread_pct: 1.0
    
  risk:
    max_position_size_pct: 5
    max_correlation: 0.7
    max_var_95: 10
```

### 1.6 Policies
```yaml
# packs/swingsigma/policies.yaml
policies:
  execution:
    order_type: "limit"
    time_in_force: "day"
    wait_for_confirmation: true
    partial_fills_allowed: true
    
  position_sizing:
    method: "kelly_fraction"
    max_position_pct: 5
    scale_in_allowed: true
    max_positions: 10
    
  risk_management:
    stop_loss_pct: 8
    take_profit_pct: 16
    trailing_stop: true
    trailing_stop_pct: 5
    time_stop_days: 10
```

---

## Step 2: Model Creation

### 2.1 User Creates Model from Pack
```python
# User Input via UI or API
create_model_request = {
    "model_id": "spy_swing_momentum_v1",
    "pack_id": "swingsigma",
    "user_id": "user_12345",
    "name": "SPY Momentum Swing",
    "description": "My SPY swing trading model using momentum strategy",
    
    # Instrument selection
    "instrument": "stocks",
    "ticker": "SPY",
    
    # Strategy selection (from pack)
    "strategy_id": "momentum_swing",
    
    # Indicator selection (subset of pack indicators)
    "selected_indicators": [
        "rsi",
        "macd", 
        "adx",
        "ema_20",
        "ema_50",
        "bollinger_bands",
        "volume_ma"
    ],
    
    # Feature selection
    "selected_features": [
        "rsi_divergence",
        "macd_cross",
        "trend_strength",
        "volume_surge",
        "momentum_composite"
    ],
    
    # Risk profile
    "risk_profile": "balanced",
    
    # Override some default parameters
    "parameter_overrides": {
        "rsi_period": 21,  # Changed from default 14
        "stop_loss_pct": 6,  # Tighter than default 8
        "max_position_pct": 3  # Smaller than default 5
    }
}

# API Response
model_created_response = {
    "success": true,
    "model": {
        "id": "spy_swing_momentum_v1",
        "status": "created",
        "created_at": "2024-01-15T10:00:00Z",
        "next_step": "configure_sweep"
    }
}
```

### 2.2 Generated Model Configuration
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
  - rsi:
      period: 21  # Overridden
  - macd:
      fast_period: 12
      slow_period: 26
      signal_period: 9
  - adx:
      period: 14
      threshold: 25
  - ema_20:
      period: 20
  - ema_50:
      period: 50
  - bollinger_bands:
      period: 20
      std_dev: 2
  - volume_ma:
      period: 20
      
features:
  - rsi_divergence
  - macd_cross
  - trend_strength
  - volume_surge
  - momentum_composite
  
risk_management:
  stop_loss_pct: 6  # Overridden
  take_profit_pct: 16
  max_position_pct: 3  # Overridden
  trailing_stop: true
  trailing_stop_pct: 5
```

---

## Step 3: Sweep Configuration

### 3.1 User Configures Sweep
```python
# Simple Sweep Configuration (Beginner)
simple_sweep_config = {
    "model_id": "spy_swing_momentum_v1",
    "sweep_type": "simple",
    "date_range": {
        "start": "2022-01-01",
        "end": "2023-12-31"
    },
    "parameters": {
        "thresholds": [0.50, 0.55, 0.60, 0.65, 0.70],
        "allowed_hours": ["all_day", "morning_only", "afternoon_only"],
        "position_size_pct": [1, 2, 3]
    },
    "tag": "initial_sweep_jan2024"
}

# Custom Sweep Configuration (Advanced)
custom_sweep_config = {
    "model_id": "spy_swing_momentum_v1",
    "sweep_type": "custom",
    "date_range": {
        "start": "2022-01-01",
        "end": "2023-12-31"
    },
    "parameters": {
        # Core parameters
        "thresholds": [0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75],
        "allowed_hours": [
            [9, 10],
            [9, 10, 11],
            [13, 14, 15],
            [14, 15, 16],
            "all_day"
        ],
        "position_size_pct": [1, 2, 3, 4, 5],
        
        # Additional parameters
        "rsi_period": [14, 21, 28],
        "stop_loss_pct": [4, 6, 8, 10],
        "take_profit_pct": [12, 16, 20],
        "trailing_stop_pct": [3, 5, 7]
    },
    "quality_gates": {
        "min_trades": 30,
        "min_sharpe": 0.7,
        "max_drawdown_pct": 25
    },
    "tag": "advanced_optimization_jan2024"
}
```

### 3.2 Sweep Execution
```python
# System generates all combinations
sweep_combinations = [
    {
        "combo_id": 1,
        "threshold": 0.50,
        "allowed_hours": "all_day",
        "position_size_pct": 1,
        "config_hash": "abc123"
    },
    {
        "combo_id": 2,
        "threshold": 0.50,
        "allowed_hours": "all_day",
        "position_size_pct": 2,
        "config_hash": "def456"
    },
    # ... 45 total combinations for simple sweep
    # ... 2,940 combinations for custom sweep
]

# Example of one backtest run
backtest_run = {
    "combo_id": 15,
    "config": {
        "threshold": 0.60,
        "allowed_hours": [9, 10, 11],
        "position_size_pct": 2
    },
    "execution_log": [
        {
            "timestamp": "2024-01-15T10:30:00Z",
            "status": "started",
            "message": "Loading data matrix"
        },
        {
            "timestamp": "2024-01-15T10:30:05Z", 
            "status": "processing",
            "message": "Calculating indicators"
        },
        {
            "timestamp": "2024-01-15T10:30:15Z",
            "status": "processing",
            "message": "Running backtest simulation"
        },
        {
            "timestamp": "2024-01-15T10:30:45Z",
            "status": "completed",
            "message": "Backtest complete, calculating metrics"
        }
    ]
}
```

---

## Step 4: Backtest Results & Leaderboard

### 4.1 Individual Backtest Result
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
  "trades_sample": [
    {
      "entry_date": "2022-01-15",
      "exit_date": "2022-01-19",
      "entry_price": 450.25,
      "exit_price": 458.75,
      "return": 0.0189,
      "duration_days": 4
    },
    {
      "entry_date": "2022-02-03",
      "exit_date": "2022-02-08",
      "entry_price": 442.10,
      "exit_price": 438.90,
      "return": -0.0072,
      "duration_days": 5
    }
    // ... more trades
  ]
}
```

### 4.2 Leaderboard
```json
{
  "sweep_id": "sweep_20240115_103000",
  "model_id": "spy_swing_momentum_v1",
  "total_combinations": 45,
  "passed_gates": 28,
  "failed_gates": 17,
  "leaderboard": [
    {
      "rank": 1,
      "combo_id": 15,
      "config": {
        "threshold": 0.60,
        "allowed_hours": [9, 10, 11],
        "position_size_pct": 2
      },
      "sharpe": 1.85,
      "return": 0.287,
      "trades": 87,
      "gate": "PASS",
      "selection_checkbox": false
    },
    {
      "rank": 2,
      "combo_id": 23,
      "config": {
        "threshold": 0.65,
        "allowed_hours": [13, 14, 15],
        "position_size_pct": 2
      },
      "sharpe": 1.72,
      "return": 0.245,
      "trades": 62,
      "gate": "PASS",
      "selection_checkbox": false
    },
    {
      "rank": 3,
      "combo_id": 8,
      "config": {
        "threshold": 0.55,
        "allowed_hours": "all_day",
        "position_size_pct": 3
      },
      "sharpe": 1.54,
      "return": 0.312,
      "trades": 124,
      "gate": "PASS",
      "selection_checkbox": false
    }
    // ... remaining results
  ]
}
```

---

## Step 5: Training

### 5.1 User Selection for Training
```python
# User selects top 2 configurations
training_selection = {
    "model_id": "spy_swing_momentum_v1",
    "selected_configs": [
        {
            "combo_id": 15,
            "rank": 1,
            "config": {
                "threshold": 0.60,
                "allowed_hours": [9, 10, 11],
                "position_size_pct": 2
            }
        },
        {
            "combo_id": 23,
            "rank": 2,
            "config": {
                "threshold": 0.65,
                "allowed_hours": [13, 14, 15],
                "position_size_pct": 2
            }
        }
    ],
    "training_params": {
        "algorithm": "xgboost",
        "validation_method": "time_series_split",
        "test_size": 0.2,
        "calibration": "sigmoid"
    }
}
```

### 5.2 Training Process
```python
# Training Job 1
training_job_1 = {
    "job_id": "train_001",
    "model_id": "spy_swing_momentum_v1",
    "combo_id": 15,
    "status": "training",
    "progress": [
        {"step": "data_preparation", "status": "complete", "duration": 45},
        {"step": "feature_engineering", "status": "complete", "duration": 120},
        {"step": "model_training", "status": "in_progress", "duration": 300},
        {"step": "validation", "status": "pending", "duration": null},
        {"step": "calibration", "status": "pending", "duration": null}
    ],
    "hyperparameters": {
        "n_estimators": 200,
        "max_depth": 5,
        "learning_rate": 0.01,
        "subsample": 0.8,
        "colsample_bytree": 0.8
    }
}

# Training Results
training_results_1 = {
    "job_id": "train_001",
    "model_id": "spy_swing_momentum_v1",
    "trained_model_id": "spy_swing_momentum_v1_trained_001",
    "combo_id": 15,
    "status": "completed",
    "metrics": {
        "training": {
            "accuracy": 0.72,
            "precision": 0.68,
            "recall": 0.75,
            "f1_score": 0.71,
            "auc_roc": 0.78
        },
        "validation": {
            "accuracy": 0.69,
            "precision": 0.65,
            "recall": 0.71,
            "f1_score": 0.68,
            "auc_roc": 0.74
        }
    },
    "feature_importance": [
        {"feature": "momentum_composite", "importance": 0.24},
        {"feature": "trend_strength", "importance": 0.18},
        {"feature": "rsi_divergence", "importance": 0.15},
        {"feature": "macd_cross", "importance": 0.12},
        {"feature": "volume_surge", "importance": 0.10}
    ],
    "model_artifacts": {
        "model_file": "models/spy_swing_momentum_v1_trained_001.pkl",
        "scaler_file": "models/spy_swing_momentum_v1_scaler_001.pkl",
        "metadata_file": "models/spy_swing_momentum_v1_meta_001.json"
    }
}
```

---

## Step 6: Model Publishing

### 6.1 Review and Publish Decision
```python
# User reviews both trained models
model_review = {
    "trained_models": [
        {
            "id": "spy_swing_momentum_v1_trained_001",
            "combo_id": 15,
            "sharpe_backtest": 1.85,
            "sharpe_validation": 1.72,
            "user_decision": "publish"
        },
        {
            "id": "spy_swing_momentum_v1_trained_002",
            "combo_id": 23,
            "sharpe_backtest": 1.72,
            "sharpe_validation": 1.45,
            "user_decision": "discard"  # Validation performance dropped
        }
    ]
}

# Publish the selected model
publish_request = {
    "trained_model_id": "spy_swing_momentum_v1_trained_001",
    "publish_settings": {
        "name": "SPY Morning Momentum",
        "description": "Trades SPY momentum in morning hours with 58% win rate",
        "alert_frequency": "5_minutes",
        "max_alerts_per_day": 3,
        "paper_trade_first": true,
        "paper_trade_duration_days": 14
    }
}

publish_response = {
    "success": true,
    "published_model": {
        "id": "pub_spy_momentum_001",
        "status": "paper_trading",
        "paper_trade_start": "2024-01-16T09:30:00Z",
        "paper_trade_end": "2024-01-30T09:30:00Z",
        "live_date": "2024-01-30T09:30:00Z"
    }
}
```

---

## Step 7: Alert Generation (Production)

### 7.1 Real-Time Data Processing
```python
# Every 5 minutes during market hours
realtime_data = {
    "timestamp": "2024-01-30T10:15:00Z",
    "ticker": "SPY",
    "ohlcv": {
        "open": 452.30,
        "high": 453.85,
        "low": 451.90,
        "close": 453.45,
        "volume": 2847300
    },
    "indicators_calculated": {
        "rsi": 61.5,
        "macd": {
            "macd_line": 1.23,
            "signal_line": 0.98,
            "histogram": 0.25
        },
        "adx": 28.4,
        "ema_20": 451.20,
        "ema_50": 448.75,
        "bollinger_bands": {
            "upper": 456.80,
            "middle": 452.10,
            "lower": 447.40
        },
        "volume_ma": 2103400
    },
    "features_calculated": {
        "rsi_divergence": 0.12,
        "macd_cross": true,
        "trend_strength": 0.73,
        "volume_surge": true,
        "momentum_composite": 0.68
    }
}

# Model prediction
model_prediction = {
    "model_id": "pub_spy_momentum_001",
    "timestamp": "2024-01-30T10:15:00Z",
    "prediction": {
        "signal": "BUY",
        "confidence": 0.72,
        "predicted_return": 0.018,
        "predicted_duration_days": 4
    },
    "thresholds_check": {
        "confidence_threshold": 0.60,
        "passes": true
    },
    "time_check": {
        "allowed_hours": [9, 10, 11],
        "current_hour": 10,
        "passes": true
    }
}
```

### 7.2 Generated Alert
```json
{
  "alert_id": "alert_20240130_101500_001",
  "timestamp": "2024-01-30T10:15:00Z",
  "model_id": "pub_spy_momentum_001",
  "user_id": "user_12345",
  
  "signal": {
    "action": "BUY",
    "instrument": "stock",
    "ticker": "SPY",
    "confidence": 0.72,
    "urgency": "immediate"
  },
  
  "order_details": {
    "order_type": "limit",
    "quantity": 22,  // Based on 2% position size of $50,000 account
    "entry_price": 453.50,
    "stop_loss": 426.29,  // 6% stop loss
    "take_profit": 525.61,  // 16% take profit
    "time_in_force": "day",
    "valid_until": "2024-01-30T16:00:00Z"
  },
  
  "metadata": {
    "strategy": "momentum_swing",
    "pack": "swingsigma",
    "features": {
      "rsi": 61.5,
      "macd_cross": true,
      "trend_strength": 0.73,
      "volume_surge": true
    },
    "backtest_stats": {
      "historical_win_rate": 0.58,
      "avg_return": 0.028,
      "avg_duration": 4.2
    }
  },
  
  "routing": {
    "destinations": [
      {
        "service": "sigma_sim",
        "status": "sent",
        "timestamp": "2024-01-30T10:15:01Z"
      },
      {
        "service": "user_email",
        "status": "sent",
        "timestamp": "2024-01-30T10:15:02Z"
      },
      {
        "service": "mobile_push",
        "status": "sent",
        "timestamp": "2024-01-30T10:15:02Z"
      }
    ]
  }
}
```

### 7.3 Paper Trading Execution (SigmaSim)
```json
{
  "paper_trade_id": "sim_20240130_001",
  "alert_id": "alert_20240130_101500_001",
  "execution": {
    "status": "filled",
    "fill_price": 453.48,
    "fill_time": "2024-01-30T10:15:30Z",
    "slippage": -0.02,
    "commission": 0.00
  },
  "position": {
    "ticker": "SPY",
    "quantity": 22,
    "entry_price": 453.48,
    "current_price": 454.20,
    "unrealized_pnl": 15.84,
    "unrealized_pnl_pct": 0.16
  }
}
```

### 7.4 Performance Tracking
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
    "avg_trade_return": 0.0053,
    "best_trade": 0.0189,
    "worst_trade": -0.0094
  },
  "comparison_to_backtest": {
    "win_rate": {
      "backtest": 0.58,
      "paper": 0.625,
      "difference": "+0.045"
    },
    "sharpe": {
      "backtest": 1.85,
      "paper": 1.68,
      "difference": "-0.17"
    }
  },
  "recommendation": "APPROVE_FOR_LIVE_TRADING"
}
```

---

## Step 8: Live Trading (After Paper Validation)

### 8.1 Transition to Live
```python
live_trading_approval = {
    "model_id": "pub_spy_momentum_001",
    "paper_trading_complete": true,
    "paper_performance_acceptable": true,
    "user_approval": true,
    "live_settings": {
        "broker": "interactive_brokers",
        "account_id": "DU123456",
        "max_capital": 50000,
        "max_position_size": 1000,  # dollars per position
        "enable_sigma_pilot": true
    },
    "go_live_date": "2024-02-14T09:30:00Z"
}
```

### 8.2 Live Alert to Sigma Pilot
```json
{
  "alert_id": "alert_20240214_101500_001",
  "model_id": "pub_spy_momentum_001",
  "routing": {
    "destinations": [
      {
        "service": "sigma_pilot",
        "status": "sent",
        "broker": "interactive_brokers",
        "account": "DU123456",
        "order_id": "ORD_2024021410001"
      }
    ]
  },
  "execution": {
    "status": "filled",
    "fill_price": 456.72,
    "fill_time": "2024-02-14T10:15:45Z",
    "commission": 1.00,
    "slippage": -0.03
  }
}
```

---

## Complete Configuration Summary

### Final Active Model
```yaml
production_model:
  # Identity
  id: "pub_spy_momentum_001"
  original_model: "spy_swing_momentum_v1"
  pack: "swingsigma"
  
  # Configuration (winning combination)
  config:
    threshold: 0.60
    allowed_hours: [9, 10, 11]
    position_size_pct: 2
    
  # Indicators
  indicators:
    rsi: {period: 21}
    macd: {fast: 12, slow: 26, signal: 9}
    adx: {period: 14}
    ema_20: {period: 20}
    ema_50: {period: 50}
    bollinger_bands: {period: 20, std: 2}
    volume_ma: {period: 20}
    
  # Risk Management
  risk:
    stop_loss_pct: 6
    take_profit_pct: 16
    max_position_pct: 3
    trailing_stop_pct: 5
    
  # Performance
  performance:
    backtest_sharpe: 1.85
    paper_sharpe: 1.68
    live_sharpe: null  # TBD
    win_rate: 0.58
    avg_trade_days: 4.2
    
  # Status
  status: "live_trading"
  paper_validated: true
  live_since: "2024-02-14T09:30:00Z"
```

---

## Appendix: Data Flow Diagram

```
1. Pack Definition (YAML files)
        ↓
2. User Creates Model (selects subset)
        ↓
3. Sweep Configuration (parameter ranges)
        ↓
4. Backtest Execution (45+ combinations)
        ↓
5. Leaderboard Ranking (by Sharpe ratio)
        ↓
6. User Selection (pick best configs)
        ↓
7. ML Training (XGBoost model)
        ↓
8. Publish Decision (review metrics)
        ↓
9. Paper Trading (SigmaSim validation)
        ↓
10. Live Trading (Sigma Pilot execution)
```

This complete example shows every step with actual configurations, parameters, and expected outputs throughout the entire Sigmatiq workflow.