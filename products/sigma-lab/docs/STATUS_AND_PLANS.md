# Sigmatiq Sigma: Status and Plans (Updated)

This document reflects the current status after recent implementation work and outlines the next milestones.

## Docs Changelog (BTB v1)
- Added: ADR 0005 — BTB pipeline and risk profiles (`docs/adrs/0005-btb-pipeline-and-risk-profiles.md`).
- Added: Matrix Contract v1 (`docs/specs/Matrix_Contract_v1.md`).
- Added: BTB UI Spec v1 (`docs/ui/BTB_UI_Spec_v1.md`).
- Added: BTB API Spec v1 (`docs/api/BTB_API_Spec_v1.md`).
- Added: Risk Profile Schema (`docs/specs/Risk_Profile_Schema.md`).
- Added: Gate & Scoring Spec v1 (`docs/specs/Gate_and_Scoring_Spec_v1.md`).
- Added: BTB Runbook (operator guide) (`docs/runbooks/BTB_Runbook.md`).
- Added: QA Checklist (`docs/tests/BTB_QA_Checklist.md`).

BTB + Assistant (additions)
- Added: AI Assistant Spec v1 (`docs/ui/AI_Assistant_Spec_v1.md`).
- Added: Assistant API Spec v1 (`docs/api/Assistant_API_Spec_v1.md`).
- Added: Assistant QA Checklist (`docs/tests/Assistant_QA_Checklist.md`).
- Added: DB Schema Deltas v1 (`docs/specs/DB_Schema_Deltas_v1.md`).
- Added: Backend Implementation Plan v1 (`docs/plans/Backend_Implementation_Plan_v1.md`).
- Added: Error Catalog v1 (`docs/api/Error_Catalog_v1.md`).
- Added: Quotas & Rate Limits v1 (`docs/api/Quotas_and_Rate_Limits_v1.md`).

Template-first Create (additions)
- Added: ADR 0006 — Template-first Create + split Designer vs Composer (`docs/adrs/0006-template-first-create-and-split-designer-composer.md`).
- Added: Model Templates Spec v1 (`docs/specs/Model_Templates_Spec_v1.md`).
- UI docs updated: Create is now a Template Picker; Designer added as structure editor; Composer remains BTB workspace.

Signals (additions)
- Added: Signals API Spec v1 (`docs/api/Signals_API_Spec_v1.md`).
- DB deltas: signals table and live rollup views documented in `docs/specs/DB_Schema_Deltas_v1.md`.
- UI docs: Signals now has Leaderboard | Log | Analytics; Model Detail includes a Performance tab (P1).



Impacts (no breaking changes to vision):
- Vision remains intact; these documents clarify pipeline, risk profiles, and reproducibility.
- Minor updates recommended to existing docs (see below) to reference BTB v1.

## Completed
- Product-first layout: Sigma Lab under `products/sigma-lab/` with API, UI, data/artifacts consolidated per product.
- Core layout: standardized to `sigma_core/` package; skeleton-aligned modules present.
- API
  - Pack-aware endpoints (`/models`, `/build_matrix`, `/train`, `/backtest`, `/model_detail`).
  - Pydantic request models; `GET /` index and `GET /healthz` (Polygon connectivity incl. IV snapshot).
  - Policy enforcement: operational routes require a valid per-model policy; `/validate_policy` endpoint; effective execution shown in `/model_detail`.
- Features & Indicators
  - Indicator set loader + builder wiring; extensive builtins: momentum, volatility/rolling std, RSI, EMA, EMA slope, distance-to-EMA, returns, sold_flow_ratio, IV–realized spread (via Polygon greeks), daily momentum family (shifted), composite momentum score.
  - ZeroSigma indicator set expanded to include intraday + daily indicators and composite score.
- Data
  - Polygon-only adapters for hourly/daily bars; option chain snapshot (IV/Greeks) and OI snapshot; strict cache policy (never cache today; cache historical only).
- Backtest
  - Walk-forward split + embargo; threshold/top_pct; confidence sizing; optional calibration.
  - Momentum gate (policy-driven or override): zero positions below threshold.
  - Plot to `products/sigma-lab/static/backtest_plots/<model_id>/cum_returns.png`.
- DB/Leaderboard
  - Postgres integration (no container requirement); lazy pool and clear errors.
  - Backtest runs persisted: `backtest_runs` with normalized columns (best_sharpe_hourly, best_cum_ret, trades_total, tag) + params/metrics JSON, plots/data URIs.
  - Per-fold persistence in `backtest_folds`.
  - `GET /leaderboard` endpoint and Makefile target; supports `tag` filter for sweeps/smoke.
  - Migrations: `0001_init.sql`, `0002_add_backtest_runs.sql`, `0003_backtest_folds_and_cols.sql`.
- Tooling & Docs
  - Makefile targets for UI, health, build/train/backtest, gated variants, pipeline, validate-policy, leaderboard, and live indicator testing.
  - Model creation script with auto-generated names (`ticker_asset_horizon_cadence[_algo|_variant]`) and policy scaffolding.
  - Windows-friendly API runner: `products/sigma-lab/api/run_api.py` (removes shell/env quoting pitfalls).
  - Sweeps backend (`POST /backtest_sweep`) + `make sweep`; smoke pipeline (`make smoke`) with summary and conditional training; docs updated.
  - Docs: policy schema, model naming, updated STATUS_AND_PLANS, and TODOs; Excel indicator catalog importer that generates JSON summaries and missing-vs-repo.

