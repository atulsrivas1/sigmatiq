# Sigmatiq Entity Data Dictionary (v1.1)

**Purpose:** Canonical entities, fields, enums, and relationships for Packs → Models → Sweeps → Training → Publishing → Alerts.  
**Timestamps:** ISO‑8601 UTC. **IDs:** UUID unless noted. **Types:** `string|int|float|bool|timestamp|enum|json|array|uri`.  
Grounded in the requirements, workflow, and transcript. 【10†source】【8†source】【9†source】

---

## Legend
- **Req?**: Y = required, N = optional
- **PK**: Primary key
- **FK**: Foreign key
- **Idx**: Indexed

---

## A) Identity, Auth, RBAC

### Organization
| Field | Type | Req? | Notes |
|---|---|---|---|
| org_id (PK) | string | Y | Tenant boundary |
| name | string | Y |  |
| plan_tier | enum | Y | free\|premium\|pro. Drives quotas. 【10†source】 |
| created_at | timestamp | Y |  |

**Rels:** 1→* Users, Packs, Models, Webhooks, BrokerAccounts.

### User
| Field | Type | Req? | Notes |
|---|---|---|---|
| user_id (PK) | string | Y |  |
| org_id (FK) | string | Y | Organization |
| email (Idx) | string | Y | Unique per org |
| name | string | N |  |
| role_id (FK) | string | Y | Role |
| mfa_enabled | bool | Y |  |

### Role
| Field | Type | Req? | Notes |
|---|---|---|---|
| role_id (PK) | string | Y |  |
| name | string | Y |  |
| permissions | array | Y | Machine scopes |

### APIKey
| Field | Type | Req? | Notes |
|---|---|---|---|
| key_id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| hash | string | Y | Secret hash |
| scopes | array | Y |  |
| created_at | timestamp | Y |  |
| revoked_at | timestamp | N |  |

### AuditLog
| Field | Type | Req? | Notes |
|---|---|---|---|
| event_id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| actor_type | enum | Y | user\|system |
| actor_id | string | Y |  |
| action | string | Y | CRUD verb |
| target_type | string | Y | Entity name |
| target_id | string | Y |  |
| timestamp | timestamp | Y |  |
| payload | json | N |  |

【10†source】

---

## B) Market Data and Instruments

### InstrumentType (enum)
`stock | option | future`. 【10†source】

### Instrument
| Field | Type | Req? | Notes |
|---|---|---|---|
| instrument_id (PK) | string | Y |  |
| type | enum | Y | InstrumentType |
| symbol | string | Y | e.g., SPY |
| metadata | json | N |  |

#### StockSpec
| Field | Type | Req? | Notes |
|---|---|---|---|
| instrument_id (FK) | string | Y | Instrument |
| exchange | string | N |  |
| lot_size | int | N |  |

#### OptionSpec
| Field | Type | Req? | Notes |
|---|---|---|---|
| instrument_id (FK) | string | Y | Instrument |
| underlying_symbol | string | Y |  |
| contract_size | int | Y |  |
| default_dte | int | Y | Days to expiration |
| default_strike_selector | enum | Y | ATM\|OTM_5\|OTM_10\|ITM_5\|ITM_10 【10†source】 |

#### FutureSpec
| Field | Type | Req? | Notes |
|---|---|---|---|
| instrument_id (FK) | string | Y | Instrument |
| contract_code | string | Y | e.g., ES |
| contract_month_policy | enum | Y | front\|back\|specific |
| roll_strategy | enum | Y | calendar\|volume\|oi 【10†source】 |

### OHLCVBar
| Field | Type | Req? | Notes |
|---|---|---|---|
| instrument_id (FK, Idx) | string | Y |  |
| ts (Idx) | timestamp | Y |  |
| interval | enum | Y | 1m\|5m\|1h\|1d |
| open,high,low,close | float | Y |  |
| volume | float | Y |  |

### IndicatorSeriesPoint
| Field | Type | Req? | Notes |
|---|---|---|---|
| series_id (PK) | string | Y |  |
| instrument_id (FK, Idx) | string | Y |  |
| name (Idx) | string | Y | rsi\|macd\|adx\|ema_20... |
| ts (Idx) | timestamp | Y |  |
| values | json | Y | e.g., macd_line/signal |

### FeatureSeriesPoint
| Field | Type | Req? | Notes |
|---|---|---|---|
| series_id (PK) | string | Y |  |
| instrument_id (FK, Idx) | string | Y |  |
| name (Idx) | string | Y | trend_strength\|bb_squeeze... |
| ts (Idx) | timestamp | Y |  |
| values | json | Y |  |

