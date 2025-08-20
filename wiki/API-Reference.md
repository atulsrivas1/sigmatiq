# API Reference

## Overview

The Sigmatiq Sigma Lab API is a RESTful service built with FastAPI that provides programmatic access to all platform features.

**Base URL**: `http://localhost:8001/api/v1`

## 🔑 Authentication

All API requests require authentication using a Bearer token in the Authorization header:

```http
Authorization: Bearer <your-token>
```

### Get Authentication Token

```http
POST /auth/token
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## 📊 Models API

### List Models

Get a paginated list of models with optional filtering.

```http
GET /models?pack_id=zerosigma&limit=10&offset=0
```

**Query Parameters:**
- `model_id` (optional): Filter by model ID
- `pack_id` (optional): Filter by pack ID
- `limit` (optional, default=100): Maximum results to return
- `offset` (optional, default=0): Number of results to skip

**Response:**
```json
{
  "items": [
    {
      "model_id": "AAPL_equity_5d_daily",
      "pack_id": "swingsigma",
      "updated_at": "2024-01-15T10:30:00Z",
      "sharpe": 1.85,
      "cum_ret": 0.125,
      "lineage": {
        "matrix_sha": "abc123...",
        "config_sha": "def456...",
        "risk_profile": "Balanced"
      }
    }
  ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

### Create Model

Create a new model from a template.

```http
POST /models
Content-Type: application/json

{
  "template_id": "zerosigma_default",
  "name": "TSLA 0DTE Strategy",
  "risk_profile": "Conservative",
  "config": {
    "ticker": "TSLA",
    "indicators": ["RSI", "MACD", "BB"]
  }
}
```

**Response:**
```json
{
  "model_id": "TSLA_options_0d_intraday",
  "pack_id": "zerosigma",
  "created_at": "2024-01-15T10:30:00Z",
  "status": "created"
}
```

### Get Model Details

```http
GET /models/{model_id}
```

**Response:**
```json
{
  "model_id": "AAPL_equity_5d_daily",
  "pack_id": "swingsigma",
  "config": {
    "ticker": "AAPL",
    "indicators": ["RSI", "MACD"],
    "thresholds": {
      "entry": 0.7,
      "exit": 0.3
    }
  },
  "metrics": {
    "sharpe": 1.85,
    "cum_ret": 0.125,
    "max_drawdown": -0.08,
    "win_rate": 0.62
  },
  "lineage": {
    "matrix_sha": "abc123...",
    "created_by": "user123",
    "created_at": "2024-01-10T09:00:00Z"
  }
}
```

## 🔄 BTB Pipeline API

### Build Matrix

Generate a training matrix for a model.

```http
POST /build_matrix
Content-Type: application/json

{
  "model_id": "AAPL_equity_5d_daily",
  "start_date": "2023-01-01",
  "end_date": "2023-12-31",
  "features": ["close", "volume", "RSI", "MACD"]
}
```

**Response:**
```json
{
  "matrix_sha": "7f8a9b2c3d4e5f6g",
  "rows": 252,
  "columns": 15,
  "size_mb": 2.4,
  "status": "completed",
  "path": "matrices/AAPL_equity_5d_daily_7f8a9b2c.parquet"
}
```

### Train Model

Train a model using a specific matrix.

```http
POST /train
Content-Type: application/json

{
  "model_id": "AAPL_equity_5d_daily",
  "matrix_sha": "7f8a9b2c3d4e5f6g",
  "allowed_hours": [9, 10, 11, 12, 13, 14, 15],
  "config": {
    "learning_rate": 0.001,
    "epochs": 100,
    "batch_size": 32
  }
}
```

**Response:**
```json
{
  "job_id": "train_abc123",
  "status": "queued",
  "estimated_time": 300,
  "queue_position": 3
}
```

### Run Backtest

Execute a backtest for a trained model.

```http
POST /backtest
Content-Type: application/json

{
  "model_id": "AAPL_equity_5d_daily",
  "config": {
    "kind": "thresholds",
    "value": 0.7,
    "allowed_hours": [9, 10, 11, 12, 13, 14, 15],
    "splits": 5
  },
  "matrix_sha": "7f8a9b2c3d4e5f6g",
  "start_date": "2023-06-01",
  "end_date": "2023-12-31"
}
```

**Response:**
```json
{
  "backtest_id": "bt_xyz789",
  "model_id": "AAPL_equity_5d_daily",
  "status": "running",
  "metrics": null,
  "estimated_completion": "2024-01-15T10:35:00Z"
}
```

### Run Sweep

Execute multiple backtests with different configurations.

```http
POST /backtest_sweep
Content-Type: application/json

{
  "model_id": "AAPL_equity_5d_daily",
  "risk_profile": "Balanced",
  "sweep": {
    "thresholds": [0.5, 0.6, 0.7, 0.8],
    "allowed_hours": [[9,10,11], [12,13,14], [9,10,11,12,13,14,15]],
    "top_pct": [5, 10, 15]
  },
  "tag": "sweep_2024Q1"
}
```

**Response:**
```json
{
  "sweep_id": "sweep_123abc",
  "total_configs": 36,
  "status": "running",
  "progress": 0,
  "tag": "sweep_2024Q1"
}
```

## 📈 Leaderboard API

### Get Leaderboard

Retrieve ranked backtest results.

```http
GET /leaderboard?pack_id=swingsigma&risk_profile=Balanced&pass_gate=true&limit=10
```

**Query Parameters:**
- `model_id`: Filter by model
- `pack_id`: Filter by pack
- `tag`: Filter by sweep tag
- `risk_profile`: Filter by risk profile
- `pass_gate`: Only show passing results
- `sort_by`: Metric to sort by (sharpe, cum_ret, etc.)
- `limit`: Max results
- `offset`: Pagination offset

**Response:**
```json
{
  "items": [
    {
      "rank": 1,
      "backtest_id": "bt_abc123",
      "model_id": "AAPL_equity_5d_daily",
      "metrics": {
        "sharpe": 2.15,
        "cum_ret": 0.185,
        "max_drawdown": -0.06,
        "win_rate": 0.68,
        "trades": 145
      },
      "gate": {
        "pass": true,
        "reasons": []
      },
      "config": {
        "threshold": 0.7,
        "allowed_hours": [9,10,11,12,13,14,15]
      }
    }
  ],
  "total": 25
}
```

## 📡 Signals API

### Get Live Signals

Retrieve current trading signals.

```http
GET /signals?model_id=AAPL_equity_5d_daily&status=active&limit=20
```

**Query Parameters:**
- `model_id`: Filter by model
- `start`: Start timestamp
- `end`: End timestamp  
- `status`: Signal status (active, filled, cancelled)
- `limit`: Max results
- `offset`: Pagination offset

**Response:**
```json
{
  "items": [
    {
      "signal_id": "sig_123",
      "model_id": "AAPL_equity_5d_daily",
      "ticker": "AAPL",
      "action": "BUY",
      "quantity": 100,
      "price": 185.50,
      "timestamp": "2024-01-15T09:30:00Z",
      "status": "active",
      "confidence": 0.85,
      "expected_return": 0.025
    }
  ],
  "total": 5
}
```

### Signals Leaderboard

Get performance rankings for live signals.

```http
GET /signals/leaderboard?pack=swingsigma&risk_profile=Balanced&start=2024-01-01&end=2024-01-15
```

**Response:**
```json
{
  "items": [
    {
      "model_id": "AAPL_equity_5d_daily",
      "pack_id": "swingsigma",
      "metrics": {
        "total_signals": 15,
        "success_rate": 0.73,
        "avg_return": 0.018,
        "sharpe_live": 1.95
      },
      "period": {
        "start": "2024-01-01",
        "end": "2024-01-15"
      }
    }
  ]
}
```

## 🏥 Health Check API

### System Health

Check overall system health.

```http
GET /healthz
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "components": {
    "database": "healthy",
    "cache": "healthy",
    "polygon_api": "healthy",
    "worker_queue": "healthy"
  },
  "version": "1.0.0"
}
```

### Component Health

Check specific component health.

```http
GET /healthz?ticker=AAPL&pack_id=swingsigma&model_id=AAPL_equity_5d_daily
```

**Response:**
```json
{
  "ticker": {
    "status": "healthy",
    "last_update": "2024-01-15T10:29:00Z",
    "data_quality": 1.0
  },
  "pack": {
    "status": "healthy",
    "models_count": 12,
    "active_signals": 3
  },
  "model": {
    "status": "healthy",
    "last_backtest": "2024-01-14T15:00:00Z",
    "performance": "meeting_target"
  }
}
```

## 📤 Export API

### Export Backtest Results

Export backtest results to CSV.

```http
GET /export/backtest/{backtest_id}?format=csv
```

**Response:**
```csv
timestamp,action,price,quantity,pnl,cumulative_pnl
2024-01-02T09:30:00Z,BUY,185.50,100,0,0
2024-01-02T15:45:00Z,SELL,187.25,100,175,175
...
```

### Export Leaderboard

Export leaderboard data.

```http
GET /export/leaderboard?tag=sweep_2024Q1&format=csv
```

## 🔧 Admin API

### Update Model Config

Update model configuration (admin only).

```http
PATCH /admin/models/{model_id}
Content-Type: application/json
Authorization: Bearer <admin-token>

{
  "config": {
    "thresholds": {
      "entry": 0.75,
      "exit": 0.25
    }
  }
}
```

### Delete Model

Delete a model and its artifacts (admin only).

```http
DELETE /admin/models/{model_id}
Authorization: Bearer <admin-token>
```

## 🔍 Common Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## 📝 Error Response Format

All errors follow a consistent format:

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "The 'start_date' parameter is invalid",
    "details": {
      "field": "start_date",
      "reason": "Must be in YYYY-MM-DD format"
    }
  },
  "request_id": "req_abc123xyz"
}
```

## 🚦 Rate Limiting

API rate limits per tier:

| Tier | Requests/Minute | Requests/Hour | Concurrent Backtests |
|------|----------------|---------------|---------------------|
| Free | 60 | 1000 | 1 |
| Basic | 300 | 10000 | 5 |
| Pro | 1000 | 50000 | 20 |
| Enterprise | Unlimited | Unlimited | Unlimited |

Rate limit headers in response:
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1642082400
```

