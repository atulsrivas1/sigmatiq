# Pack System Requirements Document

## Document Information
- **Version**: 1.0
- **Date**: January 2024
- **Status**: Draft
- **Audience**: Engineering, Product, QA Teams

## 1. Overview

### 1.1 Purpose
This document defines the complete requirements for the Pack System, which forms the foundation of the Sigmatiq trading platform. The Pack System encompasses Packs, Models, Sweeps, Training, and Alert Generation.

### 1.2 Scope
The Pack System includes:
- Strategy Pack definition and management
- Model creation from packs
- Parameter optimization through sweeps
- Model training and validation
- Alert generation from trained models

## 2. Pack Requirements

### 2.1 Pack Definition
A Pack is a cohesive trading blueprint that defines a specific trading personality and approach.

#### 2.1.1 Core Components
| Component | Description | Required |
|-----------|-------------|----------|
| **Namespace** | Unique identifier (e.g., `swingsigma`) | Yes |
| **Supported Instruments** | Array of tradeable types `["stocks", "options", "futures"]` | Yes |
| **Default Instrument** | Primary instrument type | Yes |
| **Indicators** | Available technical indicators from shared library | Yes |
| **Features** | Derived calculations from indicators | Yes |
| **Strategies** | Pre-configured trading approaches | Yes |
| **Gates** | Quality control thresholds | Yes |
| **Policies** | Execution and risk management rules | Yes |
| **Tags** | Searchable attributes for discovery | Yes |

#### 2.1.2 Pack Personality Dimensions
```yaml
time_horizon: [seconds, minutes, hours, days, weeks, months]
risk_appetite: [conservative, balanced, aggressive]
decision_style: [technical, fundamental, sentiment, flow]
market_preference: [trending, ranging, volatile, all_weather]
execution_character: [aggressive, patient, adaptive]
```

### 2.2 Pack Types

#### 2.2.1 Official Packs
- Created and maintained by Sigmatiq team
- Fully tested and validated
- Regular updates and support
- Available to all users

#### 2.2.2 Premium User Packs
- Created by premium/pro users
- Private by default
- Optional submission for community review
- Can be monetized if approved

### 2.3 Pack Validation Rules

#### 2.3.1 Coherence Validation
- **MUST** reject mismatched indicator/timeframe combinations
- **MUST** ensure risk profile consistency across all settings
- **MUST** validate instrument compatibility

#### 2.3.2 Minimum Requirements
- **MUST** have at least 3 indicators
- **MUST NOT** exceed 15 indicators (prevent overfitting)
- **MUST** define all required gates
- **MUST** include at least 1 default strategy

#### 2.3.3 Performance Requirements
- **MUST** successfully backtest on 1 year of data
- **MUST** generate at least 10 trades in backtest
- **SHOULD** achieve Sharpe ratio > -0.5

## 3. Model Requirements

### 3.1 Model Definition
A Model is a user-created instance derived from a Pack with specific configuration choices.

#### 3.1.1 Model Creation Process
```
User Inputs:
├── Pack Selection (required)
├── Model Name (required, unique per user)
├── Instrument Choice (from pack's supported_instruments)
├── Indicator Selection (subset of pack's indicators)
├── Strategy Selection (from pack's strategies)
├── Risk Profile (conservative/balanced/aggressive)
└── Instrument-Specific Settings (if applicable)
```

#### 3.1.2 Model Constraints
- **MUST** use only components available in parent pack
- **MUST** maintain pack's coherence rules
- **MUST** have unique name within user's account
- **CAN** use subset of pack's indicators (minimum 1)

### 3.2 Instrument-Specific Requirements

#### 3.2.1 Stock Models
```yaml
Required Settings:
  ticker: string (e.g., "SPY")
  position_type: [long, short, both]
  share_size: integer or percentage
```

#### 3.2.2 Options Models
```yaml
Required Settings:
  underlying: string (e.g., "SPY")
  option_type: [call, put, both]
  default_dte: integer (days to expiration)
  default_strike: [ATM, OTM_5, OTM_10, ITM_5, ITM_10]
  contract_size: integer
```

#### 3.2.3 Futures Models
```yaml
Required Settings:
  contract: string (e.g., "ES")
  contract_month: [front, back, specific]
  contract_size: integer
  roll_strategy: [calendar, volume, oi]
```

## 4. Sweep Requirements

### 4.1 Sweep Definition
A Sweep is a systematic test of multiple parameter combinations to find optimal trading configurations.

### 4.2 Sweep Modes

#### 4.2.1 Simple Sweep (Default)
```yaml
Parameters:
  thresholds: [0.50, 0.55, 0.60, 0.65, 0.70]
  allowed_hours: [[9,10], [13,14,15], [all_day]]
  top_pct: [0.05, 0.10, 0.15]
Max Combinations: 45
```

#### 4.2.2 Custom Sweep (Premium Feature)
```yaml
Core Parameters:
  thresholds: [custom array]
  allowed_hours: [custom array]
  top_pct: [custom array]
  
Optional Parameters:
  stop_loss: [array of percentages]
  take_profit: [array of ratios]
  max_positions: [array of integers]
  
Pack-Specific Parameters:
  # Options packs
  strike_selection: [array of strike types]
  dte_target: [array of days]
  
  # Swing packs
  hold_days: [array of integers]
  
  # Micro packs
  entry_type: [market, limit, stop]
```

