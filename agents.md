# Sigmatiq Agents Guide (Codex/LLM)

Guiding Principle — North Star
- Single, overriding goal: make trading simple for non‑traders with zero domain knowledge.
- Agent stance: be the constructive critic. Flag, push back on, or propose alternatives to any change that increases complexity, assumes trader expertise, or weakens safety-by-default.

Critic Gate (Mandatory)
- Every session (whiteboarding, design, PR review) must include a Critic pass before decisions are accepted.
- The Critic pass must explicitly document:
  - Risks to novice users (jargon, parameter soup, hidden state, non-reversible actions).
  - Safety gaps (missing quotas/guardrails/undo, unclear costs/risks).
  - Complexity increases (more steps, multi-screen flows) and simpler alternatives.
  - Plain-language confirmation of defaults, scope, and opt-out.
- If the Critic pass finds material issues, do not proceed; propose a simpler, safer alternative.
- Design rules for every decision
  - Plain language: no jargon or acronyms without inline explanations.
  - Safe defaults: conservative, reversible, and capped risk; opt‑in for anything advanced.
  - One-screen, one‑tap bias: minimize steps, hide advanced options behind “Advanced”.
  - Progressive disclosure: show details only when needed; provide examples and previews first.
  - Outcomes over indicators: lead with “what it means” before “how it’s computed”.
  - Teach as you go: micro‑tooltips and short “why it matters” blurbs.
  - Guardrails: quotas, sanity checks, undo/rollback, and clear confirmations.
- Quick checklist before accepting work
  - Does this reduce decisions and jargon for novices?
  - Can a first‑time user succeed in under 60 seconds?
  - Are defaults safe and clearly reversible with an obvious off switch?
  - Is there a simpler preset/story-driven path instead of parameter soup?
  - Are risks, costs, and delays explained in plain language up front?
  - Is there a preview or example output before committing?
- Anti‑patterns to block
  - Exposing raw technical parameters without presets or explanations.
  - Unbounded universes, unguarded automation, or risky defaults.
  - Multi‑step wizards where a single preset would suffice.
  - Metrics without context (e.g., Sharpe, AUC) shown to novices without translation.
  - Irreversible actions or hidden state changes.

Purpose
- Give future AI agents fast, accurate context to work effectively in this repo.
- Map docs ↔ code, call out contracts, and highlight safe workflows and pitfalls.

Quick Orientation
- Start with `docs/START_HERE.md` and `docs/Home.md` for overall platform context.
- Domain specs: `docs/indicators`, `docs/indicator_sets`, `docs/trading_strategies`, `docs/catalog`.
- Core code referenced by these docs lives in `products/sigma-core/`.

Key Concepts
- Indicators: Single-Indicator scope. Registry of compute classes that produce columns from market data frames. See `docs/indicators` for API, architecture, and use-cases.
- Indicator Sets: Collections of indicators + params treated as a unit for feature engineering. See `docs/indicator_sets` for set API/specs.
- Trading Strategies: Higher-level logic that consumes features and emits signals; see `docs/trading_strategies`.
- Catalog: Content models and AI-assistant-facing metadata for indicators/sets/strategies; see `docs/catalog`.

Sigma-Core Code Map
- `sigma_core/indicators`
  - `base.py`: `Indicator` ABC with `calculate(df) -> pd.DataFrame`.
  - `builtins/*.py`: 90+ packaged indicators (e.g., `rsi.py`, `macd.py`).
  - `registry.py`: Dynamic loader; registers classes from `builtins` into an in-process registry.
- `sigma_core/features`
  - `sets.py`: Pydantic models for `IndicatorSpec`, `IndicatorSet` (name, version, indicators[]).
  - `builder.py`: `FeatureBuilder` to compose features: base features + indicator features via registry + extras; `select_features()` defines model inputs.
- `sigma_core/registry`
  - `indicator_registry.py`: DB-backed registry for persisted indicator sets (CRUD). Uses `sigma_core.storage.relational`.
  - `artifacts.py`: Pydantic models for DB rows (indicator sets/specs, models, policies).