## 🔄 Webhooks

Configure webhooks to receive real-time updates:

### Register Webhook

```http
POST /webhooks
Content-Type: application/json

{
  "url": "https://your-domain.com/webhook",
  "events": ["backtest.completed", "signal.generated"],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload

```json
{
  "event": "backtest.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "backtest_id": "bt_abc123",
    "model_id": "AAPL_equity_5d_daily",
    "status": "success",
    "metrics": {
      "sharpe": 1.85
    }
  },
  "signature": "sha256=..."
}
```

## 📚 SDK Support

Official SDKs available:

- **Python**: `pip install sigmatiq-sdk`
- **JavaScript/TypeScript**: `npm install @sigmatiq/sdk`
- **Go**: `go get github.com/sigmatiq/sdk-go`

### Python Example

```python
from sigmatiq import SigmatiqClient

client = SigmatiqClient(api_key="your-api-key")

# Create model
model = client.models.create(
    template_id="swingsigma_default",
    name="My Strategy",
    risk_profile="Balanced"
)

# Run backtest
result = client.backtest.run(
    model_id=model.id,
    config={"threshold": 0.7}
)

print(f"Sharpe: {result.metrics.sharpe}")
```

---

**Need help?** Check our [API Playground](https://api.sigmatiq.com/playground) or [contact support](mailto:api@sigmatiq.com)