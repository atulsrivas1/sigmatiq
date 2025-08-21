# Discussion Notes - Strategy Packs Definition

## Date: 2025-08-21

### Topic: Defining Strategy Packs in Sigma System Context

**Participants**: User & Assistant

---

## Discussion Points

### Starting Question
- User wants to define exactly what a strategy pack is in the Sigma system context
- Need clear, precise definition that fits the platform

---

## Notes

### User's Definition
- Strategy pack = **namespace** 
- Models derive default policies from it
- Not just a template, but a container/grouping mechanism

### Implications
- Pack provides inheritance structure
- Models are instances that inherit from pack defaults
- Pack defines the boundaries/rules that models operate within

### Pack Components
- **Indicators**: Selected subset from shared indicator library
- **Risk Gates**: Selected subset from shared risk gates library
- **Tags**: 
  - Risk profile (conservative/balanced/aggressive)
  - Direction (long/short/both)
  - Other identifying characteristics

### Architecture
- Shared libraries (indicators, gates) → reusable components
- Packs select/configure from these libraries
- Models inherit pack's selections

---

## Assistant's Independent Vision of a Pack

### What I imagine a pack to be:
- **A personality or trading style** - like "aggressive momentum trader" or "cautious value investor"
- **A complete toolkit** - everything needed for that style: indicators, time horizons, asset preferences
- **A learning pathway** - starts simple, unlocks complexity as user gains experience
- **A community** - users of same pack share tips, compare results
- **A living thing** - adapts to market conditions, learns from collective user outcomes

### Pack as a Product
- Like choosing a character class in a game
- Each has strengths/weaknesses
- Some work better in certain "market weather"
- Users might collect multiple packs for different conditions

---

## Parameters That Define Pack "Vibe"

### Core Personality Parameters
1. **Time Horizon** 
   - Seconds (micro) → Minutes (scalp) → Days (swing) → Weeks (position) → Months (invest)
   - This sets the "pace" of the pack

2. **Risk Appetite**
   - Max drawdown tolerance
   - Position concentration 
   - Use of leverage/options
   - Stop loss tightness

3. **Decision Style**
   - Indicator-heavy (technical) vs Event-driven (catalyst) vs Flow-based (momentum)
   - Threshold for action (hair-trigger vs patient)

4. **Market Preference**
   - Trending vs Ranging vs Volatile
   - Bull vs Bear vs Neutral
   - Liquid vs Niche

5. **Execution Character**
   - Aggressive (market orders) vs Passive (limit orders)
   - All-in vs Scale-in
   - Binary vs Gradual exits

---

## Vibe → Technical Requirements Mapping

### Each vibe dimension needs specific tools:

**Time Horizon** → Indicator Selection
- Seconds: Order book imbalance, microprice, VPIN
- Days: RSI, MACD, Bollinger Bands  
- Months: Moving averages (50/200), fundamental ratios

**Risk Appetite** → Gate Configuration
- Conservative: Min 50 trades, Max 10% DD, Sharpe > 1.0
- Aggressive: Min 20 trades, Max 40% DD, Sharpe > 0.3

**Decision Style** → Feature Engineering
- Technical: Price-derived features only
- Event: Calendar features, news sentiment
- Flow: Volume, order flow, whale tracking

**Market Preference** → Entry/Exit Logic
- Trending: ADX > 25, breakout confirmation
- Volatile: VIX percentile, IV rank
- Ranging: Bollinger squeeze, mean reversion

**Execution** → Policy Settings
- Aggressive: market_orders: true, slippage_tolerance: high
- Patient: limit_orders: true, wait_for_confirmation: true

---

## Final Definition of Strategy Pack

### Strategy Pack = A cohesive trading personality with:

1. **Namespace** - Unique identifier and model grouping
2. **Vibe** - Trading personality defined by 5 dimensions
3. **Technical Stack** - Vibe-appropriate indicators, gates, policies
4. **Inheritance Model** - Models derive defaults from pack
5. **Tags** - Searchable attributes for discovery

### The Formula:
**Vibe (personality)** → **Requirements (tools)** → **Configuration (settings)** → **Models (instances)**

