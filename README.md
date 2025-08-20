# Sigmatiq - Institutional-Grade Trading Platform for Retail Investors

![License](https://img.shields.io/badge/license-Proprietary-red)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![TypeScript](https://img.shields.io/badge/typescript-5.0%2B-blue)
![Status](https://img.shields.io/badge/status-Active%20Development-green)

## Overview

Sigmatiq is an institutional-grade trading platform designed for retail investors, providing the complete lifecycle from strategy discovery to automated execution. The platform features model authoring, comprehensive backtesting, paper trading simulation, and automated execution with enterprise-level risk controls.

### Core Philosophy
- **Evidence over opinion** - All signals carry provenance, assumptions, and expected ranges
- **Transparency first** - Model cards, data sheets, and post-trade attribution are standard
- **Risk-aware by default** - Conservative controls enabled by default; users must opt into higher risk
- **Human control** - Automation is reversible and bounded by user policies
- **Continuous learning** - Every trade feeds evaluation loops and improves models

## Architecture

The platform is structured as a monorepo with modular components that will eventually be migrated to separate repositories.

### Product Suite

#### Sigma Lab - Model Authoring & Evaluation
Build, train, and backtest trading models with institutional-grade validation through the BTB (Build → Train → Backtest) pipeline.

- Feature selection with 90+ built-in technical indicators
- Walk-forward and cross-validation testing
- Transaction cost and slippage modeling
- Comprehensive model cards with SHA-based lineage tracking
- Support for multiple trading strategies (ZeroSigma, SwingSigma, LongSigma, OvernightSigma, MomentumSigma)

#### Sigma Sim - Paper Trading Environment
Broker-accurate simulation with realistic fill modeling for strategy validation before capital deployment.

- L1/L2 queue position simulation
- Policy engine for risk management
- Forward-test reporting with drift detection
- Experiment tracking and benchmark comparison

#### Sigma Market - Strategy Marketplace
Curated catalog of AI and human strategies with transparent performance metrics.

- Out-of-sample performance verification
- Slippage-aware returns reporting
- Capacity and stability grading
- Versioned model cards with full disclosure

#### Sigma Pilot - Automated Execution
Policy-driven automation with comprehensive risk controls for live trading.

- Per-feed capital caps and loss limits
- Broker integration with dry-run capabilities
- Real-time monitoring and anomaly detection
- Post-trade attribution analysis

### Technology Stack

**Backend:**
- FastAPI (Python 3.10+) - REST API framework
- PostgreSQL - Primary database
- Polygon.io - Market data provider
- Pydantic - Data validation
- SQLAlchemy - ORM (optional)

**Frontend:**
- React 18 with TypeScript
- Vite - Build tool with HMR
- CSS-in-JS with semantic design tokens
- React Context for state management

**Infrastructure:**
- Docker for containerization
- Environment-based configuration
- Comprehensive logging and monitoring

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL (optional, for database features)
- Polygon.io API key for market data

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sigmatiq.git
cd sigmatiq
```

2. Set up Python environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment:
```bash
cd products/sigma-lab
cp .env.example .env
# Edit .env with your configuration:
# - POLYGON_API_KEY=your_api_key
# - DB_HOST=localhost
# - DB_PORT=5432
# - DB_NAME=sigmalab
# - DB_USER=your_user
# - DB_PASSWORD=your_password
```

4. Initialize database (if using PostgreSQL):
```bash
psql -U your_user -d sigmalab -f products/sigma-lab/api/migrations/0001_init.sql
```

5. Start the backend API:
```bash
python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload
```

6. Start the frontend (in a new terminal):
```bash
cd products/sigma-lab/ui
npm install
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- API: http://localhost:8001
- API Documentation: http://localhost:8001/docs

### Development with Mock API

For UI development without the full backend:

```bash
cd products/sigma-lab/mock-api
pip install -r requirements.txt
python app.py
```

The mock API will run on http://localhost:8010

## Trading Packs

### ZeroSigma (0DTE Options)
High-frequency intraday options strategies focusing on same-day expiration contracts.
- Hourly signal generation
- Options flow analysis
- Greeks-based entry/exit

### SwingSigma (2-10 Day Holdings)
Medium-term swing trading strategies for both equities and options.
- Daily rebalancing
- Technical pattern recognition
- Risk-adjusted position sizing

### LongSigma (63+ Day Holdings)
Long-term investment strategies with quarterly rebalancing.
- Fundamental factor integration
- Sector rotation models
- Portfolio optimization

### OvernightSigma (Overnight Gaps)
Strategies exploiting overnight price movements and opening gaps.
- Close-to-open arbitrage
- News sentiment analysis
- Pre-market positioning

### MomentumSigma (Trend Following)
Volatility-scaled momentum strategies with adaptive position sizing.
- Multi-timeframe analysis
- Dynamic stop-loss adjustment
- Regime detection

## API Endpoints

### Core Operations
```
GET  /models                    # List all models
POST /models                    # Create new model
GET  /models/{model_id}         # Get model details
PATCH /models/{model_id}        # Update model configuration

GET  /leaderboard              # View backtest results
POST /backtest                 # Run single backtest
POST /backtest_sweep           # Run grid search backtest

POST /build_matrix             # Build training matrix
POST /train                    # Train model
POST /preview_matrix           # Preview and validate data
```

### Monitoring
```
GET  /signals                  # Live signal data
GET  /signals/leaderboard      # Live performance metrics
GET  /signals/summary          # Aggregated statistics
GET  /health                   # System health check
GET  /healthz                  # Detailed health status
```

### Administration
```
GET  /admin/jobs               # View background jobs
GET  /admin/quotas             # Manage user quotas
GET  /admin/risk-profiles      # Configure risk profiles
GET  /admin/audit              # View audit logs
```

## Key Features

### 90+ Technical Indicators
- **Momentum**: RSI, MACD, Stochastic, Williams %R, TSI, CCI
- **Trend**: ADX, Aroon, EMA, SMA, KAMA, Ichimoku, Parabolic SAR
- **Volatility**: Bollinger Bands, ATR, Keltner Channels, Donchian Channels
- **Volume**: OBV, MFI, CMF, VWAP, Volume Profile
- **Options**: IV analytics, PCR, Gamma/OI concentration, Greeks analysis

### Risk Management System
- Three risk profiles: Conservative, Balanced, Aggressive
- Position sizing algorithms with Kelly criterion
- Stop-loss and take-profit automation
- Maximum drawdown controls (ES95 limits)
- Daily and per-trade loss limits
- Gate system for strategy validation

### Advanced Backtesting
- Walk-forward analysis with out-of-sample testing
- Cross-validation with time-series splits
- Transaction cost modeling with spread estimation
- Slippage estimation based on volume
- Regime-aware testing with market condition filters
- Parity bracket analysis for entry/exit optimization

### Lineage & Reproducibility
- SHA-based fingerprinting for all artifacts
- Complete audit trail for model lifecycle
- Matrix, config, and policy versioning
- Reproducible backtests with stored parameters
- Model card generation with performance metrics

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sigma_core --cov=sigma_platform --cov-report=term-missing

# Run specific test modules
pytest products/sigma-lab/api/tests/test_api.py -v
pytest products/sigma-core/tests/test_indicators.py -v
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

### Getting Started
- [Platform Overview](products/sigma-lab/docs/INDEX.md)
- [Conventions & Standards](products/sigma-lab/docs/CONVENTIONS.md)
- [Quick Start Guide](products/sigma-lab/docs/QUICKSTART.md)

### API Documentation
- [BTB Pipeline API](products/sigma-lab/docs/api/BTB_API_Spec_v1.md)
- [Signals API](products/sigma-lab/docs/api/Signals_API_Spec_v1.md)
- [Admin API](products/sigma-lab/docs/api/Admin_API_Spec_v1.md)
- [Assistant API](products/sigma-lab/docs/api/Assistant_API_Spec_v1.md)

### UI Documentation
- [UI Requirements](products/sigma-lab/docs/ui/Sigma_Lab_UI_Requirements_v1.md)
- [BTB UI Specification](products/sigma-lab/docs/ui/BTB_UI_Spec_v1.md)
- [AI Assistant UI](products/sigma-lab/docs/ui/AI_Assistant_Spec_v1.md)

### Architecture Decision Records
- [System Architecture](products/sigma-lab/docs/adr/0001-architectural-overview.md)
- [BTB Pipeline Design](products/sigma-lab/docs/adr/0005-btb-pipeline-and-risk-profiles.md)
- [UI Workflow](products/sigma-lab/docs/adr/0006-template-first-create-and-split-designer-composer.md)

## Project Status

### Completed Features
- Core BTB pipeline (Build, Train, Backtest)
- Model creation with templates
- Sweeps for grid search optimization
- Leaderboard for result comparison
- Risk profile system
- Lineage tracking
- Basic UI with theme support
- Command palette navigation
- Mock API for development

### In Progress
- Signals monitoring UI
- Model Designer interface
- Options overlay functionality
- AI Assistant integration
- Enhanced gate system
- Selection cart persistence

### Roadmap
- **Phase 1 (0-3 months)**: Core pipeline completion, UI polish, testing suite
- **Phase 2 (3-6 months)**: Sigma Market MVP, Sigma Pilot risk caps, observability
- **Phase 3 (6-12 months)**: Multi-asset support, international markets, SDK release

## Security & Compliance

- Environment-based configuration for sensitive data
- Admin token authentication for protected endpoints
- Input validation through Pydantic models
- SQL injection protection via parameterized queries
- Comprehensive audit logging
- Model risk management with documented lifecycle
- No survivor bias in backtesting
- Point-in-time data enforcement

## Contributing

This is currently a private repository. For partnership inquiries or to report issues, please contact the development team.

### Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript strict mode for frontend
- Write tests for new features
- Update documentation for API changes
- Use semantic commit messages

## License

Proprietary - All rights reserved. This software is proprietary and confidential.

## About Sigmatiq

Sigmatiq is building the future of retail trading by democratizing access to institutional-grade tools and strategies. Our mission is to deliver measurable edge across the retail trading journey with transparent models, realistic testing, and controlled automation.

---

**Vision**: Level the playing field by packaging quantitative methods and AI into trustworthy tools anyone can use.

**Mission**: Deliver measurable edge across the retail trading journey with transparent models, realistic testing, and controlled automation.

---

*Built with conviction that retail traders deserve better tools.*