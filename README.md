# Sigmatiq - Institutional-Grade Trading Platform for Retail Investors

![License](https://img.shields.io/badge/license-Proprietary-red)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-Active%20Development-green)

## 🚀 Overview

Sigmatiq is an institutional-grade, retail-first platform that transforms market data and AI models into actionable trading signals, safe practice environments, and automated execution capabilities. Built to level the playing field for retail traders, Sigmatiq provides transparent, evidence-based trading tools with enterprise-level risk controls.

### Core Philosophy
- **Evidence over opinion** - All signals carry provenance, assumptions, and expected ranges
- **Transparency first** - Model cards, data sheets, and post-trade attribution are standard
- **Risk-aware by default** - Conservative controls enabled by default; users must opt into higher risk
- **Human control** - Automation is reversible and bounded by user policies
- **Continuous learning** - Every trade feeds evaluation loops and improves models

## 🏗️ Architecture

> **Note**: Products are currently structured in a monorepo for rapid development. Each product will eventually be migrated to its own repository.

### Product Suite

#### 🔬 **Edge Lab** - Model Authoring & Evaluation
Build, train, and backtest trading models with institutional-grade validation.
- Feature/indicator selection with 90+ built-in technical indicators
- Walk-forward and cross-validation testing
- Transaction cost and slippage modeling
- Comprehensive model cards with lineage tracking
- Support for multiple trading strategies (ZeroEdge, SwingEdge, LongEdge, OvernightEdge, MomentumEdge)

#### 📊 **Edge Sim** - Paper Trading Environment
Broker-accurate simulation with realistic fill modeling.
- L1/L2 queue position simulation
- Policy engine for risk management (sizing, stop-loss, take-profit)
- Forward-test reporting with drift detection
- Experiment tracking and benchmark comparison

#### 🛒 **Edge Market** - Strategy Marketplace
Curated catalog of AI and human strategies with transparent performance metrics.
- Out-of-sample performance verification
- Slippage-aware returns reporting
- Capacity and stability grading
- Versioned model cards with full disclosure

#### 🎯 **Edge Pilot** - Automated Execution
Policy-driven automation with comprehensive risk controls.
- Per-feed capital caps and loss limits
- Broker integration with dry-run capabilities
- Real-time monitoring and anomaly detection
- Post-trade attribution analysis

### Core Libraries

- **Edge Core** - Shared Python library for datasets, features, indicators, models, backtests
- **Edge Platform** - API/server utilities, database helpers, audit, lineage tracking
- **Edge Workers** - Background task processing and orchestration

## 🚦 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL (optional, for database features)
- Polygon.io API key for market data

### Installation

1. Clone the repository:
```bash
git clone https://github.com/atulsrivas1/sigmatiq.git
cd sigmatiq
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cd products/edge-lab
cp .env.example .env
# Edit .env with your POLYGON_API_KEY and database settings
```

4. Start the API server:
```bash
python products/edge-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload
```

### Common Operations

Build a trading matrix:
```bash
make build MODEL_ID=spy_opt_0dte_hourly PACK_ID=zeroedge START=2024-01-01 END=2024-12-31
```

Train a model:
```bash
make train MODEL_ID=spy_opt_0dte_hourly ALLOWED_HOURS=13,14,15
```

Run backtests:
```bash
make backtest MODEL_ID=spy_opt_0dte_hourly THRESHOLDS=0.55,0.60,0.65 SPLITS=5
```

View leaderboard:
```bash
curl "http://localhost:8001/leaderboard?model_id=spy_opt_0dte_hourly"
```

## 📦 Trading Packs

### ZeroEdge (0DTE Options)
High-frequency intraday options strategies focusing on same-day expiration contracts.

### SwingEdge (5-20 Day Holdings)
Medium-term swing trading strategies for both equities and options.

### LongEdge (63+ Day Holdings)
Long-term investment strategies with quarterly rebalancing.

### OvernightEdge (Overnight Gaps)
Strategies exploiting overnight price movements and opening gaps.

### MomentumEdge (Trend Following)
Volatility-scaled momentum strategies with adaptive position sizing.

## 🔧 Key Features

### 90+ Technical Indicators
- **Momentum**: RSI, MACD, Stochastic, Williams %R, TSI
- **Trend**: ADX, Aroon, EMA, SMA, KAMA, Ichimoku
- **Volatility**: Bollinger Bands, ATR, Keltner Channels
- **Volume**: OBV, MFI, CMF, Volume-Weighted indicators
- **Options**: IV analytics, PCR, Gamma/OI concentration, Greeks

### Advanced Backtesting
- Walk-forward analysis
- Cross-validation with time-series splits
- Transaction cost modeling
- Slippage estimation
- Regime-aware testing

### Risk Management
- Position sizing algorithms
- Stop-loss and take-profit automation
- Maximum drawdown controls
- Exposure limits per symbol/sector
- Daily loss limits

## 📚 Documentation

Comprehensive documentation is available in `products/edge-lab/docs/`:

- [Platform Overview](products/edge-lab/docs/Sigmatiq_Vision_and_Product_Ecosystem.md)
- [API Contract](products/edge-lab/docs/CONTRACT.md)
- [Conventions & Standards](products/edge-lab/docs/CONVENTIONS.md)
- [Documentation Index](products/edge-lab/docs/INDEX.md)
- [Pack Roadmap](products/edge-lab/docs/PACKS_ROADMAP.md)

### API Documentation
- [Signals API](products/edge-lab/docs/api/Signals_API_Spec_v1.md)
- [Build-Train-Backtest API](products/edge-lab/docs/api/BTB_API_Spec_v1.md)
- [Admin API](products/edge-lab/docs/api/Admin_API_Spec_v1.md)
- [Pack Management](products/edge-lab/docs/api/Packs_API_Spec_v1.md)

## 🛡️ Security & Compliance

- Model risk management with documented lifecycle
- AI transparency through model cards and data sheets
- No survivor bias in backtesting
- Point-in-time data enforcement
- Mandatory forward testing before production
- Comprehensive audit logging
- User protection with conservative defaults

## 🔮 Roadmap

### Phase 0-3 Months
- Core data/feature pipelines
- Backtest engine with walk-forward validation
- Initial model packs deployment
- EdgeSim MVP release

### Phase 3-6 Months
- Edge Market v1 with billing integration
- Edge Pilot with risk caps
- Enhanced observability dashboard
- Model card standardization

### Phase 6-12 Months
- Multi-asset class support
- Creator SDK release
- International market expansion
- Advanced governance dashboards

## 🤝 Contributing

This is currently a private repository. For partnership inquiries or to report issues, please contact the development team.

## 📄 License

Proprietary - All rights reserved. This software is proprietary and confidential.

## 🏢 About Sigmatiq

Sigmatiq is building the future of retail trading by democratizing access to institutional-grade tools and strategies. Our mission is to deliver measurable edge across the retail trading journey with transparent models, realistic testing, and controlled automation.

---

**Vision**: Level the playing field by packaging quantitative methods and AI into trustworthy tools anyone can use.

**Mission**: Deliver measurable edge across the retail trading journey with transparent models, realistic testing, and controlled automation.

---

*Built with conviction that retail traders deserve better tools.*