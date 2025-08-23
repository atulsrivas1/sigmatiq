# Requirements — Alerts AI (Novice-First)

## Product Outcomes
- Generate BUY/SELL alerts with plain-language summaries (no jargon) and a suggested position plan.
- Plan fields: Stop-Loss %, Take-Profit %, Max Hold (bars/time), Confidence band/signal strength.
- Coverage: stocks first; simple options path via ATM proxy (min DTE, delta target) with conservative defaults.
- Safety: per-user alert quotas, symbol diversity, one-tap mute/snooze, preview before subscribe.

## Non-Goals (MVP)
- No auto-execution or brokerage integration.
- No complex options strategies beyond a single-leg ATM proxy.
- No parameter soup — users pick preset/watchlist and timeframe only.

## Inputs & Features
- Use curated indicator sets as primary features (via FeatureBuilder/select_features()).
- Context extras: regime flags (volatility, trend), session context, ATR.
- Parity: same sets/flags used offline and online via Polygon loaders and auto_build endpoints.

## Labels & Targets
- Stock path: TP/SL-within-max-hold → positive if TP hit before SL within H bars.
- Options proxy path: TP/SL on ATM option premium estimate or normalized return.
- Multi-horizon per timeframe (e.g., daily H=5, hourly H=24, 5m H=36), configurable.

## Models
- Baseline: gradient-boosted trees (XGBoost) to predict probability of TP-before-SL.
- Score → Decision: calibrated score mapped to BUY/SELL/HOLD with thresholds meeting alert budgets.
- Plan: SL/TP in ATR or %, max-hold bars, sizing_hint; regime-aware bends.
- Reasons: top 2–3 simplified feature contributions for explanations (LLM templates consume).

## Safety & Guardrails
- Alert quotas per-user per-timeframe (e.g., 5/day baseline, hourly opt-in).
- Position caps: default small % of notional; options capped to small contract counts; min DTE.
- Universe caps: enforce recipe/preset guardrails (`universe_cap`).
- Compliance: educational framing, clear disclaimers, easy opt-out.
- Event throttle: reduce/suspend during extreme regimes unless opted-in.

## Model Registry (DB + Config)
- Registry: `sc.model_specs` (id, version, status, target_kind/id/version, timeframe, market, instrument).
- Config JSONB validated by Pydantic (dev side):
  - `featureset`: { set_id+version | strategy_id+version | indicators[] (synthetic) } + extra_flags.
  - `label_cfg`: { horizon_bars, tp_pct, sl_pct, max_hold_bars, options_proxy? }.
  - `thresholds`: { buy_min_score, sell_min_score, hold_band, budgets, diversity }.
  - `guardrails`: { exposure_caps, regime_bends, options }.
  - `artifacts`: { model_uri, calibration_uri, git_sha }.
  - `plan_template` (optional): { stop_atr, tp_atr, max_hold_bars, sizing_hint }.
- View: `sc.v_model_specs_published` (latest published per model_id).
 - Novice fields on registry rows (DB columns):
   - `novice_ready` (bool), `beginner_summary` (text),
   - `simple_defaults` (JSONB: e.g., operation/timeframe/cap),
   - `explainer_templates` (JSONB: summary/why/how_to_check templates; may include *_alt variants),
   - `risk_notes` (JSONB: regime/event caveats).
   - `assistant_hints` (JSONB): tips/cautions for the AI assistant (e.g., { tips:[], cautions:[] }).
 - Taxonomy fields (DB columns) to classify models:
   - `horizon`: one of `0dte|intraday|swing|position|long_term`.
   - `style`: one of `momentum|mean_reversion|trend_follow|breakout|volatility|carry|stat_arb`.
   - `tags`: free-form string array to refine discovery (e.g., `['buy_the_dip','large_cap']`).
   - `instrument_profile` (JSONB): e.g., `{ dte_band:'0dte'|'short'|'mid'|'long', delta_target:0.5, legs:'single' }`.
   - `suitability` (JSONB): e.g., `{ preferred_regimes:['trending'], avoid:['high_event_risk'] }`.

