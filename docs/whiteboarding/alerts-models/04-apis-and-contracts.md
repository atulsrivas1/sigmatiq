# APIs & Contracts — Alerts AI

## Model Scoring Service (internal)
- Input: { symbol, timeframe, market, instrument, features (latest row), context }
- Output: {
  decision: "buy"|"sell"|"hold",
  score: float (0..1),
  plan: { stop_pct, take_profit_pct, max_hold_bars, sizing_hint },
  reasons: [short strings],
  kind: "stock"|"option", option_hint?: { type: "call"|"put", dte_min, delta_target }
}

## Public API (to add)
- `POST /alerts/preview`:
  - Request: { model_id (or target_kind+id) OR pack_id, preset_id|watchlist_id, timeframe?, market?, instrument?, cap? }
  - Response: { run_id, evaluated, matched: [{ symbol, decision, score, plan, reasons }], pack_consensus?: { matched_models, policy } }
  - Behavior: resolves cohort, fetches features, if pack_id → score all models in the pack and apply consensus policy (majority/weighted/all, min_quorum, thresholds) to emit final BUY/SELL/HOLD; enforces budgets/diversity.
- `POST /alerts/subscribe`: { target_kind/id/version or model_id/version, timeframe, preset_id|watchlist_id, budgets, channels }
- `GET /alerts/feed`: { timeframe?, page? } → list with decision/plan/status/outcomes; also POST `/alerts/{id}/dismiss`, `/alerts/{id}/mute`.

## Recipes/Workflows Integration
- `/recipes/run`: accept `{ model_id | use_model:true }` to score instead of rule filter.
- `/workflows/run`: new step `{ kind:"model", model_id, version?, top_k?, min_score?, timeframe?, preset_id|watchlist_id? }`.

## Sigma Core touchpoints
- Features and screening
  - `/indicator_sets/auto_build`, `/strategies/auto_build` for features.
  - `/screen/auto`, `/indicator_sets/auto_screen`, `/strategies/auto_screen` for rule cohorts.
- Backtests and datasets (implemented)
  - `POST /models/dataset/build` — builds CSV/Parquet datasets for training/backtests; records `sc.model_training_runs`.
  - `POST /backtest/run` — backtest a feature set over a universe; supports `mode: simple` (auto‑uses `rth_thresholds_basic`). In simple mode, responses include `metrics_explained`. Pass `?fields=full` to include `metrics_explained` in advanced mode.
  - `POST /models/{model_id}/backtest/sweep` — grid‑search thresholds/top_pct; persists best; supports `mode: simple` and `sweep_preset_id`. In simple mode, responses include `metrics_explained`. Pass `?fields=full` to include `metrics_explained` in advanced mode.
  - `POST /packs/{pack_id}/backtest/run` — consensus backtest for a model pack; supports `consensus_override` and `mode: simple`. In simple mode, responses include `metrics_explained`. Pass `?fields=full` to include `metrics_explained` in advanced mode.
  - `POST /packs/{pack_id}/backtest/sweep` — grid‑search consensus; supports `consensus_override`. In simple mode, responses include `metrics_explained`. Pass `?fields=full` to include `metrics_explained` in advanced mode.
  - `GET /backtests/leaderboard` — filter by `pack_id|model_id|tag|timeframe`; returns plain-language `summary`.
  - Pass `?fields=full` to include `metrics_explained` (plain definitions for Sharpe, trades, etc.).

List Endpoint Parity
- Most list endpoints accept `fields=full` (Catalog, Presets, Recipes, Leaderboard). Extras are included where applicable (e.g., `metrics_explained` on leaderboard and backtests); for others it is reserved for parity.
- Persistence (DB)
  - Runs: `sc.model_backtest_runs`, folds: `sc.model_backtest_folds` (pack_id, metrics, best_config, summary).
  - Presets: `sc.backtest_sweep_presets` — reusable grids/guardrails (e.g., `rth_thresholds_basic`).
  - Packs: `sc.model_packs`, `sc.model_pack_components` (weights, consensus policy).

Examples (concise)
- Backtest (simple mode):
  - `POST /backtest/run` body: `{ "timeframe":"hour", "universe": {"preset_id":"liquid_etfs","cap":10}, "features": {"set_id":"macd_trend_pullback_v1","version":1}, "label": {"kind":"hourly_direction","params":{"k_sigma":0.3}}, "mode":"simple" }`
- Pack backtest with majority override:
  - `POST /packs/consensus_v1/backtest/run` body: `{ "timeframe":"hour", "universe": {"preset_id":"liquid_etfs","cap":10}, "thresholds":[0.55,0.6,0.65], "consensus_override": {"policy":"majority","min_quorum":1.5,"min_score":0.6} }`

Metrics Explained (example)
```json
{
  "metrics_explained": {
    "avg_sharpe_hourly": "Steadiness of gains per hour (higher is steadier).",
    "trades_total": "Total number of trades across all folds.",
    "cum_ret_sum": "Total return across all folds (no compounding)."
  }
}
```
