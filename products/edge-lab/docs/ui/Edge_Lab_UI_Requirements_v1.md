# Edge Lab UI — Requirements (v1)

Scope: UI for Edge Lab (authoring + evaluation). This document enumerates pages, purpose, user stories, data/endpoint needs, interactions, states, acceptance criteria, and references wireframes in `ui/Edge_Lab_UI_Wireframes_v1.md`. Priorities: P0 (now), P1 (next), P2 (later).

## Global
- Navigation: Dashboard, Models, Packs, Build/Train/Backtest, Sweeps, Leaderboard, Signals, Overlay, Health, Docs.
- Theming: semantic tokens with multiple themes (`light|dark|slate|paper`), app-level theme switcher, `prefers-color-scheme` default + `localStorage` override, pack accent via `data-edge` or `--accent` token.
- Density: global density modes `compact|cozy|comfortable` via `data-density` tokens for tables/cards.
- Assistant: docked chat panel with context-aware guidance across pages; suggests next actions and can read DB/CSV/Excel reports (read-only) to answer questions. Actions that trigger compute require explicit user confirmation in-chat.
- Risk: global Risk Profile selector (Conservative/Balanced/Aggressive) persisted per user; Selection Cart drawer persists chosen configurations across pages.
- Gate Badges: compact chips indicating pass/fail against profile budgets (MaxDD, ES95, parity/capacity, trades). Hover/focus shows a “Why failed?” tooltip with humanized reasons (e.g., `min_trades_not_met`, `spread_above_limit`). Tooltips must be keyboard-accessible and meet contrast guidelines across themes.
- State: type-safe API client; optimistic toasts; retry w/backoff.
- Accessibility: WCAG AA (AAA for critical text pairs), keyboard navigation, `:focus-visible` rings via `--ring` token, color-blind safe palettes, aria labels; no keyboard traps.
- Responsiveness: desktop-first with tablet/mobile layouts for lists and details.
- Errors: banner + per-field errors; empty/loading states across pages.

---

## 1) Dashboard (P0)
- Purpose: At-a-glance status and quick actions.
- Stories:
  - See recent models and last runs (build/train/backtest).
  - Quick actions: Create Model, Run Backtest, Open Sweeps.
  - Health status (API/DB/data coverage hints).
- Data/APIs: `/models`, `/leaderboard?limit=10`, `/healthz`.
- Acceptance: loads within 2s; cards link to detail pages; health “ok/warn/error”.

## 2) Models — List (P0)
- Purpose: Browse and manage models.
- Stories: filter/search by `model_id`, `pack_id`; sort by updated; open detail; create model.
- Data/APIs: `GET /models` (supports query); `POST /models` (opens wizard).
- Acceptance: server-side pagination; inline actions (Open, Backtest, Sweeps).

## 2a) Models — Templates Gallery (P1, optional)
- Purpose: Browse curated templates by pack/horizon; preview details; start Create prefilled.
- Stories:
  - Filter templates by pack, horizon, cadence; search by name/tag.
  - View template details (indicator set, policy defaults, sweeps defaults, description).
  - Action: Use Template → opens Create Model with `template_id` preselected.
- Data/APIs: `GET /model_templates`.
- Acceptance: filters work; Use Template deep-links to Create with prefilled template; loads within 1s with ≤100 templates.

## 3) Models — Create (Template Picker) (P0)
- Purpose: Create a model quickly from a curated template; customize later in Designer.
- Steps:
  1) Choose Template: cards with pack/horizon/cadence/description.
  2) Name & Risk Profile: model name/ID preview and risk profile chips (C/B/A).
  3) Create: success screen with [Open Composer] [Open Designer].
- Data/APIs: `GET /model_templates`, `POST /models { template_id, name, risk_profile }`.
- Acceptance: creates model in ≤ 3 clicks and deep-links to Composer or Designer.

