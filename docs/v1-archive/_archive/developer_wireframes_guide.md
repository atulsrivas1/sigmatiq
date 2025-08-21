# Sigma Lab UI — Developer Wireframes Guide (Authoritative)

This guide consolidates UI requirements, wireframes, component specs, actions/flows, and API mappings into one implementable document. It covers global elements and every page route with explicit component states and data contracts.

Conventions
- Routes are hash-based (e.g., `#/dashboard`).
- All endpoints are relative to the API root; query strings shown inline.
- JSON shapes are representative; fields may include additional keys from the backend without breaking the UI.
- Component names (Button, Drawer, Table) are logical; map to your component library equivalents.

Global Elements
- Risk Profile Selector (top-right)
  - Values: `conservative | balanced | aggressive | custom`.
  - Behavior: persists in `localStorage`; forwards `risk_profile` to Signals views; annotates Leaderboard/Sweeps guards.
  - States: default to `balanced` if missing; disabled when Admin modal open; tooltip: “Applies guardrails across metrics, sweeps, and training.”
- Gate Badges (inline chips)
  - Kinds: Momentum, Trades, MaxDD, ES95, Parity, Capacity.
  - States: pass (green), warn (amber), fail (red), n/a (grey). Tooltip shows reason keys (e.g., `min_trades_not_met`).
  - Placement: near run rows (Sweeps/Leaderboard) and in Designer header.
- Assistant (floating button, bottom-right)
  - Opens Drawer (right) with model/pack context; provides page‑aware suggestions, endpoint help, and “explain this panel”.
  - States: loading (typing indicator), error (retry), offline mode hint.
- Command Palette (Ctrl/Cmd‑K)
  - Data source: `docs/ui/command_palette.json`.
  - Actions navigate routes and can prefill forms (e.g., open Backtest with last config).
- Selection Cart (toolbar chip + Drawer)
  - Stores selected runs/templates/models across pages; actions: Train Selected, Compare, Export CSV; persists until user clears.

Layout/Styling Standards
- Grid: 12 columns, 24px gutters; breakpoints for desktop/tablet/mobile.
- Typography: 16px headers, 14px body, 13–14px table rows.
- States: skeletons for loading; inline banners for errors; empty states with CTA.
- Accessibility: WCAG AA; `:focus-visible` rings; keyboard nav across tabs, drawers, modals.

----------------------------------------------------------------

Page: Dashboard — Route `#/dashboard`
Purpose & Description
- Overview of recent activity and system health with quick actions.

Components & Placement
- Header Bar: Title + Risk Selector + Command Palette + Assistant.
- Quick Actions (3 Cards): Build Matrix, Run Backtest, Open Signals.
- Summary Leaderboard (Table, Top 10): Model, Pack, Sharpe, CumRet, Trades, Updated.
- Health Widget (Card): API ok, DB ok, data coverage.

Actions → Endpoints
- Load models: GET `/models?pack_id=<pack>` → `{ models: [{ id, config }] }`.
- Leaderboard: GET `/leaderboard?limit=10` → `{ ok, rows, limit, offset, next_offset }`.
- Health: GET `/healthz` → `{ ok, version, db_ok, coverage_pct, ... }`.

Wireframe (ASCII)
+-----------------------------------------------------------+
| Dashboard                       [Risk][Cmd][Asst]         |
+-----------------------------------------------------------+
| [Build Matrix] [Run Backtest] [Open Signals]              |
+----------------------+------------------------------------+
| Summary Leaderboard  | Health                             |
| Table (Top 10)       | - API: OK                          |
|                      | - DB: OK                           |
|                      | - Coverage: 92%                    |
+----------------------+------------------------------------+

States
- Loading: skeletons for cards/table.
- Empty: “No recent runs” with link to Sweeps.
- Error: banner with retry; console logs details.

----------------------------------------------------------------

Page: Packs Overview — Route `#/packs`
Purpose & Description
- Browse packs; jump to templates and models within a pack.

Components
- Packs Grid (Cards): name, description excerpt, counts (templates/models).
- Optional Sidebar Filters: by content (has templates/models).

