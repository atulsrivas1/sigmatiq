Sigmatiq Sigma Mock API

Overview
- Purpose: FastAPI server that mocks SigmaLab API responses for UI work.
- Parity: Shapes mirror the real endpoints with safe static data.
- CORS: Enabled for all origins.

Quick Start
- Python 3.10+
- Install: pip install -r products/sigma-lab/mock-api/requirements.txt
- Dev: make -C products/sigma-lab/mock-api dev (reload on changes)
- Run: make -C products/sigma-lab/mock-api run (port 8010)
- Docs: http://localhost:8010/docs
- Smoke: make -C products/sigma-lab/mock-api smoke (sets MOCK_API_URL or defaults to http://localhost:8010)

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
  - Accepts `model_id, pack_id, tag, risk_profile, pass_gate, limit, offset`
  - Returns `{ ok, rows, limit, offset, next_offset }`
  - Row fields include: `started_at, model_id, pack_id, sharpe, trades, win_rate, max_drawdown, cum_ret, tag, gate { pass, reasons[] }, lineage { matrix_sha, policy_sha, config_sha, risk_profile }`
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
  - Returns { path, rows, matrix_sha, profile { features, rows, label_balance, nan_pct } }
- POST `/preview_matrix`
  - Body: { model_id, pack_id, start, end }
  - Returns { nan_stats, columns, rows }
- POST `/train`
  - Body: { model_id, pack_id, csv?, calibration? }
  - Returns { model_out, rows, calibration }
- POST `/backtest`
  - Body: { model_id, pack_id }
  - Returns { summary: { sharpe, trades, win_rate, max_dd }, artifacts }

- POST `/models`
  - Body: { template_id, name, risk_profile }
  - Returns { ok, model_id, template_id, risk_profile }

- POST `/backtest_sweep`
  - Body: { model_id, risk_profile, sweep: { thresholds_variants[], hours_variants[], top_pct_variants[] }, tag? }
  - Returns { ok, rows: [ { kind, value, allowed_hours, sharpe, cum_ret, trades, gate { pass, reasons[] }, parity, capacity, tag, lineage, csv } ] }

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
