# Docs Index

This repo organizes documentation under `docs/` with brand-level docs at the root and product docs under `docs/Sigma/`. The code for products lives under `products/` and mirrors the same names. See `CONVENTIONS.md` for standards.

## Conventions & Overview
- `CONVENTIONS.md`
- `SIGMA_REPOSITORIES.md`
- `Sigmatiq_Vision_and_Product_Ecosystem.md`
- `ENGINEERING_STATUS.md`, `STATUS_AND_PLANS.md`, `BACKLOG.md`, `PACKS_ROADMAP.md`, `Release_Summary.md`

## Sigma Suite
- `Sigma/sigma-core/` — Core libraries, indicators, scoring
- `Sigma/sigma-platform/` — Platform layer, policies, shared specs and UI shell
- `Sigma/sigma-lab/` — Product/API, runbooks, ops, app UI
- `Sigma/sigma-market/` — Market docs and help content
- `Sigma/sigma-sim/` — Simulation planning
- `Sigma/sigma-pilot/` — Pilot-related ADRs

## Brand Docs (root)
- `AGENTS.md`, `CONTRACT.md`, `CONVENTIONS.md`
- `SIGMATIQ_Vision_V1.md`, `Sigmatiq_Messaging_Matrix_v1.xlsx`, `Sigmatiq_Tone_of_Voice_Guide_v1.md`
- `design_diagrams.puml`

## Product Docs

### sigma-core
- `Sigma/sigma-core/model_naming.md`
- Indicators: `Sigma/sigma-core/indicators/`
- Specs: `Sigma/sigma-core/specs/Gate_and_Scoring_Spec_v1.md`
- ADRs: `Sigma/sigma-core/adrs/0001-architectural-overview.md`, `0002-versioning-system.md`

### sigma-platform
- Policy: `Sigma/sigma-platform/policy_schema.md`
- Specs: `Sigma/sigma-platform/specs/` (model cards, templates, signals, matrix contract, risk profile)
- UI: `Sigma/sigma-platform/ui/` (App shell, design tokens, nav tree, pages, archive)

### sigma-lab
- API: `Sigma/sigma-lab/api/` (Admin, Assistant, BTB, Packs, Signals, UI map)
- Runbooks: `Sigma/sigma-lab/runbooks/`
- Plans: `Sigma/sigma-lab/plans/`
- Tests: `Sigma/sigma-lab/tests/`
- TODOs: `Sigma/sigma-lab/todos/`
- Specs: `Sigma/sigma-lab/specs/DB_Schema_Deltas_v1.md`
- UI: `Sigma/sigma-lab/ui/` (Assistant, BTB, CustomModelBuilder, Sigma Lab UI docs)
- ADRs: `Sigma/sigma-lab/adrs/0003-sigma-packs.md`, `0005-btb-pipeline-and-risk-profiles.md`, `0006-template-first-create-and-split-designer-composer.md`
- Audit: `Sigma/sigma-lab/BACKEND_AUDIT.md`, `Sigma/sigma-lab/DB_NAMING_AND_SEPARATION.md`

### sigma-market
- `Sigma/sigma-market/help/`
- `Sigma/sigma-market/Sigma_Market_Monetization_Vision_v1.md`

### sigma-sim
- `Sigma/sigma-sim/Sigmatiq_Execution_Plan_GoNoGo_SigmaSim.md`

### sigma-pilot
- ADRs: `Sigma/sigma-pilot/adrs/0004-sigma-pilot-execution.md`

## Archive
- Historical docs are under `_archive/` for reference.