Actions → Endpoints
- List packs: GET `/packs` → `{ ok, packs: [{ id, meta }] }` (meta from `pack.yaml` if present).

Wireframe
+-----------------------------------------------------------+
| Packs Overview                 [Risk][Cmd][Asst]          |
+-----------------------------------------------------------+
| [ Pack A ] [ Pack B ] [ Pack C ] ...                      |
|  - Templates: 12   - Models: 24                           |
+-----------------------------------------------------------+

States: loading cards, empty, error (retry).

----------------------------------------------------------------

Page: Pack Detail — Route `#/packs/:id`
Purpose & Description
- Pack metadata plus Templates/Indicator Sets/Recent Models tabs.

Components
- Meta Card: title, intro, links (repo/docs) from `pack.yaml`.
- Tabs: Templates | Indicator Sets | Recent Models.
  - Templates (Grid): `{ template_id, name, horizon, cadence, template_version }`.
  - Indicator Sets (List): `{ name }` with modified date.
  - Recent Models (Table): `{ model_id, created_at? }` with actions.

Actions → Endpoints
- Pack: GET `/packs/{pack_id}` → `{ ok, pack: { meta, indicator_sets, templates, models } }`.
- Templates: GET `/packs/{pack_id}/templates` → `{ ok, templates: [...] }`.
- Indicator Sets: GET `/packs/{pack_id}/indicator_sets` → `{ ok, indicator_sets: [...] }`.

Wireframe
+-----------------------------------------------------------+
| Pack: zerosigma                 [Risk][Cmd][Asst]          |
+----------------------+------------------------------------+
| Meta                 | Tabs: Templates | Indicator Sets   |
| - Description        |        | Recent Models             |
| - Links              | [Template Card][Template Card]     |
+----------------------+------------------------------------+

----------------------------------------------------------------

Page: Models List — Route `#/models`
Purpose & Description
- Browse/search models; open Designer or Composer; create models.

Components
- Toolbar: Pack Filter, Search, Create Model button.
- Models Table: columns Model, Pack, Horizon, Cadence, Last Backtest, Actions.

Actions → Endpoints
- Models: GET `/models?pack_id=<pack>` → `{ models: [{ id, config }] }`.

Wireframe
+-----------------------------------------------------------+
| Models                         [Risk][Cmd][Asst]          |
+-----------------------------------------------------------+
| [Pack=All] [Search...] [Create Model]                     |
+-----------------------------------------------------------+
| Model                         Pack  Horz Cad  LastBT  ...|
| spy_opt_0dte_hourly           zero  0dte hr   2025-08-12 |
+-----------------------------------------------------------+

States: loading table skeleton; empty with CTA; error with retry.

----------------------------------------------------------------

Page: Templates Gallery — Route `#/models/templates`
Purpose & Description
- Discover templates across packs; seed Create Model.

Components
- Filters: Pack, Horizon, Cadence, Search.
- Gallery: Template cards.

Actions → Endpoints
- List templates: GET `/model_templates?pack=<opt>` → `{ ok, templates: [{ pack, template_id, name, horizon, cadence, template_version }] }`.

Wireframe
+-----------------------------------------------------------+
| Templates Gallery               [Risk][Cmd][Asst]         |
+-----------------------------------------------------------+
| [Pack] [Horizon] [Cadence] [Search]                       |
+-----------------------------------------------------------+
| [Template][Template][Template] ...                        |
+-----------------------------------------------------------+

----------------------------------------------------------------

Page: Create Model — Route `#/models/new`
Purpose & Description
- Create a model from a template; prefill fields; persist assets.

Components
- Form: Template (picker), Ticker, Asset Type (opt|eq), Horizon, Cadence, Algo, Variant, Pack, Indicator Set (optional).
- Submit Button with validation feedback.

Actions → Endpoints
- Create: POST `/models`
  - Request: `{ ticker, asset_type?, horizon?, cadence?, algo?, variant?, pack_id?, indicator_set_name? }`.
  - Response: `{ ok, model_id, paths: { config, policy }, message }`.

