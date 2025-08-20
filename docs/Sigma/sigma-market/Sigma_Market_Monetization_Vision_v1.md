# Sigma Market — Monetized Model Feeds (Vision v1)

## Summary
Enable creators to monetize their models by publishing signal feeds in a curated marketplace with strong trust, safety, and guardrails. Start with subscription pricing and rigorous disclosures; expand later to bundles and enterprise.

## Principles
- Trust first: integrity checks, out‑of‑sample proof, net‑of‑fees metrics, parity reporting.
- Safety always: capacity/seat limits, entitlement gating, audit logs, moderation controls.
- Transparency: versioned model cards, lineage fingerprints, change logs, risk statements.
- Additive design: product‑first repos; API contracts evolve additively; clear SDK support.

## Monetization Models
- v0: subscription tiers (retail, pro). No performance fees in v0.
- Later: bundles, enterprise seats, signal frequency tiers; performance fees only if compliant.

## Trust & Safety
- Integrity: walk‑forward only; point‑in‑time data; out‑of‑sample proof; net‑of‑fees returns.
- Parity: publish sim→live variance; delist/downgrade on drift.
- Capacity: estimate slippage/capacity; set seat limits; monitor slippage deltas.
- Lineage: stamp `{pack_sha, indicator_set_sha, model_config_sha, policy_sha}` on listings/signals.
- Change control: versioned listings; visible change logs; cooling‑off for risky changes.

## Product Scope (v0)
- Listings
  - API: `POST /market/listings` (create/update), `GET /market/listings` (search/filter), `GET /market/listings/{id}`.
  - Data: title, description, model_id, pack_id, lineage, pricing_tier, capacity, disclosures refs, trust score.
- Disclosures & Trust
  - API: `GET /market/listings/{id}/disclosures` (model card, backtests net‑of‑fees, Sigma Sim variance, change log).
  - Scoring: `GET /market/scores` returns risk‑adjusted trust score and capacity estimates.
- Subscriptions/Entitlements
  - API: `POST /market/subscribe`, `GET /market/subscriptions`, `POST /market/cancel`.
  - Middleware: entitlement gate for `/signals` and any push channel.
- Sigma Lab Integration
  - “Publish to Market” action → creates draft listing with latest model card, lineage, thresholds, and sweep summary.
  - Gating: require Sigma Sim burn‑in and integrity OK.
- SDK
  - Client for listings, disclosures, entitlements, scores; paginated queries and caching.
- Delivery
  - Pull: `GET /signals?model_id=...` (entitlement required).
  - Later: webhooks/streaming (rate‑limited per tier).

## Compliance & Operations
- Disclosures: standardized risk statements; badges for backtest/forward/live.
- KYC/AML for creators and payout setup (W‑9/W‑8); payout ledger and statements.
- Moderation: evidence‑based takedowns for improper claims; audit logs for publish/update/unpublish.

## Scoring & Discovery
- Trust score components: risk‑adjusted net returns, stability, capacity, sim→live delta.
- Discovery filters: capacity, risk band, regime stability, disclosure completeness.

## Rollout
- Alpha (private): invite 5–10 creators; manual curation; subscription‑only; mod tools.
- Beta (waitlist): self‑serve publish with gating; basic admin dashboard; SDK published.
- GA: larger catalog; bundles; org/enterprise seats; optional gateway routing.

## Acceptance Criteria (v0)
- Listings CRUD + entitlements live; unpaid users blocked from `/signals`.
- Each listing shows model card, backtest (net‑of‑fees), Sigma Sim variance, lineage, version history.
- Trust score and capacity estimates visible; parity metrics updated weekly.
- Audit logs for publish/update/unpublish; payout ledger entries for creators.

## Risks & Mitigations
- Overfitting/inflated results → o/s gates, parity reporting, net‑of‑fees metrics, moderation.
- Capacity/signal decay → seat limits, slippage alerts, churn monitoring, delisting policy.
- Regulatory complexity → strict disclosures, marketing rule checks; avoid perf fees in v0.

## Next Steps (Implementation Plan)
1) Schema & API
   - Define `listings`, `subscriptions`, `disclosures`, `scores` schemas and routes.
   - Add entitlement middleware on `/signals` (and later push endpoints).
2) Sigma Lab Flow
   - Add “Publish to Market” draft flow with integrity gate (Sigma Sim burn‑in required).
   - Generate disclosures bundle from existing model card + sweep/backtest artifacts.
3) SDK & UI
   - sigma-sdk: listings/subscriptions client; trust score accessors; pagination helpers.
   - Sigma Market UI: listing pages with disclosures, pricing, capacity, trust score; subscribe/renew flows.
4) Admin & Ops
   - Minimal admin dashboard (approve/reject listings; view audit; payouts ledger).
   - Payout mechanics (stub) and monthly statements.

