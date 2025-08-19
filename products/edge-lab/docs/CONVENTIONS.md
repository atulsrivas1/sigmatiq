Docs Conventions

- Product root: `products/edge-lab/`.
- API start (Windows/macOS/Linux): `python products/edge-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`.
- Env: place in `products/edge-lab/.env` (POLYGON_API_KEY, DB_* including optional DB_SCHEMA=app).
- Outputs: all generated files live under `products/edge-lab/{matrices,artifacts,live_data,static,reports}` by model id.
- Paths in examples use forward slashes; on Windows, they work in PowerShell/CMD as shown.
- Avoid external CLI deps in examples (no `jq`); show plain curl or Make.
- Package names: `edge_core` (shared libs), `edge_platform` (platform helpers). Product name: Edge Lab.
- Leaderboard: supports `tag` filter for sweeps/smoke.

