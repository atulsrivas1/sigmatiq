# Strategy Pack Pipeline Mapping

## BTB Pipeline Integration Checklist

Each strategy pack follows the standard Build → Train → Backtest pipeline with pack-specific customizations.

### 1. EarnPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_earnings_calendar.py`
  - Input: Ticker list, date range
  - Output: `data/earnings/calendar.csv`
- **Script**: `scripts/data/fetch_iv_surface.py`
  - Input: Options chains for earnings tickers
  - Output: `data/options/iv_surface.parquet`

#### Features Phase
- **Notebook**: `notebooks/features/earnpack_features.ipynb`
  - Input: Price data, earnings calendar, IV data
  - Output: `matrices/earnpack_features.csv`
- Key features: IV rank, earnings drift, volume surge

#### Template Phase
- **Config**: `packs/earnpack/templates/quarterly.yaml`
- **Validation**: `scripts/validate/check_earnpack_template.py`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_earnpack_sweep.py`
  - Input: Feature matrix, template config
  - Output: `sweeps/earnpack_results.json`
- Parameter grid: IV thresholds, days before earnings, position sizing

#### Train Phase
- **Script**: `scripts/train/train_earnpack_model.py`
  - Input: Best sweep configs, feature matrix
  - Output: `models/earnpack_xgboost.pkl`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_earnpack.py`
  - Input: Trained model, test data
  - Output: `reports/earnpack_backtest.html`

#### Gates Phase
- **Validation**: `scripts/gates/validate_earnpack.py`
- Checks: Min 20 trades, max 30% drawdown, Sharpe > 0.6

#### Publish Phase
- **Script**: `scripts/publish/deploy_earnpack.py`
- Version: `earnpack_v0.1.0`
- Release notes: Initial earnings volatility strategy

---

### 2. TrendPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_trend_universe.py`
  - Input: Futures, ETFs, large-caps
  - Output: `data/trend/universe.csv`

#### Features Phase
- **Notebook**: `notebooks/features/trendpack_features.ipynb`
  - Input: OHLCV, volume profile
  - Output: `matrices/trendpack_features.csv`
- Key features: EMA ribbon, ADX, MACD, trend strength

#### Template Phase
- **Config**: `packs/trendpack/templates/momentum.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_trendpack_sweep.py`
- Parameter grid: ADX thresholds, ribbon periods, stop loss levels

#### Train Phase
- **Script**: `scripts/train/train_trendpack_model.py`
- Algorithm: XGBoost with trend-specific features

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_trendpack.py`
- Metrics: Trend capture ratio, whipsaw frequency

#### Gates Phase
- Checks: Min 30 trades, max 25% drawdown, Sharpe > 1.0

#### Publish Phase
- Version: `trendpack_v0.1.0`

---

### 3. VolPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_vix_term_structure.py`
  - Input: VIX futures chain
  - Output: `data/volatility/term_structure.csv`
- **Script**: `scripts/data/fetch_options_metrics.py`
  - Input: SPX options
  - Output: `data/volatility/options_metrics.parquet`

#### Features Phase
- **Notebook**: `notebooks/features/volpack_features.ipynb`
- Key features: Contango, RV/IV spread, VVIX, term structure

#### Template Phase
- **Config**: `packs/volpack/templates/regime.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_volpack_sweep.py`
- Parameter grid: VIX percentiles, contango thresholds

#### Train Phase
- **Script**: `scripts/train/train_volpack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_volpack.py`

#### Gates Phase
- Checks: Min 25 trades, max 35% drawdown, Sharpe > 0.5

#### Publish Phase
- Version: `volpack_v0.1.0`

---

### 4. PairPack Pipeline

#### Data Phase
- **Script**: `scripts/data/find_pairs.py`
  - Input: Universe of stocks
  - Output: `data/pairs/cointegrated_pairs.csv`

#### Features Phase
- **Notebook**: `notebooks/features/pairpack_features.ipynb`
- Key features: Correlation, cointegration, z-score, half-life

#### Template Phase
- **Config**: `packs/pairpack/templates/stat_arb.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_pairpack_sweep.py`
- Parameter grid: Z-score thresholds, correlation minimums

#### Train Phase
- **Script**: `scripts/train/train_pairpack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_pairpack.py`

#### Gates Phase
- Checks: Min 40 trades, max 20% drawdown, Sharpe > 1.2

#### Publish Phase
- Version: `pairpack_v0.1.0`

---

### 5. MicroPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_tick_data.py`
  - Input: Exchange direct feed
  - Output: `data/microstructure/ticks.parquet`
- **Script**: `scripts/data/fetch_order_book.py`
  - Input: Level 2 data
  - Output: `data/microstructure/book_snapshots.parquet`

#### Features Phase
- **Notebook**: `notebooks/features/micropack_features.ipynb`
- Key features: Book imbalance, order flow, microprice, VPIN

#### Template Phase
- **Config**: `packs/micropack/templates/hft.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_micropack_sweep.py`
- Parameter grid: Tick targets, hold times, book imbalance

#### Train Phase
- **Script**: `scripts/train/train_micropack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_micropack.py`
- Special: Tick-by-tick simulation

#### Gates Phase
- Checks: Min 100 trades, max 10% drawdown, Sharpe > 2.5

#### Publish Phase
- Version: `micropack_v0.1.0`

---

### 6. SeasonPack Pipeline