### DataSnapshot
| Field | Type | Req? | Notes |
|---|---|---|---|
| snapshot_id (PK) | string | Y |  |
| date_range | json | Y | start,end |
| data_source_version | string | Y |  |
| hash | string | Y | Repro anchor |

【9†source】【10†source】【8†source】

---

## C) Packs (Blueprints)

### Pack
| Field | Type | Req? | Notes |
|---|---|---|---|
| pack_id (PK) | string | Y | Namespace |
| name | string | Y |  |
| version | string | Y | SemVer |
| metadata.vibe | json | Y | time_horizon, risk_appetite, decision_style, market_preference, execution_character |
| supported_instruments | array | Y |  |
| default_instrument | enum | Y |  |
| tags | array | Y |  |
| author | string | Y |  |
| created_at | timestamp | Y |  |

### IndicatorDef
| Field | Type | Req? | Notes |
|---|---|---|---|
| pack_id (FK) | string | Y |  |
| id (PK) | string | Y | rsi\|macd... |
| name | string | Y |  |
| params_schema | json | Y |  |

### FeatureDef
| Field | Type | Req? | Notes |
|---|---|---|---|
| pack_id (FK) | string | Y |  |
| id (PK) | string | Y |  |
| name | string | Y |  |
| calculation | string | Y | Code ref |

### StrategyDef
| Field | Type | Req? | Notes |
|---|---|---|---|
| pack_id (FK) | string | Y |  |
| id (PK) | string | Y |  |
| name | string | Y |  |
| description | string | N |  |
| entry_logic | array | Y | Expr list |
| exit_logic | array | Y | Expr list |

### GatePolicy
| Field | Type | Req? | Notes |
|---|---|---|---|
| pack_id (FK) | string | Y |  |
| quality | json | Y | min_trades, min_sharpe, max_drawdown, min_win_rate |
| execution | json | Y | slippage, volume, spread |
| risk | json | Y | position size, correlation, VaR |

### ExecPolicy / PositionSizingPolicy / RiskMgmtPolicy
| Field | Type | Req? | Notes |
|---|---|---|---|
| pack_id (FK) | string | Y |  |
| fields | json | Y | order_type, tif, kelly_fraction, stops... |

### PackValidationReport
| Field | Type | Req? | Notes |
|---|---|---|---|
| pack_id (FK) | string | Y |  |
| version | string | Y |  |
| status | enum | Y | PASS\|FAIL |
| errors | array | N | {code,message} |
| warnings | array | N |  |

【8†source】【10†source】

---

## D) Models

### Model
| Field | Type | Req? | Notes |
|---|---|---|---|
| model_id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| pack_id (FK) | string | Y |  |
| name (Idx) | string | Y | Unique per user |
| description | string | N |  |
| created_at | timestamp | Y |  |
| status | enum | Y | draft\|configured\|published\|retired |

### ModelConfig
| Field | Type | Req? | Notes |
|---|---|---|---|
| model_id (FK, PK) | string | Y |  |
| instrument | json | Y | type + specifics |
| strategy_id | string | Y |  |
| selected_indicators | array | Y | subset of pack |
| selected_features | array | Y | subset of pack |
| risk_profile | enum | Y |  |
| overrides | json | N | param overrides |

### ModelVersion
| Field | Type | Req? | Notes |
|---|---|---|---|
| model_version_id (PK) | string | Y |  |
| model_id (FK) | string | Y |  |
| pack_version | string | Y |  |
| config_yaml | string | Y |  |
| hash | string | Y |  |
| created_at | timestamp | Y |  |

【9†source】【10†source】【8†source】

---

## E) Sweeps and Backtests

### Sweep
| Field | Type | Req? | Notes |
|---|---|---|---|
| sweep_id (PK) | string | Y |  |
| model_id (FK) | string | Y |  |
| type | enum | Y | simple\|custom |
| date_range | json | Y | start,end |
| parameters | json | Y | per registry |
| quality_gates | json | N | overrides |
| tag | string | N |  |
| plan_tier | enum | Y | free\|premium\|pro |
| combo_cap | int | Y | plan limit |

### SweepRun
| Field | Type | Req? | Notes |
|---|---|---|---|
| sweep_id (FK, PK) | string | Y |  |
| status | enum | Y | queued\|running\|cancelled\|completed\|failed |
| progress | float | Y | 0–1 |
| started_at | timestamp | N |  |
| ended_at | timestamp | N |  |
| data_snapshot_id (FK) | string | Y |  |
| pruning_used | bool | Y |  |

