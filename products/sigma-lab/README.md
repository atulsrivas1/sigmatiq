Sigma Lab — Product

- API package: `products/sigma-lab/api` (FastAPI app with routers/services)
- UI: `products/sigma-lab/ui` (to be split into a standalone repo later)
- Migrations: `products/sigma-lab/api/migrations`
- Data/artifacts: `products/sigma-lab/{matrices,artifacts,live_data,static,reports}`

Run locally
- Env: set `POLYGON_API_KEY` and optional DB settings in `products/sigma-lab/.env` (supports `DB_SCHEMA`, default `app`).
- Start API: `python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload`

Common Make targets
- Build: `make build MODEL_ID=<id> PACK_ID=<pack> START=<YYYY-MM-DD> END=<YYYY-MM-DD>`
- Train: `make train MODEL_ID=<id> ALLOWED_HOURS=13,14,15`
- Backtest: `make backtest MODEL_ID=<id> THRESHOLDS=0.55,0.60,0.65 SPLITS=5`
- Sweep: `make sweep MODEL_ID=<id> THRESHOLDS=... TOP_PCT=... ALLOWED_HOURS=... TAG=<name>`
- Smoke: `make smoke MODEL_ID=<id> START=<YYYY-MM-DD> END=<YYYY-MM-DD>`
- Leaderboard: `curl -sS "http://localhost:8001/leaderboard?model_id=<id>&tag=<name>"`

References
- Docs index: `products/sigma-lab/docs/INDEX.md`
- Conventions: `products/sigma-lab/docs/CONVENTIONS.md`
- API Contract: `products/sigma-lab/docs/CONTRACT.md`
