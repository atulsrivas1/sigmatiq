Sigmatiq Sigma Core

Scope
- Shared Python library: datasets, features, indicators, models, backtests, evaluation, storage, registry.
- No API/UI in this repo when split — published as a package and consumed by product APIs/workers.

Backtests & Consensus — Quick Start
- Run API locally: `make api-run` (FastAPI on 8050)
- Apply migrations: `make db-migrate`
- One-off backtest: `POST /backtest/run` with `{ timeframe, universe, features, label }` (use `mode: "simple"` for preset thresholds/hours)
- Model sweep: `POST /models/{model_id}/backtest/sweep` with grid or `mode: "simple"`
- Pack backtest: `POST /packs/{pack_id}/backtest/run` (supports `consensus_override`)
- Leaderboard: `GET /backtests/leaderboard?pack_id=...` for top runs

Local Dev (placeholder)
- Test: pytest -q
- Lint/Type: ruff check .; black --check .; mypy .
- Build: python -m build (pyproject)

Notes
- In this workspace, sources live at products/sigma-core/sigma_core.
- Product Makefiles set PYTHONPATH to include this folder for local runs.

Repo vs Package Naming
- Repo folder uses kebab-case: `sigma-core` (human-friendly, URLs)
- Python package uses snake_case: `sigma_core` (import-friendly)
  This is why you see `products/sigma-core/sigma_core` — it’s expected.