- `sigma_core/data`: Loaders and dataset helpers used by pipelines.
- `sigma_core/backtest/engine.py`: Cross-validated backtest harness using XGBoost; selects positions by threshold or top% confidence.
- `sigma_core/evaluation`: Metrics and reporting utilities.
- `sigma_core/live`: Runtime stubs for live trading (`runtime.py` is minimal).
- `sigma_core/services/lineage.py`: SHA lineage for packs/configs/indicator sets.
- `sigma_core/storage/relational.py`: Postgres connection pool (requires `psycopg2` + DB_* env vars).

Contracts & Data Shapes
- Indicator class
  - Extend `sigma_core.indicators.base.Indicator` and implement `calculate(df: pd.DataFrame) -> pd.DataFrame`.
  - Input df: time-indexed bars and/or options columns; common columns include `timestamp`, `open/high/low/close/volume`, plus domain-specific fields (see indicator docs).
  - Output df: one or more new columns, aligned to input index. Handle missing inputs defensively; many builtins output zeros if prerequisites are missing (see `builtins/rsi.py`).
- Naming guidance (from docs)
  - Prefer `snake_case`. Multi-output indicators append suffixes per output.
  - Keep stability across versions; breaking changes should bump an explicit `version` in metadata (tracked in docs/catalog and DB models).
- Feature selection
  - `FeatureBuilder.select_features()` enumerates prefixes used as ML inputs (e.g., `rsi_`, `macd_`, `bb_upper_`, `atr_`, `ema_`, options flow aggregates). Add new prefixes when introducing novel features.

Common Workflows
- Compute a single indicator in code
  - `from sigma_core.indicators.registry import get_indicator`
  - `cls = get_indicator("rsi"); out = cls(period=14).calculate(df)`
- Compose features from an indicator set
  - Build an `IndicatorSet` (Pydantic) and pass to `FeatureBuilder(indicator_set=...)`; call `add_indicator_features(df)`.
- Add a new builtin indicator
  - Create `products/sigma-core/sigma_core/indicators/builtins/<name>.py` defining a class extending `Indicator`.
  - Optional class attrs `CATEGORY`, `SUBCATEGORY`. The loader will infer a registry key from class name if `NAME` not provided.
  - Ensure robust handling of missing required columns and return a DataFrame with deterministic column names.
- Define/persist an indicator set (DB-backed)
  - Use `sigma_core.registry.indicator_registry.IndicatorRegistry.create_indicator_set(...)` to insert a set and its members (requires DB env vars and `psycopg2`).
  - List/fetch via `list_indicator_sets()`, `get_indicator_set(name, version)`.
- Seed the catalog (SQL generation)
  - Make targets in `products/sigma-core/Makefile` call scripts in `products/sigma-core/scripts/` to emit SQL seeds:
    - `gen-indicator-seed`, `gen-set-seed`, `gen-strategy-seed`, `gen-workflow-seed`.
  - Seeds pull from code (introspection) + `docs/catalog/overrides` and examples.

APIs (implemented; novice-first surface)
- Indicators (single)
  - `POST /indicators/validate`, `POST /indicators/compute`, `POST /screen`, `POST /screen/auto`.
- Indicator Sets
  - CRUD minimal (`POST /indicator_sets`, list/get, publish with guardrails check).
  - Feature build: `POST /indicator_sets/build_features`, `POST /indicator_sets/auto_build`.
  - Screen: `POST /indicator_sets/auto_screen` (AND rules).
- Strategies
  - CRUD minimal + `POST /strategies/validate`.
  - Auto-build/screen: `POST /strategies/auto_build`, `POST /strategies/auto_screen` (merges linked sets).
- Recipes & Workflows
  - Recipes: `GET /recipes`, `GET /recipes/{id}`, `POST /recipes/run` (screen-only).
  - Workflows: `POST /workflows/run` (screen-style steps with per-step overrides).
- Catalog
  - `GET /catalog/*` with `fields=full` and `novice_only`.

