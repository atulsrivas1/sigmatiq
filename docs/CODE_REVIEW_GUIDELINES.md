**Purpose & North Star**
- **Goal:** Keep trading simple for non‑traders; default to safety.
- **Constructive Critic:** Reviewers actively reduce complexity, jargon, and risk.

**Mandatory Critic Gate**
- **Require:** A documented Critic pass before approval.
- **Check Risks:** Jargon, parameter soup, hidden state, irreversible actions.
- **Check Safety:** Quotas, caps, guardrails, clear costs/risks, undo/rollback.
- **Check Simplicity:** One‑screen flows, presets over raw params, progressive disclosure.
- **Confirm Defaults:** Plain language of scope, on/off switches, reversibility.
- **Outcome:** If material issues remain, request changes with a simpler alternative.

**Review Scope & Flow**
- **Design First:** Validate problem framing vs. North Star; prefer simpler paths.
- **API & Contracts:** Confirm specs match docs; parameters named plainly; safe defaults.
- **Data & Migrations:** Validate schema/migrations; enforce novice fields/guardrails.
- **Implementation:** Fail‑safe behavior; caps applied; defensive input handling.
- **Docs & Catalog:** Docs updated; seeds/lints pass; Postman examples novice‑safe.
- **Testing & Postman:** Unit/integration tests added where patterns exist; examples run.

**API & Contracts**
- **Plain Params:** Avoid raw/opaque parameters; provide presets and examples.
- **Safe Defaults:** Conservative, reversible, opt‑in for advanced features.
- **Consistency:** Align with existing patterns (`mode: simple`, `fields=full`).
- **Responses:** Include `summary`; add `metrics_explained` in simple mode or when `fields=full`.
- **Caps:** Enforce ≤ 90 days and ≤ 50 symbols across related endpoints.
- **Consensus:** For pack endpoints, echo `consensus` and `policy`; validate compatibility.
- **Errors:** Plain‑language 400s with next steps; avoid leaking internals.

**Data & Migrations**
- **Idempotency:** Migrations re‑runnable; no destructive defaults.
- **Novice Fields:** Enforce `novice_ready`, `beginner_summary`, `guardrails` where required.
- **Indexes/Views:** Add where needed (e.g., leaderboard filters); document rationale.
- **Seeds:** Regenerate seeds when content or shapes change; keep lints green.

**Safety & Guardrails**
- **Quotas/Caps:** Hard caps on dates/symbols/sweep combos; budget throttles where applicable.
- **Guardrails:** Exposure caps, allowed hours defaults, min trades; DB checks for published novice content.
- **Reversibility:** Obvious off switches; soft‑fail or no‑op on missing env/keys.
- **Fail‑Safe Computes:** Indicators/features return zeros/empties instead of exceptions.

**Novice Experience**
- **Plain Language:** Avoid jargon/metrics without translation; add tooltips/explainers.
- **Simple Mode:** Prefer `mode: simple` with safe presets (e.g., `rth_thresholds_basic`).
- **Progressive Disclosure:** Hide advanced options; show examples and previews first.
- **Catalog:** `fields=full` returns human‑friendly details; `novice_only` filters supported.

**Performance & Cost**
- **Safe by Default:** Avoid heavy defaults; bound universes and windows.
- **Caching:** Respect data cache rules (never cache “today” for Polygon loaders).
- **Efficiency:** Parquet partitioning for datasets; avoid O(N×M) loops when vectorizable.

**Security & Privacy**
- **DB Access:** Parameterize queries; no string interpolation.
- **Secrets:** Read from env; do not log secrets or large payloads.
- **Gating:** Gate DB/network paths when env/config is unavailable.

**Testing & Quality**
- **Unit Tests:** Add targeted tests where patterns exist (e.g., fail‑safe compute, caps).
- **Integration:** Exercise hot paths with small, safe inputs; prefer copy/paste runnable examples.
- **Lints:** Keep `lint-*` targets green (catalog, strategies, training cfg, etc.).
- **Postman:** Update and verify examples use safe presets and caps; add consensus variations.

**Documentation & Catalog**
- **Docs Match Code:** Update docs under `docs/*` and whiteboarding notes for new behavior.
- **Spec Clarity:** Document new params, caps, and simple‑mode behavior.
- **Seeds & Overrides:** Align overrides (novice fields, simple_defaults, guardrails) and regenerate seeds.

**Developer Experience & Style**
- **Surgical Changes:** Minimal, focused diffs; align with existing naming and folder structure.
- **Defensive Code:** Check inputs; return helpful errors; avoid breaking call sites.
- **Style:** No one‑letter variables; avoid inline license headers; follow repo conventions.
- **Independence:** Keep product self‑sufficient (scripts, migrations, .env within product).

**PR Checklist (Reviewer)**
- **North Star:** Does this reduce decisions and jargon for novices?
- **Critic Gate:** Are risks, costs, caps, and reversibility plainly documented?
- **Safety:** Caps enforced (dates/symbols/combos); guardrails present; safe defaults.
- **API:** `mode: simple` supported where relevant; `fields=full` returns extras.
- **Errors:** Plain‑language errors with next steps for common failures (DB/env/network).
- **Docs:** Specs updated; examples copy/paste runnable; catalog content aligned.
- **Tests:** Focused tests added; Postman request(s) added/updated.
- **Seeds/Lints:** Seeds regenerated; lints pass; migrations idempotent.

**Blockers (Auto‑Reject)**
- **Raw Params:** Exposing low‑level parameters without presets or explanations.
- **Unbounded Work:** No caps on universes/dates/combos; risky defaults.
- **Multi‑Step Wizardry:** Complex flows where a single preset suffices.
- **Opaque Metrics:** Sharpe/AUC/etc. shown without plain‑language translation.
- **Irreversible Changes:** Hidden state mutations; missing undo/rollback.

**Good Change Examples**
- **Simple Preset:** Adds `mode: simple` to an endpoint with RTH defaults and caps.
- **Novice Response:** Adds `summary` and `metrics_explained` when `fields=full`.
- **Guardrails:** Enforces `min_trades` and consensus echo on pack backtests.
- **Docs + Postman:** Updates docs, seeds, and Postman in the same PR.

**References**
- **Agents Guide:** `agents.md` (North Star, guardrails, workflows).
- **APIs:** `docs/*/api-spec.md`, whiteboarding packs, and Postman collection.
- **Code Map:** `products/sigma-core/sigma_core/*` and API layer.
- **Lints:** `make lint-*`; Seeds: `gen-*-seed` + `make db-migrate`.

