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
- `/indicator_sets/auto_build`, `/strategies/auto_build` for features.
- `/screen/auto`, `/indicator_sets/auto_screen`, `/strategies/auto_screen` for rule cohorts.
 - Pack consensus: load `sc.v_model_packs_published` + `sc.model_pack_components` for pack definition.