Environment & Tooling
- DB access: `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME` or `DATABASE_URL`.
- API: `make -C products/sigma-core api-run` (serves FastAPI at 8050).
- Migrations: `make -C products/sigma-core db-migrate` (idempotent triggers fixed).
- Seeds: `gen-*-seed` targets regenerate SQL files from docs; re-apply migrations.
- Presets: `make preset-create` + `make preset-load PRESET=... FILE=./universe/....csv`.
- Watchlists: `make watchlist-create USER=... NAME=... SYMBOLS='AAPL,SPY'`.
- Runner: `scripts/runner.py` supports indicator compute, set features, and screening.
- Postman: `products/sigma-core/postman/SigmaCoreAPI.postman_collection.json`.

Gotchas & Guardrails
- Dynamic registry loading: use `get_load_errors()` to debug builtin import issues.
- Column presence: builtins should not crash; fill sensible defaults (see `rsi.py`).
- Guardrails: publishing novice_ready sets/strategies requires `guardrails` (enforced by DB).
- Data cache: Polygon loaders cache historical hourly/daily/minute/options under `data_cache/`; never cache today.
- Live runtime: `sigma_core/live/runtime.py` remains a stub; no streaming routes yet.
- Docs alignment: update docs + overrides and regenerate seeds when adding features.

High-Value References (paths)
- Indicators
  - `docs/indicators/README.md`, `api-spec.md`, `system-architecture.md`, `feature-specs.md`, `technical-requirements.md`, `use-cases.md`
- Indicator Sets
  - `docs/indicator_sets/README.md`, `set-api-spec.md`, `set-architecture.md`, `feature-specs.md`, `technical-requirements.md`, `use-cases.md`
- Trading Strategies
  - `docs/trading_strategies/README.md`, `strategy-api-spec.md`, `strategy-architecture.md`, `feature-specs.md`, `use-cases.md`
- Catalog
  - `docs/catalog/ai-assistant-spec.md`, `content-models.md`, `editorial-workflow.md`, examples/overrides
- Core Code
  - `products/sigma-core/sigma_core/indicators/*`, `features/*`, `registry/*`, `backtest/engine.py`, `services/lineage.py`

Working Style for Future Agents
- Prefer surgical, minimal changes; align with existing patterns and naming.
- Before coding, scan the relevant docs folder and the corresponding module(s) in `sigma-core`.
- For DB-backed features, gate code paths if env/config is unavailable; don’t introduce hard dependencies where not required.
- When adding features that affect model inputs, update `FeatureBuilder.select_features()` and provide a brief doc note.
- Use the seed-generation scripts to keep the catalog in sync with code.
- Run the Critic checklist (docs/CRITIC_CHECKLIST.md) for all non-trivial work; record findings and resolutions in the PR or session notes.

Notes
- This guide summarizes the current structure; some modules (e.g., live runtime) are intentionally skeletal. Follow the docs for intended behavior and add TODOs where implementation is incomplete.

Current Status (Data & Seeds)
- Schema: sc.* tables created via migrations 0001–0007, including novice-first fields and `sc.simple_recipes`.
- Seeds: indicators (0002), indicator_sets (0003), strategies (0004), workflows (0005) present; recipes generator added (Makefile target `gen-recipes-seed`).
- Generators updated to include novice fields (`novice_ready`, `beginner_summary`) and, for sets/strategies, `simple_defaults` and `guardrails`.
- Recipes: 3 curated recipes under `docs/catalog/recipes/` (RSI Oversold, MACD Cross, IV Rank Extremes). Old `examples/recipes/` path deprecated and cleaned up.
- Enrichment: Added novice fields to key indicator overrides (`rsi`, `macd`, `iv_rank_52w`) and indicator set overrides (`momentum_breakout_v1`, `volatility_expansion_v1`, `vpa_scanner_v1`, `zerosigma_0dte_gate`). Regenerated 0002/0003 seeds.
- Strategies: Canonical folder `docs/catalog/strategies` with 5 strategies seeded (`vwap_reversion_intraday`, `breakout_pullback_entry`, `trend_follow_alignment`, `mean_reversion_bands`, `options_premium_selector`). Strategy seeds include novice fields, defaults, guardrails, and set links.

