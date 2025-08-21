# Complete User Guide

This comprehensive guide covers all aspects of using the Sigmatiq platform for trading model development, backtesting, and signal generation.

## Table of Contents

1. [Platform Overview](#platform-overview)
2. [Dashboard](#dashboard)
3. [Model Management](#model-management)
4. [Build-Train-Backtest Pipeline](#build-train-backtest-pipeline)
5. [Strategy Packs](#strategy-packs)
6. [Risk Management](#risk-management)
7. [Performance Analysis](#performance-analysis)
8. [Signals and Monitoring](#signals-and-monitoring)
9. [Advanced Features](#advanced-features)
10. [Best Practices](#best-practices)

## Platform Overview

### Core Workflow
The Sigmatiq platform follows a structured workflow:

1. **Discover**: Browse templates or create custom models
2. **Build**: Generate training data with technical indicators
3. **Train**: Optimize model parameters (optional)
4. **Backtest**: Test performance on historical data
5. **Validate**: Use sweeps to test multiple configurations
6. **Deploy**: Move to paper trading or live signals
7. **Monitor**: Track ongoing performance

### Navigation
- **Dashboard**: Overview and quick actions
- **Models**: Browse, create, and manage your trading models
- **Signals**: Monitor live performance and signal history
- **Health**: System status and diagnostics

## Dashboard

Your dashboard provides an at-a-glance view of your trading activities:

### Recent Models
- Shows your latest created or modified models
- Quick actions: Open, Backtest, Run Sweeps
- Performance sparklines for visual trends

### Last Runs
- Recent backtest and training activities
- Status indicators (completed, running, failed)
- Quick links to results

### Quick Actions
- **Create Model**: Start the model creation wizard
- **Run Backtest**: Quick backtest on existing model
- **Sweeps**: Batch test multiple configurations
- **Health Check**: System diagnostics

### Health Summary
- System status indicators
- Data feed health
- API connectivity status
- Recent error summaries

## Model Management

### Creating Models

#### Using Templates (Recommended for Beginners)
1. Click **"Create Model"** from dashboard
2. Choose a strategy pack:
   - **ZeroSigma**: Same-day options trading
   - **SwingSigma**: Multi-day swing trades
   - **LongSigma**: Long-term positions
   - **OvernightSigma**: Gap trading
   - **MomentumSigma**: Momentum-based strategies

3. Select specific template within pack
4. Name your model and choose risk profile
5. Click "Create & Go to Composer"

#### Custom Model Creation (Advanced)
1. Choose "Custom" template
2. Configure indicators manually
3. Set up policy rules
4. Define risk parameters

### Model Designer

The Designer lets you customize model structure:

#### Indicator Selection
- **Technical Indicators**: 90+ built-in options including:
  - Moving Averages (SMA, EMA, VWAP)
  - Momentum (RSI, MACD, Stochastic)
  - Volatility (Bollinger Bands, ATR)
  - Volume (OBV, MFI, Volume Profile)
  - Options-specific (Greeks, IV, OI)

#### Policy Configuration
- **Entry Rules**: When to open positions
- **Exit Rules**: When to close positions
- **Risk Limits**: Position sizing and stop-losses
- **Market Conditions**: When to trade vs. stay flat

#### Validation
- Real-time policy validation
- Error detection and suggestions
- Compatibility checks with selected pack

## Build-Train-Backtest Pipeline

### Build Phase

#### Data Selection
- **Date Range**: Choose training period (6-18 months recommended)
- **Universe**: Single ticker (SPY) or multiple assets
- **Frequency**: Daily, hourly, or intraday data

#### Matrix Generation
- Downloads historical price/volume data
- Calculates all selected technical indicators
- Creates feature matrix for model training
- Provides data quality metrics

#### Quality Checks
- **Completeness**: Percentage of non-missing data
- **Balance**: Distribution of bullish vs bearish signals
- **Stationarity**: Data stability over time
- **Outliers**: Unusual data points flagged

### Train Phase (Optional)

#### When to Use Training
- Custom models benefit most from training
- Template models often work well without training
- Use when you want to optimize parameters

#### Training Process
- **Algorithm Selection**: Gradient Boosting (default), Random Forest, or Neural Networks
- **Cross-Validation**: Prevents overfitting with time-series splits
- **Parameter Optimization**: Automatic hyperparameter tuning
- **Validation**: Out-of-sample testing during training

#### Training Results
- **Model Artifacts**: Saved trained models
- **Feature Importance**: Which indicators matter most
- **Validation Metrics**: Performance on held-out data
- **Calibration**: Probability calibration for decision thresholds

### Backtest Phase

#### Single Backtest
- Tests one specific configuration
- Shows detailed performance metrics
- Includes trade-by-trade analysis
- Generates performance plots

#### Key Metrics Explained
- **Sharpe Ratio**: Risk-adjusted returns (higher is better)
  - < 0.5: Poor performance
  - 0.5-1.0: Decent performance  
  - 1.0-2.0: Good performance
  - > 2.0: Excellent performance

- **Total Return**: Cumulative profit/loss percentage
- **Maximum Drawdown**: Worst peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Average Trade**: Mean profit per trade
- **Trade Count**: Number of trades executed

#### Realistic Simulation
- **Transaction Costs**: Includes broker fees and spreads
- **Slippage**: Market impact and execution delays
- **Liquidity**: Accounts for bid-ask spreads
- **Survivorship Bias**: Avoids looking into the future

## Strategy Packs

### ZeroSigma (0DTE Options)
**Purpose**: Same-day options expiry trading
**Time Horizon**: Intraday (1-6 hours)
**Best For**: Active traders comfortable with options

**Key Features:**
- Gamma exposure analysis
- Implied volatility tracking  
- Options flow patterns
- End-of-day positioning

**Risk Considerations:**
- High frequency of trades
- Time decay risk
- Liquidity requirements
- Requires active monitoring

### SwingSigma
**Purpose**: Multi-day swing trading
**Time Horizon**: 2-10 days
**Best For**: Part-time traders seeking medium-term opportunities

**Key Features:**
- Trend reversal identification
- Support/resistance analysis
- Momentum confirmation
- Risk-adjusted position sizing

**Strategies Include:**
- Breakout trading
- Mean reversion
- Momentum following
- Range trading

### LongSigma  
**Purpose**: Long-term investment strategies
**Time Horizon**: 3-12 months
**Best For**: Patient investors focused on fundamental trends

**Key Features:**
- Sector rotation signals
- Economic cycle analysis
- Valuation-based entries
- Low turnover approach

**Risk Considerations:**
- Longer holding periods
- Market cycle exposure
- Fundamental analysis integration

### OvernightSigma
**Purpose**: Gap trading strategies
**Time Horizon**: Overnight holds
**Best For**: Traders capitalizing on overnight market moves

**Key Features:**
- After-hours sentiment analysis
- Gap identification and fading
- Overnight risk management
- Pre-market positioning

### MomentumSigma
**Purpose**: Volatility-scaled momentum strategies  
**Time Horizon**: Variable (1-30 days)
**Best For**: Traders seeking trending markets

**Key Features:**
- Volatility-adjusted position sizing
- Trend strength measurement
- Momentum confirmation signals
- Dynamic exit strategies

## Risk Management

### Risk Profiles

#### Conservative
- **Position Size**: 1-2% of capital per trade
- **Stop Losses**: Tight (2-5% maximum loss)
- **Diversification**: High (10+ positions)
- **Drawdown Limit**: 10% maximum
- **Best For**: New users, retirement accounts, risk-averse investors

#### Balanced  
- **Position Size**: 2-5% of capital per trade
- **Stop Losses**: Moderate (3-8% maximum loss)
- **Diversification**: Medium (5-10 positions)
- **Drawdown Limit**: 15% maximum
- **Best For**: Experienced traders, growth accounts

#### Aggressive
- **Position Size**: 5-10% of capital per trade  
- **Stop Losses**: Wide (5-15% maximum loss)
- **Diversification**: Lower (3-7 positions)
- **Drawdown Limit**: 25% maximum
- **Best For**: Professional traders, speculation accounts

### Gate System

Automated quality controls that prevent poor models from trading:

#### Performance Gates
- **Minimum Sharpe**: Must exceed 0.5
- **Maximum Drawdown**: Cannot exceed profile limits
- **Minimum Trades**: Must have sufficient trading frequency
- **Win Rate**: Must exceed random chance (adjustable)

#### Quality Gates
- **Data Quality**: Minimum data completeness requirements
- **Backtest Period**: Sufficient historical testing
- **Out-of-Sample**: Performance on unseen data
- **Stability**: Consistent performance across time periods

#### Risk Gates
- **Position Concentration**: Maximum exposure per asset
- **Sector Limits**: Diversification requirements  
- **Correlation**: Maximum correlation between strategies
- **Leverage**: Maximum leverage allowed

### Position Sizing

#### Kelly Criterion (Advanced)
- Optimal position sizing based on win rate and average win/loss
- Automatically calculated based on backtest results
- Conservative scaling (typically 25-50% of full Kelly)

#### Fixed Percentage
- Simple percentage of capital per trade
- Easy to understand and implement
- Good for beginners and conservative approaches

#### Volatility Adjusted
- Position size varies based on expected volatility
- Larger positions in lower volatility periods
- Risk parity across different market conditions

## Performance Analysis

### Understanding Results

#### Equity Curves
- **Smooth Upward**: Consistent performance
- **Choppy but Rising**: Volatile but profitable
- **Flat**: No edge detected
- **Declining**: Strategy not working

#### Drawdown Analysis
- **Duration**: How long losing periods last
- **Magnitude**: How deep losses get
- **Recovery**: How quickly capital is recovered
- **Frequency**: How often drawdowns occur

#### Trade Analysis
- **Win/Loss Distribution**: Size and frequency of wins vs losses
- **Holding Periods**: How long positions are held
- **Seasonality**: Performance by month, day, or time
- **Market Regime**: Performance in different market conditions

### Benchmarking

#### Market Comparison
- Compare to buy-and-hold SPY
- Risk-adjusted performance (Sharpe ratio)
- Maximum drawdown comparison
- Volatility comparison

#### Peer Comparison
- Compare to other similar strategies
- Risk profile comparisons
- Performance attribution
- Relative rankings

### Statistical Significance

#### Confidence Intervals
- Performance range estimates
- Statistical significance of outperformance
- Monte Carlo simulation results
- Bootstrap analysis

#### Robustness Testing
- Parameter sensitivity analysis
- Time period stability
- Market regime analysis
- Out-of-sample validation

## Signals and Monitoring

### Live Signal Generation

#### Signal Components
- **Direction**: Long, short, or neutral
- **Confidence**: Model conviction (0-100%)
- **Expected Return**: Predicted profit target
- **Risk**: Expected loss if wrong
- **Duration**: Expected holding period

#### Signal Validation
- **Real-time Checks**: Ensure signal quality
- **Market Condition Filters**: Skip unfavorable conditions
- **Risk Limit Checks**: Ensure position limits not exceeded
- **Correlation Analysis**: Avoid over-concentration

### Performance Monitoring

#### Real-time Metrics
- **Live P&L**: Current profit/loss
- **Drawdown**: Current decline from peak
- **Hit Rate**: Percentage of winning trades
- **Average Return**: Mean profit per closed trade

#### Signal Analytics
- **Entry Analysis**: How well entry timing performs
- **Exit Analysis**: Effectiveness of exit rules
- **Slippage**: Difference between expected and actual fills
- **Attribution**: Which components drive performance

### Alert System

#### Performance Alerts
- Significant drawdown events
- Exceptional performance periods
- New equity highs or lows
- Risk limit breaches

#### System Alerts
- Data feed issues
- Model calculation errors
- Broker connectivity problems
- Risk system failures

## Advanced Features

### Sweeps (Batch Testing)

#### Configuration Grids
- Test multiple thresholds simultaneously
- Vary risk parameters systematically
- Compare different time horizons
- Evaluate robustness across settings

#### Results Analysis
- **Heatmaps**: Visual parameter sensitivity
- **Pareto Frontier**: Risk/return tradeoffs
- **Stability**: Consistency across parameters
- **Selection**: Choose optimal configurations

### Leaderboard

#### Model Comparison
- Rank models by performance metrics
- Filter by pack, risk profile, or time period
- Compare similar strategies
- Identify top performers

#### Selection Cart
- Collect multiple promising configurations
- Batch operations (training, monitoring)
- Portfolio-level analysis
- Diversification optimization

### Custom Indicators

#### Indicator Builder (Advanced Users)
- Create custom technical indicators
- Combine existing indicators mathematically
- Market microstructure indicators
- Alternative data integration

#### Validation and Testing
- Statistical properties validation
- Predictive power analysis
- Correlation with existing indicators
- Performance attribution

## Best Practices

### Model Development

#### Start Simple
1. Use template models initially
2. Understand basic concepts before customizing
3. Focus on one strategy pack at a time
4. Master risk management first

#### Iterative Improvement
1. Test small changes systematically
2. Keep detailed records of what works
3. Use sweeps to validate improvements
4. Focus on risk-adjusted returns, not just returns

#### Avoid Common Pitfalls
1. **Overfitting**: Don't optimize too much on historical data
2. **Look-ahead Bias**: Don't use future information
3. **Data Mining**: Don't try endless combinations without theory
4. **Survivorship Bias**: Include delisted stocks in backtests

### Risk Management

#### Position Sizing Rules
1. Never risk more than 1-2% per trade (conservative)
2. Limit total portfolio risk to 10-15% drawdown
3. Diversify across uncorrelated strategies
4. Use stop losses consistently

#### Monitoring and Adjustment
1. Review performance weekly, not daily
2. Allow sufficient time for strategies to work (6+ months)
3. Adjust position sizes based on performance
4. Have exit criteria for underperforming models

### Operational Excellence

#### Record Keeping
1. Document all model changes and rationale
2. Track performance attribution by component
3. Maintain notes on market conditions during trades
4. Regular performance reviews and analysis

#### Continuous Learning
1. Study both winning and losing trades
2. Analyze performance by market regime
3. Stay updated on market structure changes
4. Learn from other users' approaches

### Psychology and Discipline

#### Emotional Management
1. Follow your models' signals consistently
2. Don't override systems based on hunches
3. Prepare mentally for inevitable drawdown periods
4. Maintain long-term perspective

#### System Trust
1. Paper trade new models thoroughly
2. Start with small position sizes
3. Gradually increase size as confidence builds
4. Have objective criteria for stopping strategies

## Troubleshooting

### Common Issues

#### Poor Backtest Performance
- **Check data quality**: Ensure sufficient, clean data
- **Verify time periods**: Avoid unusual market periods
- **Review indicators**: Make sure they make economic sense
- **Consider transaction costs**: Are they realistic?

#### Inconsistent Results
- **Parameter sensitivity**: Use sweeps to check robustness
- **Market regime changes**: Test across different periods
- **Look-ahead bias**: Verify no future data usage
- **Random variation**: Consider statistical significance

#### System Performance
- **Slow calculations**: Check data size and complexity
- **Memory issues**: Reduce date ranges or indicator count
- **Connection problems**: Verify network and API status
- **Browser issues**: Try different browsers or clear cache

### Getting Help

#### Self-Service Resources
1. **Built-in Help**: Tooltips and contextual help
2. **AI Assistant**: Ask questions about any feature
3. **Documentation**: Comprehensive guides and references
4. **Video Tutorials**: Step-by-step walkthroughs

#### Support Options
1. **Knowledge Base**: Searchable FAQ and how-to articles
2. **Community Forum**: User discussions and shared strategies
3. **Direct Support**: Email or chat for technical issues
4. **Training Sessions**: Live demonstrations and Q&A

---

This user guide provides comprehensive coverage of Sigmatiq's features. For specific technical details, see individual product documentation in the `/products` directory.