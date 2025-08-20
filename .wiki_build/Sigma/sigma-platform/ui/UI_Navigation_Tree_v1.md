# UI Navigation Tree — v1

## Status
Draft — aligns with BTB UI Spec v1 and AI Assistant Spec v1

## Canonical Pipeline

Primary workflow: Build → Sweeps (Backtests) → Leaderboard → Selection → Train.

- Build (Matrix): construct and profile the matrix; capture `matrix_sha`.
- Sweeps (Backtests): run configuration grid (thresholds/hours/top%); apply Risk Profile; Gate results.
- Leaderboard: compare, filter (Pass Gate only), and select best configs.
- Train: launch training only for selected, gate‑passing configs.

Note: The "Backtest" tab under Runs is for one‑off/ad‑hoc tests; the Sweeps page is the default backtesting surface for discovery.

## Tree & Objectives

- Dashboard (`#/dashboard`): At-a-glance status, quick actions, system health.
- Packs (`#/packs`): Explore packs and act in context.
  - Overview: description/scope, risk profile presets, indicator sets, docs.
  - Templates (Gallery): filtered by pack; "Use Template" opens Create preselected.
  - Recent Models in Pack: quick links (Compose/Design) for that pack.
- Models (`#/models`): Browse, create, and manage models.
  - List: Search/filter models; quick actions.
  - Templates (Gallery) — optional (`#/models/templates`): Browse templates; filter by pack/horizon; "Use Template" opens Create preselected.
  - Create Model (`#/models/new`): Template Picker (choose template → name → risk). Deep-link to Designer or Composer.
  - Designer (`#/models/:id/designer`): Edit indicator set/policy/metadata; save prompts rebuild.
  - Composer (`#/models/:id/composer`): Build → Sweeps → Leaderboard → Train pipeline for the saved model.
    - Build (`#/models/:id/composer/build`): Construct matrix; Matrix Profile; capture `matrix_sha`.
    - Sweeps (`#/models/:id/composer/sweeps`): Configure backtests; apply Risk Profile; Gate; add to Selection.
    - Leaderboard (`#/models/:id/composer/leaderboard`): Compare results; filter; “Pass Gate only”; select.
    - Train (`#/models/:id/composer/train`): Queue gate‑passing selections; progress; lineage.
- Signals (`#/signals`): Live monitoring and comparisons for signals.
  - Leaderboard: Live period metrics by model/risk (Sharpe, CumRet, Win, Trades, Fill, Slip, Capacity).
  - Log: Filterable signal entries/fills; CSV export.
  - Analytics: Equity/drawdown, calendar/hour heatmaps; parity/capacity (options).
- Options Overlay (`#/overlay`): Convert stock signals to options; parity/capacity checks; export.
- Health (`#/health`): API/DB/data coverage status; troubleshooting links.
- Docs (`#/docs`): Launch key documentation (runbooks, specs, policy schema).
- Assistant (drawer): Context-aware chat guidance; reads docs/DB/reports; suggests next actions (execution only on confirm).
- Selection Cart (drawer): Persistent list of chosen configs; batch compare/train handoff.

## Notes
- Risk Profile selector and Gate Badges are global UX elements that influence Sweeps, Leaderboard, and Train.
- This tree reflects the static-HTML-first UI; functionality will wire to API endpoints per BTB API Spec v1.

## ASCII Diagram