Wireframe
+-----------------------------------------------------------+
| Create Model                    [Risk][Cmd][Asst]          |
+-----------------------------------------------------------+
| [Template] [Pack] [Ticker] [AssetType] [Horizon] [Cadence]|
| [Algo] [Variant] [IndicatorSet (opt)] [Submit]            |
+-----------------------------------------------------------+

States: client validation; success toast with links to Designer/Composer.

----------------------------------------------------------------

Page: Model Designer — Route `#/models/:id/designer`
Purpose & Description
- Edit indicator set and policy; validate; patch config.

Components
- Header: Model id, Pack, Gate Badges.
- Tabs: Indicator Set | Policy | Metadata.
  - Indicator Set Editor: form or YAML/JSON; validate indicator names/params.
  - Policy Editor: YAML; show Execution Effective summary (slippage_bps, size_by_conf, conf_cap, momentum_gate/column/min).
  - Metadata: render `config` YAML; inline form for partial patch.
- Validation Drawer (right): shows schema errors and suggestions.

Actions → Endpoints
- Validate Policy: GET `/validate_policy?model_id=&pack_id=` → `{ ok, path, errors: [] }`.
- Patch Config: PATCH `/models/{model_id}`
  - Request: `{ pack_id, config: { ...partial } }` → `{ ok, path, config }`.
- Upsert Indicator Set: POST `/indicator_sets`
  - Request: `{ pack_id, scope: 'pack'|'model', model_id?, name, indicators: [{name, ...params}] }`
  - Response: `{ ok, path, count, message }`.
- Detail Context: GET `/model_detail?model_id=&pack_id=` → `{ ok, config, config_yaml, policy, policy_json, policy_valid, policy_errors, execution_effective }`.

Wireframe
+-----------------------------------------------------------+
| Designer: spy_opt_0dte_hourly   [Risk][Cmd][Asst]          |
| Gate: [Momentum:Pass][Trades:Warn]                         |
+---------------------------+-------------------------------+
| Tabs: Indicators | Policy | Metadata                      |
| Editor (left)     | Validation Drawer (right)             |
+---------------------------+-------------------------------+

States: editor linting; validation status; save/patch success/failure.

----------------------------------------------------------------

Page: Composer — Build — Route `#/models/:id/composer/build`
Purpose & Description
- Build training matrix; QA profile; lineage/matrix_sha capture.

Components
- Build Form: Start, End, k_sigma, fixed_bp, distance_max, dump_raw, ticker.
- Actions: Run Build, Preview Matrix.
- Matrix QA Card: monotonic_time, non_negative_vol, session_alignment, iv_sanity, NaN stats.

Actions → Endpoints
- Build Matrix: POST `/build_matrix`
  - Request: `{ model_id, start, end, out_csv?, pack_id?, k_sigma?, fixed_bp?, distance_max?, dump_raw?, raw_out?, ticker? }` → `{ ok, out_csv }`.
- Preview Matrix: POST `/preview_matrix`
  - Request: `{ model_id, start, end, pack_id?, max_rows? }` → `{ ok, rows, qa: {...}, nan_stats: [...] }`.

Wireframe
+-----------------------------------------------------------+
| Composer: Build                 [Risk][Cmd][Asst]          |
+--------------------+--------------------------------------+
| Build Params       | Matrix QA (badged cards)             |
| [Start][End][... ] | - Monotonic: OK                      |
| [Run Build][Prev]  | - Vol: OK                            |
+--------------------+--------------------------------------+

States: pending (spinner on buttons), success toast with CSV path, error banner.

----------------------------------------------------------------

Page: Composer — Sweeps — Route `#/models/:id/composer/sweeps`
Purpose & Description
- Run threshold/hour/top% variants; apply guards; rank results.

Components
- Sweep Form: `thresholds_variants` (chips), `allowed_hours_variants` (chips), `top_pct_variants`, `splits`, `embargo`, guards (`min_trades`, `min_sharpe`).
- Results Table: Kind, Params, BestSharpe, BestCumRet, Total Trades, Tag, Gate Badges, Actions (Compare, Add to Selection, Backtest).