### 4.3 Sweep Execution

#### 4.3.1 Performance Requirements
- **MUST** complete simple sweep within 5 minutes
- **SHOULD** provide progress updates every 10 seconds
- **MUST** handle up to 1000 combinations for custom sweeps
- **MUST** support cancellation mid-sweep

#### 4.3.2 Quality Gates
```yaml
Filtering:
  min_trades: integer (default: 20)
  min_sharpe: float (default: 0.0)
  max_drawdown: percentage (default: 50%)
  min_win_rate: percentage (optional)
```

### 4.4 Sweep Results

#### 4.4.1 Leaderboard Display
| Field | Type | Description |
|-------|------|-------------|
| Rank | Integer | Position by Sharpe ratio |
| Configuration | Object | Parameter combination |
| Sharpe Ratio | Float | Risk-adjusted return |
| Total Return | Percentage | Raw performance |
| Trade Count | Integer | Number of trades |
| Max Drawdown | Percentage | Largest loss |
| Gate Status | Enum | PASS/MARGINAL/FAIL |
| Gate Reasons | Array | Why failed (if applicable) |

#### 4.4.2 Data Persistence
- **MUST** save all sweep results to database
- **MUST** tag results for filtering
- **MUST** maintain audit trail
- **SHOULD** export to CSV

## 5. Training Requirements

### 5.1 Training Selection
Users select one or more configurations from sweep leaderboard for training.

#### 5.1.1 Selection Rules
- **CAN** select multiple configurations
- **SHOULD** warn if selecting >5 configurations
- **MUST** only allow PASS or MARGINAL gate status
- **SHOULD** highlight similar configurations

### 5.2 Training Process

#### 5.2.1 ML Training Specifications
```yaml
Algorithm: XGBoost (default)
Parameters:
  n_estimators: [100, 200] (swept)
  max_depth: [3, 5, 7] (swept)
  learning_rate: [0.01, 0.1] (swept)
  
Validation:
  method: time_series_split
  folds: 5
  embargo: 1 day
  
Output:
  model_file: pickle format
  metadata: JSON with parameters
  performance: validation metrics
```

#### 5.2.2 Training Performance
- **MUST** complete within 15 minutes per configuration
- **MUST** provide progress updates
- **MUST** save checkpoints for recovery
- **SHOULD** support parallel training

### 5.3 Post-Training

#### 5.3.1 Model Review
Each trained model presents:
- Final training metrics
- Validation performance
- Feature importance
- Sample predictions

#### 5.3.2 Publish/Discard Decision
```yaml
User Actions:
  publish:
    - Model goes live
    - Starts monitoring real-time data
    - Begins alert generation
    
  discard:
    - Model deleted
    - Resources freed
    - Audit log entry
```

## 6. Alert Generation Requirements

### 6.1 Real-Time Processing

#### 6.1.1 Data Ingestion
```yaml
Frequency:
  0DTE Packs: every tick or 1 minute
  Swing Packs: every 5-15 minutes
  Position Packs: every hour
  
Data Required:
  - Current price (OHLCV)
  - Volume metrics
  - Options data (if applicable)
  - Market internals
```

#### 6.1.2 Feature Calculation
- **MUST** calculate all model indicators in real-time
- **MUST** handle missing data gracefully
- **MUST** maintain calculation history
- **SHOULD** cache intermediate results

### 6.2 Alert Structure

#### 6.2.1 Stock Alert
```json
{
  "alert_id": "uuid",
  "timestamp": "ISO-8601",
  "model_id": "string",
  "action": "BUY|SELL|HOLD",
  "instrument": "stock",
  "ticker": "string",
  "quantity": integer,
  "confidence": float (0-1),
  "entry_price": float,
  "stop_loss": float,
  "take_profit": float,
  "urgency": "immediate|day|good_till",
  "valid_until": "ISO-8601"
}
```

#### 6.2.2 Options Alert
```json
{
  "alert_id": "uuid",
  "timestamp": "ISO-8601",
  "model_id": "string",
  "action": "BUY|SELL|HOLD",
  "instrument": "option",
  "underlying": "string",
  "option_type": "call|put",
  "strike": float,
  "expiration": "YYYY-MM-DD",
  "contracts": integer,
  "confidence": float (0-1),
  "entry_price": float,
  "stop_loss": float,
  "take_profit": float,
  "urgency": "immediate|day|good_till",
  "valid_until": "ISO-8601"
}
```

### 6.3 Alert Distribution

#### 6.3.1 Routing Options
- **Sigma Pilot**: For automated execution
- **Sigma Sim**: For paper trading validation
- **User Notifications**: Email, SMS, Push
- **API Webhook**: Custom integrations

#### 6.3.2 Conflict Resolution
When multiple models signal same ticker:
- User-defined wrapper rules apply
- Options: first-wins, highest-confidence, ensemble
- Audit log for all decisions