### Key Insight:
The vibe isn't just branding - it determines the entire technical stack. Mismatched components (like microsecond indicators for monthly investing) would break the coherence of the pack.

### Examples:
- **ZeroSigma**: Speed demon vibe → Tick indicators → Loose gates → High-frequency models
- **SwingSigma**: Patient hunter vibe → Daily indicators → Balanced gates → Multi-day models
- **DividPack**: Income seeker vibe → Fundamental indicators → Conservative gates → Quarterly models

---

## Trading Strategies vs Packs

### Question: How do traditional "trading strategies" relate to packs?

### Answer: 
**Pack = Container that holds multiple strategies**

### Traditional Trading Strategy:
- Specific rules: "Buy RSI < 30, Sell RSI > 70"
- Fixed parameters
- Single approach

### Pack Architecture:
```
Pack (SwingSigma)
├── Indicators (RSI, MACD, ADX...)
├── Gates (min trades, max DD...)
├── Policies (position sizing, stops...)
└── STRATEGIES (pre-defined settings)
    ├── "Momentum Swing" (RSI=14, MACD fast=12, ADX>25)
    ├── "Mean Reversion" (RSI=21, BB=2std, ADX<20)
    └── "Breakout Swing" (Donchian=20, Volume>2x, ADX>30)
```

### Key Insight:
**Strategies are just pre-configured combinations of the pack's available tools!**

- Pack = The toolbox + personality
- Strategy = A specific configuration/recipe using those tools
- Model = User's instance of a strategy with their own tweaks

---

## Tagging System for Discovery

### Pack-Level Tags:
- **Risk**: conservative, balanced, aggressive
- **Direction**: long_only, short_only, long_short
- **Timeframe**: intraday, swing, position, investment
- **Market**: trending, ranging, volatile, all_weather
- **Asset**: equities, options, futures, crypto, multi_asset
- **Style**: technical, fundamental, sentiment, quantitative
- **Experience**: beginner, intermediate, advanced

### Strategy-Level Tags:
- **Inherits all pack tags** (automatic)
- **Plus strategy-specific tags**:
  - **Specific approach**: momentum, mean_reversion, breakout, arbitrage
  - **Win rate**: high_probability, balanced, asymmetric
  - **Frequency**: high_freq, moderate, low_freq
  - **Capital**: small_account, standard, institutional
  - **Special conditions**: earnings_play, pre_market, power_hour

### Tag Inheritance Example:
```
SwingSigma Pack Tags: [swing, technical, long_short, intermediate]
    ↓ inherits to
"Momentum Swing" Strategy Tags: [swing, technical, long_short, intermediate] 
                               + [momentum, high_freq, standard]
    ↓ user creates
Model Tags: [all inherited] + [user_custom_tags]
```

### Example Filter Flow:
User: "Show me conservative, long-only swing strategies for beginners"
→ Filters to: SwingSigma pack → "Mean Reversion Swing" strategy

---

## User-Created Packs Discussion

### Question: Should users be able to create their own packs?

### Considerations:
- **Quality Control**: User packs might be poorly designed
- **Coherence**: Users might mix incompatible indicators/timeframes
- **Support**: Who maintains and updates user packs?
- **Discovery**: How to separate official vs community packs?
- **Liability**: What if user packs lose money for others?

### Possible Approaches:
1. **No user packs** - Only official, tested packs
2. **Private user packs** - Users can create for themselves only
3. **Community packs** - Share with approval/review process
4. **Pack builder wizard** - Guided creation with guardrails

### Decision: Premium Feature Tiers

#### Free Tier:
- Use official packs
- Create models from existing strategies
- Basic customization of parameters

#### Premium Tier ($X/month):
- **Create private packs** (up to 5)
- **Pack builder wizard** with validation
- **Custom indicators** from extended library
- **Advanced backtesting** (longer history, more granular data)

#### Pro Tier ($XX/month):
- **Unlimited private packs**
- **Submit packs for community review**
- **Monetize approved packs** (revenue share)
- **White-label packs** for their clients
- **API access** for programmatic pack creation

### Benefits of Premium Model:
- Quality maintained (free users get tested packs)
- Revenue stream from power users
- Natural progression path
- Community packs vetted before release
- Reduces support burden

