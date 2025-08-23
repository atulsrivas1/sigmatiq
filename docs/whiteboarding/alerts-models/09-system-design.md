# System Design — Extensible Alerts AI

## 1. Architecture Overview
- Offline (training): Data adapters → Feature pipelines (FeatureBuilder) → Labelers → Train & calibrate → Register ModelSpec vN (DB: sc.model_specs).
- Online (serving): FeatureSource (auto_build) → Scorer(ModelSpec) → PlanGenerator → LLM Explainer → Guardrails → Deliver alert (DB: runs/alerts/delivery/outcomes).

## 2. Core Interfaces (Python-ish)
- FeatureSource.fetch(symbol, timeframe, market, set_id|strategy_id) → Dict[str, float]
- Labeler.build(symbol, timeframe, horizon, plan_spec) → label {0/1, meta}
- ModelSpec: {id, version, featureset, label_cfg, model_uri, thresholds, guardrails}
- Scorer.score(features, context) → {decision, score, reasons}
- PlanGenerator.make(decision, score, context) → {stop_pct, take_profit_pct, max_hold_bars, sizing_hint}

## 3. Extensibility Points
- MarketAdapter: timezone, currency, calendars, data provider routing.
- InstrumentAdapter: equities|etfs|options|fx; owns Labeler + PlanGenerator nuances.
- RegimeAdapter: regime flags + threshold bending (conservative in high vol).
- FeatureSet: binds to indicator_set or strategy IDs; synthetic indicator lists allowed via featureset.indicators[].

## 4. Data & Pipelines
- Reuse Sigma Core: `/indicator_sets/auto_build` (or strategy) to compute features; Polygon cached loaders for offline.
- Never cache today to avoid stale live data; ensure tz-aware indices.
- Cohort runners resolve universes via presets/watchlists.

## 5. Serving & APIs
- Internal Scoring Service: gRPC/HTTP endpoint `POST /score` with batch support; stateless; model registry on disk/S3.
- Public APIs to add: `/alerts/preview`, `/alerts/subscribe`, `/alerts/feed`; extend `/recipes/run` and `/workflows/run` to use models.
- Observability: metrics for precision@K, alert volume, throttling, latency.

## 6. Storage
- Model registry: sc.model_specs (+ view sc.v_model_specs_published), artifacts in object store.
- Alerts: sc.alert_runs, sc.alerts, sc.alert_delivery, sc.alert_outcomes; sc.alert_subscriptions; sc.user_alert_settings.
- Model packs: sc.model_packs (+ view sc.v_model_packs_published), sc.model_pack_components; pack refs on runs/alerts for lineage.
- Cohort vs Per‑Ticker targeting: `sc.model_specs.scope` JSONB records targeting domain (allow_presets/allow_symbols/filters).
 - Training: `sc.model_specs.training_cfg` holds reproducible settings; `sc.model_training_runs` captures training lineage + metrics.

## 7. Safety & Guardrails
- Per-user budgets; diversity constraints; cooldown windows per symbol.
- Exposure caps; options DTE min and max leverage hints.
- Phrasing policies in explainer layer; disclaimers always visible.

## 8. Rollout Plan
- Phase 1: daily + hourly, equities only, US market; /alerts/preview and workflow model step.
- Phase 2: options ATM proxy; EU/IN market adapters; recipe model binding; /alerts/subscribe/feed.
- Phase 3: personalized cohorts; A/B threshold tuning per regime; FX experimental.
