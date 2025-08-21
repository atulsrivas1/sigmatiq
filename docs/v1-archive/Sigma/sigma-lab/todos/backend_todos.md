# Backend TODOs — BTB + Assistant

Scope: Track actionable items to move from documentation to implementation. No code changes until approved.

## High Priority
- [ ] Draft SQL migration files in `products/sigma-lab/api/migrations/` per `specs/DB_Schema_Deltas_v1.md` (0004..0006), mark as placeholders.
- [ ] Prepare OpenAPI YAML sketch for new endpoints: `/matrix/*`, `/sweeps/*`, `/leaderboard`, `/train/*`, `/assistant/query` (docs-only, checked into `docs/api/openapi_btb_v1.yaml`).
- [ ] Define allowlisted SQL templates for Assistant DB tools (leaderboard summaries, run detail) with parameter validation.
- [ ] Quotas config scaffold (no enforcement): defaults and env overrides per `api/Quotas_and_Rate_Limits_v1.md`.

### API ↔ Makefile alignment (real backend)
- [ ] Add GET `/leaderboard` API in `products/sigma-lab/api/routers` that calls `sigma_core.registry.backtest_registry.leaderboard(pack_id, model_id, limit, offset, order_by)` and returns rows (with paging fields).
- [ ] Add GET `/models` API to list existing model configs (enumerate `packs/<pack_id>/model_configs/*.yaml`) or update the Makefile `models` target to use existing GET `/model_templates?pack=$(PACK_ID)`.
- [ ] Update Makefile `validate-policy` target to call existing GET `/policy/explain?model_id=$(MODEL_ID)&pack_id=$(PACK_ID)` (or add an alias GET `/validate_policy` that proxies to `/policy/explain`).
- [ ] Ensure Makefile help text and `docs/MAKEFILE_GUIDE.md` reflect the real endpoints and parameters.
- [ ] Verify env prereqs in docs: DB envs for `sigma_core.storage.relational.get_db` and `POLYGON_API_KEY`; migrations applied under `products/sigma-lab/api/migrations`.
- [ ] Optionally add `check-backend` smoke target docs (health → build → train → backtest → leaderboard) and link from wiki.

## Medium Priority
### DB Integration — Persistence Coverage
- [ ] Sweeps: add `backtest_sweeps` (spec/status/timestamps) and `sweep_results` (params/metrics/csv_uri) tables; persist from sweep route; add list/detail endpoints.
- [ ] Policy snapshots: persist effective policy on every build/train/backtest (simple: `policy_snapshot` JSONB on run tables; normalized: `policy_snapshots` with FK).
- [ ] Artifacts: add `artifacts` table (kind|uri|sha256|size|created_at|run_id FK); persist matrix CSV, model pkl, plots; return URIs, not local paths.
- [ ] Object storage: wire S3/MinIO writers and store stable URIs in DB (env-configured buckets); document creds/envs.
- [ ] Read endpoints: list/detail for `build_runs` and `training_runs` (filters: pack_id, model_id, tag, dates, paging).
- [ ] Schema versioning: add `schema_migrations` table to track applied migration ids/checksums.
- [ ] Add DB views for leaderboard summaries (optional) to simplify Assistant queries.
- [ ] Logging/metrics plan: request IDs, structured logs, counters for gate pass rate, cache hit rate, concurrent jobs.
- [ ] Error catalog wiring: map exceptions → codes from `api/Error_Catalog_v1.md` (docs-only plan).

## Low Priority
- [ ] Backfill script plan for lineage fields on historical runs.
- [ ] Admin overrides process for quotas (policy doc + audit fields).

## Notes
- Keep all artifacts under docs/ until implementation is approved; avoid code or DB changes.
