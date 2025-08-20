Sigmatiq Sigma Mock API

Overview
- Purpose: FastAPI server that mocks SigmaLab API responses for UI work.
- Parity: Shapes mirror the real endpoints with safe static data.
- CORS: Enabled for all origins.

Quick Start
- Python 3.10+
- Install: pip install -r products/mock-api/requirements.txt
- Dev: make -C products/mock-api dev (reload on changes)
- Run: make -C products/mock-api run (port 8010)
- Docs: http://localhost:8010/docs

Endpoints
- GET `/`
  - Info + endpoints list
  - curl -sS http://localhost:8010/
- GET `/health`
  - { ok, version, now, deps }
  - curl -sS http://localhost:8010/health | jq .
- GET `/models`
  - { models: [{ id, config: { model_id, ticker, algo, pack }}, ...] }
  - curl -sS http://localhost:8010/models | jq .
- GET `/model_detail?model_id=<id>&pack_id=<pack>`
  - { ok, config, policy_valid, policy_source, execution_effective, policy_errors }
  - curl -sS "http://localhost:8010/model_detail?model_id=spy_opt_0dte_hourly&pack_id=zerosigma" | jq .
- GET `/indicator_sets`
  - { ok, groups: [{ group, indicators: [...] }] }
  - curl -sS http://localhost:8010/indicator_sets | jq .
- GET `/leaderboard?limit=&offset=`
  - { ok, rows, limit, offset, next_offset }
  - curl -sS "http://localhost:8010/leaderboard?limit=2&offset=0" | jq .
- GET `/signals?limit=&offset=`
  - Example model signals
  - curl -sS "http://localhost:8010/signals?limit=10" | jq .
- GET `/option_signals?limit=&offset=`
  - Example option signals
  - curl -sS "http://localhost:8010/option_signals?limit=5" | jq .
- GET `/policy/explain?model_id=&pack_id=`
  - { ok, schema_ok, schema_errors, execution_effective, checks }
  - curl -sS "http://localhost:8010/policy/explain?model_id=spy_opt_0dte_hourly&pack_id=zerosigma" | jq .
- POST `/calibrate_thresholds`
  - Body: { model_id, grid?, top_n?, ... }
  - Returns grid counts + recommended_threshold
  - curl -sS -X POST http://localhost:8010/calibrate_thresholds     -H "Content-Type: application/json"     -d '{"model_id":"spy_opt_0dte_hourly","grid":"0.5,0.55,0.6"}' | jq .
- POST `/scan`
  - Body: { pack_id, model_id, indicator_set, start, end, tickers|universe_csv, top_n }
  - Returns per-ticker scores
  - curl -sS -X POST http://localhost:8010/scan     -H "Content-Type: application/json"     -d '{"pack_id":"swingsigma","model_id":"universe_eq_swing_daily_scanner","indicator_set":"swing_eq_breakout_scanner","start":"2024-07-01","end":"2024-07-05","tickers":"AAPL,MSFT"}' | jq .
- POST `/build_matrix`
  - Body: { model_id, pack_id, start, end }
  - Returns { path, rows }
- POST `/preview_matrix`
  - Body: { model_id, pack_id, start, end }
  - Returns { nan_stats, columns, rows }
- POST `/train`
  - Body: { model_id, pack_id, csv?, calibration? }
  - Returns { model_out, rows, calibration }
- POST `/backtest`
  - Body: { model_id, pack_id }
  - Returns { summary: { sharpe, trades, win_rate, max_dd }, artifacts }

UI Integration Tips
- Point your UI API base to http://localhost:8010.
- Use `limit` and `offset` for pagination; `next_offset` is provided.
- Keep request shapes in sync with real API to avoid translation code later.

Extending
- Modify products/mock-api/mock_api/app.py to add/augment endpoints.
- If you need dynamic data, load from JSON files and run in `--reload`.

Troubleshooting
- Port conflict: change `--port` or Makefile.
- CORS issues: this mock sets permissive CORS; confirm dev server is using the same origin.
