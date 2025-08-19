Edge Lab Backlog

Scope: near-term priorities for the Edge Lab product (API/UI + packs), with crisp acceptance criteria. Use this list to drive the next sessions.

P0 — Now (1–2 weeks)
- Tests: /backtest_sweep + smoke
  - Add unit tests for sweep guards (min_trades, min_sharpe) and grid selection.
  - Add a lightweight integration test that mocks minimal matrix to exercise endpoints shape-only.
  - Acceptance: pytest passes locally; CI job stub present for shape tests.
- UI Sweeps polish
  - Add tag filter input; surface `report_path`; show trades/parity columns; CSV export; “Train this combo” action.
  - Acceptance: results table shows columns [thr|top_pct, allowed_hours, sharpe, cum_ret, trades, tag, parity?]; CSV exported with header.
- Parity in sweeps
  - When brackets are enabled in policy, compute parity summary per combo and include in returned runs and report JSON.
  - Acceptance: sweep JSON includes `parity` summary (ok, trades, hit_rates), and it renders in the UI when present.

P1 — Next (2–4 weeks)
- Leaderboard: deeper tags + aggregates
  - Add model-level aggregates and persistent tag filtering in store layer (edge_core or API service).
  - Acceptance: GET /leaderboard supports grouping by model_id; tag filter applies server-side.
- Observability & health
  - Structured logging + LOG_LEVEL env; expand `/healthz` with DB status + data coverage hints.
  - Acceptance: logs include request ids, timings; healthz returns `{ db:{ok}, data:{coverage%} }` for a probe ticker.

P2 — Later
- API quality-of-life
  - `/backtest_runs/{id}` to fetch a run+folds; pagination on sweeps if needed.
  - Acceptance: endpoint returns normalized run and folds with lineage + tag.
- Docs hygiene
  - Keep CONTRACT/runbooks current; prune archive periodically; add “Last audited” stamp to INDEX.
  - Acceptance: INDEX links valid (link check passes); AGENTS.md updated with any new conventions.

How we work this list
- Every session starts by reading AGENTS.md, INDEX.md, then this BACKLOG.
- We pick the top P0 item, implement, and check acceptance.
- We update this file as work completes or priorities shift.

Top 3 next actions (proposed)
1) Tests for /backtest_sweep + smoke (P0)
2) UI Sweeps: tag filter + columns + CSV + Train action (P0)
3) Parity in sweeps (compute + render) (P0)
