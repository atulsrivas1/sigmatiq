# Sigmatiq Documentation

## Start Here
- Start Here page: [[Start Here|start_here]] (curated quick links)
- Modeling pipeline: [[Modeling Pipeline Guide|modeling_pipeline_guide]]
- Concepts and allowed values: [[Modeling Reference|modeling_reference]]
- Make targets overview: [[Makefile Guide|makefile_guide]]
- Indicators catalog: [[INDICATORS_REFERENCE.md|INDICATORS_REFERENCE]]

Quick start
- Configure `.env` (DB_* and POLYGON_API_KEY) and run `make db-migrate`.
- Start API: `uvicorn products.sigma-lab.api.app:app --host 0.0.0.0 --port 8001`.
- Run the smoke: `make check-backend BASE_URL=http://localhost:8001 TICKER=SPY PACK_ID=zerosigma MODEL_ID=spy_opt_0dte_hourly START=2024-01-01 END=2024-03-31`.

Welcome to the Sigmatiq documentation hub. Brand-level docs live at the root; product docs live under `Sigma/` and mirror `products/` in the codebase.

## Brand Docs
- Vision: [[SIGMATIQ_Vision_V1.md|SIGMATIQ_Vision_V1]]
- Repositories: [[SIGMA_REPOSITORIES.md|SIGMA_REPOSITORIES]]
- Engineering: [[ENGINEERING_STATUS.md|ENGINEERING_STATUS]], [[STATUS_AND_PLANS.md|STATUS_AND_PLANS]], [[BACKLOG.md|BACKLOG]], [[PACKS_ROADMAP.md|PACKS_ROADMAP]], [[Release_Summary.md|Release_Summary]]
- UI & Tone: [[SIGMATIQ_UI_Implementation_Guide.md|SIGMATIQ_UI_Implementation_Guide]], [Sigmatiq_Messaging_Matrix_v1.xlsx](Sigmatiq_Messaging_Matrix_v1.xlsx), [[Sigmatiq_Tone_of_Voice_Guide_v1.md|Sigmatiq_Tone_of_Voice_Guide_v1]]

## Sigma Suite
- Core: [[Sigma Core|sigma-core]]
- Platform: [[Sigma Platform|sigma-platform]]
- Lab (API & App): [[Sigma Lab|sigma-lab]]
- Market: [[Sigma Market|sigma-market]]
- Sim: [[Sigma Sim|sigma-sim]]
- Pilot: [[Sigma Pilot|sigma-pilot]]

## Getting Started
- Start here: [[Modeling Pipeline Guide|modeling_pipeline_guide]] (end‑to‑end modeling workflow)
- Reference: [[Modeling Reference|modeling_reference]] (packs, models, policies, indicators, features)
- Code roots: see `products/` for the corresponding implementations.
- Conventions: [[CONVENTIONS.md|CONVENTIONS]]
- Architecture: see [[Architecture.md|Architecture]] for rendered diagrams.

For a detailed directory listing, see [[INDEX.md|INDEX]].