## In Progress / Next
- Stocks-only pipeline
  - Add a stock dataset builder (bars→features→labels) and a stock-focused indicator set under `swingsigma`.
  - Scaffold example equity model configs/policies so `swingsigma` shows up in `/models` and runs E2E.
- Policy-driven calibration
  - Add `/calibrate_thresholds` (global/per-hour) and a Make target to tune thresholds on recent matrices; persist best configs.
- Ops & UX
  - Expand `/healthz` with DB connectivity and a simple entitlement/rate-limit hint.
  - Structured logging across API/data paths; env-driven log levels.
  - Optional: `/backtest_runs/<id>` endpoint to fetch a run + folds; richer leaderboard aggregations (by model).
- Tests (no mocks policy)
  - Add API smoke tests (shape-only) and integration checks that run only with live Polygon + opt-in env flag.

### Doc updates to make (light edits)
- Update `policy_schema.md` to include `risk_profile` and `risk_budget` blocks (align with Risk Profile Schema).
- Update `specs/Model_Cards_and_Lineage.md` to add `risk_profile` and `risk_sha` fields in lineage examples.
- Update UI docs (`ui/Sigma_Lab_UI_Requirements_v1.md`, `ui/Sigma_Lab_UI_Wireframes_v1.md`) to mention Risk Profile selector, Gate Badges, and Selection Cart.
- Update `runbooks/zerosigma_0dte_pipeline.md` to reference sweeps → gate → train flow and Risk Profile presets.
- Add a brief “Using the Assistant” section to UI docs/wizard guidance linking to the assistant spec and capabilities.

### TODOs (no code changes yet)
- Draft SQL migration placeholders under `products/sigma-lab/api/migrations/` per `specs/DB_Schema_Deltas_v1.md`.
- Prepare OpenAPI YAML sketch for BTB + Assistant endpoints under `docs/api/openapi_btb_v1.yaml`.
- Define allowlisted SQL templates for Assistant DB tools (read-only) and parameter validation plan.
- Quotas config defaults and env overrides per `api/Quotas_and_Rate_Limits_v1.md`.
- See `docs/todos/Backend_TODOs.md` for the full list.
## Notes
- Database: designed for local or cloud Postgres (no containers). Apply SQL migrations with `psql`.
- Caching: historical-only cache; today’s requests always live.
- Naming: model_id auto-generated; policy is mandatory per model.

See `docs/todos/*` for granular items. Completed items have been reflected here and in the TODO notes.

---

## Packs Roadmap (overview)

This workstream tracks the multi-pack plan. Details live in `docs/PACKS_ROADMAP.md`.

- ZeroSigma (0DTE, opt): baseline done; next: PCR/OI features, IV rank/percentile, smile width; additional idea sets (opening_drive, gamma_unwind).
- SwingSigma (eq/opt): add daily-focused indicator sets (breakout, meanrevert) and labels; stock pipeline E2E; options term structure (30d vs 90d).
- LongSigma (eq/opt): carry/term structure, LR R², Ulcer Index (optional); daily labels 63–252d.
- OvernightSigma (eq/opt): close→open signals (last-hour, VWAP, gap metrics), EOD IV and OI deltas; labels and preview checks around opens.
- MomentumSigma (eq/opt): vol-scaled momentum ladder, ADX gate; options with IV bias filters.

## Indicators Backlog (overview)

Full list in `docs/indicators/INDICATORS_BACKLOG.md` with priorities and owners. Top missing items:

- Regime: VIX level/Δ, VIX term slope (needs Polygon index adapter).
- Options structure: PCR volume/OI, OI change/trend; daily ATM IV store → IV Rank/Percentile, ATM IV z-score; smile width.
- Intraday derived: RSI last-hour, returns last 30m, close vs intraday VWAP (delta/ratio), day range position, volume z-score.
- Calendar: EOM/EOQ/OPEX/holiday-eve flags.

## Idea Sets Integration

We’ll import curated indicator sets from `edge_packs_ideas/` into pack defaults and model templates. Alias map for compatibility:

- returns→ret, stddev→rolling_std, bollinger→bollinger_bands, iv_skew_25d_rr→iv_skew_25d.

Work items:
- Copy idea sets into `products/sigma-lab/packs/<pack>/indicator_sets/` (keeping original names).
- Add alias mapping in indicator set loader (non-breaking) so existing YAMLs resolve correctly.
- Implement missing indicators above in batches; wire to `/preview_matrix` and UI.

Imported so far:
- ZeroSigma: `zerosigma_default` (base), `zerosigma_headfake_reversal_v1` (from zerosigma_headfake_reversal_files), `zerosigma_pin_drift_v1`, `zerosigma_pin_drift_v2` (from zerosigma_pin_drift_files).
Planned next:
- ZeroSigma: `zerosigma_opening_drive`, `zerosigma_gamma_unwind` (pending indicator coverage for PCR/OI/VIX).