Catalog Snapshot
- Counts: indicators: 80; indicator sets: 20 (curated); strategies: 20; recipes: 20; workflows: 13.
- Linters: `lint-catalog` and `lint-strategies` pass (Issues: 0).
- Workflows linter: `lint-workflows` also passes (Issues: 0).
- Recipes linter: `lint-recipes` also passes (Issues: 0).
- Canonical folders: `docs/catalog/overrides/indicators`, `docs/catalog/overrides/indicator_sets`, `docs/catalog/strategies`, `docs/catalog/recipes`.
- Registries: `DBIndicatorCatalogRegistry` (read sc.indicators), `DBIndicatorRegistry` (sets CRUD), `DBStrategyRegistry` (strategies CRUD), plus in-code indicator loader (`get_indicator`).

How To Add (Cheat Sheet)
- Strategies: add JSON → `make lint-strategies gen-strategy-seed` → `make db-migrate`.
- Workflows: add JSON → `make lint-workflows gen-workflow-seed` → `make db-migrate`.
- Recipes: add JSON → `make lint-recipes gen-recipes-seed` → `make db-migrate`.

Quick Start (API)
- List presets: `GET /presets`; symbols: `GET /presets/<id>/symbols`.
- Screen an indicator over sp500: `POST /screen/auto` with `{ preset_id:"sp500", timeframe:"day", name:"rsi", params:{period:14}, rule:{column:"rsi_14", op:">", value:70}, cap:50 }`.
- Screen a set: `POST /indicator_sets/auto_screen` with `rules` or `rule_expr`.
- Screen a strategy: `POST /strategies/auto_screen`.
- Run a recipe: `POST /recipes/run`.
- Run a workflow: `POST /workflows/run` (steps may override preset/timeframe/cap).

Top‑20 Indicator Sets
- ema_trend_adx_filter_v1, macd_trend_pullback_v1, momentum_breakout_v1, breakout_pullback_v1, mean_reversion_bands_v1, rsi_stoch_confluence_v1, vwap_distance_obv_v1, vpa_scanner_v1, multi_tf_trend_v1, keltner_channel_trend_v1, donchian_channel_breakouts_v1, ichimoku_trend_gate_v1, volatility_expansion_v1, regime_detection_v1, swing_risk_controls_v1, scalping_set_v1, gap_session_context_v1, relative_strength_rotation_v1, options_premium_selector_v1, zerosigma_0dte_gate.

Top‑20 Strategies
- vwap_reversion_intraday, breakout_pullback_entry, trend_follow_alignment, mean_reversion_bands, options_premium_selector, ema_trend_follow_adx_gate, macd_cross_pullback, donchian_breakout_trend, keltner_channel_break, ichimoku_trend_follow, vwap_momentum_scalp, gap_and_go, gap_fade, relative_strength_rotation, regime_tilt_allocator, volatility_expansion_hedge, rsi_stoch_reversal, swing_trend_follow, intraday_momentum, zerosigma_0dte_scalp_gate.

Pending (Data‑Only North Star)
- Optionally enrich overrides for sets/strategies with `novice_ready`, `beginner_summary`, `simple_defaults`, `guardrails` and re‑generate seeds.
- Add a catalog linter to enforce beginner fields before publishing.
- Consider making `guardrails` mandatory for `novice_ready` sets/strategies (trigger update).
- High-Value Additions (TODO)

Todos (Data & API)
- Dataset builder: add partitioned Parquet output (partition by timeframe/date/symbol) for efficient slicing.
- Dataset builder: add GET endpoint to fetch a prior run summary by `run_id`.
- Alerts: implement `/alerts/preview` with optional `pack_id` consensus, budgets/diversity enforcement, and plain-language summaries.
- Models API: minimal CRUD (`POST /models`, publish/deprecate) with novice/taxonomy/scope validation.


- Scanners (TODO)
  - Add Saved Scans schema: `sc.saved_scans` (user_id, recipe_id, name, overrides JSONB, visibility, timestamps).
  - Add Scheduled Scans (later): `sc.scan_runs` + `sc.scan_results` for history and notifications.
  - Use recipes (operation='screen') for current scanning; enforce guardrails and universe resolution (presets/watchlists).