### SweepCombination (ConfigEval)
| Field | Type | Req? | Notes |
|---|---|---|---|
| sweep_id (FK) | string | Y |  |
| combo_id (PK) | int | Y | Seq |
| params | json | Y | evaluated combo |
| config_hash | string | Y | lineage |
| backtest_metrics | json | Y | see below |
| gate_results | json | Y | pass/marginal/fail |
| rank | int | N | leaderboard rank |
| kept | bool | Y | after pruning |

### BacktestMetrics (shape)
`total_return, annualized_return, sharpe_ratio, sortino_ratio, max_drawdown, win_rate, profit_factor, total_trades, avg_trade_duration_days, best_trade, worst_trade, avg_winner, avg_loser`. 【8†source】

### LeaderboardEntry
| Field | Type | Req? | Notes |
|---|---|---|---|
| sweep_id (FK) | string | Y |  |
| rank (PK) | int | Y |  |
| combo_id (FK) | int | Y |  |
| sharpe | float | Y |  |
| return | float | Y |  |
| trades | int | Y |  |
| max_drawdown | float | Y |  |
| gate_status | enum | Y | PASS\|MARGINAL\|FAIL |

### SweepError
| Field | Type | Req? | Notes |
|---|---|---|---|
| sweep_id (FK) | string | Y |  |
| reason_code | string | Y | SWS‑1001…4001 |
| message | string | Y |  |
| detail | json | N |  |

【10†source】【8†source】

---

## F) Training and Artifacts

### TrainingJob
| Field | Type | Req? | Notes |
|---|---|---|---|
| job_id (PK) | string | Y |  |
| model_id (FK) | string | Y |  |
| combo_id (FK) | int | Y |  |
| status | enum | Y | queued\|training\|completed\|failed\|cancelled |
| progress | array | Y | steps with durations |
| hyperparameters | json | Y |  |
| data_snapshot_id (FK) | string | Y |  |
| seed | int | Y | deterministic |

### TrainingMetrics
| Field | Type | Req? | Notes |
|---|---|---|---|
| job_id (FK, PK) | string | Y |  |
| training | json | Y | accuracy, precision, recall, f1, auc_roc |
| validation | json | Y | same shape |

### FeatureImportance
| Field | Type | Req? | Notes |
|---|---|---|---|
| trained_model_id (FK, PK) | string | Y |  |
| items | array | Y | {feature, importance}[] |

### TrainedModel (Artifact)
| Field | Type | Req? | Notes |
|---|---|---|---|
| trained_model_id (PK) | string | Y |  |
| model_id (FK) | string | Y |  |
| combo_id (FK) | int | Y |  |
| artifact_uri | uri | Y | pickle path |
| scaler_uri | uri | N |  |
| metadata_uri | uri | Y |  |
| config_hash | string | Y |  |
| data_snapshot_id (FK) | string | Y |  |
| created_at | timestamp | Y |  |
| status | enum | Y | ready\|deprecated |

【10†source】【8†source】

---

## G) Publishing and Lifecycle

### PublishRequest
| Field | Type | Req? | Notes |
|---|---|---|---|
| trained_model_id (FK, PK) | string | Y |  |
| name | string | Y |  |
| description | string | N |  |
| alert_frequency | enum | Y | e.g., 5_minutes |
| max_alerts_per_day | int | Y |  |
| paper_trade_first | bool | Y |  |
| paper_trade_duration_days | int | N |  |

### PublishedModel
| Field | Type | Req? | Notes |
|---|---|---|---|
| published_model_id (PK) | string | Y |  |
| trained_model_id (FK) | string | Y |  |
| org_id (FK) | string | Y |  |
| status | enum | Y | paper_trading\|live_trading\|paused\|retired |
| paper_trade_start | timestamp | N |  |
| paper_trade_end | timestamp | N |  |
| live_date | timestamp | N |  |
| settings | json | Y |  |

### PaperTradeSession
| Field | Type | Req? | Notes |
|---|---|---|---|
| published_model_id (FK, PK) | string | Y |  |
| period_start | timestamp | Y |  |
| period_end | timestamp | Y |  |
| results | json | Y | trades, win_rate, sharpe, drawdown... |

### LiveDeployment
| Field | Type | Req? | Notes |
|---|---|---|---|
| published_model_id (FK, PK) | string | Y |  |
| broker_account_id (FK) | string | Y |  |
| max_capital | float | Y |  |
| max_position_size | float | Y | dollars per position |
| enable_sigma_pilot | bool | Y |  |
| go_live_date | timestamp | Y |  |
| status | enum | Y | active\|paused |

