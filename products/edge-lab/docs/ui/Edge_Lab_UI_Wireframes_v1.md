# Edge Lab UI — Wireframes (v1)

Scope: Edge Lab (authoring + evaluation). ASCII wireframes for P0 pages with detailed columns, filters, states, and interactions. See Requirements: `ui/Edge_Lab_UI_Requirements_v1.md`.

Conventions
- Shell: top bar + collapsible left sidebar + main content.
- Accent: pack color via `data-edge`/`--accent` token.
- Theming: theme toggle in top bar (light/dark/slate/paper) with `prefers-color-scheme` default.
- Density: density switch in top bar (compact/cozy/comfortable) that affects table/card spacing.
- States: [loading], [empty], [error] placeholders on lists and detail panes.

---

## Routes
- `/` → Dashboard
- `/models` → Models List
- `/models/new` → Create Model Wizard
- `/packs` → Packs Overview
- `/models` → Models List
- `/models/templates` → Templates Gallery (optional)
- `/models/new` → Create Model (Template Picker)
- `/models/:modelId/designer` → Designer (structure)
- `/models/:modelId/composer/build|sweeps|leaderboard|train` → Composer tabs
- `/signals` → Signals (Leaderboard | Log | Analytics)
- `/docs` → Docs launcher
- `/admin/*` → Admin (admin-only)

---

## Canonical Pipeline (Note)
Build → Sweeps (Backtests) → Leaderboard → Selection → Train.

- Build: construct matrix and inspect Matrix Profile; capture `matrix_sha`.
- Sweeps: run configuration grid (thresholds/hours/top%); apply Risk Profile; Gate results.
- Leaderboard: compare, filter (Pass Gate only), and select.
- Train: launch training only for selected, gate‑passing configs.

Backtest under Runs is for ad‑hoc tests; discovery should use Sweeps.

---

## Layout Shell
```
+--------------------------------------------------------------------------------+
| Topbar: [☰] Edge Lab    [Search ⌘K]   [Theme ◑] [Density ▾]    [Docs] [Health] [User] |
+---------+----------------------------------------------------------------------+
| Sidebar | Dashboard                                                            |
| [ ]Dash | Models                                                               |
| [ ]Mods | Build/Train/Backtest                                                 |
| [ ]B/T/B| Sweeps                                                               |
| [ ]Swps | Leaderboard                                                          |
| [ ]Ldbd | Docs                                                                 |
+---------+----------------------------------------------------------------------+
| Footer (status bar: API base, ENV, health hint)                                |
+--------------------------------------------------------------------------------+
```

---

## Dashboard (P0)
```
+----------------------------+  +--------------------------------------------+
| Recent Models              |  | Last Runs                                   |
| model_id           Actions |  | time                model_id     action     |
| spy_opt_0dte...   [Open]  |  | 2025-08-16 11:50   spy_opt...    Backtest   |
| spy_eq_swing...   [Open]  |  | 2025-08-15 16:10   spy_eq...      Train     |
+----------------------------+  +--------------------------------------------+

+----------------------------+  +--------------------------------------------+
| Quick Actions              |  | Health                                      |
| [Create Model]            |  | API: ok  DB: warn  Data: ok                  |
| [Run Backtest] [Sweeps]   |  | [View details] → /health                     |
+----------------------------+  +--------------------------------------------+
```
Details
- Recent Models columns: model_id, pack_id, updated_at, [Open] → detail.
- Last Runs columns: time, model_id, action, status; link to plots/leaderboard where applicable.
- Health: shows API/DB/data coverage quick status; link to health page.
- Empty states: “No recent models yet” with CTA [Create Model].

---

## Models — List (P0)
```
Filters: [Search model_id…] [Pack ▼]     [Create Model]

+----------------------------------------------------------------------------------------------+
| model_id                | pack_id   | updated_at        | sharpe | pnl ▶   | actions         |
| spy_opt_0dte_hourly     | zeroedge  | 2025-08-16 11:50  |  2.41  | ▷▴▴▵▴   | [Open] [Run]    |
| spy_eq_swing_daily      | swingedge | 2025-08-15 16:10  |  1.12  | ▷▵▵▴▵   | [Open] [Run]    |
| aapl_eq_intraday_hourly | swingedge | 2025-08-14 10:20  |  0.85  | ▷▵▴▵▵   | [Open] [Run]    |
+----------------------------------------------------------------------------------------------+
Actions (row): [Open] [Sweeps] [Backtest]
Pagination: « 1 2 3 »  rows/page: 20 (density switch affects row height)
```
Details
- Search matches model_id prefix/substring; Pack filter narrows results; sort by updated_at default.
- Keyboard: Tab through filters; table rows focusable; Enter opens detail.
- Empty: “No models match your filters.” CTA [Clear filters].
- Error: banner with retry; show last successful fetch timestamp.

