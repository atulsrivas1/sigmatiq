# Sigma Lab UI — Requirements (v1, Developer Edition)

Purpose: Unambiguous, build‑ready requirements for Sigma Lab’s UI. This document defines routes, user stories, data contracts, interactions, states, a11y, storage, performance, and acceptance criteria. See wireframes in `ui/Sigma_Lab_UI_Wireframes_v1.md` and implementation mapping in `ui/SIGMATIQ_UI_Implementation_Guide.md`.

Priorities: P0 (now), P1 (next), P2 (later).

Global
- Navigation: Dashboard, Packs, Models, Composer (Build/Backtest/Train), Sweeps, Leaderboard, Signals, Overlay, Health, Docs, Admin.
- Disable unimplemented routes: use `implementedPaths` in `src/config/menu.ts` to render non-clickable items with “Coming soon” titles.
- Theming: themes `dark|midnight|light|slate` via `data-theme` on `<html>`. Persist `localStorage['theme']`. Focus and surfaces adhere to tokens.
- Density: `data-density` on `<html>` with `compact|cozy|comfortable`. Persist `localStorage['ui.density']`. Tables/cards consume density tokens.
- Accent: `data-sigma` per pack controls `--accent`.
- Risk Profile: `Conservative|Balanced|Aggressive` persisted `localStorage['risk.profile']`. Selection Cart persisted as `localStorage['selection.cart']`.
- State & API: typed client `src/services/api.ts`. Retry/backoff for 5xx/429; request abort on unmount; optimistic toasts where safe.
- A11y: WCAG AA; visible `:focus-visible` rings; role landmarks (header/nav/main/footer); ESC closes; tooltips available on focus.
- Errors/Loading/Empty: uniform patterns (skeleton → empty message + CTA → error banner with retry).
- Performance: ≤ 2s for P0 lists with ≤50 rows; lazy-load heavy visuals.

Storage Keys
- `theme`, `ui.density`, `risk.profile`, `selection.cart`, `auth_token`.

Data Types (shared)
- Model: `{ model_id: string; pack_id: string; updated_at?: string; sharpe?: number; win_rate?: number; trades?: number }`
- LeaderboardRow: `{ id?: string; started_at?: string; model_id: string; pack_id: string; metrics?: { sharpe?: number; cum_ret?: number; win_rate?: number; trades?: number; max_drawdown?: number }; gate?: { pass: boolean; reasons?: string[] }; lineage?: { matrix_sha?: string; config_sha?: string; policy_sha?: string; risk_profile?: string; risk_sha?: string }; tag?: string }`

1) Dashboard (P0)
- Purpose: At‑a‑glance status and quick actions.
- Stories
  - View recent models (5) and last runs (10) with links.
  - Launch quick actions: Create Model, Run Backtest, Open Sweeps.
  - See health: API/DB/Data coverage short status.
- API
  - GET `/models?limit=5` → `{ models: Model[] }`
  - GET `/leaderboard?limit=10` → `{ rows: LeaderboardRow[] }`
  - GET `/health` → `{ api: 'ok|warn|error', db: 'ok|warn|error', data: 'ok|warn|error' }`
- Interactions
  - Row click opens detail (Model Designer or plots/leaderboard when applicable).
  - “View details” opens Health.
- States
  - Loading: card skeletons (2–3 placeholders each).
  - Error: card‑level banner + Retry; show last successful timestamp.
  - Empty: message + CTA to Create Model.
- A11y: Cards focusable; buttons labelled; keyboard tab order consistent.
- Acceptance
  - Loads ≤ 2s; link targets correct; health displays 3 statuses and links to `/health`.

2) Models — List (P0)
- Purpose: Browse and manage models.
- Stories: Filter by pack; search model_id; sort; open Designer/Composer; create model.
- API: GET `/models?search=&pack_id=&limit=&offset=` → `{ models: Model[] }`
- URL/State: Persist `search`, `pack_id`, `order_by`, `limit`, `offset` in query params.
- Sorting: columns `model_id|pack_id|sharpe|updated_at`; default `updated_at desc`.
- Actions: [Open Designer], [Open Composer Build/Backtest], [Sweeps].
- States: loading skeleton; empty with [Clear filters]; error banner + Retry.
- A11y: Sort buttons expose `aria-sort`; rows keyboard‑activatable; Enter opens.
- Acceptance: server paging supported; filters preserved on refresh; actions navigate correctly.

