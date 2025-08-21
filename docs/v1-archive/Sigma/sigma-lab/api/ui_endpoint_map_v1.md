# UI Endpoint Map v1 — Pages ↔ API

## Status
Draft — ties current UI surfaces to backend endpoints (implemented or specified)

## Dashboard
- GET `/models?pack_id=` (recent models)
- GET `/leaderboard?limit=10` (last runs)
- GET `/healthz` (status)

## Packs (pack-first)
- GET `/packs` (list)
- GET `/packs/{pack_id}` (overview: meta, indicator sets, templates, models)
- GET `/packs/{pack_id}/templates` (gallery)
- GET `/packs/{pack_id}/indicator_sets`
- CTA: Create Model (opens Template Picker pre-filtered)

## Models — List
- GET `/models?pack_id=`

## Models — Templates Gallery (optional)
- GET `/model_templates?pack=` (spec’d) or `/packs/{pack_id}/templates` (implemented pack-scoped)

## Create Model (Template Picker)
- GET `/model_templates?pack=` (spec)
- POST `/models { template_id, name, risk_profile }` (spec)

## Designer (Structure)
- GET `/indicator_sets?pack_id=` (implemented router exists)
- GET `/validate_policy?model_id=&pack_id=` (implemented)
- PATCH `/models/{id}` (spec; planned)

## Composer — Build
- POST `/build_matrix` or `/matrix/build` (spec vs app; align during wiring)
- GET `/preview_matrix` (if used) or included in Build response

## Composer — Sweeps (Backtests)
- POST `/sweeps/run` (spec) or `/backtest_sweep` (existing) — align routes
- GET `/sweeps/{id}/status` (spec)
- GET `/sweeps/{id}/results?limit=&offset=` (spec)

## Composer — Leaderboard
- GET `/leaderboard?model_id=&pack_id=&risk_profile=&limit=&offset=` (implemented in backtest router)

## Composer — Train
- POST `/train/batch { jobs: [...] }` (spec)
- GET `/train/jobs?model_id=&risk_profile=&status=&limit=&offset=` (spec)

## Signals — Leaderboard | Log | Analytics
- GET `/signals/leaderboard?pack=&risk_profile=&start=&end=&limit=&offset=` (implemented CSV fallback)
- GET `/signals?model_id=&start=&end=&status=&limit=&offset=` (implemented)
- GET `/signals/summary?model_id=&risk_profile=&start=&end` (implemented CSV fallback)

## Model Performance (drawer)
- GET `/models/{id}/performance?start=&end` (implemented)

## Options Overlay
- POST `/options_overlay` (router exists)

## Assistant
- POST `/assistant/query` (spec)

## Admin (admin-only)
- GET `/admin/jobs`, POST `/admin/jobs/{id}/retry|cancel` (spec; stubs return forbidden until RBAC)
- GET `/admin/quotas`, PATCH `/admin/quotas` (spec; stubs)
- GET/PATCH `/admin/risk-profiles` (spec; stubs)
- GET `/admin/packs`, GET `/admin/indicator_sets?pack=` (spec; stubs)
- GET/POST/PATCH `/admin/templates` and `/admin/templates/{id}/publish` (spec; stubs)
- GET/PATCH `/admin/flags` (spec; stubs)
- GET `/admin/health` (spec; stubs)
- GET `/admin/audit` (spec; stubs)
- GET/PATCH/POST `/admin/users` (spec; stubs)

## Notes
- Where both “spec” and “implemented” endpoint names differ (e.g., `/matrix/build` vs `/build_matrix`), align during UI wiring.
- Signals endpoints are CSV-backed now; DB-backed aggregation can be added later without changing shapes.