---

## Models — Create (Template Picker) (P0)
```
Step 1: Choose Template
[ ZeroEdge Starter ]  [ Swing Momentum ]  [ Long Trend ]  [ Overnight Gap ]
Card: pack, horizon, cadence, short description

Step 2: Name & Risk
Model Name [__________]   Model ID preview: spy_opt_0dte_hourly
Risk: (o) Conservative  (•) Balanced  ( ) Aggressive

Step 3: Create
[Create and Open Composer]   [Create and Open Designer]
Success: “Model created from ZeroEdge Starter”
```
Details
- Disable Next until required fields valid; show inline errors.
- Preview failure shows reasons (NaN %, missing data); allow back to adjust.
- Success navigates to Model Detail.

---

## Model Context & Performance Drawer (P1)
```
Context Bar (visible on Designer & Composer)
[model_id] [pack] [risk badge] [template tag]  Lineage: [pack@a1b2] [policy@e5f6] [matrix@c7d8]
Actions: [Open Designer] [View Performance]


- Features: indicator_set: zeroedge_pin_drift_v1
- Policy: execution.momentum_gate=false  [Validate]
- Latest: Build (2025-08-15), Backtest (2025-08-16)


[Integrity OK] [Parity -2.1%] [Capacity Medium]   Lineage: [pack@a1b2] [policy@e5f6]


[Build] Start/End | [Train] Allowed Hours | [Backtest] Thr/Top% Splits [Run]


[Open Sweeps] [Open Leaderboard] [Open Signals] [Options Overlay]
```
Details
-  opens side panels with forms and submit; shows progress + toasts.
- Links route to their dedicated pages with model preselected.

Performance Drawer (opens over current page)
```
Period [Last 30d ▼]
Cards: [ Sharpe 1.18 ] [ Cum Ret +6.2% ] [ Win 58% ] [ Trades 142 ] [ Fill 87% ] [ Slip $0.03 ]
Charts: [ Equity/Drawdown ]   [ Calendar Heatmap ]   [ Hour Heatmap ]
Parity/Capacity (options): [ Spread dist ] [ OI/ADV bars ]
Data freshness: 12m ago; Coverage: 98%
```

---

## Build / Train (P0)
```
Tabs: [Build] [Backtest] [Train]

Build
Start [____]  End [____]   [Run Build]
[loading…]  Result: matrix path + preview link

Train
Allowed Hours [13,14,15]   [Run Train]
[done]  Artifact: artifacts/spy_opt_0dte_hourly/gbm.pkl

Backtest (re‑run Sweeps config)
Selected: Thr [0.60]  Top% [—]  Hours [13,14,15]  Splits [5]  Matrix [c7d8]  Tag [rerun-2025-08-16]
Date: Start [____]  End [____]   [Run Backtest]
Plot: cum_returns.png
Metrics: sharpe, cum_ret, trades; [Open Leaderboard]

(P1) Parity Panel
- Underlying vs Premium parity summary for period tested

(P1) Calendar Heatmap
- Daily hit rate / sharpe with hover tooltips

(BTB v1)
- Show `matrix_sha` and [Matrix Profile] button (modal with NaN%, label balance, leakage flags, coverage by hour/day).
- Train tab only enables gate‑passing selections by default; overrides prompt for confirmation.
```
Details
- Show last run timestamp, payload echo (sanitized), and links to artifacts.
- Error panel shows validation errors from server; enable retry.

---

## Packs — Overview (P0)
```
Header: zeroedge  [Open Docs]

Presets: [Conservative] [Balanced] [Aggressive] (risk budgets summary)
Indicator Sets: [ zeroedge_core_v2 ] [ pin_drift_v1 ] [ headfake_v2 ] [view all]
Templates (Gallery): [ ZeroEdge Starter ] [ Opening Drive ] [ Gamma Unwind ]  [View All]
Recent Models in Pack:  spy_opt_0dte_hourly  [Compose] [Design]

[Create Model from this Pack]
```

---


