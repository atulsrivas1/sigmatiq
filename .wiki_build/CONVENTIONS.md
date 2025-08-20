Docs Conventions

- Product root: `products/sigma-lab/`.
- API start (Windows/macOS/Linux): `python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`.
- Env: place in `products/sigma-lab/.env` (POLYGON_API_KEY, DB_* including optional DB_SCHEMA=app).
- Outputs: all generated files live under `products/sigma-lab/{matrices,artifacts,live_data,static,reports}` by model id.
- Paths in examples use forward slashes; on Windows, they work in PowerShell/CMD as shown.
- Avoid external CLI deps in examples (no `jq`); show plain curl or Make.
- Package names: `sigma_core` (shared libs), `sigma_platform` (platform helpers). Product name: Sigma Lab.
- Leaderboard: supports `tag` filter for sweeps/smoke.