2a) Models — Templates Gallery (P1)
- Purpose: Browse curated templates by pack/horizon; start Create prefilled.
- API: GET `/model_templates?pack=&horizon=&cadence=&q=` → `{ templates: [...] }`
- Interactions: filter chips, search, card click → `#/models/new?template_id=`.
- Acceptance: loads ≤ 1s for 100 templates; card focus ring and aria‑labels present.

3) Models — Create (Template Picker) (P0)
- Purpose: Create model from a template quickly; customize later.
- Steps
  1) Choose Template (cards with pack/horizon/cadence/description)
  2) Name & Risk (name input, model_id preview, risk chips)
  3) Create (buttons to open Composer or Designer)
- API
  - GET `/model_templates`
  - POST `/models { template_id, name, risk_profile }` → `{ model_id }`
- Validation: name required; template required; show server error banner (first line).
- A11y: All fields labelled; Next disabled until valid.
- Acceptance: ≤ 3 clicks to create; navigates to chosen destination.

4) Model — Overview (P0)
- Purpose: Central hub for a model; quick runs and performance (P1).
- Sections: Summary; Trust HUD (integrity/parity/capacity); Lineage chips; Latest artifacts; Quick links.
- API: GET `/models?model_id=...`; GET `/leaderboard?model_id=...&limit=5`; GET `/model_card?model_id=...&pack_id=...`.
- A11y: Lineage chips are buttons with copy affordances; badges with tooltips open on focus.
- Acceptance: shows latest actions; quick links enabled when data present; performance tab loads ≤ 2s for 30d and shows freshness.

5) Composer — Build/Backtest/Train (P0)
- Purpose: Run and review pipeline actions.
- Tabs
  - Build: choose date window; run build; show `matrix_sha` + Matrix Profile (NaN%, label balance, leakage flags, coverage by hour/day).
  - Backtest: single run with config prefilled from Sweeps/Leaderboard; echo payload; show metrics/plots; link to leaderboard; optional tag.
  - Train: queue only Gate‑passing selections from Selection Cart; track job progress.
- API
  - POST `/build_matrix { model_id, pack_id, start, end }` → `{ matrix_sha, profile }`
  - POST `/backtest { model_id, pack_id, config, matrix_sha?, tag? }` → `{ run_id, plots, metrics }`
  - POST `/train { model_id, pack_id, csv?, calibration? }` → `{ job_id }`
  - GET `/leaderboard?model_id=...&limit=1`
- States: queued/running/done; errors show payload excerpt and retry button.
- A11y: Tabs keyboard accessible; forms labelled; pre/code blocks have copy buttons.
- Acceptance: Backtest prefilled from prior context; Build shows `matrix_sha` and profile; Train disables non‑passing by default, override prompts confirmation.

6) Sweeps (P0)
- Purpose: Grid search for thresholds/hours/top% with Risk Profile and Gate badges.
- Controls
  - Risk Profile: selector chips (persisted)
  - Variants: thresholds, allowed hours, top % (comma‑list inputs per variant row)
  - Guards (per profile): `min_trades`, `max_drawdown_pct`, `es95_mult`, `spread_pct_max`, `oi_min`, `volume_min`, `fill_rate_min`, optional `adv_bps_max`
  - Tag input
  - Actions: Validate, Run Sweep, Reset to Profile Defaults
- What‑if Panel: controls for threshold/topN/hours; shows deltas (Sharpe/Trades/Ret) non‑blocking.
- Results Table
  - Columns: kind (thr/top%), value, allowed_hours, sharpe, cum_ret, trades, Gate (chip + tooltip reasons), parity, capacity, tag, CSV, actions [Add], [Compare]
  - Selection Cart: persistent list in `localStorage['selection.cart']`
- API
  - POST `/backtest_sweep { model_id, risk_profile, sweep: { thresholds_variants[], hours_variants[], top_pct_variants[] }, tag? }`
  - GET `/leaderboard?model_id=...&tag=...` (client filter OK)
