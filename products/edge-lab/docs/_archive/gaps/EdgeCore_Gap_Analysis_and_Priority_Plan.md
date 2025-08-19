# EdgeCore Gap Analysis and Priority Plan (Sigmatiq)
Note on naming: “EdgeCore” in this document refers to the shared Python package `edge_core` (core libraries). The product in this workspace is Edge Lab (API/UI under `products/edge-lab/`). Where this doc says “EdgeCore focus,” read it as “stabilize `edge_core` libraries and their usage in Edge Lab.”
> EdgeCore Tasks Checklist: docs/gaps/EdgeCore_Tasks_Checklist.md


> Go/No-Go & EdgeSim PRD: docs/Sigmatiq_Execution_Plan_GoNoGo_EdgeSim_PRD_v1_UPDATED_2025-08-16.md

Purpose: Close EdgeCore gaps first (models, backtests, previews, signals) before moving to EdgeSim, EdgeMarket, and EdgePilot.

## Scope & Priority
- Focus now: EdgeCore only (2–4 sprints). EdgeSim/EdgeMarket/EdgePilot follow after EdgeCore acceptance.
- Success guardrails: transparency (model cards), data QA gates, lineage, and backtest→alerts parity.

## EdgeCore — Current State (high level)
- ✅ Scanners and ML paths, modular API, indicators library.
- ✅ Walk‑forward backtests, bracketed stock alerts, options overlay.
- ✅ Signals DB with read/write, list/summary APIs; docs/runbooks updated.
- ⚠️ Gaps remain around documentation artifacts, lineage, data QA, and parity.

## Gaps → Work Items (EdgeCore)

1) Model Cards & Data Sheets (Transparency)
- Gap: No standardized model card/data sheet produced for any run.
- Plan:
  - Define a model card schema (YAML + Markdown): data windows, assumptions, features, labels, evaluation method, performance ranges, caveats, failure modes, runtime deps.
  - Generate on build/train/backtest and write to `packs/<pack>/model_cards/<model_id>.md` (plus JSON for API).
  - Add API `GET /model_card?model_id=...` and link from run outputs.
- Acceptance:
  - Every model has a card; cards render in UI and are versioned alongside configs.

2) Lineage Fingerprints (Reproducibility)
- Gap: We are not stamping pack/model/policy SHAs consistently into outputs/DB.
- Plan:
  - Compute and stamp `{pack_sha, indicator_set_sha, model_config_sha, policy_sha}` into CSVs and signals DB on write; add to backtest_runs table.
  - Expose in `GET /signals` and backtest results.
- Acceptance:
  - 100% of signals and backtests carry lineage fields; can diff runs by lineage.

3) Data QA & Preview Gates (Quality)
- Gaps: QA is light; preview does not hard‑fail on invariants.
- Plan:
  - Add invariants: monotonic time, non‑negative volume, session alignment, IV sanity checks.
  - In `/preview_matrix` report violations; configure hard‑fail (30% NaN) and warn (10%) thresholds; block run if fail.
  - Extend `/healthz` with data coverage hints (IV/chain presence, bars continuity) for selected tickers.
- Acceptance:
  - Preview hard‑fails on major issues; healthz reflects coverage status; violations visible in UI/CLI.

4) Backtest Parity — Entry & Brackets (Realism)
- Gap: Backtests don’t enforce the exact entry_mode and bracket exits we publish in alerts.
- Plan:
  - Stocks: add entry_mode=next_session_open parity and ATR bracket exits to backtest engine; report slippage assumptions.
  - Options (EdgeCore parity subset): when quotes available, use quote‑based fills; otherwise BS with IV fallback; tag simulated leg pricing method.
- Acceptance:
  - Parity report shows backtest → alerts consistency (entry price rule + exits); unit tests + example report.

5) Documentation & UX Hygiene
- Gap: No unified operator flow for EdgeCore; fragmented docs.
- Plan:
  - Add “EdgeCore Operator Guide” (preview → build → train → backtest → signals) with examples per pack.
  - Link model cards, preview QA report, lineage, and best‑practice checklists.
- Acceptance:
  - Single doc/entry page to run a model from scratch with quality gates and artifacts.

## Proposed Timeline (EdgeCore)
- Sprint 1–2 (Weeks 1–2):
  - Model card generator + API; lineage stamping in signals/backtests.
  - Preview QA invariants + thresholds; healthz coverage hints.
- Sprint 3 (Week 3):
  - Backtest parity for stocks (entry_mode + ATR brackets); documentation refresh.
- Sprint 4 (Week 4):
  - Options parity (quote/BS fallback tagging); polish + acceptance review.

## Acceptance Criteria (EdgeCore)
- Every model build/train/backtest writes a model card; `/model_card` returns the latest.
- Signals and backtests include lineage fingerprints; `/signals` returns them.
- `/preview_matrix` produces NaN/QA summary and fails on configured thresholds; `/healthz` shows coverage.
- Backtest parity demonstrates entry_mode + bracket exits alignment with live alerts (stocks); options parity initial pass ready.

---

## Post‑EdgeCore Backlog (for visibility)

EdgeSim
- /paper endpoints (accounts, orders, alerts stream) with in‑memory store.
- Fill models (next‑open, NBBO mid ± slippage; queue heuristics); pacing and policy enforcement.
- Sim→live variance tracking and reporting.

EdgeMarket
- /feeds (list/detail/subscribe stub), entitlements, disclosures.
- Integrity checks (OOS proof flag, slippage‑aware returns), risk‑adjusted scoring.

EdgePilot
- Policy‑bounded execution against a mock broker adapter; caps, cooldowns; audit logs.

Observability/KPIs
- Aggregation for: activation→first sim, sim→live, attach, OOS share, slippage delta, risk‑limit hits.

Governance
- Audit logs for model/policy/overlay changes; periodic re‑validation job with drift alerts.
