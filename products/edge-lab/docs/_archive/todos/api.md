API (edge_api/app.py)

Completed
- Path bootstrapping and package rename to `edge_core`.
- Added `GET /` index and `GET /healthz`.
- Pydantic request models for build/train/backtest.
- Pack-aware paths (`pack_id` param) across endpoints.
- Policy enforcement + validation endpoint; effective execution exposed in `/model_detail`.
- DB-backed leaderboard and backtest persistence.

Pending
- Structured logging (replace prints) with request context.
- Normalize backtest response keys for threshold vs top_pct.