## 4) Model — Overview (P0)
- Purpose: Single hub for a model; overview and settings (edits).
- Sections: Summary (pack, features, policy, template), Trust HUD (integrity/parity/capacity badges) and Lineage chips (`pack_sha • config_sha • policy_sha • template_id`), Latest artifacts, Quick links to Designer/Composer, Model card link.
- Performance tab (P1): period picker; summary cards (Sharpe/Sortino, Cum Return, Win Rate, Trades, Fill Rate, Avg Slippage); charts (equity & drawdown, calendar & hour heatmaps); parity/capacity panel for options. Shows data freshness and coverage.
- Data/APIs: `/models`, `/leaderboard?model_id=...`, `/models/:id/performance?start&end`, `/model_card`.
- Acceptance: shows last actions; Trust HUD renders when data available; lineage chips clickable (open diff/view); contextual quick actions enabled. Performance tab loads within 2s for 30d and cites freshness.

## 5) Build / Train (P0)
- Purpose: Run and review core pipeline actions.
- Stories:
  - Build: choose date window; run; link to matrix preview/download.
  - Backtest: re‑run a chosen Sweeps/Leaderboard configuration (single backtest); prefilled with thresholds/top%/hours/splits and `matrix_sha`.
  - Train (post‑selection): queue only Gate‑passing selections from Leaderboard/Cart; track progress.
- Data/APIs: `/build_matrix`, `/train`, `/backtest`, `/leaderboard`.
- States: queued/running/done; error surfaces payload excerpt.
- Acceptance: Build shows metrics/plots and `matrix_sha`; Backtest pre‑fills from Sweeps/Leaderboard and persists with tag; Train enqueues only gate‑passing by default. (P1) Parity panel and calendar heatmap on Backtest results.

## 6) Sweeps (P0)
- Purpose: Grid search across thresholds/hours/top_pct.
- Stories:
  - Run sweep with variants (`thresholds_variants`, `allowed_hours_variants`, `top_pct_variants`).
  - Risk Profile selector (Conservative/Balanced/Aggressive) pre-fills editable guards (per profile): `min_trades`, `max_drawdown_pct`, `es95_mult`, and parity/capacity limits (spread %, OI, volume, fill rate). Tag runs.
  - Adjust What‑if controls (threshold, top‑N, hours) and see instant deltas (e.g., +Sharpe/−Trades) reflected in the results preview.
  - See results table with columns: threshold/top_pct, allowed_hours, sharpe, cum_ret, trades, Gate (pass/fail badges with tooltips), parity, capacity, tag; CSV export includes lineage fields.
  - Row actions: [Backtest] (deep‑link to Composer › Backtest prefilled), [Add to Selection], [Compare] (equity/drawdown/hour‑wise heatmap). Selection Cart persists across pages.
- Data/APIs: `POST /backtest_sweep`, `GET /leaderboard?tag=...` (client filter supported), model card link.
- Acceptance: displays top N results; What‑if deltas update quickly; CSV exported (with lineage fields); Gate badges show reasons; [Add to Selection] updates a persistent cart.

## 7) Leaderboard (P0)
- Purpose: Browse persisted backtests.
- Stories: filter by model/pack/tag/risk_profile; toggle "Pass Gate only"; sort by sharpe/cum_ret/date; open run detail; (P1) show sparklines for PnL/drawdown/hit-rate.
- Data/APIs: `GET /leaderboard?model_id=&pack_id=&tag=&limit=&offset=`.
- Acceptance: pagination works; tag/risk filters applied; Gate badges render with tooltips; [Backtest], [Add to Selection], and [Compare selected] present; clicking row opens detail (if available).

## 8) Signals (P1)
- Purpose: Monitor live signals and compare models by live performance.
- Tabs: Leaderboard | Log | Analytics.
- Leaderboard
  - Stories: compare models by live period metrics (Sharpe/Sortino, Cum Return, Win Rate, Trades, Fill Rate, Avg Slippage, Capacity). Filter by model/pack/risk_profile/date/tag. Optional “Pass Gate only”.
  - Data/APIs: `GET /signals/leaderboard?pack=&risk_profile=&start=&end&limit=&offset=`.
- Acceptance: paginated; sorts by metric; rows include lineage badge; row click opens Model Overview > Performance.
- Log
  - Stories: view latest signals with filters (model/date/ticker/status). Columns: ts, model, side, entry_ref_px, fill_px, slippage, status, rr, pnl, tag.
  - Data/APIs: `GET /signals?model_id=&start=&end=&status=&limit=&offset=`.
  - Acceptance: CSV export; stable schema; preserves filters on refresh.