#### Data Phase
- **Script**: `scripts/data/build_seasonal_database.py`
  - Input: 15 years historical data
  - Output: `data/seasonal/patterns.csv`

#### Features Phase
- **Notebook**: `notebooks/features/seasonpack_features.ipynb`
- Key features: Seasonal averages, win rates, analog years

#### Template Phase
- **Config**: `packs/seasonpack/templates/calendar.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_seasonpack_sweep.py`
- Parameter grid: Entry timing, consistency thresholds

#### Train Phase
- **Script**: `scripts/train/train_seasonpack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_seasonpack.py`

#### Gates Phase
- Checks: Min 12 trades, max 20% drawdown, Sharpe > 0.8

#### Publish Phase
- Version: `seasonpack_v0.1.0`

---

### 7. CryptoPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_onchain_metrics.py`
  - Input: Glassnode API
  - Output: `data/crypto/onchain.csv`
- **Script**: `scripts/data/fetch_defi_tvl.py`
  - Input: DeFiLlama API
  - Output: `data/crypto/defi_metrics.csv`

#### Features Phase
- **Notebook**: `notebooks/features/cryptopack_features.ipynb`
- Key features: NVT, exchange flows, funding rates, whale activity

#### Template Phase
- **Config**: `packs/cryptopack/templates/onchain.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_cryptopack_sweep.py`
- Parameter grid: On-chain thresholds, sentiment scores

#### Train Phase
- **Script**: `scripts/train/train_cryptopack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_cryptopack.py`

#### Gates Phase
- Checks: Min 30 trades, max 40% drawdown, Sharpe > 0.8

#### Publish Phase
- Version: `cryptopack_v0.1.0`

---

### 8. DividPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_dividend_calendar.py`
  - Input: Dividend aristocrats list
  - Output: `data/dividends/calendar.csv`

#### Features Phase
- **Notebook**: `notebooks/features/dividpack_features.ipynb`
- Key features: Yield, payout ratio, option premium, coverage

#### Template Phase
- **Config**: `packs/dividpack/templates/enhanced.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_dividpack_sweep.py`
- Parameter grid: Yield thresholds, days to ex-div

#### Train Phase
- **Script**: `scripts/train/train_dividpack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_dividpack.py`

#### Gates Phase
- Checks: Min 20 trades, max 15% drawdown, Sharpe > 1.0

#### Publish Phase
- Version: `dividpack_v0.1.0`

---

### 9. EventPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_event_calendar.py`
  - Input: FDA calendar, M&A database
  - Output: `data/events/calendar.csv`

#### Features Phase
- **Notebook**: `notebooks/features/eventpack_features.ipynb`
- Key features: Event proximity, option skew, historical reactions

#### Template Phase
- **Config**: `packs/eventpack/templates/catalyst.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_eventpack_sweep.py`
- Parameter grid: Days before event, hedge ratios

#### Train Phase
- **Script**: `scripts/train/train_eventpack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_eventpack.py`

#### Gates Phase
- Checks: Min 15 trades, max 40% drawdown, Sharpe > 0.4

#### Publish Phase
- Version: `eventpack_v0.1.0`

---

### 10. RebalPack Pipeline

#### Data Phase
- **Script**: `scripts/data/fetch_index_changes.py`
  - Input: Russell reconstitution list
  - Output: `data/rebalance/changes.csv`

#### Features Phase
- **Notebook**: `notebooks/features/rebalpack_features.ipynb`
- Key features: Weight changes, ETF flows, inclusion probability

#### Template Phase
- **Config**: `packs/rebalpack/templates/index.yaml`

#### Sweeps Phase
- **Script**: `scripts/sweeps/run_rebalpack_sweep.py`
- Parameter grid: Days early, probability thresholds

#### Train Phase
- **Script**: `scripts/train/train_rebalpack_model.py`

#### Backtest Phase
- **Script**: `scripts/backtest/backtest_rebalpack.py`

#### Gates Phase
- Checks: Min 20 trades, max 15% drawdown, Sharpe > 1.2

#### Publish Phase
- Version: `rebalpack_v0.1.0`

---

## Common Pipeline Components

### Shared Scripts
- `scripts/common/load_template.py` - Template loader
- `scripts/common/validate_indicators.py` - Indicator validation
- `scripts/common/compute_metrics.py` - Performance metrics
- `scripts/common/apply_gates.py` - Gate validation
- `scripts/common/generate_report.py` - HTML/PDF reports

### Shared Notebooks
- `notebooks/common/eda_template.ipynb` - Exploratory data analysis
- `notebooks/common/feature_importance.ipynb` - Feature ranking
- `notebooks/common/backtest_analysis.ipynb` - Result analysis

### CI/CD Pipeline
```yaml
# .github/workflows/pack_validation.yml
name: Pack Validation
on:
  push:
    paths:
      - 'packs/**'
      - 'scripts/**'
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Templates
        run: python scripts/validate/check_all_templates.py
      - name: Run Unit Tests
        run: pytest tests/packs/
      - name: Check Gate Compliance
        run: python scripts/gates/validate_all_packs.py
```

## Deployment Checklist

- [ ] Data sources connected and validated
- [ ] Feature engineering pipeline tested
- [ ] Template YAML validated
- [ ] Sweeps completed with sufficient samples
- [ ] Training converged with good metrics
- [ ] Backtest passed all gates
- [ ] Risk limits configured
- [ ] Documentation updated
- [ ] Version tagged and released
- [ ] Monitoring dashboards configured