【8†source】

---

## H) Execution and Brokers

### BrokerAccount
| Field | Type | Req? | Notes |
|---|---|---|---|
| broker_account_id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| broker | enum | Y | interactive_brokers\|... |
| account_ref | string | Y |  |
| status | enum | Y | connected\|error |

### Order
| Field | Type | Req? | Notes |
|---|---|---|---|
| order_id (PK) | string | Y |  |
| published_model_id (FK) | string | Y |  |
| instrument_id (FK) | string | Y |  |
| side | enum | Y | buy\|sell |
| type | enum | Y | limit\|market\|stop |
| qty | float | Y |  |
| limit_price | float | N | if type=limit |
| time_in_force | enum | Y | day\|gtc |
| status | enum | Y | placed\|filled\|cancelled\|rejected |
| placed_at | timestamp | Y |  |

### Fill
| Field | Type | Req? | Notes |
|---|---|---|---|
| fill_id (PK) | string | Y |  |
| order_id (FK) | string | Y |  |
| price | float | Y |  |
| qty | float | Y |  |
| ts | timestamp | Y |  |
| commission | float | Y |  |
| slippage | float | Y |  |

### Position
| Field | Type | Req? | Notes |
|---|---|---|---|
| position_id (PK) | string | Y |  |
| instrument_id (FK) | string | Y |  |
| qty | float | Y |  |
| avg_price | float | Y |  |
| unrealized_pnl | float | Y |  |
| opened_at | timestamp | Y |  |
| closed_at | timestamp | N |  |

### ExecutionLog
| Field | Type | Req? | Notes |
|---|---|---|---|
| order_id (FK) | string | Y |  |
| event_ts | timestamp | Y |  |
| message | string | Y |  |

【8†source】

---

## I) Alerts and Delivery

### Alert (Core)
| Field | Type | Req? | Notes |
|---|---|---|---|
| alert_id (PK) | string | Y |  |
| timestamp | timestamp | Y |  |
| published_model_id (FK) | string | Y |  |
| action | enum | Y | BUY\|SELL\|HOLD |
| instrument | enum | Y | stock\|option\|future |
| ticker | string | Y | or `underlying` for options |
| quantity | float | Y | or `contracts` for options |
| confidence | float | Y | 0–1 |
| entry_price | float | Y |  |
| stop_loss | float | N |  |
| take_profit | float | N |  |
| urgency | enum | Y | immediate\|day\|good_till |
| valid_until | timestamp | Y |  |

**Optional blocks**
- `metadata{ strategy, pack, features{}, backtest_stats{} }`  
- `schema_version`

### AlertGenerationMetric
| Field | Type | Req? | Notes |
|---|---|---|---|
| alert_id (FK, PK) | string | Y |  |
| t_ingress | timestamp | Y | T0 |
| t_persist | timestamp | Y | T1 |
| latency_ms | float | Y | T1−T0 |
| p99_budget_met | bool | Y | SLO |
【10†source】【8†source】

### AlertRoute
| Field | Type | Req? | Notes |
|---|---|---|---|
| alert_id (FK) | string | Y |  |
| destination | enum | Y | sigma_sim\|sigma_pilot\|email\|sms\|push\|webhook |
| status | enum | Y | sent\|delivered\|failed |
| attempted_at | timestamp | Y |  |
| delivered_at | timestamp | N |  |
| delivery_latency_ms | float | N |  |

### ConflictResolutionPolicy
| Field | Type | Req? | Notes |
|---|---|---|---|
| org_id (FK, PK) | string | Y |  |
| policy | enum | Y | first_wins\|highest_confidence\|ensemble |
| rules | json | N | tie‑breaks |

【10†source】

---

## J) Webhooks and Notifications

### WebhookEndpoint
| Field | Type | Req? | Notes |
|---|---|---|---|
| endpoint_id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| url | string | Y |  |
| secret | string | Y | HMAC |
| events | array | Y | subscribed events |
| status | enum | Y | active\|disabled |

### EmailSubscription
| Field | Type | Req? | Notes |
|---|---|---|---|
| id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| address | string | Y |  |
| status | enum | Y | active\|unsubscribed |

### PushDevice
| Field | Type | Req? | Notes |
|---|---|---|---|
| id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| device_token | string | Y |  |
| status | enum | Y | active\|revoked |

---

## K) Telemetry, Quotas, Reliability

