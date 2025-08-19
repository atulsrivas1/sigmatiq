# Build → Backtest (Sweeps) → Leaderboard → Train — UI Spec v1

## Status
Draft — aligns with ADR 0005 and Matrix Contract v1

## Goals
- Make the BTB pipeline intuitive: configure sweeps, inspect results, select configs, and train — with clear guardrails.
- Surface “why” behind outcomes: pass/fail gates, risk budgets, lineage shas.
- Support risk profiles (Conservative/Balanced/Aggressive) without fracturing model IDs.

## Routes & Page Roles
- `#/sweeps` — Configure and run sweeps (backtests). Manage risk profile and guards. Inspect results. Add to Selection.
- `#/leaderboard` — Rank/compare results. Filter, gate, and select best configs. Batch actions.
- `#/runs` (Train tab) — Review selected configs, set training options, and queue training. Show progress.
- `#/models` — Browse models; open a model to view lineage and recent runs; link to Sweeps and Train.

## Shared UI Elements
- Risk Profile selector: Conservative | Balanced | Aggressive (badges). Persists per user and page.
- Selection Cart: persistent drawer listing chosen configs (model_id, matrix_sha, config tuple, risk_profile). Actions: Remove, Compare, Train Selected.
- Gate Badges: chips indicating pass/fail for budgets (MaxDD, ES, Capacity/Parity, Trades). Tooltip shows brief reason.
- Lineage Snippet: `matrix_sha`, `config_sha`, `policy_sha`, `risk_sha` in popover; copy buttons.

## Sweeps Page (`#/sweeps`)
Sections
- Header: Page title + Risk Profile selector + docs link.
- Control Panel
  - Model select (from registry).
  - Sweep Dimensions
    - Threshold variants (comma-separated lists).
    - Allowed Hours variants (e.g., 13,14,15) — intraday packs only.
    - Top % variants (for top‑N style policies).
  - Risk Envelope (per profile defaults; fully editable)
    - min_trades, max_drawdown_pct, es95_mult, spread_pct_max, oi_min, volume_min, fill_rate_min, adv_bps_max (as applicable), allowed_hours lock.
  - Actions: Validate, Run Sweep, Reset to Profile Defaults.
- What‑If Panel: sliders for threshold/top%/hours showing delta chips (Sharpe/Trades/Return). Non‑blocking.
- Results
  - Table columns: Kind (thr/top%), Thr/Top%, Allowed Hours, Sharpe, Cum Return, Trades, Parity/Capacity, Tag, Actions.
  - Per row: equity sparkline, Gate Badges (chips), CSV button, Add to Selection, Compare.
  - Empty State: helpful text linking to Control Panel.

Interactions
- Risk Profile changes prefill Sweep Dimensions ranges and Risk Envelope.
- Run Sweep: kicks off job; show progress; update table incrementally.
- Add to Selection: stores row (normalized key) in persistent cart with selected `risk_profile`.
- Compare: opens modal with side‑by‑side charts (equity curve, drawdown, hour‑wise heatmap) for selected rows.

## Leaderboard Page (`#/leaderboard`)
Sections
- Header: Page title + Export CSV + Risk Profile filter + "Pass Gate only" toggle.
- Filters: Model, Pack, Tag; optional date window.
- Visuals
  - Scatter: Sharpe vs Cum Return; point size = Trades; color = Allowed Hours bucket; hover shows metrics + Gate status.
  - Table: Started At, Model ID, Pack, Best Sharpe, Best Return, Trades, Win Rate, Tag, Actions (View, Add to Selection, Compare).
- Compare Modal
  - Equity curves overlay with shaded drawdowns.
  - Hour‑wise performance heatmap (intraday).
  - Budget usage bars (MaxDD, ES, Capacity/Parity).
  - Lineage snippet for each row.

Interactions
- "Pass Gate only" hides rows that fail current profile budgets.
- Add to Selection adds the configuration tuple + `risk_profile` to cart.
- Batch actions (top toolbar): Compare selected, Train Selected.

## Train (Runs) Page (`#/runs` → Train tab)
Sections
- Selected Configs (grouped by `risk_profile`)
  - Columns: Model ID, Matrix (sha7), Config (thr/top%/hours/splits), Gate (pass/fail), Actions (Remove, Inspect).
  - Badges: risk_profile, pack.
- Training Options
  - Algorithms (per config or global): e.g., GBM, RF, NN (defaults per pack).
  - Concurrency and quotas (per user/profile defaults).
  - Seeds and tags.
- Queue Summary
  - List of jobs to start; lineage preview; estimated durations.
  - Start Training button; progress area with live statuses.

Interactions
- Remove from selection updates the persistent cart across pages.
- Start Training queues all passing configs; failures require override confirmation with tag.

## Matrix Profile (from Runs > Build)
- Button opens modal with Matrix Contract v1 diagnostics:
  - Summary (features, rows, label balance, NaN%).
  - Missingness heatmap, correlation heatmap.
  - Leakage summary (flags with short explanations).
  - Coverage by hour/day; drift chart.
  - `matrix_sha` and copy buttons.

## Normalized Keys & Lineage
- Config key (for caching/selection): `(model_id, matrix_sha, kind, value, allowed_hours, splits, tag, risk_profile)`.
- Runs and artifacts stamped with: `matrix_sha`, `config_sha`, `policy_sha`, `risk_profile`, `risk_sha`.

## Data Contracts (high‑level)
- GET `/leaderboard?model_id=&risk_profile=&pass_gate=1` → rows [{ id, started_at, model_id, pack_id, metrics { sharpe, return, trades, win_rate, max_dd }, config { kind, value, allowed_hours, splits, tag }, lineage { matrix_sha, config_sha, policy_sha, risk_profile, risk_sha }, gate { pass, reasons[] } }]
- POST `/sweeps/run` body: { model_id, matrix_sha?, risk_profile, sweep: { thresholds_variants[], hours_variants[], top_pct_variants[] }, risk_budget_overrides?, tag } → { sweep_id }
- GET `/sweeps/{id}/status` → progress, partial rows
- POST `/train/batch` body: { jobs: [{ model_id, config, matrix_sha, risk_profile, algorithm, seed, tag }] } → { job_ids[] }

## Acceptance Criteria
- Sweeps shows Risk Profile presets with editable Risk Envelope; results include Gate Badges and actions (CSV, Add to Selection, Compare).
- Leaderboard filters by risk_profile; supports "Pass Gate only" and batch selection actions.
- Selection Cart persists across pages/sessions; Train tab lists selections grouped by profile; Start Training enqueues only passing rows unless overridden.
- Matrix Profile modal displays diagnostics and `matrix_sha`.
- All pages expose short “why” tooltips for pass/fail and lineage copy buttons.

## Notes
- Visualizations can ship as static first (sparklines, heatmaps placeholders), with real charts later.
- This spec intentionally mirrors ADR 0005 and Matrix Contract v1 for consistency and auditability.

