# Getting Started with Sigmatiq Sigma Lab

This guide will help you set up and start using Sigmatiq Sigma Lab for algorithmic trading.

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **Python**: 3.9 or higher
- **Node.js**: 18.0 or higher
- **PostgreSQL**: 14.0 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 10GB free space

### Required API Keys
- **Polygon.io API Key**: Sign up at [polygon.io](https://polygon.io) for market data access

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/atulsrivas1/sigmatiq.git
cd sigmatiq
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# API Configuration
POLYGON_API_KEY=your_polygon_api_key_here

# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sigmalab
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# API Server
API_HOST=0.0.0.0
API_PORT=8001

# Development
DEBUG=true
```

### 3. Database Setup

#### Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from [PostgreSQL official site](https://www.postgresql.org/download/windows/)

#### Create Database

```bash
psql -U postgres
CREATE DATABASE sigmalab;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE sigmalab TO your_db_user;
\q
```

#### Run Migrations

```bash
psql -U your_db_user -d sigmalab -f products/sigma-lab/api/migrations/0001_init.sql
```

### 4. Backend Setup

#### Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Start API Server

```bash
python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload
```

The API will be available at `http://localhost:8001`

### 5. Frontend Setup

#### Install Node Dependencies

```bash
cd products/sigma-lab/ui
npm install
```

#### Start Development Server

```bash
npm run dev
```

The UI will be available at `http://localhost:5173`

### 6. Mock API (Optional - for UI Development)

If you want to develop the UI without the backend:

```bash
cd products/mock-api
pip install -r requirements.txt
make dev
```

Mock API will run on `http://localhost:8010`

## 🎯 Your First Model

### Step 1: Access the Dashboard

Navigate to `http://localhost:5173` in your browser. You'll see the main dashboard with:
- Recent Models
- Last Runs
- Quick Actions
- System Health

### Step 2: Create a New Model

1. Click **"Create Model"** in Quick Actions
2. Select a trading pack template:
   - **ZeroSigma**: For 0DTE options strategies
   - **SwingSigma**: For 2-10 day swing trades
   - **LongSigma**: For long-term investments

3. Configure your model:
   - **Name**: Give your model a descriptive name
   - **Risk Profile**: Choose Conservative, Balanced, or Aggressive
   - **Indicators**: Select technical indicators to use

### Step 3: Build Training Matrix

1. Navigate to your model's Composer page
2. Click the **Build** tab
3. Select date range for historical data
4. Click **"Build Matrix"** to generate training data

### Step 4: Run Backtests

1. Go to the **Backtest** tab
2. Configure test parameters:
   - Threshold values
   - Allowed trading hours
   - Position sizing

3. Click **"Run Backtest"** to execute

### Step 5: Analyze Results

1. View the **Leaderboard** to compare results
2. Check performance metrics:
   - Sharpe Ratio
   - Cumulative Returns
   - Win Rate
   - Maximum Drawdown

3. Review gate status (pass/fail criteria)

## ⚙️ Configuration

### Risk Profiles

| Profile | Description | Max Drawdown | Position Size |
|---------|-------------|--------------|---------------|
| **Conservative** | Low risk, steady returns | 10% | 1-2% per trade |
| **Balanced** | Moderate risk/reward | 20% | 3-5% per trade |
| **Aggressive** | High risk, high potential | 30% | 5-10% per trade |

### Trading Hours Configuration

Define allowed trading hours in your model:

```python
allowed_hours = [9, 10, 11, 12, 13, 14, 15]  # 9 AM to 3 PM EST
```

### Indicator Sets

Available technical indicators include:
- Moving Averages (SMA, EMA, WMA)
- Momentum (RSI, MACD, Stochastic)
- Volatility (Bollinger Bands, ATR)
- Volume (OBV, Volume Profile)
- 90+ additional indicators

## 🧪 Testing Your Setup

### Run Core Tests

```bash
pytest products/sigma-core/tests -q
```

### Run API Tests

```bash
pytest products/sigma-lab/api/tests -q
```

### Run Frontend Tests

```bash
cd products/sigma-lab/ui
npm test
```

## 🔍 Troubleshooting

### Common Issues

#### Database Connection Error
```
Error: could not connect to database
```
**Solution**: Check PostgreSQL is running and credentials in `.env` are correct

#### Polygon API Error
```
Error: Invalid API key
```
**Solution**: Verify your Polygon.io API key in `.env`

#### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port in configuration or stop conflicting service

#### Module Import Error
```
ModuleNotFoundError: No module named 'sigma_core'
```
**Solution**: Ensure you're in the project root and virtual environment is activated

### Getting Help

- Check [FAQ](FAQ)
- Browse [GitHub Issues](https://github.com/atulsrivas1/sigmatiq/issues)
- Join [Discussions](https://github.com/atulsrivas1/sigmatiq/discussions)

## 📚 Next Steps

- Read the [Architecture Overview](Architecture) to understand the system design
- Learn about the [BTB Pipeline](BTB-Pipeline) for model development
- Explore [Trading Packs](Trading-Packs) for different strategies
- Review [API Reference](API-Reference) for integration

## 🎥 Video Tutorials

Coming soon:
- Installation Walkthrough
- Creating Your First Model
- Understanding Backtests
- Advanced Configuration

---

**Need help?** Open an issue on [GitHub](https://github.com/atulsrivas1/sigmatiq/issues) or check our [Discord community](#)