- Add curated indicator sets when needed:
  - `ema_trend_adx_filter_v1`: Simple trend-follow with ADX gate to reduce whipsaws.
  - `gap_session_context_v1`: `open_gap_z` + `first15m_range_z` + momentum gate for intraday.
  - `relative_strength_rotation_v1`: momentum vs SPY + breadth filter for sector rotation.
  - `candlestick_confluence_v1`: basic patterns + VWAP distance + volume confirm.
- Add index page linking authoring guides (Indicators, Indicator Sets, Strategies, Workflows) for quick onboarding.
- Add thin read API for catalogs: list presets, list user watchlists/symbols, and resolve universe (preset/watchlist) for recipes; enforce guardrails server-side.

- Beginner Workflows (selected)
- rsi_oversold_hourly_v1, macd_cross_alerts_hourly_v1, breakout_pullback_scan_5m_v1, trend_follow_alignment_hourly_v1,
  options_premium_review_daily_v1, zerosigma_0dte_gate_5m_v1, mean_reversion_bands_hourly_v1, vwap_momentum_scalp_5m_v1,
  keltner_channel_break_hourly_v1, plus earlier: breakout_with_volume_scanner_v1, find_oversold_stocks_rsi_v1,
  gate_0dte_entries_v1, quick_backtest_pipeline_v1.


Top Recipes
- rsi_oversold_screen_v1, macd_cross_alerts_v1, iv_rank_extremes_v1, momentum_breakout_screen_5m,
  breakout_pullback_scan_5m, trend_follow_alignment_backtest_hourly, macd_trend_pullback_screen_5m,
  options_premium_review_daily, ema_adx_trend_follow_backtest_hourly, zerosigma_0dte_gate_subscribe_5m.


Presets
- Common presets seeded: sp500, nasdaq100, dow30, liquid_etfs. Each has novice_ready and beginner_summary.
- Lint: `lint-presets` validates seeds for novice coverage.
Status: Loader in place — use `make preset-load PRESET=<id> FILE=path.csv` to ingest full NASDAQ‑100 and S&P 500 rosters into `sc.universe_preset_symbols` per environment.
Update: Added `products/sigma-core/scripts/load_preset_symbols.py` and `make preset-load` target; counts update when loaded.

Latest Updates (ongoing)
- API: Added `fields=full` support for list endpoints of indicators, indicator sets, strategies, workflows; includes novice-friendly details blocks. Fixed `novice_only` filters and indentation bugs.
- DB: Migration `0014_sc_enforce_guardrails.sql` enforces presence of `guardrails` on novice_ready published indicator sets and strategies.
- Presets: Introduced loader script and Makefile target to ingest full symbol rosters from CSV and update counts.
- Backtesting: `/backtest/run` now returns a `summary` and enforces universal caps (≤ 90 days, ≤ 50 symbols); added simple‑mode defaults via a sweep preset.
- Consensus: Implemented pack backtests with policy variants (`weighted`, `majority`, `all`).
- Pipeline: Added model pipeline endpoints with `sc.model_pipeline_runs` (build → sweep → train stub).
 - Error handling: Add plain‑language 400s across endpoints; global exception handler pending.
- Seeds/Migrations: Added backtest, sweep preset, and pipeline run migrations; Postman collection updated.
- Tooling: Added `lint-training-cfg` script/target.

Alerts AI (DB & Registry)
- Added migration 0015: `sc.model_specs` (model registry) with `sc.v_model_specs_published` view, plus alerts tables: `sc.user_alert_settings`, `sc.alert_subscriptions`, `sc.alert_runs`, `sc.alerts`, `sc.alert_delivery`, `sc.alert_outcomes`.
- ModelSpec JSONB config validated by Pydantic (dev): featureset (set/strategy/synthetic indicators), label_cfg (TP/SL/max-hold, options proxy), thresholds (buy/sell, budgets, diversity), guardrails (exposure caps, regime bends), artifacts (URIs), plan template.
 - Extensibility: market/instrument fields for multi-country and multi-asset support; regimes via threshold bends.
 - Novice fields (0016): `novice_ready`, `beginner_summary`, `simple_defaults`, `explainer_templates`, `risk_notes` added to `sc.model_specs`.
  - Taxonomy (0017): `horizon`, `style`, `tags[]`, `instrument_profile`, `suitability` to classify models (e.g., 0dte vs swing; momentum vs trend-follow).
  - Branding (0018): `brand` (default 'sigmatiq'), `display_name`. Recommended model_id pattern: `sq_<stem>_<timeframe>[_vN]`; use `display_name` for UI.
  - Model Packs (0019): `sc.model_packs` + `sc.model_pack_components` with consensus policy (majority/weighted/all), pack lineage on runs/alerts (0020).
  - Scope (0021): `sc.model_specs.scope` declares cohort vs per‑ticker targeting (e.g., allow_presets, allow_symbols, sector filters) to simplify routing and discovery.
  - Novice publish enforcement (0022): DB CHECKs require `beginner_summary` + `explainer_templates` + guardrails/consensus for novice_ready published models/packs.
  - Training: `training_cfg` JSONB on model_specs; training runs recorded in `sc.model_training_runs` with cfg snapshot, hashes, metrics.