## Sweeps (P0)
```
Controls
Risk Profile [Conservative | Balanced | Aggressive]
Thresholds variants [0.50,0.52,0.54 | 0.55,0.60,0.65]
Allowed hours variants [13,14|13,14,15]
Top % variants [0.10,0.15]
Guards (per profile): Min trades [5]  Max DD [%] [20]  ES95× [2.0]  Spread [%prem] [10]  OI [500]  Volume [200]
Tag [demo]   [Run Sweep]

What‑if Panel
- Threshold [====|---]   Δ +0.18 Sharpe   Δ −22 Trades

Results (Gate + actions)
+--------------------------------------------------------------------------------------------------------------+
| kind    | thr/top% | allowed_hours | sharpe | cum_ret | trades | Gate | parity | capacity | tag  | CSV | act          |
| top_pct | 0.10     | 13,14         | 0.41   | 0.9999  | 1      | FAIL |  —     |  high    | demo | [↧] |[Add] [Compare]|
| thr     | 0.60     | 13,14,15      | 0.33   | 0.9999  | 1      | PASS |  ok    | medium   | demo | [↧] |[Add] [Compare]|
+--------------------------------------------------------------------------------------------------------------+
[Export All CSV]  Selection Cart [2]
```
Details
- If parity available from policy brackets, show parity column with hit rates.
- Row actions: train with selected params; open leaderboard filtered by tag.
- Empty: “No results. Adjust variants or relax guards.”

---

## Leaderboard (P0)
```
Filters: Model [spy_opt_0dte_hourly]  Pack [zeroedge]  Risk [Balanced]  Pass Gate only [✓]  Tag [demo]  Sort [sharpe ▼]  Density [▾]

+--------------------------------------------------------------------------------+
| started_at         | model_id            | best_sharpe | best_cum_ret | Gate | tag | act           |
| 2025-08-16 11:50   | spy_opt_0dte_hourly | 0.41        | 0.9999       | PASS | demo| [Add] [Compare]|
| 2025-08-15 16:10   | spy_opt_0dte_hourly | 0.33        | 0.9999       | FAIL | smoke| [Add] [Compare]|
+--------------------------------------------------------------------------------+
Selection Cart [2]
Pagination: « 1 2 3 »
```
Details
- Tag chip inputs (type ahead); server filter via `tag` query supported.
- Row click opens run detail (P2); for now opens plots/metrics drawer.

---

## Signals (P1)
Tabs: [Leaderboard] [Log] [Analytics]

Leaderboard
```
Filters: Pack [zeroedge]  Risk [Balanced]  Period [Last 30d]  Pass Gate only [ ]

+-----------------------------------------------------------------------------------------------------------+
| model_id             | risk | period          | Sharpe | CumRet | Win | Trades | Fill | Slip | Capacity | tag |
| spy_opt_0dte_hourly  |  B   | 2025-07-18→08-16|  1.18  | 6.2%   | 58% | 142    | 87%  | 0.03 | Medium   | live|
+-----------------------------------------------------------------------------------------------------------+
```

Log
```
Filters: Date [2025-08-16]  Ticker [____]  Status [all]
+--------------------------------------------------------------------------------------------------------------+
| ts                | model_id             | side | entry_ref_px | fill_px | slippage | status  | rr  | tag |
| 2025-08-16 09:30  | spy_opt_0dte_hourly | long | 447.35       | 447.37  | 0.02     | filled  | 1.8 | live|
+--------------------------------------------------------------------------------------------------------------+
[Export CSV]
```

Analytics
```
Charts: [ Equity/Drawdown ]  [ Calendar Heatmap ]  [ Hour Heatmap ]  [ Parity/Capacity (options) ]
```

## Docs Launcher (P0)
```
Open Docs
[AGENTS.md] [BACKLOG.md] [Runbooks] [Indicators REF] [Policy Schema]
```

---

## States & Accessibility
- Loading: skeleton rows in tables; shimmer in cards.
- Empty: message + CTA where applicable (Create, Clear filters, Adjust guards).
- Error: banner with retry; preserves user inputs.
- Keyboard: Tab order follows layout; buttons and interactive chips/rows have visible `:focus-visible` rings.
- ARIA: landmarks (header/nav/main/footer); labels on controls.

## Responsive
- Tables collapse to cards; filters move into a drawer on small screens.
- Wizard uses full-screen modal on mobile; Next/Back pinned at bottom.

---

## Micro Wireframes — States (P0)

Tables (List/Leaderboard/Sweeps)
```
Loading
+----------------------------------------------+
| ██████████████████████████████████████████   |
| ██████████████████████████████████████████   |
| ██████████████████████████████████████████   |
+----------------------------------------------+

Empty
+----------------------------------------------+
| No results match your filters.               |
| [Clear filters]                              |
+----------------------------------------------+

Error
+----------------------------------------------+
| Error loading data. [Retry]                  |
| Details: <short message>                     |
+----------------------------------------------+
```

Cards (Dashboard)
```
Loading: show 2–3 shimmering rectangles in each card slot
Empty: "No recent models yet." [Create Model]
Error: banner in card + [Retry]
```

Forms (Wizard / )
```
Loading: disable submit, show inline spinner
Validation: field-level error below input, summary banner for multi-field issues
Error: server error banner with payload excerpt (first line), [Retry]
Success: toast + link to next page (e.g., Model Detail or Leaderboard)
```
