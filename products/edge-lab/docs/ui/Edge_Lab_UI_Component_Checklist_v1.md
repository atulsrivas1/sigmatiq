# Edge Lab UI — Component Checklist (v1)

Purpose: Lock down per-route components, API calls, events, and data flow for P0 pages. Use this to scaffold the UI consistently.

Conventions
- All API calls via a typed client; base URL from env.
- Each page exports a root component and child components for sections (filters, table, panels).

---

## `/` Dashboard
- Components
  - `DashboardPage`
    - `RecentModelsCard`
    - `LastRunsCard`
    - `QuickActionsCard`
    - `HealthCard`
  - Cross-cutting in shell: `ThemeToggle`, `DensitySwitch`, `CommandPalette`
- API
  - GET `/models?limit=5`
  - GET `/leaderboard?limit=5`
  - GET `/healthz`
- Events
  - Click [Create Model] → `/models/new`
  - Click [Run Backtest] → `/runs?tab=backtest`
  - Click [Open Sweeps] → `/sweeps`
- Data Flow
  - Fetch on mount; show skeletons; on error show card-level retry.

## `/models` Models List
- Components
  - `ModelsListPage`
    - `ModelsFilters` (search, pack)
    - `ModelsTable` (density-aware; optional `SparklineCell` for PnL/hit-rate)
    - `Pagination`
- API
  - GET `/models?search=&pack_id=&limit=&offset=`
- Events
  - Search input debounced → refetch
  - Pack select → refetch
  - Row [Open] → `/models/:modelId`
  - Row [Backtest] → `/runs?model_id=...&tab=backtest`
  - [Create Model] → `/models/new`
- Data Flow
  - Keep query params in URL; preserve on refresh; expose total count when available.

## `/models/new` Create Wizard
- Components
  - `CreateModelWizard`
    - steps: `BasicsStep`, `IndicatorSetStep`, `PolicyStep`, `PreviewStep`, `SaveStep`
- API
  - POST `/models`
  - POST `/indicator_sets`
  - GET `/validate_policy?model_id=&pack_id=`
  - POST `/preview_matrix`
- Events
  - Validate → enable Next; Preview → show result; Create → navigate to detail
- Data Flow
  - Local wizard state; write files via API; show path confirmation.

## `/models/:modelId` Model Detail
- Components
  - `ModelDetailPage`
    - `TrustHUD` (integrity/parity/capacity badges)
    - `LineageChips` (`pack_sha • config_sha • policy_sha`, clickable)
    - `SummaryPanel` (features/policy/latest)
    - `QuickRunPanel` (build/train/backtest)
    - `ShortcutsPanel`
- API
  - GET `/models?model_id=...`
  - GET `/leaderboard?model_id=...&limit=5`
  - GET `/model_card?model_id=...&pack_id=...`
  - POST `/build_matrix`, `/train`, `/backtest`
- Events
  - Quick run buttons open side panels; submit triggers API; toast results
  - Links open Sweeps/Leaderboard/Signals/Overlay
- Data Flow
  - Refetch after actions to update latest state.

## `/runs` Build/Train/Backtest
- Components
  - `RunsPage` (tabs: Build, Train, Backtest)
    - `BuildTab`
    - `TrainTab`
    - `BacktestTab`
      - (P1) `ParityPanel` (underlying vs premium)
      - (P1) `CalendarHeatmap` (daily sharpe/hit-rate)
- API
  - POST `/build_matrix`
  - POST `/train`
  - POST `/backtest`
  - GET `/leaderboard?model_id=...&limit=1` (open latest)
- Events
  - Submit forms; show plots/metrics on success; link to leaderboard
- Data Flow
  - Keep last payload in local state for retry.

## `/sweeps` Sweeps
- Components
  - `SweepsPage`
    - `SweepsControls`
    - `WhatIfPanel` (threshold/top‑N/hours → delta chips)
    - `SweepsResultsTable` (columns: thr/top_pct, hours, sharpe, cum_ret, trades, parity, capacity, risk, tag; row expander → per-fold/parity)
- API
  - POST `/backtest_sweep`
  - GET `/leaderboard?model_id=...&tag=...` (optional)
- Events
  - Run Sweep → load results into table; Export CSV; Train this combo
- Data Flow
  - Persist tag in URL params; save last results in in-memory store for navigation.

## `/leaderboard` Leaderboard
- Components
  - `LeaderboardPage`
    - `LeaderboardFilters` (model, pack, tag, sort, density)
    - `LeaderboardTable` (optional sparkline column)
    - `Pagination`
- API
  - GET `/leaderboard?model_id=&pack_id=&tag=&order_by=&limit=&offset=`
- Events
  - Filter changes → refetch; Row click → open drawer with plots (P2: run detail)
- Data Flow
  - Keep filters in URL; allow bookmarking; apply client-side secondary filters when needed.

## `/docs` Docs Launcher
- Components
  - `DocsLauncher`
- Links
  - `AGENTS.md`, `BACKLOG.md`, `runbooks/*`, `indicators/REFERENCE.md`, `policy_schema.md`
- Events
  - Click → open in new tab

---

## Cross-Cutting Components
- `AppShell` (Topbar, Sidebar, Footer)
- `ToastCenter` (success/error notifications)
- `ErrorBanner` (server error rendering)
- `SkeletonTable`, `SkeletonCard`
- `CsvDownloadButton` (given a data array/URL)
- `ThemeToggle` (sets `data-theme` on `html`; respects `prefers-color-scheme` + `localStorage`)
- `DensitySwitch` (sets `data-density` on root; affects table/card spacing)
- `CommandPalette` (Ctrl/⌘+K quick actions: build/train/backtest, open docs)

## API Client (typed)
- `getModels`, `createModel`, `validatePolicy`, `previewMatrix`
- `buildMatrix`, `trainModel`, `backtestModel`, `backtestSweep`
- `getLeaderboard`, `getModelCard`, `getHealthz`
  
Optional additions (P1)
- `getSignalsSummary` (for parity/heatmap context)
- `getBacktestRun` (fetch a run + folds for parity/expander)

## Patterns
- URL query state for filters/pagination; persist across reloads.
- Retry logic with exponential backoff on 5xx/429; graceful abort on cancel.
- Defensive parsing for optional fields (DB off scenarios).
- Accessibility: `:focus-visible` ring via `--ring` on all interactive controls (buttons, chips, rows, links).
- Theming: semantic tokens (`--surface-1/2`, `--text-inverse`, `--border-strong`, `--ring`), pack `--accent`.