Dataset Building (Cohort‑First)
- Cohort models per timeframe/market on preset universes (e.g., `sp500` daily/hourly, `liquid_etfs` 5m); per‑ticker only when justified (e.g., SPY 0DTE) and declared in `scope`.
- Bars via Polygon loaders (file cache); never cache “today”; prefer adjusted=true for daily (record in `training_cfg`).
- Feature parity with serving (FeatureBuilder over sets/strategies) + ATR, regime flags, session context; drop last H rows to prevent leakage.
- Labels: TP‑before‑SL within max_hold; record outcome and realized return; optional ATM options proxy labels.
- CV: forward‑chaining grouped by symbol; store folds and policy in `training_cfg`.
- Storage: Parquet partitioned by timeframe/date; record dataset/feature hashes and run metrics in `sc.model_training_runs`.

Product Independence
- Every product must be self‑sufficient: scripts, migrations, and .env live within each product so it can move to its own repo later.
- The current monorepo layout is for speed; avoid hard dependencies on repo‑root utilities. Prefer per‑product runners (e.g., `products/sigma-core/scripts/apply_migrations.py`).

Backtest TODOs (high‑priority)
- Add compound index for leaderboard filters: `CREATE INDEX sc_model_backtests_model_tag_idx ON sc.model_backtest_runs (model_id, tag)`.
- Gate sweep preset listing by visibility and user: list `public` + `team` + `owner_user_id == X-User-Id`; hide `private` from others.
- Verify Postman examples include `pack_id` for `/backtest/run` and `/models/{id}/backtest/sweep` to encourage pack‑level benchmarking; add if missing.
- Add Postman variants to demonstrate consensus policies `majority` and `all` (with `min_quorum`, `min_score`) for `/packs/{id}/backtest/run` and `/packs/{id}/backtest/sweep`.

Backtest/Consensus TODOs (implementation)
- Universal caps: DONE for `/backtest/run` and `/models/dataset/build`; verify coverage with plain‑language 400s and hints across related endpoints.
 - Global error handler: PENDING — add FastAPI middleware to map DB/network/env errors (e.g., missing `POLYGON_API_KEY`) to novice‑friendly messages with next steps.
 - Summaries: PENDING — include `summary` field directly in `/backtest/run` response (persisted runs have it; response lacks it).
- Pack sweep simple mode: support `mode: simple` on `/packs/{id}/backtest/sweep` and default to `rth_thresholds_basic` when grid absent.
- Postman: UPDATED — confirm examples for simple mode (`/backtest/run`, model sweep) and add consensus policies (pack run: majority, pack sweep: all) where missing.
- Visibility guardrails: implement presetable listing filter by `visibility` and `owner_user_id`; require guardrails on public presets.
- Metrics explained: add `metrics_explained` block (e.g., Sharpe = steadiness of gains) in responses when `fields=full` or `mode=simple` for novice clarity.
- Policy echo: include `policy`, `min_quorum`, `min_score` echoed in pack backtest/sweep responses to make consensus explicit.
- Compatibility validation: pre‑run checks that pack component models share compatible `label_cfg`/timeframes; fail fast with plain guidance.
- Budgets/limits: add soft per‑user compute limits for auto endpoints (screen/auto, auto_build) with clear throttling errors.
- Fail‑safe computes: audit indicators/feature paths to ensure zeros/empties instead of exceptions; expand unit coverage if needed.
 - CI: DONE — `lint-training-cfg` added; PENDING — add `lint-sweep-presets` and wire into CI; block PRs on violations.