Actions → Endpoints
- Run Sweep: POST `/backtest_sweep`
  - Request: `{ model_id, pack_id?, thresholds_variants?, allowed_hours_variants?, top_pct_variants?, splits?, embargo?, allowed_hours?, save?, tag?, min_trades?, min_sharpe? }`.
  - Response: `{ ok, runs: [{kind, thresholds|top_pct, allowed_hours, result: {_summary, threshold_results...}}], count, filtered, report_path }`.

Wireframe
+-----------------------------------------------------------+
| Composer: Sweeps               [Risk][Cmd][Asst]           |
+-----------------------------+-----------------------------+
| Sweep Params                | Ranked Runs (table)         |
| [thr sets][hours][guards]   |  Kind Params BestSharpe ... |
| [Run Sweeps]                |  ...                        |
+-----------------------------+-----------------------------+

States: live ranking updates; CSV export of runs; Gate badges show reasons on hover.

----------------------------------------------------------------

Page: Composer — Leaderboard — Route `#/models/:id/composer/leaderboard`
Purpose & Description
- Browse saved backtest runs; filter/sort; select for training.

Components
- Filters: Tag, OrderBy (sharpe_hourly|cum_ret), pagination.
- Runs Table: Model, Started, BestSharpe, BestCumRet, Tag, Gate Badges, Actions.

Actions → Endpoints
- Leaderboard: GET `/leaderboard?model_id=&pack_id=&limit=&order_by=&offset=&tag=` → `{ ok, rows, limit, offset, next_offset, tag }`.

Wireframe
+-----------------------------------------------------------+
| Composer: Leaderboard          [Risk][Cmd][Asst]           |
+-----------------------------------------------------------+
| [Tag][OrderBy] [Prev|Next]                                 |
+-----------------------------------------------------------+
| Model Started BestSharpe BestCum Tag [Compare][Add]        |
+-----------------------------------------------------------+

----------------------------------------------------------------

Page: Composer — Backtest — Route `#/models/:id/composer/backtest`
Purpose & Description
- Re‑run a chosen configuration (single backtest) with parity summary.

Components
- Backtest Form: target, thresholds, splits, embargo, top_pct, allowed_hours, calibration, slippage_bps, size_by_conf, conf_cap, per_hour flags, momentum gate options.
- Result Cards: BestSharpe, BestCumRet, Parity (if brackets in policy).

Actions → Endpoints
- Backtest: POST `/backtest`
  - Request: `{ model_id, csv?, target?, thresholds?, splits?, embargo?, top_pct?, allowed_hours?, slippage_bps?, size_by_conf?, conf_cap?, per_hour_thresholds?, per_hour_select_by?, calibration?, pack_id?, momentum_gate?, momentum_min?, momentum_column?, save?, tag? }`.
  - Response: `{ ok, result, best_sharpe_hourly, best_cum_ret, parity? }`.

Wireframe
+-----------------------------------------------------------+
| Composer: Backtest             [Risk][Cmd][Asst]           |
+--------------------+--------------------------------------+
| Params             | Result Cards                         |
| [ fields... ]      | [BestSharpe][BestCum][Parity?]       |
| [Run]              | Thresholds table (expandable)        |
+--------------------+--------------------------------------+

----------------------------------------------------------------

Page: Composer — Train — Route `#/models/:id/composer/train`
Purpose & Description
- Queue training for selected runs; track jobs.

Components
- Selection Cart: shows pending runs; remove chips.
- Train Button: enqueues batch; show job IDs.
- Jobs Table (optional): job_id, model, status, started, updated.

Actions → Endpoints
- Train batch (planned): POST `/train/batch` → `{ ok, jobs: [{ job_id, model_id, status }] }`.
- Jobs list (planned): GET `/train/jobs?model_id=&risk_profile=&status=&limit=&offset=` → `{ ok, rows, ... }`.