- Analytics
  - Stories: visualize live equity & drawdown; calendar and hour heatmaps; parity/capacity charts (options).
  - Data/APIs: `GET /signals/summary?model_id=&risk_profile=&start=&end`.
  - Acceptance: renders charts within 2s for 30d; displays coverage % and data freshness.

## 9) Options Overlay (P1)
- Purpose: Turn stock signals into options (single/vertical) with premium parity.
- Stories: input date/expiry/dte_target, target_delta, min_oi; show parity summary; CSV link.
- Data/APIs: `POST /options_overlay`, `GET /options/expirations`.
- Acceptance: shows overlay count; optional CSV path displayed; parity summary present when quotes exist.

## 10) Health / Status (P1)
- Purpose: System health and data coverage.
- Stories: `/healthz` at-a-glance; optional DB status; data coverage hints for selected tickers.
- Data/APIs: `GET /healthz?ticker=`; later: extend.
- Acceptance: shows ok/warn/error; links to docs for common issues.

## 11) Docs (P0)
- Purpose: Link to relevant docs quickly.
- Stories: open AGENTS.md, BACKLOG.md, runbooks, indicators reference, policy schema.
- Implementation: links open in new tab to `products/edge-lab/docs/*`.
- Acceptance: curated list updated as docs evolve.

## 12) AI Assistant (P0)
- Purpose: Guide users through BTB workflow and answer outcome questions using live context.
- Stories:
  - “Help me build a matrix for spy_opt_0dte_hourly from June 1–15.” → proposes Make/REST payload; asks for confirmation; explains fields.
  - “Which sweep configs passed Gate for Balanced profile last week?” → queries leaderboard (read-only) and summarizes top rows with links.
  - “Why did this config fail?” → explains Gate reasons and suggests budget/parameter adjustments.
  - “What is the average Sharpe from this report?” → reads CSV/XLSX report (preview-limited) and answers with a cited stat and small table.
  - “What’s next?” → suggests next steps (e.g., run sweep, compare configs, queue training) with one-click actions.
- Data/APIs: `/assistant/query` (streaming), server-mediator tools for docs search, reports read, DB summaries, and (optional) pipeline execution after confirmation.
- Acceptance: cites sources; does not run compute without user confirmation; respects read-only constraints and parameter validation; provides concise, accurate answers.

---

## 13) Command Palette (P0)
- Purpose: Fast, keyboard-first navigation and actions across the app.
- Shortcut: `Cmd/Ctrl + K` to open; fuzzy search over commands and recent models.
- Actions (initial):
  - Open Composer (current model context if available; otherwise prompt to pick a model)
  - Open Designer (current model context or pick a model)
  - Create Model (open Template Picker)
  - Open Signals (choose: Leaderboard | Log | Analytics)
  - Open Docs (Docs launcher or specific doc by fuzzy match)
  - Open Health
- Behavior:
  - If user is inside a model context (Designer/Composer), actions scope to that `model_id` by default.
  - Otherwise, palette shows a model picker for model-scoped actions.
  - Results show command name, scope (e.g., model id), and destination route preview.
- Acceptance:
  - Opens with `Cmd/Ctrl + K`; closes with `Esc`.
  - Filters and executes in ≤150ms on local dev data scale.
  - Respects focus/ARIA roles; fully keyboard accessible.

## Cross-Cutting Requirements
- Routing: SPA routes for each page; 404 fallback.
- Client: typed API client; base URL from env; centralized error handling and toasts.
- Theming: app-level theme toggle in topbar; `prefers-color-scheme` default; pack `--accent` applied to key accents. See `ui/AppShell_Platform_v1.md` for platform behaviors and tokens.
- Tables: virtualization for large sets; sticky headers; accessible markup; optional sparklines column.
- Forms: client validation + server validation; inline field errors; clear `:focus-visible` outlines.
- Files: download endpoints for CSV/plots; handle auth-less local dev.
- Feature flags: enable P1/P2 features without code churn.
- Accessibility: keyboard shortcuts (Command Palette), high-contrast theme toggle, focus management on route change.

