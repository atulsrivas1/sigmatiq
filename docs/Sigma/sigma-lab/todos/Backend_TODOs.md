# Backend TODOs — BTB + Assistant

Scope: Track actionable items to move from documentation to implementation. No code changes until approved.

## High Priority
- [ ] Draft SQL migration files in `products/sigma-lab/api/migrations/` per `specs/DB_Schema_Deltas_v1.md` (0004..0006), mark as placeholders.
- [ ] Prepare OpenAPI YAML sketch for new endpoints: `/matrix/*`, `/sweeps/*`, `/leaderboard`, `/train/*`, `/assistant/query` (docs-only, checked into `docs/api/openapi_btb_v1.yaml`).
- [ ] Define allowlisted SQL templates for Assistant DB tools (leaderboard summaries, run detail) with parameter validation.
- [ ] Quotas config scaffold (no enforcement): defaults and env overrides per `api/Quotas_and_Rate_Limits_v1.md`.

## Medium Priority
- [ ] Add DB views for leaderboard summaries (optional) to simplify Assistant queries.
- [ ] Logging/metrics plan: request IDs, structured logs, counters for gate pass rate, cache hit rate, concurrent jobs.
- [ ] Error catalog wiring: map exceptions → codes from `api/Error_Catalog_v1.md` (docs-only plan).

## Low Priority
- [ ] Backfill script plan for lineage fields on historical runs.
- [ ] Admin overrides process for quotas (policy doc + audit fields).

## Notes
- Keep all artifacts under docs/ until implementation is approved; avoid code or DB changes.