Wireframe
+-----------------------------------------------------------+
| Composer: Train               [Risk][Cmd][Asst]            |
+-----------------------------------------------------------+
| Selection: [Run#1][Run#2] [Train Selected]                 |
+-----------------------------------------------------------+
| Jobs: job_id model status started updated                  |
+-----------------------------------------------------------+

States: pending, success (toasts), failure (retry).

----------------------------------------------------------------

Page: Signals — Route `#/signals`
Purpose & Description
- Monitor live signals; compare model performance; inspect logs and analytics.

Components
- Tabs: Leaderboard | Log | Analytics.
- Leaderboard Table: Model, Sharpe, Sortino, CumRet, Win%, Trades, Fill, Slip, Capacity, Freshness.
- Log Table: ts, model, ticker, side, entry_ref_px, slippage, status, rr, pnl, tag.
- Analytics: summary cards and charts (equity/drawdown, hour heatmap).

Actions → Endpoints
- Leaderboard: GET `/signals/leaderboard?pack=&risk_profile=&start=&end=&limit=&offset=` → `{ ok, rows: [{ model_id, period, metrics, lineage }], total }`.
- Summary: GET `/signals/summary?model_id=&risk_profile=&start=&end` → `{ ok, model_id, period, metrics }`.
- Log: GET `/signals?model_id=&start=&end=&tickers=&limit=&offset=` → `{ ok, count, rows, limit, offset, next_offset }`.

Wireframe
+-----------------------------------------------------------+
| Signals                        [Risk][Cmd][Asst]           |
+-----------------------------------------------------------+
| Tabs: Leaderboard | Log | Analytics                        |
| [Pack][Start][End][Prev|Next]                              |
| Table                                                   |
+-----------------------------------------------------------+

States: loading rows; empty (no signals); error banner with retry. Freshness badge shows seconds (tooltip: last ts).

----------------------------------------------------------------

Page: Options Overlay — Route `#/overlay`
Purpose & Description
- Transform stock signals to option overlays (single/vertical); parity checks; export/save.

Components
- Form: Model, Date, Expiry or DTE, Option Mode, Spread Width, Side Override, Target Delta, Min OI, Include Parity toggles.
- Overlay Table: OccSymbol, Expiry, Strike, Type, Delta, IV Used, Entry/Stop/Target Premium Est, Net Debit/Credit (vertical), Stop/Target Value.
- Actions: Run, Save/Replace, Export CSV.

Actions → Endpoints
- Overlay: POST `/options_overlay`
  - Request: `{ model_id, pack_id?, date?, expiry?, dte_target?, option_mode?, spread_width?, side_override?, target_delta, min_oi, limit, include_underlying_parity?, include_premium_parity?, write_parity_csv? }`.
  - Response: `{ ok, overlays: [...], written?, parity? }` (shape follows backend; treat fields leniently).
- Option signals (optional): GET `/option_signals?limit=&offset=` → `{ ok, rows, limit, offset, next_offset }`.

Wireframe
+-----------------------------------------------------------+
| Options Overlay                 [Risk][Cmd][Asst]          |
+--------------------+--------------------------------------+
| Params             | Overlay Results (table)              |
| [ ... ] [Run]      | OccSymbol Expiry Strike ...          |
| [Save][Export CSV] | ...                                  |
+--------------------+--------------------------------------+

----------------------------------------------------------------

Page: Health — Route `#/health`
Purpose & Description
- Display API/DB/data coverage; preview audit.

Components
- Status Cards: API OK, DB OK, Coverage %, Live freshness.
- Audit Table: path, method, status, model_id/pack_id, ts.

Actions → Endpoints
- Health: GET `/healthz`.
- Audit: GET `/audit?limit=10&offset=0` → `{ ok, rows, count, limit, offset, next_offset }`.

Wireframe
+-----------------------------------------------------------+
| Health                         [Risk][Cmd][Asst]           |
+---------------------+-------------------------------------+
| Status Cards        | Recent Audit                        |
+---------------------+-------------------------------------+

----------------------------------------------------------------

Page: Admin — Routes `#/admin/*` (Guarded)
Purpose & Description
- Admin-only management for jobs, quotas, risk profiles, packs, templates, flags, users.

Components (per sub-page)
- Toolbar: filters and bulk actions.
- Primary Table: per-entity columns.
- Drawer/Modal: details & edit forms.

Actions → Endpoints (all require `X-Admin-Token` or Bearer)
- Jobs: GET `/admin/jobs?status=&limit=&offset=`, POST `/admin/jobs/{job_id}/retry`, POST `/admin/jobs/{job_id}/cancel`.
- Quotas: GET `/admin/quotas?user=`, PATCH `/admin/quotas`.
- Risk Profiles: GET `/admin/risk-profiles`, PATCH `/admin/risk-profiles`.
- Packs: GET `/admin/packs`.
- Indicator Sets: GET `/admin/indicator_sets?pack=`.
- Templates: GET `/admin/templates`, POST `/admin/templates`, PATCH `/admin/templates/{template_id}`, POST `/admin/templates/{template_id}/publish`.
- Flags: GET `/admin/flags`, PATCH `/admin/flags`.
- Health: GET `/admin/health`.
- Audit: GET `/admin/audit?user=&action=&limit=&offset=`.
- Users: GET `/admin/users`, PATCH `/admin/users/{user_id}`, POST `/admin/users/{user_id}/rotate_token`.

Wireframe (Templates example)
+-----------------------------------------------------------+
| Admin: Templates               [Risk][Cmd][Asst]           |
+-----------------------------------------------------------+
| [New Template] [Search] [Pack]                            |
+-----------------------------------------------------------+
| TemplateID Name Pack Version [Edit][Publish]              |
+-----------------------------------------------------------+

States: NOT_IMPLEMENTED payloads currently; display guard (401/403) prompt for admin token.

----------------------------------------------------------------

Cross-Cutting Notes
- State Handling
  - Loading: skeletons for cards and tables; button spinners on long actions.
  - Errors: inline banners with retry; keep detailed message in console; show user-safe summary.
  - Empty: friendly text + CTA relevant to page (e.g., “Run Build” on Build tab).
- Tooltips & Hints
  - Use concise, single-line tooltips on metrics, columns, and gated chips; ensure keyboard accessible via focus.
- Deep Links & Filters
  - Persist filters in URL query (pack, tag, risk_profile, date ranges) for shareable state.
- Data Contracts (selected)
  - `/signals/leaderboard`: rows include `{ model_id, period: { start, end }, metrics: { sharpe, sortino, cum_return, win_rate, trades, fill_rate, avg_slippage, capacity, freshness_sec } }`.
  - `/signals/summary`: `{ metrics: same-as-above subset }`.
  - `/leaderboard`: `{ rows: [{ model_id, started_at, metrics or best_sharpe_hourly/best_cum_ret, tag, ... }], ... }`.
  - `/preview_matrix`: `{ qa: { monotonic_time: { ok, violations }, non_negative_vol: { ok, neg_pct }, session_alignment: { ok, off_pct }, iv_sanity: { ok, out_of_range_pct }, nan: { warn: [...], fail: [...] } }`.
  - `/backtest` result: `{ best_sharpe_hourly, best_cum_ret, parity? }` with `threshold_results` detail table for per-threshold metrics.

Implementation Checklist
- Routes & Nav should match `docs/ui/menu.json` and `docs/ui/command_palette.json`.
- Global: Risk Profile selector, Gate Badges, Assistant, Command Palette, Selection Cart wired on all pages.
- Forms: Validate inputs client‑side (dates, numeric ranges); disable submit while pending.
- Accessibility: keyboard path to all primary actions; focus trapping in modals only, not drawers.
- Performance: defer heavy content (plots) until expanded; paginate tables ≥ 50 rows.

Appendix: Quick Endpoint Map
- Packs: `/packs`, `/packs/{id}`, `/packs/{id}/templates`, `/packs/{id}/indicator_sets`.
- Models: `/models`, `/model_templates`, `/model_detail`, `PATCH /models/{id}`, `POST /indicator_sets`.
- Composer: `/build_matrix`, `/preview_matrix`, `/backtest`, `/backtest_sweep`, `/leaderboard`.
- Signals: `/signals`, `/signals/leaderboard`, `/signals/summary`, `/models/{id}/performance`.
- Overlay: `POST /options_overlay`, `GET /option_signals` (if available).
- Health/Audit: `/healthz`, `/audit`.
- Admin (guarded): `/admin/*` (stubs; RBAC via `X-Admin-Token`).