## Recipes & Workflows Interop
- Models can bind to recipe cohorts (target_kind=recipe) to inherit universe/timeframe/guardrails.
- Recipes/workflows can invoke models:
  - Recipes: use model_id in run to score cohort instead of rule filter.
  - Workflows: new step kind `model` → resolve universe → auto_build → score → filter/sort.

## APIs & Integration
- Feature compute at inference: `/indicator_sets/auto_build` or `/strategies/auto_build`.
- Screening fallback: `/indicator_sets/auto_screen` (rule-only cohorts).
- New alert APIs (to add):
  - `POST /alerts/preview` — resolve cohort, score via model_id, return top-K with plan, enforce budgets/diversity.
  - `POST /alerts/subscribe` — save user prefs; quotas/guardrails server-side.
  - `GET /alerts/feed` — recent alerts, outcomes; dismiss/mute endpoints.

## Deliverables (MVP)
- 2–3 recipe-backed models (RSI Oversold, MACD Trend Pullback, Keltner Break Alignment).
- Calibrated thresholds to meet budgets with precision@K targets.
- LLM explainer templates for plain-language reasons and plan recap.
- Monitoring: precision@K, alert volume, dismiss/open rate, plan hit rate.
 - Backtests: one-off backtest, model sweep, and pack consensus sweep with novice guardrails (90‑day window, universe caps).
 - Leaderboard: persisted backtest runs with plain‑language summaries; filterable by pack, model, tag.
 - Simple mode: one-tap backtests defaulting to curated sweep presets (e.g., RTH thresholds) to avoid parameter soup.

## Dataset Building (Cohort‑First, Reproducible)
- Cohort default: train per timeframe/market on preset universes (e.g., `sp500` daily/hourly, `liquid_etfs` 5m). Per‑ticker only for justified microstructure (e.g., SPY 0DTE) declared in `scope`.
- Bars & caching: use Polygon loaders with file cache; never cache “today”. Prefer adjusted=true for daily (record choice in `training_cfg`).
- Features: reuse serving sets/strategies via FeatureBuilder; add ATR, regime flags, session context; drop last H rows to prevent leakage.
- Labels: TP‑before‑SL within `max_hold_bars`; record outcome (`tp_hit|sl_hit|max_hold`) and realized return; optional ATM options proxy labels.
- Splits: forward‑chaining CV grouped by symbol; record `fold` and `cv` policy in `training_cfg`.
- Storage: Parquet partitioned by timeframe/date; record dataset/feature hashes in `sc.model_training_runs`.
 - Branding (DB columns):
   - `brand`: namespace/owner, default `'sigmatiq'`.
   - `display_name`: user-facing, plain-language name.
   - Naming convention for `model_id`: snake_case with brand prefix `sq_` (Sigmatiq), e.g., `sq_macd_trend_pullback_5m`. Use `display_name` for UI (e.g., “Sigmatiq MACD Trend Pullback (5m)”). Minor revisions tracked in `version`; major identity changes may add `_vN` to `model_id`.
 - Training configuration & runs:
   - `training_cfg` (JSONB on sc.model_specs): defines reproducible train-time settings (data windows, session hours, CV, filters, event blacklists, liquidity thresholds).
   - `sc.model_training_runs`: records lineage and summary metrics per training run (cfg snapshot, hashes, metrics, status, timing).
 - Scope (DB column):
   - `scope` JSONB: declare targeting domain, defaults to cohort models.
     - Cohort example: `{ type:'cohort', allow_presets:['sp500','liquid_etfs'], sector_filters:['tech','large_cap'] }`.
     - Per‑ticker example: `{ type:'per_ticker', allow_symbols:['SPY','QQQ'] }`.
   - Purpose: enables simple filtering/routing and discoverability without encoding scope into `model_id`.