---

## Pack Builder Wizard Validation Rules

### 1. Coherence Validation
**Time Alignment Check:**
- ❌ Reject: Tick indicators + Monthly timeframe
- ❌ Reject: Daily indicators + Seconds timeframe  
- ✅ Accept: Matched indicator/timeframe pairs

**Risk Profile Consistency:**
- ❌ Reject: Conservative tag + 50% drawdown gate
- ❌ Reject: Aggressive tag + 0.5% position size
- ✅ Accept: Aligned risk across all settings

### 2. Minimum Requirements
- **Indicators**: Min 3, Max 15 (prevent overfitting)
- **Gates**: Must have at minimum:
  - min_trades (>= 20)
  - max_drawdown (defined)
  - sharpe_ratio (>= 0)
- **Strategies**: At least 1 default strategy defined

### 3. Compatibility Matrix
```
If timeframe = "intraday":
  Required: tick/minute data indicators
  Blocked: weekly/monthly indicators
  
If style = "fundamental":
  Required: fundamental data indicators
  Optional: technical indicators
  
If asset = "options":
  Required: IV, greeks, options-specific
  Blocked: crypto-only indicators
```

### 4. Naming & Documentation
- **Pack name**: Unique, no special chars, < 20 chars
- **Description**: Required, 50-500 chars
- **Risk disclaimer**: Auto-added based on settings
- **Version**: Starts at 0.1.0

### 5. Performance Thresholds
Before allowing save:
- Must backtest successfully on 1 year data
- Sharpe > -0.5 (can lose, but not terribly)
- At least 10 trades generated
- No critical errors in logic

### 6. Wizard Flow
```
Step 1: Choose vibe (time, risk, style)
     ↓ (filters available options)
Step 2: Select indicators (only compatible shown)
     ↓ (validates combinations)
Step 3: Set gates (with sensible defaults)
     ↓ (checks coherence)
Step 4: Create one strategy (guided setup)
     ↓ (runs test backtest)
Step 5: Review & name (see validation report)
     ↓ (all checks pass)
Step 6: Save as private pack
```

### 7. Validation Report Example
```
Pack Validation Report
=====================
✅ Time coherence: PASS
✅ Risk alignment: PASS  
✅ Minimum indicators: PASS (7 selected)
✅ Required gates: PASS
⚠️ Backtest performance: MARGINAL (Sharpe 0.4)
✅ Documentation: COMPLETE

Status: APPROVED WITH WARNINGS
Recommendation: Consider tightening risk gates
```

---

## Deep Dive: Pack Components

### Question: What are all the components that make up a pack (before strategies)?

### Core Components to Define:
1. **Indicators** - What data/calculations to use
2. **Gates** - Quality control thresholds
3. **Policies** - Execution rules
4. **Features** - Derived calculations from indicators
5. **Risk Controls** - Position sizing, stops, etc.

---

## Ultimate Goal Clarification

### The End Game:
**Model → Generates Alerts → Sigma Pilot (auto-trade) OR User notifications**

### The Full Pipeline:
```
Pack (template/personality)
  ↓
Strategy (specific configuration)
  ↓
Model (trained instance)
  ↓
Alerts/Signals (BUY/SELL with confidence)
  ↓
Two paths:
  1. Sigma Pilot → Auto-execution at broker
  2. Notifications → User manual trading
```

### What the Model Must Produce:
- **Signal**: BUY/SELL/HOLD
- **Ticker**: What to trade
- **Confidence**: How sure (0-100%)
- **Size**: How much to trade
- **Entry**: Specific price/conditions
- **Exit**: Stop loss & take profit
- **Urgency**: Execute now vs good-for-day

### This means pack components must support:
- Real-time data processing
- Clear decision logic
- Risk-adjusted sizing
- Executable instructions
- Compliance/safety checks

---

## Reflection: Packs as Production Signal Generators

### What I now understand:
Packs aren't just templates or learning tools - they're **production-ready signal generation systems**.