## 7. Non-Functional Requirements

### 7.1 Performance
- Pack loading: < 1 second
- Model creation: < 5 seconds
- Simple sweep: < 5 minutes
- Custom sweep: < 30 minutes
- Training: < 15 minutes per config
- Alert generation: < 100ms from data receipt

### 7.2 Scalability
- Support 100,000 concurrent users
- Handle 1M models in system
- Process 10M alerts per day
- Store 5 years of historical data

### 7.3 Reliability
- 99.9% uptime for alert generation
- 99.5% uptime for training/sweeps
- Graceful degradation under load
- Automatic recovery from failures

### 7.4 Security
- Encryption at rest and in transit
- API authentication required
- Rate limiting per user
- Audit trail for all actions

### 7.5 Compliance
- SEC reporting capabilities
- GDPR data handling
- SOC 2 compliance
- Financial audit trails

## 8. User Interface Requirements

### 8.1 Pack Selection
- Visual cards with descriptions
- Filtering by tags
- Search functionality
- Performance previews

### 8.2 Model Builder
- Drag-and-drop interface
- Real-time validation
- Preset templates
- Advanced YAML editor (optional)

### 8.3 Sweep Configuration
- Simple/Advanced toggle
- Visual parameter ranges
- Estimated runtime display
- Progress visualization

### 8.4 Leaderboard
- Sortable columns
- Checkbox selection
- Export capabilities
- Comparison tools

### 8.5 Alert Dashboard
- Real-time alert stream
- Performance metrics
- Filter/search options
- Historical view

## 9. API Requirements

### 9.1 Pack Management
```
GET /packs - List available packs
GET /packs/{pack_id} - Get pack details
POST /packs - Create custom pack (premium)
PUT /packs/{pack_id} - Update pack
DELETE /packs/{pack_id} - Delete pack
```

### 9.2 Model Management
```
GET /models - List user's models
GET /models/{model_id} - Get model details
POST /models - Create new model
PUT /models/{model_id} - Update model
DELETE /models/{model_id} - Delete model
POST /models/{model_id}/publish - Publish model
POST /models/{model_id}/unpublish - Unpublish model
```

### 9.3 Sweep Operations
```
POST /sweeps - Start new sweep
GET /sweeps/{sweep_id} - Get sweep status
GET /sweeps/{sweep_id}/results - Get results
DELETE /sweeps/{sweep_id} - Cancel sweep
```

### 9.4 Training Operations
```
POST /training - Start training
GET /training/{job_id} - Get training status
GET /training/{job_id}/results - Get results
DELETE /training/{job_id} - Cancel training
```

### 9.5 Alert Operations
```
GET /alerts - Get recent alerts
GET /alerts/{alert_id} - Get alert details
POST /alerts/acknowledge - Mark as seen
GET /alerts/performance - Get performance metrics
```

## 10. Testing Requirements

### 10.1 Unit Testing
- 90% code coverage minimum
- All critical paths tested
- Edge cases covered

### 10.2 Integration Testing
- End-to-end flow testing
- API endpoint validation
- Database integrity checks

### 10.3 Performance Testing
- Load testing with 10,000 concurrent users
- Stress testing to find breaking points
- Latency testing for alerts

### 10.4 User Acceptance Testing
- Beta testing with 100 users
- Feedback incorporation
- Success metrics validation

## 11. Documentation Requirements

### 11.1 User Documentation
- Getting started guide
- Pack creation tutorial
- API reference
- Troubleshooting guide

### 11.2 Technical Documentation
- System architecture
- Database schema
- API specifications
- Deployment guide

## 12. Migration and Backwards Compatibility

### 12.1 Version Management
- Semantic versioning for packs
- Backwards compatibility for 2 major versions
- Migration tools for upgrades

### 12.2 Data Migration
- Automated migration scripts
- Rollback capabilities
- Data validation post-migration

## 13. Acceptance Criteria

### 13.1 Pack System
- [ ] Users can browse and select packs
- [ ] Premium users can create custom packs
- [ ] Pack validation prevents invalid configurations

### 13.2 Model System
- [ ] Users can create models from packs
- [ ] Models respect pack constraints
- [ ] Instrument-specific settings work correctly

### 13.3 Sweep System
- [ ] Simple sweeps complete in <5 minutes
- [ ] Custom sweeps support advanced parameters
- [ ] Leaderboard correctly ranks results

### 13.4 Training System
- [ ] Multiple configurations can be trained
- [ ] Training completes within SLA
- [ ] Users can publish/discard models

### 13.5 Alert System
- [ ] Alerts generate in real-time
- [ ] Alert structure contains all required fields
- [ ] Distribution works to all endpoints

## Appendices

### Appendix A: Glossary
- **Pack**: Trading strategy template with pre-configured components
- **Model**: User-created instance from a pack
- **Sweep**: Parameter optimization through backtesting
- **Gate**: Quality control threshold
- **Alert**: Trading signal generated by model

### Appendix B: References
- Vision Document v1.0
- API Specification v2.3
- Database Schema v1.5

---

**Document Status**: Ready for Review  
**Next Review Date**: February 2024  
**Owner**: Product Team