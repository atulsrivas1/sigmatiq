# Dev Whiteboarding Transcript — Extensible Alerts AI

Dev1: Let’s define core interfaces so we can plug markets/instruments later without changing business logic.
- FeatureSource: builds last-row features given {symbol, timeframe, market}. Backed by `/indicator_sets/auto_build` or strategy variant; can swap provider adapters.
- Labeler: computes training labels for {symbol, timeframe, horizon, plan_spec}. Stock and options labelers implement the same interface.
- ModelSpec: defines model type, featureset, label config, calibration method, thresholds, and guardrails.
- Scorer: loads a ModelSpec version, takes features, returns {decision, score, plan, reasons}.
- PlanGenerator: maps score + context to {stop_pct, take_profit_pct, max_hold_bars, sizing_hint}. Can be strategy/recipe aware.

Dev2: Extensibility:
- Market adapters: polygon_us, polygon_eu (future), csv_backfill; common schema {timestamp, ohlcv, currency, tz}.
- Instrument adapters: equities, etfs, options (ATM proxy), fx. Each provides Labeler + PlanGenerator knobs.
- Regime adapters: compute regime flags (volatility, trend, liquidity) and influence thresholds/sizing.

Dev3: Labeling strategy:
- TP-before-SL within max_hold for stock; options proxy via ATM premium estimate.
- Multi-horizon configs per timeframe; class balance via downsampling or focal loss if needed.
- Calibration to alert budgets per timeframe + regime, with minimum precision@K.

Dev1: Data parity:
- Offline feature compute reuses the same sets/FeatureBuilder as online via our API or local library to avoid skew.
- Historical caching added for daily/minute; never cache today — consistent online.

Dev2: Serving path:
- Scoring service calls FeatureSource, then Scorer → PlanGenerator → LLM explainer.
- Quotas + guardrails middleware enforce per-user budgets, diversity, and exposure caps before delivery.
- Storage: alerts table with inputs/outputs, plan, reasons, and outcome fields.

Dev3: Monitoring:
- Precision@K per timeframe, plan hit rates (TP vs SL), drift on features and calibration.
- A/B: threshold variants per cohort with guardrails.

Dev1: Multi-country:
- Expand Market enum and provider adapter; currency normalization; holiday/calendar service per market.
- Watch out for timezone conversions; FeatureSource returns tz-aware timestamps.

Dev2: Testing:
- Golden tests for FeatureSource on sample symbols; stochastic tests for Scorer calibration; contract tests for adapters.

Dev3: Next steps:
- Deliver System Design doc, interfaces in Python, and a stub service that scores top-10 from a preset.
