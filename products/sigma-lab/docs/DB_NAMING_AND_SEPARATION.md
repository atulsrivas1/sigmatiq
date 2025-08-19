**DB Naming & Separation**
- Model: Separate database per product (prod), optional shared platform DB. In dev/staging, one Postgres with per-product schemas is acceptable for convenience.

**Databases (prod)**
- edge_lab: Sigma Lab (packs/models authoring, lineage, backtests, model cards, QA gates)
- edge_sim: Sigma Sim (scenarios, simulation runs, artifacts index, reports)
- edge_market: Sigma Market (catalog/listings, subscriptions, entitlements)
- edge_pilot: Sigma Pilot (playbooks, guardrails, run logs, approvals)
- sigma_platform (optional): Identity/tenancy, orgs/users/roles; global catalog mirror; global audit aggregator

**Schemas (within each DB)**
- Default: `app` (or `public`)
- Optional logical areas: `audit`, `lineage`, `signals`, `options`, `backtests`

**Tables (snake_case plural)**
- Examples: `signals`, `option_signals`, `backtest_runs`, `audit_logs`, `model_cards`, `packs`, `models`, `policies`, `entitlements`, `subscriptions`

**Roles & Access**
- `<db>_rw`: application write role (used by API)
- `<db>_ro`: read-only role (used by BI/UIs that need RO)
- `<db>_migrator`: migrations role (used by CI/CD)
- Secrets per product + environment via GitHub Environments/Vault; least privilege

**Migrations**
- Per product repo: `migrations/0001_init.sql`, `0002_*.sql`, ...
- Targets: `db-migrate` applies, `db-migrate-dry` lists/validates without applying
- Strategy: expand → backfill → contract; backward-compatible changes first
- Partition high-volume tables (e.g., `signals`, `audit_logs`) by date; retention per product

**Environments**
- Dev: single Postgres acceptable; use schemas per product (`lab`, `sim`, `market`, `pilot`, `platform`) and shorter retention
- Staging/Prod: separate DB per product; backups and PITR per DB

**Environment Variables (per repo)**
- Required: `DB_HOST`, `DB_PORT`, `DB_NAME` (e.g., `edge_lab`), `DB_USER`, `DB_PASSWORD`
- Optional: `DB_SCHEMA` (default `public` or `app`), `DB_SSLMODE`, `DB_CONN_MAX`

**Gateway & Cross-Product Data**
- Prefer API/event sync between products (e.g., Lab publishes pack metadata → Market ingests)
- Avoid direct cross-DB reads; use `sigma-gateway` or service-to-service auth if necessary

**Quick Examples**
- Sigma Lab local dev (single Postgres):
  - DB_NAME=edge_lab, DB_SCHEMA=app
- Sigma Products consolidated dev DB (optional):
  - DB_NAME=edge_products, DB_SCHEMA=lab|sim|market|pilot|platform

**Checklist**
- DB per product in prod; optional platform DB only for global concerns
- Separate roles per product/env; secrets managed per environment
- Migrations scripted and gated in CI (dry-run + checksum)
- Date partition and retention on large tables
