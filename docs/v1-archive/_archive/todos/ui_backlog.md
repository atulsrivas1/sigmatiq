Sigma Lab UI Backlog — Features & Improvements

Global/Navigation
- [ ] Global status bar: API health, DB connected, active TAG filter, pack theme
- [ ] Theme & pack selectors per session with localStorage persistence
- [ ] Keyboard shortcuts: g m (models), g s (signals), g b (backtest sweep)

Models
- [ ] Models table: pagination, search by id, pack filter
- [ ] Model detail drawer: config YAML, effective execution (policy), lineage badges
- [ ] Actions: Build (date picker), Train (hours), Backtest (quick form)
- [ ] Model cards listing and download (JSON/MD)

Signals
- [ ] Signals pagination (limit/offset); filters: date, ticker, side, rank, hours
- [ ] SignalCard: confidence bar (score_total), lineage badges, tags
- [ ] Parity/Overlay quickview if policy brackets enabled
- [ ] Export signals to CSV; copy curl for API

Backtest & Leaderboard
- [ ] Leaderboard table: order_by select, TAG filter, date window selector
- [ ] Row expansion: folds chart (Sharpe/Cum vs thr), trades histogram
- [ ] Open plots_dir and data_csv_uri links if present
- [ ] Compare top-N combos (diff view)

Backtest Sweep (panel)
- [ ] As listed in sweeps_ui_todo.md (report link, guards, presets, progress, actions)

Parity Wizard (future)
- [ ] Form to configure brackets (atr_period, mults, time_stop); run parity-only
- [ ] Report parity metrics per day; store CSV to reports and show link
- [ ] Option to sync brackets back into policy template

UX/Infra
- [ ] React Query for request caching and retries (health, models, leaderboard)
- [ ] Error boundary with friendly messages and troubleshooting links
- [ ] Loading skeletons for main panes; toasts for actions
- [ ] API client: timeouts, abort controller for long sweeps

Docs & Help
- [ ] In-app help links to runbooks and CONTRACT
- [ ] Quick tour for first-time users

