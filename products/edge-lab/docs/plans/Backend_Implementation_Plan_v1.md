# Backend Implementation Plan — BTB + Assistant (v1)

## Status
Draft — phases, scope, acceptance; no code changes yet

## Team & Env
- Owners: Backend (API), Data (matrix/builders), Infra (DB/migrations/queues)
- Envs: local dev → staging → prod; feature flags for Assistant execute-on

## Phases

### Phase 1 — Contracts & Migrations
- Tasks
  - Finalize API contracts (BTB + Assistant)
  - Write SQL migrations per DB_Schema_Deltas_v1 (runs, folds, train_jobs, selections)
  - Add read-only DB views for leaderboard summaries (optional)
- Acceptance
  - Migrations apply cleanly; rollback tested
  - OpenAPI spec updated; shape tests pass

### Phase 2 — BTB Backend Surfaces
- Tasks
  - Implement `/matrix/build` (preview optional) and `GET /matrix/{sha}`
  - Implement `/sweeps/run`, `/sweeps/{id}/status`, `/sweeps/{id}/results`
  - Extend `/leaderboard` with `risk_profile`, `pass_gate`, lineage fields
  - Implement `/train/batch` and `GET /train/jobs`
  - Gate evaluation service with reason codes (pack-aware)
- Acceptance
  - Shape and happy-path tests pass; QA checklist items 1–5 satisfied (docs/tests/BTB_QA_Checklist.md)

### Phase 3 — Assistant Surfaces (Read-Only)
- Tasks
  - Implement `/assistant/query` streaming endpoint
  - Server-moderated tools: docs.search, reports.search/read_csv/read_xlsx, db.leaderboard, db.run_detail, pipeline.suggest
  - Enforce guardrails: allowlist SQL, file scopes, preview caps
- Acceptance
  - Assistant QA (read-only) passes items 1–4 and 6

### Phase 4 — Assistant (Confirm-to-Execute, Feature-Flagged)
- Tasks
  - Implement pipeline.execute tool and confirmation token flow
  - Add quotas/rate limits enforcement and errors per spec
- Acceptance
  - Assistant QA item 5 passes; quotas tested

### Phase 5 — Observability & Hardening
- Tasks
  - Structured logging, request IDs, metrics (job durations, gate pass rate, cache hit rate, quota hits)
  - Rate limiting (429) and quotas (403 with `QUOTA_EXCEEDED`); error catalog wired
  - Backfill lineage fields for recent runs (one-off script)
- Acceptance
  - Logs/metrics in place; error codes consistent; SLOs documented

## Cutover & Rollback
- Feature flags for new endpoints; dark-ship read-only Assistant first
- DB migrations are additive; rollback scripts included

## Risks & Mitigations
- Compute cost spikes: add quotas and gate-by-default training
- Schema drift: centralize lineage schema; migration tests
- Safety: read-only tools by default; confirm-to-execute flow; allowlist SQL

## References
- API: docs/api/BTB_API_Spec_v1.md, docs/api/Assistant_API_Spec_v1.md
- DB: docs/specs/DB_Schema_Deltas_v1.md
- QA: docs/tests/BTB_QA_Checklist.md, docs/tests/Assistant_QA_Checklist.md
