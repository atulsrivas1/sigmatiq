# Sigma Lab Backend Audit — Findings & Recommendations

Date: 2025-08-20
Owner: Engineering
Scope: products/sigma-core, products/sigma-platform, products/sigma-lab/api

## Summary

This document consolidates a backend review of Sigma Lab’s core libraries, platform layer, and API. It lists issues, risks, and concrete improvements, grouped by area and prioritized across quick wins, medium-term, and longer-term items.

## Architecture

- Import layering: `products/sigma-platform` re-exports from `api.services.*`, inverting dependency flow and coupling platform to API layout.
  - Action: Move shared services to `sigma-platform` (or a new `sigma-shared`) and have the API import from platform; drop `*` re-exports.
- Path hacks: `api/app.py` and `run_api.py` mutate `sys.path` to reach sibling packages.
  - Action: Use proper packaging or a dev bootstrap; remove runtime `sys.path` mutation.
- Data access: Central DB pool is good; migrations are raw SQL with ad-hoc application.
  - Action: Adopt Alembic (baseline from current SQL), or add idempotent guards and a migrations ledger.

## Reliability & Observability

- Silent failures: Multiple `except Exception: pass` hide real issues.
  - Action: Replace with structured logging; propagate or return typed errors where appropriate.
- Print statements: Core data builders print to stdout.
  - Action: Switch to `logging` with module-level loggers and log levels; add request correlation in API.
- Audit middleware: Logs POSTs but may capture sensitive payloads; swallows errors silently.
  - Action: Filter payload fields, bound body size, and log failures with reason.

## Security

- Admin auth: Single fixed token gate.
  - Action: Move to signed JWT with roles or at least rotatable tokens, plus rate limits on admin routes.
- File path inputs: `/build_matrix` and `/build_stock_matrix` accept arbitrary `out_csv`.
  - Action: Sanitize and restrict to product workspace; reject absolute/parent paths.
- Heavy operations exposed: Long/expensive tasks can be triggered without quotas.
  - Action: Add per-IP quotas and concurrency limits; offload to a job queue.

## Performance

- Polygon fetch loops: Per-strike/day minute aggregation done serially.
  - Action: Batch queries, parallelize with async/thread pool, cache repeated calls; add backoff and rate-limit awareness.
- DataFrame operations: Some redundant conversions inside loops.
  - Action: Vectorize and minimize repeated computations.

## Data Correctness

- Timezones: Generally careful, but ensure consistent tz handling across all inputs.
  - Action: Centralize tz utilities and enforce UTC/ET conversions.
- Indicator registry: Dynamic load silently skips failures.
  - Action: Log per-module load errors; expose an endpoint to list load status.
- Labeling: Flexible with fallbacks.
  - Action: Validate label configs against a schema; log when falling back.

## API Design & DX

- Dynamic router inclusion hides import errors.
  - Action: Log missing routers and expose a health summary.
- Input validation: Several fields are loosely typed and parsed manually.
  - Action: Add Pydantic validators for lists/paths/thresholds; return structured error codes.
- Background processing: Build/train/backtest run in request thread.
  - Action: Introduce `/jobs` and offload to a queue (e.g., RQ/Celery/Arq) with progress and artifacts.

## Database

- Pooling and parameterized queries: Good.
- Migrations: Raw SQL without version tracking.
  - Action: Adopt Alembic; wrap DDL in transactions and IF NOT EXISTS guards.

## Testing & CI

- Tests exist for core features/labels/registry and API smoke.
  - Action: Add negative-path tests (bad configs/policies), per-router param validation, and a few indicator compute checks.
- CI missing.
  - Action: Add GH Actions to run lint, tests, brand sweep, and docs link check; optional coverage gate.

## Notable Code Issues

- `products/sigma-platform/*`: `from api.services.x import *` re-exports.
  - Action: Refactor shared services into platform; remove re-exports.
- `api/routers/backtest.py`: Dead/stub code in `_parity_bracket_next_session_open` (an early loop with `pass`).
  - Action: Remove stub, keep the working loop; add a unit test.
- `api/app.py` vs `api/services/policy.py`: Two policy validators.
  - Action: Consolidate in a single shared function/module.
- `api/services/signals_live.py`: `coverage_pct` not computed.
  - Action: Implement or remove from output.

## Quick Wins (1–2 days)

- Replace prints with `logging` in `sigma_core.data.datasets` and add a structured logging middleware.
- Remove silent `pass` blocks; log warnings with context (module, function, input).
- Sanitize file paths for build/train endpoints; enforce workspace-only writes.
- Clean `_parity_bracket_next_session_open` stub; add one small unit test.
- Log router import failures in `app.py` and surface in `/health`.

## Medium-Term (1–2 weeks)

- Refactor shared services into `sigma_platform` and update API imports; delete re-export shims.
- Introduce background jobs and `/jobs` endpoints; move build/train/backtest to async workers.
- Implement Redis-backed rate limiting and quotas (align with docs).
- Adopt Alembic with baseline; port SQL migrations.
- Add CI pipelines for lint/tests/brand sweep/docs links and optional coverage.

## Longer-Term

- Package `sigma-core`, `sigma-platform`, and `sigma-lab` as installable packages with versions; publish internal wheels.
- Abstract data sources (Polygon et al.) with caching and resilience; add offline fixtures.
- Externalize training hyperparams and feature selection; add experiment tracking (lightweight MLflow or JSON logs).

## Proposed Next Steps

1) Quick wins batch:
- Logging + error handling improvements.
- Path sanitization in dataset/train routes.
- Backtest parity helper cleanup.

2) Shared services refactor (plan + first module: `policy.py`).

3) Background jobs scaffold and convert `/backtest`.

4) CI pipeline enabling tests + brand sweep + link check; add coverage threshold.

Notes:
- Keep changes minimal and surgical; avoid unrelated refactors while landing quick wins.
- Coordinate Alembic introduction around a quiescent period due to migration baseline.