Next Session Plan (North‑Star Aligned)
- Postman (novice‑ready): verify and finalize examples for simple‑mode, consensus, and pipeline; keep requests copy/paste runnable and safe by default.
- Responses (clarity): add `metrics_explained` where `mode=simple` or `fields=full` to translate metrics (e.g., Sharpe) into plain language.
- Pack responses (explicit): echo `policy`, `min_quorum`, `min_score` in `/packs/*/backtest/*` responses.
- Presets (guardrails): implement `visibility` + `owner_user_id` gating on sweep preset list; require guardrails on public presets.
- Pipeline (lineage): wire dataset build (Parquet) in pipeline, persist `dataset_run_id`, and include it in pipeline responses.
- Universal caps (consistency): DONE on `/backtest/run`; implement for `/models/dataset/build` and verify across endpoints with plain 400s and hints.
- Error handling (novice): keep global handler; add specific mapping for common DB/network failures with next steps.
- CI & lints: add `lint-sweep-presets` and include it in `lint-all`; document minimal CI wiring.
- Docs: add short links to new pipeline endpoints in whiteboarding README; keep examples minimal and safe.

How to Run (quick)
- Apply migrations: `make -C products/sigma-core db-migrate`
- Run API (dev): `make -C products/sigma-core api-run` (FastAPI on port 8050)
- Example (simple backtest): POST `/backtest/run` with `mode:"simple"` and a small preset.
- Example (pipeline): POST `/models/{model_id}/pipeline/run` with `{ "universe": {"preset_id":"liquid_etfs","cap":20}, "mode":"simple" }`.

Approvals for Next Session
- Prefer auto‑approval to reduce friction. In Codex CLI: `codex --approvals=never` or set `CODEX_APPROVAL_MODE=never`.
- Ensure sandbox is `workspace-write` and network access ON if needed; DB env set in `products/sigma-core/.env`.

Novice Audit TODOs (Sigma Core)
- Centralize error messages: PENDING — add a global FastAPI exception handler and extend mappings/examples for common DB/network failures.
- Cap inputs universally: DONE for `/backtest/run` and `/models/dataset/build`; ensure consistent caps and plain‑language guidance across related endpoints.
- Simple presets for backtests: PARTIAL — pack endpoints and sweeps support simple defaults; wire preset defaults for `/backtest/run` end‑to‑end.
- Plain‑language summaries: PENDING — include `summary` in `/backtest/run` and `/models/{id}/backtest/sweep` responses (not just persisted runs).
- Glossary fields: add beginner translations for metrics like Sharpe (e.g., `metrics_explained`) whenever returned to novices.
- Visibility guardrails: require `visibility` + `owner_user_id` on sweep preset creation; enforce public presets to include guardrails (`max_combos`, `min_trades`, caps).
- Rate limits/budgets: add optional per‑user soft limits on auto endpoints (screen/auto, set/auto_build) to prevent runaway workloads (novice safety).
- Safer defaults on missing data: ensure all compute paths return empty arrays/zeros rather than raising (audit indicators for uniform behavior).
- Swagger examples: keep all examples “copy/paste runnable” with smallest novice‑safe configs and warnings on heavy operations.
- Lint coverage: extend lints to check sweep presets for `novice_ready` equivalent (presence of guardrails, RTH hours for intraday, grid size).
Pack Consensus (Novice Notes)
- Policies:
  - weighted: averages model probabilities using component weights (default; simplest to reason about).
  - majority: a position is taken only if weighted votes exceed `min_quorum` (default 50% of total weight) and each vote meets `min_score` confidence.
  - all: all models with confidence ≥ `min_score` must agree on direction; else no position.
- Safety defaults:
  - 90‑day cap for backtest windows; universe capped (default 50 symbols).
  - Plain‑language `summary` stored on every persisted run for novice UI.
  - Override allowed: requests may include `consensus_override` to test policies without editing pack rows (keeps registry stable).