### MetricEvent
| Field | Type | Req? | Notes |
|---|---|---|---|
| metric_id (PK) | string | Y |  |
| org_id (FK) | string | Y |  |
| name | string | Y | e.g., alert.generation_latency |
| value | float | Y |  |
| labels | json | N | dimensions |
| ts | timestamp | Y |  |

### Quota
| Field | Type | Req? | Notes |
|---|---|---|---|
| org_id (FK, PK) | string | Y |  |
| plan_tier | enum | Y | free\|premium\|pro |
| limits | json | Y | sweeps/day, combo caps, jobs/day, alerts/day |

### UsageCounter
| Field | Type | Req? | Notes |
|---|---|---|---|
| org_id (FK) | string | Y |  |
| counter_name (PK) | string | Y |  |
| period (PK) | string | Y | yyyy‑mm |
| value | int | Y |  |
| updated_at | timestamp | Y |  |

### HealthCheck
| Field | Type | Req? | Notes |
|---|---|---|---|
| component (PK) | string | Y |  |
| status | enum | Y | ok\|degraded\|down |
| ts | timestamp | Y |  |
| detail | json | N |  |

【10†source】

---

## L) Lineage and Reproducibility

### LineageLink
| Field | Type | Req? | Notes |
|---|---|---|---|
| link_id (PK) | string | Y |  |
| from_type | string | Y |  |
| from_id | string | Y |  |
| to_type | string | Y |  |
| to_id | string | Y |  |

### HashRecord
| Field | Type | Req? | Notes |
|---|---|---|---|
| entity_type (PK) | string | Y |  |
| entity_id (PK) | string | Y |  |
| hash_type (PK) | enum | Y | config\|data\|artifact |
| hash | string | Y |  |
| created_at | timestamp | Y |  |

**Requirement:** Every alert references `config_hash`, `data_snapshot_id`, and artifact hash. 【9†source】【8†source】

---

## M) Testing Artifacts

### GoldenDataset
| Field | Type | Req? | Notes |
|---|---|---|---|
| dataset_id (PK) | string | Y |  |
| description | string | Y |  |
| date_range | json | Y |  |
| snapshot_id (FK) | string | Y |  |
| checksum | string | Y | drift guard |

### ChaosScenario
| Field | Type | Req? | Notes |
|---|---|---|---|
| scenario_id (PK) | string | Y |  |
| component | string | Y |  |
| fault_type | string | Y |  |
| parameters | json | Y |  |
| expected_behavior | string | Y |  |

【10†source】

---

## N) UI View Models (Projections)
PackCard, ModelBuilderState, SweepProgressView, LeaderboardRow, TrainingSummary, AlertTile. Ensure client/server validation parity. 【10†source】

---

## O) Enums

- **PlanTier:** free | premium | pro. 【10†source】  
- **SweepType:** simple | custom. 【10†source】  
- **GateStatus:** PASS | MARGINAL | FAIL. 【10†source】  
- **JobStatus:** queued | running/training | completed | failed | cancelled. 【10†source】  
- **PublishStatus:** paper_trading | live_trading | paused | retired. 【8†source】  
- **Destination:** sigma_sim | sigma_pilot | email | sms | push | webhook. 【10†source】

---

## P) Relationships (ER Outline)

```
Organization 1—* User
Organization 1—* Pack
Pack 1—* IndicatorDef / FeatureDef / StrategyDef / GatePolicy / ExecPolicy
Pack 1—* Model
Model 1—* ModelVersion
Model 1—* Sweep
Sweep 1—* SweepCombination (ConfigEval) 1—1 BacktestMetrics
Sweep 1—1 SweepRun 1—* SweepError
SweepCombination *—1 DataSnapshot
SweepCombination *—* LeaderboardEntry (by sweep)
Sweep (PASS/MARGINAL) *—* TrainingJob 1—1 TrainedModel
TrainedModel 1—1 PublishedModel
PublishedModel 1—* Alert 1—* AlertRoute 1—1 AlertGenerationMetric
PublishedModel 0..1—1 PaperTradeSession
PublishedModel 0..1—1 LiveDeployment 1—1 BrokerAccount
Alert *—1 LineageLink chain (to TrainedModel, DataSnapshot, ConfigHash)
OHLCVBar / IndicatorSeriesPoint / FeatureSeriesPoint *—* DataSnapshot
```

---

**Sources:** Requirements v1.0, Workflow example, and Discussion transcript. This dictionary reconciles naming and flow with v1.1 changes. 【10†source】【8†source】【9†source】
