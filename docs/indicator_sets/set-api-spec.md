# API Specification — Set Operations

Base: `/indicator_sets`

List/CRUD
- GET `/indicator_sets` → list (query: `pack_id?`, `scope?`, `category?`, `owner?`, `limit`, `offset`)
- GET `/indicator_sets/{set_id}` → fetch (raw or resolved)
- POST `/indicator_sets` → create (body: `{ pack_id?, scope, model_id?, name, category, data, version? }`)
- PATCH `/indicator_sets/{set_id}` → update via JSON Patch or shallow merge
- POST `/indicator_sets/{set_id}/publish` → bump version and publish template

Validate
- POST `/indicator_sets/validate` → `{ ok, valid, errors, warnings: { redundancy, conflicts, cost_estimate } }`

Evaluate (On-Demand)
- POST `/indicator_sets/{set_id}/evaluate`
  - Body: `{ universe|symbols, start?, end?, timeframe?, overrides?, include_inputs?, out_format? }`
  - Response: `{ ok, matches|scores, data_uri?, lineage }`

Backtest
- POST `/indicator_sets/{set_id}/backtest`
  - Body: `{ universe|symbols, start, end, thresholds?, weights?, rules?, splits?, embargo?, tag?, save? }`
  - Response: `{ ok, leaderboard, artifacts, lineage }`

Optimize
- POST `/indicator_sets/{set_id}/optimize`
  - Body: `{ bounds, objective, backtest: { start, end, splits, embargo }, budget }`
  - Response: `{ ok, best_params, best_score, report_uri }`

Streaming
- WS `/ws/indicator_sets`
  - Subscribe: `{ action: 'subscribe', set_id, universe|symbols, timeframe, throttle_ms? }`
  - Server events: `{ type: 'match'|'score'|'heartbeat', payload }`

Artifacts & Lineage
- Include set JSON + SHA, component versions/timeframes, and git sha; persist artifacts when `save=true`.

