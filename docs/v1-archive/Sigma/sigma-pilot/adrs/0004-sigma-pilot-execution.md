# ADR 0004: Sigma Pilot — Execution and Guardrails

## Status

Accepted

## Context

We need a product focused on executing policy-bounded playbooks against broker adapters with strong auditability, approvals, and risk controls. This must stay separate from Sigma Lab (authoring/backtests) while interoperating via signals and policies.

## Decision

Introduce a separate product, Sigma Pilot (API/UI), responsible for:
- Policy-bounded execution of playbooks derived from models/policies.
- Risk controls (per-playbook and global): caps, cooldowns, exposure limits, trade pacing.
- Approvals and audit logs for actions (four-eyes optional).
- Broker adapter abstraction (paper and live) with deterministic dry-run modes.
- Observability (events, metrics) and lineage linking back to the originating model/policy.

Sigma Pilot deploys independently from Sigma Lab; communication occurs via API contracts or event ingestion. Signals from Lab are the primary input; Pilot applies execution policies and submits orders via adapters.

## Scope

- Playbooks: typed definitions referencing `model_id`/`pack_id` + execution policy and constraints.
- Scheduler: cron/triggered jobs; backoffs and cooldowns baked in.
- Execution engine: translates playbooks into broker-intent operations; handles partial fills and retries per policy.
- Approvals: optional step-gates based on value/risk thresholds.
- Audit/lineage: every action/event carries `{model_id, pack_id, policy_sha, playbook_sha}`.
- Adapters: `paper`, `mock`, and pluggable `broker_*` implementations (account, orders, positions, quotes).

## Data Model (illustrative)

Database: `sigma_pilot` (dev: schema `pilot` in a shared DB is acceptable).

Tables (snake_case):
- `playbooks` (id, name, spec_json, enabled, created_at, updated_at)
- `runs` (id, playbook_id, started_at, finished_at, status, summary_json, lineage_json)
- `actions` (id, run_id, kind, request_json, response_json, status, created_at)
- `approvals` (id, run_id, approver, status, comment, created_at)
- `audit_logs` (id, entity, entity_id, event, payload_json, created_at)

Indexes for time-range queries and by `model_id`/`playbook_id` for quick drill-down.

## APIs (initial surfaces)

- `POST /playbooks` (create/update by name), `GET /playbooks`, `GET /playbooks/{id}`
- `POST /runs` (trigger playbook), `GET /runs`, `GET /runs/{id}`
- `POST /approvals/{run_id}` (approve/reject)
- `GET /audit` (filters by entity and time)

Contracts are additive and align with the global response envelope (`ok`, pagination).

## Interoperability

- Ingest signals from Sigma Lab: `GET /signals` or event/subscription.
- Reference policies from packs; effective execution policies resolved in Pilot (or provided by Lab as lineage).
- Optional gateway exposes `/api/pilot` for ingress normalization.

## Security

- RBAC per environment; least-privilege DB roles (`sigma_pilot_rw`, `sigma_pilot_ro`).
- Credentials and broker secrets managed via environment/secret store; no secrets in packs.

## Consequences

### Positive
- Strong separation of concerns; Pilot evolves execution safely without touching authoring.
- Clear audit and approval flows with reproducible lineage.
- Deterministic dry-run and paper modes facilitate testing before live.

### Negative
- Additional service to operate and observe.
- Requires disciplined schema/version management across products.

