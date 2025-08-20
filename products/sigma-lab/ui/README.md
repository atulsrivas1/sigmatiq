# Sigma Lab UI — Dev Guide

Local API configuration
- The UI calls a relative `/api` path by default. In dev, Vite proxies `/api` to the Mock API.
- To override, set `VITE_API_BASE_URL` (see `.env.development.local.example`).

Mock API
- Start mock: `make -C products/sigma-lab/mock-api dev` (http://localhost:8010)
- Smoke test: `make -C products/sigma-lab/mock-api smoke`

UI Dev
- Install deps: `cd products/sigma-lab/ui && npm install`
- Run: `npm run dev`
- Vite proxy (configured in `vite.config.ts`):
  - Proxies `/api` → `http://localhost:8010`
  - If you prefer direct calls, set `VITE_API_BASE_URL=http://localhost:8010`

Environment examples
- Copy `.env.development.local.example` to `.env.development.local` as needed.

Troubleshooting
- If you see 500s at `http://localhost:<port>/api/...`:
  - Ensure the mock is running on 8010
  - Ensure UI is running via Vite (proxy active)
  - Or set `VITE_API_BASE_URL=http://localhost:8010` to bypass the proxy