```
Sigma Lab UI
├─ Dashboard               (#/dashboard)
├─ Packs                   (#/packs)
│  ├─ Overview             (per-pack context)
│  ├─ Templates (Gallery)  (filtered by pack)
│  └─ Recent Models        (quick Compose/Design links)
├─ Models                  (#/models)
│  ├─ List                 (#/models)
│  ├─ Templates (Gallery)  (#/models/templates)  [optional]
│  ├─ Create Model         (#/models/new)
│  ├─ Designer             (#/models/:id/designer)
│  └─ Composer             (#/models/:id/composer)
│     ├─ Build             (#/models/:id/composer/build)
│     ├─ Sweeps            (#/models/:id/composer/sweeps)
│     ├─ Leaderboard       (#/models/:id/composer/leaderboard)
│     ├─ Backtest           (#/models/:id/composer/backtest)
│     └─ Train             (#/models/:id/composer/train)
├─ Signals                 (#/signals)
│  ├─ Leaderboard          (live comparisons)
│  ├─ Log                  (entries/fills)
│  └─ Analytics            (charts)
├─ Options Overlay         (#/overlay)
├─ Health                  (#/health)
├─ Docs                    (#/docs)
├─ Admin (admin-only)      (#/admin)
│  ├─ Jobs                 (#/admin/jobs)
│  ├─ Quotas & Limits      (#/admin/quotas)
│  ├─ Risk Profiles        (#/admin/risk-profiles)
│  ├─ Packs Manager        (#/admin/packs)
│  ├─ Templates Manager    (#/admin/templates)
│  ├─ Feature Flags        (#/admin/flags)
│  ├─ Data Health          (#/admin/health)
│  ├─ Audit & Logs         (#/admin/audit)
│  └─ Users & Roles        (#/admin/users)
└─ Drawers
   ├─ Assistant            (context-aware chat; read-only DB/CSV/XLSX; confirm to execute)
   └─ Selection Cart       (persistent selections; compare/train handoff)

Global: Risk Profile selector (C/B/A) • Gate Badges (pass/fail with tooltips)
```

## Menu Titles & Hover Descriptions

- Title: Dashboard — Hover: "At-a-glance status, quick actions, and system health."
- Title: Models — Hover: "Browse, create, edit, and run models."
  - Title: List — Hover: "Search and filter all models; open details."
  - Title: Templates (Gallery) — Hover: "Browse templates; filter by pack and horizon; use one to prefill Create."
  - Title: Create Model — Hover: "Pick a template, name it, choose risk."
  - Title: Designer — Hover: "Edit indicator set, policy, and metadata; save prompts rebuild."
  - Title: Composer — Hover: "Build → Sweeps → Leaderboard → Train for this model."
      - Title: Build — Hover: "Construct the training matrix; inspect Matrix Profile; copy matrix_sha."
      - Title: Sweeps — Hover: "Run backtests across thresholds/hours; apply Risk Profile; Gate results."
      - Title: Leaderboard — Hover: "Compare and filter backtest results; select configs to train."
      - Title: Train — Hover: "Queue only gate‑passing selections; monitor progress and lineage."
- Title: Signals — Hover: "Monitor live signals; compare models by live performance."
  - Title: Leaderboard — Hover: "Live period metrics (Sharpe, return, win, trades, fill, slip, capacity)."
  - Title: Log — Hover: "Filterable entries/fills with slippage, status, and PnL; export CSV."
  - Title: Analytics — Hover: "Equity/drawdown and calendar/hour heatmaps; parity/capacity charts."
- Title: Options Overlay — Hover: "Convert stock signals to options (single/vertical) with parity checks."
- Title: Health — Hover: "API/DB/data coverage status and troubleshooting."
- Title: Docs — Hover: "Open runbooks, specs, and reference documentation."
- Title: Admin — Hover: "Admin-only controls for jobs, quotas, risk profiles, packs, templates, flags, and users."
  - Title: Jobs — Hover: "Monitor/cancel/retry sweeps and training; view queue depth and worker health."
  - Title: Quotas & Limits — Hover: "View/edit per-user quotas for sweeps and training; see usage."
  - Title: Risk Profiles — Hover: "Manage global Conservative/Balanced/Aggressive presets per pack."
  - Title: Packs Manager — Hover: "Manage packs, indicator sets registry, and pack metadata."
  - Title: Templates Manager — Hover: "CRUD model templates; validate and publish versions."
  - Title: Feature Flags — Hover: "Toggle non-critical features (e.g., Assistant execute-on)."
  - Title: Data Health — Hover: "DB/migrations status, cache policy, workers; quick diagnostics."
  - Title: Audit & Logs — Hover: "Recent admin actions; export log tail; link to full logs."
  - Title: Users & Roles — Hover: "Assign roles (admin/editor/viewer); rotate API tokens."
- Title: Selection Cart (drawer) — Hover: "Persistent selected configs; compare or train in batch."
- Title: Assistant (drawer) — Hover: "Ask for help; reads docs/DB/CSV/XLSX; confirm before running jobs."

## Entry Points (No Overview)
- Dashboard: Quick Actions route directly to Composer (primary) or Designer.
- Command Palette: "Open Composer" / "Open Designer" actions scoped to a selected model.
- Models List: Row actions — primary: Compose; secondary: Design.

