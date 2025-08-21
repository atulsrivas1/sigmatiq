Agents Guide — Sigma Lab (Persistent Conventions)

Use this as the single source of truth for future coding sessions. Keep it short, current, and product-first.

Core
- Product root: `products/sigma-lab/`.
- Start API: `python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`.
- Env: place in `products/sigma-lab/.env` (required: `POLYGON_API_KEY`; optional DB_* incl. `DB_SCHEMA=app`).
- Outputs live under `products/sigma-lab/{matrices,artifacts,live_data,static,reports}`.
- No external CLI deps in docs/scripts (no `jq`); use plain curl/Make.

DB & Migrations
- Per-product DBs supported; in dev a shared DB with per-product schemas is OK (`DB_SCHEMA=app|lab|sim|...`).
- Migrations live under `products/sigma-lab/api/migrations`.
- Leaderboard supports `tag` (e.g., sweeps/smoke) via `GET /leaderboard?tag=...`.

Make Targets
- Build: `make build MODEL_ID=<id> PACK_ID=<pack> START=<YYYY-MM-DD> END=<YYYY-MM-DD>`
- Train: `make train MODEL_ID=<id> ALLOWED_HOURS=13,14,15`
- Backtest: `make backtest MODEL_ID=<id> THRESHOLDS=0.55,0.60,0.65 SPLITS=5`
- Sweep: `make sweep MODEL_ID=<id> THRESHOLDS=... TOP_PCT=... ALLOWED_HOURS=... TAG=<name>`
- Smoke: `make smoke MODEL_ID=<id> START=<YYYY-MM-DD> END=<YYYY-MM-DD>` (conditional train + summary)

API Surfaces (stability)
- `/models`, `/preview_matrix`, `/build_matrix`, `/train`, `/backtest`, `/leaderboard`, `/options_overlay`.
- `/backtest_sweep` for grids; persists with `tag` when DB configured.
- Contract rules: additive only; version paths for breaking changes. See `CONTRACT.md`.

Packs & Paths
- Packs live under `products/sigma-lab/packs/<pack>/` with `indicator_sets/`, `model_configs/`, `policy_templates/`.
- Docs must reference product-scoped paths (avoid bare `packs/`, `matrices/`, `artifacts/`, `live_data/`, `static/`).

Indicators
- v2 indicators implemented in `sigma_core` and documented in REFERENCE:
  - `open_gap_z`, `first15m_range_z`, `atm_iv_open_delta`, `gamma_density_peak_strike`, `gamma_skew_left_right`, `dist_to_gamma_peak`.
- Keep `INDICATORS_BACKLOG.md` current; status for missing/implemented tracked in `missing_vs_repo.json` (`status` field).

Docs Hygiene
- Active docs under `products/sigma-lab/docs/`; historical content under `products/sigma-lab/docs/_archive/`.
- INDEX lists only current docs; Archived section links to `_archive/` (kept for reference).
- Conventions: `CONVENTIONS.md`; Backlog: `BACKLOG.md`.
- Vision and Execution docs are active and product-first.

Naming
- `model_id`: `<ticker>_<asset>_<horizon>_<cadence>[_variant]` (snake_case).
- Python packages: underscores (`sigma_core`, `sigma_platform`). Git repos: hyphens.

Windows
- Prefer `run_api.py` and quoted curl bodies in examples. Avoid shellisms that break on Windows.

Gotchas
- Avoid stale references (`uvicorn api.app:app`, bare `packs/`, `| jq`).
- Always write product-scoped paths in docs and examples.

