# Admin API Spec v1 — RBAC, Endpoints, Acceptance

## Status
Draft — admin-only surfaces; complement to BTB and Signals APIs

## RBAC
- Require `role=admin` (JWT claim or session role) for all routes under `/admin/*`.
- Unauthorized: 401 (unauthenticated); Forbidden: 403 (authenticated non-admin).
- All destructive actions require confirmation token and are audit-logged.

## Endpoints (high-level)
- Jobs
  - GET `/admin/jobs?status=&limit=&offset=` → { rows, total }
  - POST `/admin/jobs/{id}/retry` → { ok }
  - POST `/admin/jobs/{id}/cancel` → { ok }
- Quotas
  - GET `/admin/quotas?user=` → { user_id, limits, overrides?, usage }
  - PATCH `/admin/quotas` { user_id, limits } → { ok }
  - GET `/admin/quotas/usage?user=` → { usage }
- Risk Profiles
  - GET `/admin/risk-profiles` → { pack_id, profiles: { conservative|balanced|aggressive: risk_budget, version }[] }
  - PATCH `/admin/risk-profiles` { pack_id, profile, risk_budget } → { version }
- Packs
  - GET `/admin/packs` → { packs: [...] }
  - PATCH `/admin/packs/{id}` { metadata } → { ok }
  - GET `/admin/indicator_sets?pack=` → { sets: [...] }
- Templates
  - GET `/admin/templates` → { templates: [...] }
  - POST `/admin/templates` { template } → { template_id }
  - PATCH `/admin/templates/{id}` { template } → { ok }
  - POST `/admin/templates/{id}/publish` → { version }
- Feature Flags
  - GET `/admin/flags` → { flags: [{ key, enabled, updated_at, updated_by }] }
  - PATCH `/admin/flags` { key, enabled } → { ok }
- Data Health
  - GET `/admin/health` → { db: ok|warn|err, migrations: { pending:int }, cache: { ... }, workers: { ... } }
- Audit
  - GET `/admin/audit?user=&action=&limit=&offset=` → { events: [...] }
- Users & Roles
  - GET `/admin/users` → { users: [{ id, email, role, created_at, last_active }] }
  - PATCH `/admin/users/{id}` { role } → { ok }
  - POST `/admin/users/{id}/rotate_token` → { token_once }

## Errors & Logging
- Use Error Catalog v1; include `X-Request-ID` in responses; audit destructive changes with who/when/what.

## Acceptance
- All admin endpoints return 403 for non-admins and are hidden in UI when role≠admin.
- Edits to quotas, risk profiles, packs metadata, templates, flags are versioned and audit-logged.
