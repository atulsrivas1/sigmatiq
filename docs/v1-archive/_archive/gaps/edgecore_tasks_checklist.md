# SigmaCore Tasks Checklist (Sigmatiq)

Use this checklist to track SigmaCore completion. We will strike items as they are delivered.

## Must‑Haves (Core Quality)
- [ ] Model cards & data sheets
  - [ ] Generator on build/train/backtest (MD + JSON)
  - [ ] `GET /model_card?model_id=&pack_id=` API
  - [ ] UI rendering/linking
- [ ] Lineage stamping (reproducibility)
  - [ ] Stamp `pack_sha, indicator_set_sha, model_config_sha, policy_sha` in CSVs and DB
  - [ ] Include lineage in backtest runs and API responses
- [ ] Preview QA gates (quality)
  - [ ] Invariants: monotonic time, non‑negative volume, session alignment, IV sanity
  - [ ] NaN thresholds (warn ≥10%, fail ≥30%); hard‑fail in `/preview_matrix`
  - [ ] Health coverage hints (bars continuity, IV/chain presence)
- [ ] Backtest parity (stocks)
  - [ ] Enforce `entry_mode=next_session_open`
  - [ ] Enforce ATR bracket exits; parity report

## UI (SigmaCore Operator Console)
- [ ] Model Builder: pack/indicator selection, param editor, model card preview
- [ ] Preview Pane: NaN/QA summary, fail reasons, lineage diff
- [ ] Backtest Viewer: folds, parity report (entry/brackets vs alerts)
- [ ] Signals Explorer: filters, lineage columns, diff vs yesterday
- [ ] Overlay Console: single/vertical overlay, expirations helper, results table
- [ ] Run Orchestrators: scan/train/backtest/overlay with progress & artifacts links

## SDK (Python)
- [ ] Typed client for core routes (build/train/backtest/preview/signals/overlay/model_card)
- [ ] Helpers: lineage checksums; CSV <-> DataFrame; card fetch/write
- [ ] Notebooks: end‑to‑end examples (scan→preview→backtest→signals→overlay)
- [ ] Packaging: `sigmatiq-edge` publish & version to git tags

## Observability & DevEx
- [ ] Minimal metrics aggregator (preview fails, runtimes, API latency)
- [ ] Structured logging per router with lineage context
- [ ] CI/CD: migrations (0004, 0005), API smoke, SDK tests, docs link checks
- [ ] Migration runner script (idempotent)

## Polish & Data
- [ ] Indicators docs: clean param docs and categories in `/indicators`
- [ ] Adapters hardening: backoff/timeout, selective caching, clearer QA errors
- [ ] Sample universes & demo runbook for first‑time users

## Sprints (proposed)
- Sprint A (Weeks 1–2): Model cards + `/model_card`; lineage stamping; preview QA gates; SDK core client
- Sprint B (Week 3): Backtest parity (stocks); health coverage hints; UI wiring
- Sprint C (Week 4): Options parity (tag quote/BS fallback); SDK overlay helpers; docs polish

---

Links:
- Vision: docs/Sigmatiq_Vision_and_Product_Ecosystem_v3_2025-08-16.md
- Go/No‑Go & SigmaSim PRD: docs/Sigmatiq_Execution_Plan_GoNoGo_SigmaSim_PRD_v1_UPDATED_2025-08-16.md
- SigmaCore Gaps & Plan: docs/gaps/SigmaCore_Gap_Analysis_and_Priority_Plan.md
