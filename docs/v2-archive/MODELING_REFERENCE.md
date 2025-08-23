# Modeling Reference (Concepts and Allowed Values)

This reference summarizes the main entities and parameters used to define models in Sigma Lab.

## Packs
- Location: `packs/<pack_id>`
- Contents:
  - `model_configs/`: model YAMLs with ticker, horizon, cadence, features, labels.
  - `indicator_sets/`: `<name>.yaml` listing indicators and params.
  - `policy_templates/`: `<model_id>.yaml` with execution policy knobs.
  - `model_templates/`: optional starter templates.

## Models
- Naming: `<ticker>_<asset>_<horizon>_<cadence>[_variant]`
  - asset: `opt|eq`
  - horizon: `0dte|intraday|swing|long`
  - cadence: `5m|15m|hourly|daily`
- Typical fields in `model_configs/<model_id>.yaml`:
  - `ticker`: e.g., `SPY`
  - `model`: e.g., `gbm`
  - `task`: e.g., `classification`
  - `hyperparams`: estimator hyperparameters
  - `features`: optional explicit list; otherwise auto‑selected
  - `label`: label spec (e.g., `next_bar_updown`, `horizon: 1`)
  - Optional feature flags by group (flow/dealer/oi/momentum/volatility)

## Policies (Execution)
- Effective fields (via `/policy/explain`):
  - `slippage_bps: float` – default 1.0
  - `size_by_conf: bool` – default false
  - `conf_cap: float` – default 1.0
  - Momentum gate:
    - `momentum_gate: bool` (default false)
    - `momentum_min: float` (default 0.0)
    - `momentum_column: str` (default `momentum_score_total`)
  - Brackets:
    - `enabled: bool`
    - `mode: str` (e.g., `atr`)
    - `entry_mode: str` (e.g., `next_session_open`)
    - `atr_period: int`
    - `atr_mult_stop: float`, `atr_mult_target: float`
    - `time_stop_minutes: int`
    - `min_rr: float`
    - `regime_adjust: bool`
- Options selection (for `asset=opt`):
    - `target_delta: float (0,1)`
    - `dte_target: int (>0)`
    - `min_oi: int (>=0)`
    - `min_vol: float (~0–5)`
    - `spread_width: float`
    - `weekly_ok: bool`

### Appendix: Policy Examples (Recommended Defaults)

Options (0DTE intraday, momentum-gated with ATR brackets)

```yaml
execution:
  slippage_bps: 1.0
  size_by_conf: true
  conf_cap: 1.0
  momentum_gate: true
  momentum_min: 0.0
  momentum_column: momentum_score_total
  brackets:
    enabled: true
    mode: atr
    entry_mode: next_session_open
    atr_period: 14
    atr_mult_stop: 1.2
    atr_mult_target: 2.0
    time_stop_minutes: 120
    min_rr: 1.0
    regime_adjust: false
  options:
    selection:
      target_delta: 0.35
      dte_target: 0        # 0DTE focus (same-day expiry); use 1–7 for weeklys
      min_oi: 200          # liquidity floor; raise for SPY/QQQ
      min_vol: 0.0         # 0–5 (~0–500%)
      spread_width: 5.0
      weekly_ok: true
```

Equities (hourly momentum with ATR brackets)

```yaml
execution:
  slippage_bps: 1.0
  size_by_conf: true
  conf_cap: 1.0
  momentum_gate: true
  momentum_min: 0.0
  momentum_column: momentum_score_total
  brackets:
    enabled: true
    mode: atr
    entry_mode: next_session_open
    atr_period: 14
    atr_mult_stop: 1.5
    atr_mult_target: 3.0
    time_stop_minutes: 240   # longer hold window for equities
    min_rr: 1.0
    regime_adjust: false
```

Notes
- Tune ATR multipliers per ticker/volatility regime; aim for positive RR and manageable time‑in‑market.
- Momentum gate helps avoid low‑signal hours; set `momentum_min` via sweeps/leaderboard.
- For options, enforce liquidity via `min_oi` and adjust `target_delta` per your risk appetite.

## Indicators and Features
- Indicators: see `sigma_core/indicators/builtins` for a large set (RSI, EMA, ATR, MACD, momentum_score, IV metrics, Bollinger, etc.).
- List via API: `make indicators` (flat) or `make indicators-groups` (grouped).
- Features: columns selected from the built matrix by `sigma_core.features.builder` or explicitly via `model_configs`.

## Build (Matrix)
- API: `POST /build_matrix`
- Required: `model_id`, `start`, `end` (ISO), optional `ticker`, `distance_max`, etc.
- Output: CSV under `products/sigma-lab/matrices/<model_id>/`
- DB: `build_runs` + `artifacts`

## Backtest
- API: `POST /backtest`
- Key params:
  - `thresholds: list|CSV` (e.g., `0.55,0.60,0.65`)
  - `splits: int` (e.g., `3|5`), `embargo: float`
  - `allowed_hours: list|CSV` (e.g., `13,14,15`)
  - `calibration: none|sigmoid|isotonic`
  - `momentum_gate: bool`, `momentum_min`, `momentum_column`
  - `top_pct: float` (mutually exclusive with thresholds)
- DB: `backtest_runs` + `backtest_folds` + `artifacts`
- Leaderboard: `GET /leaderboard`

## Sweeps
- API: `POST /backtest_sweep`
- Params: `thresholds_variants`, `allowed_hours_variants`, `top_pct_variants`, `splits`, `embargo`, `min_trades`, `min_sharpe`
- DB: `backtest_sweeps` + `sweep_results`
- Read: `GET /sweeps`, `GET /sweeps/{id}`

## Train
- API: `POST /train`
- Params: `model_id`, `allowed_hours`, `calibration`, optional `target`
- Output: model bundle under `products/sigma-lab/artifacts/<model_id>/`
- DB: `training_runs` + `artifacts`

## Leaderboard
- API: `GET /leaderboard?pack_id=&model_id=&limit=&offset=&order_by=sharpe|cum_ret`
- Displays best rows across backtests for a quick comparison.
