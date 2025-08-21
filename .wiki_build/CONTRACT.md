Sigmatiq Sigma API Contract (v0)

Purpose: document stable response envelopes and core endpoint shapes to keep clients/SDKs resilient.

General rules
- All endpoints return a JSON object with `ok: boolean`.
- On failure, include `error: string`.
- For list endpoints, include `limit`, `offset`, `next_offset` when pagination applies.
- Additive only: new fields may be added; existing keys are not removed or renamed without versioning.

Endpoints

1) GET /signals
- Query: `model_id?`, `pack_id?`, `date? | start?/end?`, `tickers?`, `limit?`, `offset?`
- Response:
  { ok, count: number, rows: [ { date, model_id, ticker, side?, entry_mode?, entry_ref_px?, stop_px?, target_px?, time_stop_minutes?, rr?, score_*?, rank?, pack_id?, policy_version? } ], limit, offset, next_offset }
- Notes: `rows` may be empty when DB is not configured; include `warning`.

2) GET /leaderboard
- Query: `pack_id?`, `model_id?`, `tag?`, `limit?`, `offset?`, `order_by?`
- Response: { ok, rows: [ { id, model_id, pack_id, started_at, finished_at, metrics, params, best_sharpe_hourly?, best_cum_ret?, trades_total?, tag? } ], limit, offset, next_offset } or { ok:false, error }

3) GET /model_cards
- Query: `pack_id`, `model_id`, `limit?`, `offset?`
- Response: { ok, count, cards: [ { file, created_at?, event?, path } ], limit, offset, next_offset }

4) GET /model_card
- Query: `pack_id`, `model_id`, `file?`
- Response: { ok, json: object, markdown?: string, json_path: string, md_path?: string } or { ok:false, error }

5) POST /options_overlay
- Body: { model_id, pack_id?, date?, expiry?, dte_target?, option_mode?, spread_width?, side_override?, target_delta?, min_oi?, limit?, include_underlying_parity?, include_premium_parity?, write_parity_csv? }
- Response: { ok, count, written, date, expiry, parity?: { ok, trades, hit_rate }, parity_premium?: { ok, trades, hit_rate_target, hit_rate_stop, timeouts }, parity_csv?: string } or { ok:false, error }

6) GET /policy/explain
- Query: `model_id`, `pack_id?`
- Response: { ok, schema_ok, schema_errors: string[], execution_effective: object, checks: { ok, errors: string[], warnings: string[] } }

7) GET /healthz
- Query: `ticker?`, `pack_id?`, `model_id?`
- Response: { ok, checks: object, errors: object }

Compatibility
- Future changes should only add fields. Breaking changes require a versioned path prefix (e.g., /v1beta).
8) POST /backtest_sweep
- Body: { model_id, pack_id?, thresholds_variants?: string, allowed_hours_variants?: string, top_pct_variants?: string, splits?: number, min_trades?: number, min_sharpe?: number, tag?: string }
- Response: { ok, report_path, runs: [ { kind: 'thresholds'|'top_pct', allowed_hours?, thresholds?|top_pct?, res: { ok, result, best_sharpe_hourly, best_cum_ret, parity? } } ] } or { ok:false, error }
- Notes: When DB configured, each combination is persisted with the provided `tag` for later filtering via `/leaderboard?tag=...`.