### Command Palette — Actions (initial)
- Open Composer (scoped to current model if in context; otherwise prompts to pick a model)
- Open Designer (scoped like above)
- Create Model (Template Picker)
- Open Templates (Gallery)
- Open Signals (Leaderboard | Log | Analytics)
- Open Docs (Docs launcher or direct doc fuzzy match)
- Open Health
- Open Admin: Jobs/Quotas/Risk Profiles/Packs/Templates/Flags/Users (admin-only)

## Feature Graph (Non‑menu view)

This graph shows feature dependencies, primary flows, and where each feature can be accessed from. Arrows denote typical progression; features are accessible from multiple entry points.

```
Templates → Create Model ─────────┐
                                   ├─► Designer (edit structure)
                                   │       │
                                   │       └─(Save changes that impact features/labels)► Prompt ► Composer: Build
                                   │
                                   └─► Composer: Build ──► Matrix (matrix_sha)
                                                        │
                                                        └─► Sweeps (Backtests) ──► Results ──► Leaderboard
                                                                                             │
                                                                                             └─► Selection Cart ──► Train ──► Artifacts (model)
                                                                                                                                     │
                                                                                                                                     └─► Signals: Log/Analytics/Leaderboard

Signals: Leaderboard ─► (row click) ► Model Performance (drawer)   Assistant (global) ─► opens any step (confirm to execute)

Options Overlay ◄─ from Signals (stocks) or Models (direct)       Health & Docs (global)
```

Feature entries & access points
- Templates
  - Primary: Create Model (Template Picker)
  - Secondary: Docs (templates catalog), Assistant (“recommend a template”)
- Create Model (Template Picker)
  - Primary: Models › Create Model; Dashboard CTA; Command Palette
  - Next: Open Composer (default) or Designer
- Designer (structure: indicator set, policy, metadata)
  - Primary: Models › Designer; Command Palette; success screen from Create
  - Cross‑link: Save with impactful changes prompts “Go to Composer › Build”
- Composer › Build (matrix)
  - Primary: Models › Composer › Build; Dashboard “Build”
  - Next: Sweeps; shows matrix_sha and Matrix Profile
- Composer › Sweeps (backtests)
  - Primary: Models › Composer › Sweeps; Dashboard “Open Sweeps”
  - Next: Leaderboard; Add to Selection
- Composer › Leaderboard (selection)
  - Primary: Models › Composer › Leaderboard
  - Next: Add to Selection; Train selected
- Composer › Train
  - Primary: Models › Composer › Train; Train Selected from Leaderboard/Cart
  - Output: Artifacts (model bundle) + run lineage
- Signals (Leaderboard | Log | Analytics)
  - Primary: Signals route; from Composer success messages
  - Cross‑link: Leaderboard rows open Model Performance (drawer)
- Options Overlay
  - Primary: From Signals (stock signals) or direct menu
- Health / Docs
  - Global menu and footer links
- Assistant (drawer)
  - Global; suggests next actions, reads Docs/DB/CSV/XLSX; confirm‑to‑execute for runs

Guardrails & lineage hand‑offs
- Designer → (Save) → Composer Build (when features/labels changed)
- Build → Sweeps (matrix_sha carried)
- Sweeps → Leaderboard (Gate applied; configs normalized)
- Leaderboard → Selection Cart → Train (gate‑passing enforced by default)
- Train → Signals (live performance measured, linked back via lineage)

## Feature Prerequisites
- Composer › Sweeps
  - Requires a built matrix and `matrix_sha` (from Build). Show CTA to Build if missing.
- Composer › Leaderboard
  - Requires completed sweeps/backtests persisted; otherwise prompt to run Sweeps.
- Composer › Train
  - Requires non-empty Selection Cart; by default only gate‑passing configs enqueue (overrides require confirmation and tag).
- Signals (Leaderboard/Log/Analytics)
  - Requires signals log data; display Coverage % and Freshness; show N/A when insufficient.
- Options Overlay
  - Requires stock signals (for stock→options overlay) or options context; parity/capacity data improves analytics.
- Designer
  - Saving changes that affect features/labels invalidates prior matrix; prompt to rebuild in Composer › Build.
- Performance Drawer (from Composer/Signals)
  - Shows live 30d by default if signals exist; otherwise falls back to latest backtest snapshot when available.