- A11y: Table rows and actions keyboard accessible; tooltips on focus; Export CSV button labelled.
- Acceptance: results display incrementally; What‑if changes compute deltas without blocking; [Add] updates persistent cart.

7) Leaderboard (P0)
- Purpose: Browse and compare persisted backtests.
- Filters: Model, Pack, Tag, Risk Profile, Pass Gate only, Sort (sharpe|cum_ret|date), Density.
- Table: Started At, Model ID, Pack, Gate (chip+reasons), Sharpe, Win Rate, Trades, Max DD, Cum Return, Actions (View, Add, Compare).
- Batch: select rows (checkbox); [Compare selected] (modal); [Train Selected].
- API: GET `/leaderboard?model_id=&pack_id=&tag=&risk_profile=&pass_gate=&limit=&offset=` → `{ rows, total? }`
- A11y: “Select all” checkbox controls page; checkboxes labelled by model_id.
- Acceptance: pagination works; filters applied to API; selected count visible; actions enabled when selection > 0.

8) Signals (P1)
- Tabs: Leaderboard | Log | Analytics.
- Leaderboard API: GET `/signals/leaderboard?pack=&risk_profile=&start=&end&limit=&offset=`
- Log API: GET `/signals?model_id=&start=&end=&status=&limit=&offset=`
- Analytics API: GET `/signals/summary?model_id=&risk_profile=&start=&end`
- Acceptance: pagination, sorting, lineage badges, and drawer to Model Performance (P1) present.

9) Options Overlay (P1)
- Inputs: date/expiry/dte_target, target_delta, min_oi; show parity summary; CSV link.
- API: POST `/options_overlay`, GET `/options/expirations`
- Acceptance: overlay count displayed; CSV path shown if available; parity summary present when quotes exist; inputs validated.

10) Health (P1)
- Purpose: system/API/DB/data coverage.
- API: GET `/health` (and `/healthz?ticker=` when added)
- Acceptance: statuses summarized with badges; deep links to docs.

11) Docs (P0)
- Purpose: open runbooks/specs/reference docs quickly.
- Implementation: curated list links to `products/sigma-lab/docs/**` in new tab.
- Acceptance: accurate links; list updated as docs evolve.

12) AI Assistant (P0)
- Read‑mostly tool with guarded actions; inline hooks per page.
- API: POST `/assistant/query { message, context }` → streamed response; server mediates tools.
- Tools server‑side: `docs.search`, `reports.read_csv`, `reports.read_xlsx`, `db.leaderboard`, `db.run_detail`, `pipeline.suggest`, (opt‑in) `pipeline.execute`.
- Acceptance: cites sources; never runs compute without confirmation; scope for DB/files limited; guardrails enforced.

Admin (P2)
- Jobs: GET `/admin/jobs`, POST `/admin/jobs/{id}/retry`, `/admin/jobs/{id}/cancel`.
- Quotas: GET `/admin/quotas?user=`, PATCH `/admin/quotas`, GET `/admin/quotas/usage?user=`.
- Risk Profiles: GET `/admin/risk-profiles`, PATCH `/admin/risk-profiles`.
- Packs Manager: GET `/admin/packs`, PATCH `/admin/packs`.
- Templates: GET `/admin/templates`, POST `/admin/templates`, PATCH `/admin/templates/{id}`, POST `/admin/templates/{id}/publish`.
- Feature Flags: GET `/admin/flags`, PATCH `/admin/flags`.
- Data Health: GET `/admin/health`, POST `/admin/diagnostics/run`.
- Audit & Logs: GET `/admin/audit`, GET `/admin/logs/tail`.
- Users & Roles: GET `/admin/users`, PATCH `/admin/users/{id} { role }`, POST `/admin/users/{id}/rotate_token`.
- Acceptance: admin actions prompt confirmation; success toasts; audit trail created.

Appendix — Gate Reasons (IDs → humanized)
- min_trades_not_met → “Minimum trades not met”
- es95_exceeds → “Expected Shortfall exceeds budget”
- max_dd_exceeds → “Max drawdown exceeds budget”
- spread_above_limit → “Option spread above limit”
- oi_below_min → “Open interest below minimum”
- volume_below_min → “Volume below minimum”
- fill_rate_below_min → “Fill rate below minimum”