### This changes everything:
1. **Indicators** aren't just for backtesting - they must handle live data feeds
2. **Strategies** aren't just parameter sets - they're complete trading logic
3. **Models** aren't just trained ML - they're live decision engines
4. **Gates** aren't just quality metrics - they're safety switches for real money

### The pack is really:
**A complete, coherent trading system that can safely generate executable signals**

### Critical implications:
- Every pack must be "broker-ready" (signals that translate to real orders)
- Indicators must gracefully handle missing/delayed data
- Risk controls must work in real-time (not just backtest)
- Policies must map to actual broker capabilities
- Everything must be auditable (why did it signal?)

### Pack components should be designed as:
```
Pack = Production Trading System
├── Data Pipeline (indicators → features)
├── Decision Engine (strategy logic)
├── Risk Manager (position sizing, stops)
├── Signal Generator (executable alerts)
├── Safety System (gates, checks)
└── Audit Trail (logging, explanations)
```

### This explains why:
- Coherence validation is critical (can't have broken production systems)
- Time alignment matters (real-time constraints)
- Gates are mandatory (protecting real capital)
- Premium users create packs (responsibility for production systems)

---

## Correction: Pack vs Model Roles

### User Clarification:
**Model = The actual trading system**
**Pack = Instructions/blueprint for how models should trade**

### Revised Understanding:
```
Pack (Blueprint/Instructions)
  ↓ tells how to
Strategy (Specific configuration)
  ↓ creates
Model (The actual trading system)
  ↓ generates
Signals (BUY/SELL alerts)
```

### Pack is like:
- **A recipe book** - not the kitchen
- **Building blueprints** - not the building
- **DNA** - not the organism
- **Constitution** - not the government

### Model is:
- The live, trained instance
- The actual decision maker
- The thing that processes real-time data
- The signal generator

### So Pack provides:
- Rules and boundaries
- Available tools (indicators)
- Quality standards (gates)
- Execution policies
- Risk guidelines

### Model uses Pack's instructions to:
- Build itself during training
- Make decisions during trading
- Stay within defined boundaries
- Follow the pack's "personality"

---

## Major Revision: Model Creation & Training Flow

### New Understanding:
**Model = Subset of pack components selected by user**

### Complete Flow:
```
1. Pack (Full menu of options)
   ├── All indicators available
   ├── All features
   ├── All strategies
   ├── All gates
   └── All policies

2. User Creates Model (Selects subset)
   ├── Pick some indicators from pack
   ├── Pick some features
   ├── Pick strategy
   ├── Pick gates
   └── Set parameters

3. Generate Sweeps (Test variations)
   → Multiple configurations tested
   → Different parameter combinations
   → Build backtest results

4. Leaderboard (Rank results)
   → Sort by Sharpe ratio
   → See what worked best
   → Pick top 2 configurations

5. Train Model (Use best configs)
   → Take top 2 from leaderboard
   → Train ML model on these
   → Lock in the winning formula

6. Generate Alerts (Production)
   → Trained model + real-time data
   → Produces BUY/SELL signals
   → Sends to Sigma Pilot or users
```

### Key Insights:
- **Pack = Supermarket** (all possible ingredients)
- **Model Definition = Shopping list** (what user selected)
- **Sweeps = Recipe testing** (try different amounts)
- **Leaderboard = Taste test results** (what worked best)
- **Training = Final recipe** (lock in the best version)
- **Alerts = Cooking live** (actual production)

### This means:
- Users have flexibility within pack boundaries
- Not forced to use everything in pack
- Can experiment with different combinations
- Best combinations get trained
- Only proven configurations go live

---

## Current Sweep Implementation Analysis

### What exists now (from code):
```python
BacktestSweepRequest:
- thresholds_variants: ["0.55,0.60,0.65", ...]  # Confidence levels
- allowed_hours_variants: ["13,14,15", ...]      # Trading hours
- top_pct_variants: [0.10, 0.15, ...]           # Top percentile
- splits: 5                                      # Cross-validation folds
- embargo: 0.0                                   # Holdout period
- min_trades: 20                                 # Quality gate
- min_sharpe: 0.5                               # Performance gate
```

### Current sweep tests:
- **Parameter combinations** (thresholds × hours × top_pct)
- **Each combo gets backtested**
- **Results filtered by gates** (min_trades, min_sharpe)
- **Ranked by Sharpe ratio**
- **Saved to database with tags**

### What's good:
✅ Tests multiple parameter combinations
✅ Has quality gates
✅ Saves results for comparison
✅ Tags for organization
✅ Parity calculations for options

### What might be missing for our vision:
❓ **Indicator selection variations** (currently uses all from model)
❓ **Feature combinations** (which features to use)
❓ **Strategy variations** (if model has multiple strategies)
❓ **Risk profile sweeps** (conservative vs aggressive)
❓ **ML hyperparameters** (for training phase)

### Proposed enhancement:
```python
EnhancedSweepRequest:
# Current (keep these)
- thresholds_variants
- allowed_hours_variants  
- top_pct_variants

# New additions
- indicator_sets: [["RSI", "MACD"], ["RSI", "ADX", "MACD"]]
- feature_sets: [["momentum", "volume"], ["all"]]
- strategy_variants: ["momentum_swing", "mean_reversion"]
- risk_profiles: ["conservative", "balanced"]
- ml_params: [{"n_estimators": 100}, {"n_estimators": 200}]
```

### Should we:
1. **Keep current** - Just sweep execution parameters
2. **Expand** - Also sweep model composition
3. **Two-phase** - Composition sweep first, then parameter sweep

### User Clarification:
**Model definition already includes:**
- Selected indicators
- Selected strategy
- Selected risk profile

**Sweep finds the alpha by testing:**
- Different thresholds (confidence levels)
- Different time windows (hours)
- Different position sizing (top %)

### So the flow is:
```
1. User creates Model
   - Picks indicators: [RSI, MACD]
   - Picks strategy: "momentum_swing"
   - Picks risk profile: "balanced"
   (This is FIXED for this model)

2. Sweep tests parameters
   - Thresholds: [0.50, 0.55, 0.60, 0.65, 0.70]
   - Hours: [[9,10], [13,14,15], [9,10,11,14,15]]
   - Top %: [0.05, 0.10, 0.15]
   (Find best COMBINATION of these)

3. Result
   - Best config: threshold=0.60, hours=[13,14,15], top=0.10
   - This is the "alpha" - the edge
```

### Key insight:
- **Model = WHAT to use** (ingredients)
- **Sweep = HOW to use it** (recipe fine-tuning)
- The alpha comes from finding the optimal parameters for the chosen model composition

---

## Sweep Enhancement Discussion

### Current sweep parameters:
- Thresholds (entry confidence)
- Allowed hours (when to trade)
- Top % (position sizing)

### What else might affect alpha?

**Exit parameters:**
- Stop loss levels? (2%, 5%, 10%)
- Take profit targets? (1:1, 2:1, 3:1 risk/reward)
- Time stops? (exit after N hours/days)

**Execution parameters:**
- Order types? (market, limit, limit with buffer)
- Slippage assumptions? (optimistic, realistic, pessimistic)

**Portfolio parameters:**
- Max concurrent positions? (1, 3, 5, 10)
- Correlation limits? (max correlation between positions)
- Sector concentration? (max per sector)

**Market filters:**
- Volatility regimes? (only trade when VIX < X)
- Trend filters? (only trade when SPY > 200 MA)
- Volume filters? (min volume requirements)

---

## Solution: Simple + Custom Sweeps

### Simple Sweep (Default - for beginners):
```python
SimpleSweep:
- thresholds: [0.50, 0.55, 0.60, 0.65, 0.70]
- allowed_hours: [[9,10], [13,14,15], [all_day]]
- top_pct: [0.05, 0.10, 0.15]
```
**Just 3 parameters, ~45 combinations max**

### Custom Sweep (Advanced - premium feature):
```python
CustomSweep:
# Core (always available)
- thresholds: [custom...]
- allowed_hours: [custom...]
- top_pct: [custom...]

# Optional additions
- stop_loss: [0.02, 0.05, 0.10]
- take_profit: [1.5, 2.0, 3.0]
- max_positions: [1, 3, 5]

# Pack-specific
- strike_selection: ["ATM", "5%_OTM"]  # Options packs
- hold_days: [1, 3, 5]                 # Swing packs
- entry_type: ["market", "limit"]      # Micro packs
```

### UI Flow:
```
Sweep Configuration
├── Mode: [Simple] [Custom]
│
├── Simple Mode (default)
│   ├── Quick Preset: Conservative | Balanced | Aggressive
│   └── Auto-fills reasonable ranges
│
└── Custom Mode (advanced)
    ├── Core parameters (editable)
    ├── [+ Add Parameter] button
    ├── Pack-specific options appear
    └── Warning: "More parameters = longer runtime"
```

### Benefits:
- Beginners aren't overwhelmed
- Advanced users can optimize deeply
- Pack-specific parameters available
- Natural progression path
- Prevents overfitting (warning on too many params)

---

## Instruments (Stocks vs Options) in Packs/Models/Sweeps

### The Challenge:
Options and stocks have fundamentally different characteristics:

**Stocks:**
- Single instrument (SPY)
- Buy/Sell/Short
- No expiration
- Linear payoff

**Options:**
- Multiple strikes/expirations per underlying
- Calls/Puts
- Time decay (theta)
- Non-linear payoff (gamma)
- Implied volatility component

### Questions to resolve:
1. Does a pack support one instrument type or multiple?
2. How does model specify what to trade?
3. What instrument-specific parameters need sweeping?
4. How do signals specify the exact instrument?

---

## Solution: Instrument Handling

### 1. Pack Level - Declares Capabilities
```yaml
pack: zerosigma
supported_instruments: ["options"]  # Options only
default_instrument: "options"

pack: swingsigma  
supported_instruments: ["stocks", "options"]  # Both
default_instrument: "stocks"
```

### 2. Model Level - User Chooses
```python
Model Creation:
- Pack: SwingSigma
- Instrument: "stocks"  # or "options"
- Ticker: "SPY"
- (If options): 
  - Default DTE: 7
  - Default strike: "ATM"
```

### 3. Sweep Level - Instrument-Specific Parameters

**Stock Sweeps:**
```python
- thresholds: [0.50, 0.60, 0.70]
- allowed_hours: [[9,10], [13,14,15]]
- position_size: [100_shares, 200_shares]
```

**Options Sweeps (additional):**
```python
- strike_selection: ["ATM", "5%_OTM", "10%_OTM"]
- dte_target: [0, 1, 7, 30]  # Days to expiration
- option_type: ["call", "put", "both"]
- contract_size: [1, 5, 10]
```

### 4. Signal Level - Complete Specification

**Stock Signal:**
```json
{
  "action": "BUY",
  "instrument": "stock",
  "ticker": "SPY",
  "quantity": 100,
  "order_type": "limit",
  "price": 450.50
}
```

**Options Signal:**
```json
{
  "action": "BUY",
  "instrument": "option",
  "underlying": "SPY",
  "option_type": "call",
  "strike": 455,
  "expiration": "2024-12-20",
  "contracts": 5,
  "order_type": "limit",
  "price": 2.50
}
```

### Key Design Decisions:
- Packs declare what they CAN trade
- Models lock in what they WILL trade
- Sweeps optimize HOW to trade it
- Signals specify EXACTLY what to execute

---

## Post-Sweep: Leaderboard to Training

### After Sweeps Complete:
1. **Leaderboard shows all tested configurations**
2. **User picks top performers**
3. **Training begins**
4. **Model goes live**

### The Leaderboard:
```
Rank | Config                          | Sharpe | Return | Trades | Gate
-----|--------------------------------|--------|--------|--------|------
1    | thr=0.60, hrs=[13,14], top=10% | 1.85   | 24%    | 87     | ✅ PASS
2    | thr=0.65, hrs=[13,14], top=5%  | 1.72   | 18%    | 62     | ✅ PASS  
3    | thr=0.55, hrs=[9,10], top=10%  | 1.45   | 22%    | 124    | ✅ PASS
4    | thr=0.50, hrs=[all], top=15%   | 0.92   | 31%    | 248    | ⚠️ MARGINAL
5    | thr=0.70, hrs=[14,15], top=5%  | 0.45   | 8%     | 18     | ❌ FAIL (min_trades)
```

### Question: How many configs to train?

### User Clarification:
**Users select which configurations to train** - not automatic top 2

### Selection Process:
```
Leaderboard Interface:
├── Checkbox next to each row
├── User selects 1 or more configs
├── Click "Train Selected"
└── Training begins for chosen configs
```

### User Considerations:
- **Performance**: Pick highest Sharpe
- **Diversification**: Pick different time/threshold combos
- **Risk tolerance**: Pick based on drawdown/trades
- **Gate status**: Only pick PASS (or accept MARGINAL)

### Example Selection Scenarios:

**Conservative User**:
- Picks only #1 (highest Sharpe, proven)

**Diversified User**:
- Picks #1 (afternoon trading)
- Picks #3 (morning trading)
- Different times = different market conditions

**Experimental User**:
- Picks #1, #2, #3
- Runs multiple models in parallel
- Compares live performance

### Training Process:
- Each selected config becomes a trained model
- User might end up with multiple models from one sweep
- Each can generate signals independently

### User Clarification:
**Each trained config becomes a separate model**

### Model Lifecycle:
```
Selected Configs → Training → Multiple Trained Models
                                    ↓
                            User Decision:
                            ├── Publish (goes live, generates alerts)
                            └── Discard (delete, never used)
```

### Example Flow:
1. User selects 3 configs from leaderboard
2. Training creates 3 models:
   - Model_A: thr=0.60, hrs=[13,14]
   - Model_B: thr=0.55, hrs=[9,10]  
   - Model_C: thr=0.65, hrs=[15,16]
3. After training, user reviews each
4. Decisions:
   - Model_A → Publish ✅ (starts generating alerts)
   - Model_B → Publish ✅ (starts generating alerts)
   - Model_C → Discard ❌ (didn't like final metrics)

### Published Models:
- Run independently
- Generate their own alerts
- Can be turned on/off individually
- Have their own performance tracking
- User manages them separately

### Benefits:
- Test multiple hypotheses
- Run different strategies for different conditions
- Easy A/B testing in production
- Can disable underperformers
- Portfolio of models vs single model risk

---

## Published Models → Real-Time Alert Generation

### The Alert Generation Pipeline:
```
Real-Time Data → Published Model → Decision → Alert → Distribution
```

### Step-by-Step Process:

**1. Data Ingestion**
```python
Every tick/minute/hour (based on model):
- Price data (OHLCV)
- Volume data
- Options data (if needed)
- Market internals
```

**2. Feature Calculation**
```python
Model calculates its indicators:
- RSI = calculate_rsi(prices, period=14)
- MACD = calculate_macd(prices)
- Features = combine(RSI, MACD, volume_surge)
```

**3. Model Prediction**
```python
Trained ML model evaluates:
- Confidence = model.predict_proba(features)
- If confidence > threshold (0.60):
  - Signal = "BUY"
- Else:
  - Signal = "HOLD"
```

**4. Alert Generation**
```json
{
  "timestamp": "2024-01-15T13:45:00Z",
  "model_id": "spy_swing_model_a",
  "signal": "BUY",
  "ticker": "SPY",
  "confidence": 0.72,
  "entry_price": 450.50,
  "stop_loss": 445.00,
  "take_profit": 460.00,
  "position_size": 100,
  "urgency": "immediate",
  "valid_until": "2024-01-15T15:00:00Z"
}
```

### Questions:
1. How often does each model check for signals?
2. What happens if multiple models signal same ticker?
3. How are conflicting signals handled?

### User Clarification:

**Signal Frequency:**
- Pack defines default (e.g., ZeroSigma = 1 minute)
- User can override (e.g., change to 5 minutes)

**Multiple Models:**
- User can create a "wrapper" around their models
- Wrapper handles filtering and conflict resolution
- User defines rules (first signal wins, highest confidence, etc.)

**Distribution:**
- Flexible - user decides where alerts go
- But that's later - **first priority is generating trustworthy alerts**

### The Real Priority:
```
Current Goal: Pack → Model → Sweep → Train → Reliable Alerts
Future Goal: Alert routing, conflict resolution, auto-trading
```

### Focus Areas for Trust:
1. **Quality Gates** - Only pass good backtests
2. **Paper Trading** - Test with fake money first
3. **Confidence Scores** - Show how sure the model is
4. **Performance Tracking** - Monitor live vs backtest
5. **Kill Switches** - Stop if performance degrades

### Building Trust Timeline:
```
Phase 1: Generate alerts (even if not perfect)
Phase 2: Track accuracy (are alerts profitable?)
Phase 3: Refine models (improve based on live data)
Phase 4: User confidence (consistent performance)
Phase 5: Enable auto-trading (only after trust established)
```

### User Clarification:
**SigmaSim = Paper trading platform for validation**

---

## Complete Flow Summary: Pack to Trusted Alerts

### The Full Journey:

**1. Pack Creation**
```
Pack (Template/Blueprint)
├── Supported instruments [stocks, options]
├── Available indicators [RSI, MACD, ADX...]
├── Available strategies [momentum, mean_reversion...]
├── Risk gates [min_trades, max_dd...]
├── Policies [position_sizing, stops...]
└── Tags [swing, technical, intermediate...]
```

**2. Model Definition**
```
User creates Model from Pack:
├── Select subset of indicators [RSI, MACD]
├── Choose strategy [momentum_swing]
├── Pick instrument [SPY options]
├── Set risk profile [balanced]
└── Name it [spy_momentum_balanced]
```

**3. Sweep Optimization**
```
Test parameter combinations:
├── Simple mode: 3 params, ~45 combos
├── Custom mode: Add more parameters
├── Run backtests on each combo
├── Filter by gates (min_trades, min_sharpe)
└── Generate leaderboard
```

**4. Training Selection**
```
From Leaderboard:
├── User reviews all results
├── Selects promising configs (1-5)
├── Each selection gets trained
├── Creates multiple models
└── User reviews training results
```

**5. Model Publishing**
```
For each trained model:
├── Review final metrics
├── Decide: Publish or Discard
├── Published models go live
└── Start monitoring real-time data
```

**6. Alert Generation**
```
Live models process data:
├── Ingest real-time prices
├── Calculate indicators/features
├── ML model makes prediction
├── If confidence > threshold
└── Generate detailed alert
```

**7. Trust Building (via SigmaSim)**
```
Paper Trading Validation:
├── Alerts → SigmaSim (fake money)
├── Track performance daily
├── Compare to backtest results
├── Build confidence over weeks
└── Graduate to real trading
```

**8. Production Trading**
```
After SigmaSim validation:
├── Alerts → Sigma Pilot (auto-trade)
├── Or → User notifications
├── Monitor live P&L
├── Kill switch if degrades
└── Continuous improvement
```

### The Products Work Together:
- **Sigma Lab**: Create and train models
- **SigmaSim**: Validate with paper trading
- **Sigma Market**: Share/sell proven models
- **Sigma Pilot**: AI-powered real trading execution

### The Complete Pipeline:
```
Sigma Lab (Create) 
    ↓
SigmaSim (Validate with paper trading)
    ↓
Sigma Market (Publish proven models)
    ↓
Sigma Pilot (AI executes real trades)
```

### Key Insight:
- SigmaSim is the trust bridge (proves models work)
- Sigma Market is the distribution platform (share/sell models)
- **Sigma Pilot is the final destination - AI-powered automated trading**

### Sigma Pilot's Role:
```
Receives Signals from:
├── Your own models (from Lab)
├── Purchased models (from Market)
└── Subscribed signals (from other traders)

AI Engine:
├── Manages position sizing
├── Handles order execution
├── Monitors risk in real-time
├── Adjusts for market conditions
├── Manages portfolio across multiple models
└── Executes at optimal prices

User Benefits:
├── Hands-off trading
├── 24/7 monitoring (crypto)
├── Professional execution
├── Risk management
└── Performance tracking
```

### The Trust Journey:
1. **Lab**: "I built a model"
2. **Sim**: "It works with fake money"
3. **Market**: "Others want to use it"
4. **Pilot**: "AI trades it with real money"

Each step builds more confidence before real capital is at risk.