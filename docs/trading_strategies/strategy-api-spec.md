# API Specification — Trading Strategies

Base: `/strategies`

CRUD
- GET `/strategies` → list (query: `pack_id?`, `model_id?`, `tag?`, `owner?`, `limit`, `offset`)
- GET `/strategies/{strategy_id}` → fetch config, policy, indicator-set refs
- POST `/strategies` → create from template or components
- PATCH `/strategies/{strategy_id}` → update
- POST `/strategies/{strategy_id}/publish` → bump version

Backtest & Walk-Forward
- POST `/strategies/{strategy_id}/backtest` → `{ start, end, splits?, embargo?, tx_costs?, slippage?, tag?, save? }`
- POST `/strategies/{strategy_id}/walk_forward` → `{ windows, retrain?, params, tag?, save? }`

Optimize
- POST `/strategies/{strategy_id}/optimize` → `{ bounds, objective, budget, backtest: { ... } }`

Deploy & Monitor
- POST `/strategies/{strategy_id}/deploy` → `{ venue, paper|live, risk_profile, capital }`
- GET `/strategies/{strategy_id}/live_status`
- POST `/strategies/{strategy_id}/pause` | `/resume` | `/close_all`

Events (WebSocket)
- WS `/ws/strategies` → subscribe to signals/orders/fills/pnl

Artifacts & Lineage
- All runs persist config/policy/indicator-set refs + SHA, git sha, and artifacts (plots, reports, CSVs).