## Priorities Summary
- P0: Dashboard, Models (List/Detail), Create Wizard, Build/Train/Backtest, Sweeps, Leaderboard, Docs launcher.
- P1: Signals, Overlay, Health.
- P2: Run detail pages (backtest run/exp), admin tools, advanced pack/indicator editors.

## Acceptance (Release Gate)
- All P0 pages implemented with loading/empty/error states.
- Endpoints wired: `/models`, `/preview_matrix`, `/build_matrix`, `/train`, `/backtest`, `/backtest_sweep`, `/leaderboard`, `/model_card`.
- CSV/plot links working; tag filter functioning; “Train this combo” action present.
- Accessibility smoke pass on P0; lighthouse performance reasonable on desktop.


## 14) Admin (P1, admin-only)
- Purpose: Administer jobs, quotas, presets, packs, templates, flags, and users; monitor health and audit activity.
- RBAC: UI hidden for non-admins; backend enforces `role=admin`; non-admin access returns 403.

### Admin — Jobs (P1)
- Stories: view/retry/cancel sweeps and train jobs; inspect payload; see queue depth and worker status.
- Data/APIs: `GET /admin/jobs?status=&limit=&offset=`, `POST /admin/jobs/{id}/retry`, `POST /admin/jobs/{id}/cancel`.
- Acceptance: destructive actions require confirm; actions logged; pagination works; live refresh.

### Admin — Quotas & Limits (P1)
- Stories: view per-user quotas (sweeps/day, train concurrency/day); edit values; see usage & recent quota hits.
- Data/APIs: `GET /admin/quotas?user=`, `PATCH /admin/quotas { user_id, limits }`, `GET /admin/quotas/usage?user=`.
- Acceptance: edits audited; validate ranges; show effective limits and overrides with expiry.

### Admin — Risk Profiles (P1)
- Stories: edit global presets for Conservative/Balanced/Aggressive per pack (risk_budget fields); draft/publish workflow.
- Data/APIs: `GET /admin/risk-profiles`, `PATCH /admin/risk-profiles { pack_id, profile, risk_budget }`.
- Acceptance: changes versioned (`risk_profile_version`); publish requires confirmation; impacts new sweeps only.

### Admin — Packs Manager (P1)
- Stories: view packs; manage indicator sets registry; edit pack metadata; validate indicator coverage.
- Data/APIs: `GET /admin/packs`, `PATCH /admin/packs/{id}`, `GET /admin/indicator_sets?pack=`.
- Acceptance: edits audited; coverage warnings highlighted; links to docs/specs.

### Admin — Templates Manager (P1)
- Stories: CRUD templates; validate; draft/publish with version; attach to packs; preview YAML.
- Data/APIs: `GET /admin/templates`, `POST /admin/templates`, `PATCH /admin/templates/{id}`, `POST /admin/templates/{id}/publish`.
- Acceptance: schema validation; publish requires confirm; template usages listed.

### Admin — Feature Flags (P1)
- Stories: toggle non-critical features (Assistant execute-on, ad-hoc Backtest tab, Signals Leaderboard visibility).
- Data/APIs: `GET /admin/flags`, `PATCH /admin/flags { key, enabled }`.
- Acceptance: changes immediate; flagged in UI; logged.

### Admin — Data Health (P1)
- Stories: see DB connectivity, migrations status, cache policy, worker heartbeat; quick diagnostics.
- Data/APIs: `GET /admin/health`.
- Acceptance: green/yellow/red statuses; link to detailed health page; export diagnostics bundle.

### Admin — Audit & Logs (P1)
- Stories: recent admin actions stream; filter by user/action; export tail; link to full logs.
- Data/APIs: `GET /admin/audit?user=&action=&limit=&offset=`.
- Acceptance: includes request IDs; no secrets; export CSV.

### Admin — Users & Roles (P1)
- Stories: list users; assign roles (admin/editor/viewer); rotate API tokens; disable accounts.
- Data/APIs: `GET /admin/users`, `PATCH /admin/users/{id} { role }`, `POST /admin/users/{id}/rotate_token`.
- Acceptance: changes require confirm; audit log entries created; tokens shown once then masked.
