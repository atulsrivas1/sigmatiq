**Sigma Family Repositories**
- Purpose: Define the set of repos, folder structures, naming conventions, and CI/CD guardrails for the Sigma product family.

**Recommended Model (Polyrepo per Product UI/API)**
- Separate repository for each product API and each product UI.
- Common shared repositories for platform/core, SDK, infra, and packs.
- Optional gateway repository to provide a unified ingress across products.

Note: In this workspace, Sigma Lab is organized as a product under `products/sigma-lab/` and the shared libraries are packaged as `sigma_core` and `sigma_platform` within the same repo for development convenience. The repo split described below is the target long-term polyrepo model.

**Repo Overview**
- Common repos (shared by all products):
  - **sigma-core**: Core Python libs (data, features, indicators, models, backtests, registry, storage).
  - **sigma-platform**: API/platform utilities (db sessions, migrations tooling, audit, lineage, pagination, policy, IO helpers). Can be a separate repo or a subpackage inside `sigma-core`.
  - **sigma-sdk-py**: Python SDK with typed client, paginated iterators, lineage helpers, and contract tests.
  - **sigma-infra**: Infra as code (Helm/Terraform), GH Actions reusable workflows, base Helm charts.
  - **sigma-packs**: Strategy content (indicator sets, model configs, policy templates) versioned independently of runtime code.
- Product API repos (one per product):
  - **sigma-lab-api**, **sigma-sim-api**, **sigma-market-api**, **sigma-pilot-api**
- Product UI repos (one per product):
  - **sigma-lab-ui**, **sigma-sim-ui**, **sigma-market-ui**, **sigma-pilot-ui**
- Optional:
  - **sigma-gateway**: Mounts `/api/{product}` to route requests to product APIs.

**Naming Conventions**
- **Repos**: lowercase with hyphens (e.g., `sigma-core`, `sigma-apis`, `sigma-ui`).
- **Python packages**: lowercase with underscores (e.g., `sigma_core`, `sigma_platform`).
- **Docker images**: `ghcr.io/<org>/<repo>[:tag]`, hyphens preferred (e.g., `ghcr.io/org/sigma-zerosigma-api`).
- **PyPI vs import**: Project names may use hyphens (e.g., `sigma-sdk`), import uses underscore (`edge_sdk`).

**sigma-core (repo)**
- **Purpose**: Shareable core logic across products; no API server code.
- **Top-level**:
  - `sigma_core/`: datasets, features, indicators, models, backtests, evaluation, storage, registry
  - `tests/`: unit and integration tests
  - `pyproject.toml` / `setup.cfg`: build metadata
  - `README.md`, `CHANGELOG.md`
- **CI/CD**:
  - Lint, type check, tests, coverage, SAST, dep scan
  - Publish package on tag to private PyPI (SemVer)
- **Contracts**:
  - Stable function signatures for critical utilities
  - Backward-compatible changes preferred

**sigma-platform (repo or subpackage in sigma-core)**
- **Purpose**: Shared API/server utilities used by product apps and workers.
- **Top-level**:
  - `sigma_platform/`: db session, config, audit, lineage, pagination, policy, IO helpers
  - `migrations/core/`: shared DB schema (signals, option_signals, backtests, audit)
  - `scripts/`: `apply_migrations.py`, `seed_data.py`
  - `tests/`, build files, docs
- **CI/CD**:
  - Same as `sigma-core`, publish package on tag
  - Migration dry-run job (checks SQL syntax/orders)

**Product API repos (per product)**
- **Purpose**: Own the API server and product-specific workers for one product.
- **Top-level (example: sigma-lab-api)**:
  - `edge_api/`: FastAPI app package
    - `app.py`: ASGI app entrypoint (or `apps/<product>/app.py`)
    - `routers/`: group by area; may include `common/` (if duplicated) and product-specific modules
    - `services/`: thin wrappers calling `sigma_platform`
  - `workers/`: product jobs (scanners, live loops)
  - `migrations/`: SQL migrations for product + shared core schema
  - `scripts/`: migrate/seed, utilities
  - `infra/`: Dockerfile, Helm chart/values
  - `tests/`: unit + API contract tests
- **CI/CD**:
  - Lint, type check, tests, contract tests
  - DB migration dry-run + checksum verify
  - Build/push Docker image, Helm deploy (dev→stg→prod) with approvals; run pre-deploy migrations

**Product UI repos (per product)**
- **Purpose**: Own the product’s user interface independently of other products.
- **Top-level (example: sigma-lab-ui)**:
  - `src/`: routes, components, brand tokens, product-specific features
  - `public/`: index.html, favicons
  - `vite.config.ts` (or Next.js config): API base pointing to the product API
  - `Makefile` / npm scripts: install/dev/build/preview
- **CI/CD**:
  - Lint, type check, unit/e2e (Playwright), build
  - Deploy independently (CDN/static hosting or container)
- **Config**:
  - Env-driven API base (e.g., `VITE_API_BASE_URL`) targeting the matching product API

**sigma-sdk-py (repo, optional but recommended)**
- **Purpose**: Stable SDK for apps and notebooks; enforces API contracts in CI.
- **Top-level**:
  - `edge_sdk/`: typed client, paginated iterators, lineage helpers
  - `tests/`: contract tests against stub/golden schemas
  - Build files, README
- **CI/CD**:
  - Lint, type check, tests
  - Publish on tag (SemVer)

**sigma-infra (repo, optional)**
- **Purpose**: Shared infra/ops tooling and reusable workflows.
- **Top-level**:
  - `helm/`: base charts or umbrella charts per app
  - `terraform/`: cluster, networking, databases, secrets
  - `.github/workflows/`: reusable Actions (build-python, build-node, docker-scan, deploy)
- **CI/CD**:
  - Validate Helm templates, Terraform plan, policy checks; no app builds here

**sigma-packs (repo, optional)**
- **Purpose**: Versioned strategy content independent of runtime code.
- **Top-level**:
  - `{pack_id}/`: `indicator_sets/`, `model_configs/`, `policy_templates/`
  - `tools/`: validators, lints, schema checks
- **CI/CD**:
  - Validate pack schemas and policies; optionally publish pack bundles

**Routing & Deployment Patterns**
- **Direct mode (recommended)**: Each UI points to its matching product API base URL; deploy independently.
- **Gateway mode (optional)**: `sigma-gateway` mounts `/api/{product}` → simplifies unified ingress; UIs can target gateway paths.

**Product Scope Summaries**
- **Sigma Lab (sigma-lab-api / sigma-lab-ui)**: Pack and model authoring and management. Create/validate packs (indicator sets, model configs, policies), orchestrate build/train/backtest, lineage/model cards, QA gates, publish to `sigma-packs`, audit/governance.
- **Sigma Sim (sigma-sim-api / sigma-sim-ui)**: Simulation and scenario engines. Define scenarios, run batch sims/backtests, compare outcomes, manage artifacts and reports.
- **Sigma Market (sigma-market-api / sigma-market-ui)**: Marketplace and subscriptions. List packs/models, manage subscriptions/entitlements, catalog search, product metadata.
- **Sigma Pilot (sigma-pilot-api / sigma-pilot-ui)**: Automation/execution. Playbooks, guardrails, schedulers, live hooks; approvals and audit for actions.
- **Environments**: dev/staging/prod via GitHub Environments; secrets per env; manual prod approvals.

**Release & Versioning**
- **sigma-core/platform**: SemVer with release notes; dependabot/renovate to bump downstream pins.
- **Product APIs**: Per-repo tags (e.g., `zerosigma-api:vX.Y.Z`) plus `:sha` images; Helm chart appVersion sync.
- **Product UIs**: SemVer per repo; Changesets or conventional commits.

**Security & Quality Gates**
- SAST (Bandit), pip-audit, Trivy scans, Gitleaks, license checks.
- Contract tests: ensure response envelopes and pagination remain stable.
- DB migration strategy: expand → backfill → contract; migration dry-run in CI.

**Decision Points**
- **sigma-platform placement**: separate repo vs `sigma_core.sigma_platform` subpackage.
- **Gateway adoption**: use gateway from day one vs introduce later.
- **Packs coupling**: keep in `sigma-apis` vs separate `sigma-packs` repo for curated content.

**Migration (From Current Repo)**
- Phase 1: Create new repos: `sigma-core`, `sigma-platform`, `sigma-lab-api`, `sigma-lab-ui` (start with Sigma Lab). Extract shared libs into `sigma-core`/`sigma-platform` with compatibility shims.
- Phase 2: Move current API into `sigma-lab-api` (pack/model authoring, training/backtest orchestration), move UI into `sigma-lab-ui` (retain branding/assets). Update Make targets and docs accordingly.
- Phase 3: Split migrations: keep shared schema in `sigma-platform` (or duplicate in product repos) and product-specific migrations in `sigma-lab-api`.
- Phase 4: Add `sigma-sim-api/ui`, `sigma-market-api/ui`, `sigma-pilot-api/ui` as they come online; establish CI templates across repos.
- Phase 5: Stand up per-repo CI/CD; publish `sigma-core/platform`; pin versions in product APIs; add optional `sigma-gateway` if needed.

**Review Checklist**
- **Ownership**: CODEOWNERS assigned per repo/path; branch protections in place.
- **Isolation**: UI builds independently; product apps deploy independently or via gateway.
- **Contracts**: SDK + CI contract tests wired; pagination/envelope stability documented.
- **DB**: Migrations gated and reversible; seeds available; env secrets configured.
- **Security**: Scans enabled; dependency pinning and update automation configured.

**Next Steps**
- Confirm polyrepo model and repository names.
- Decide whether `sigma-platform` lives standalone or inside `sigma-core`.
- I can scaffold initial READMEs and GitHub Actions templates for each repo on approval.

**Alternative (Monorepo options, for reference)**
- APIs monorepo (`sigma-apis`) and single UI (`sigma-ui`) can be used if you later prefer cross-product atomic changes and path-filtered CI. Not the current recommendation but documented for completeness.
**Final Naming Matrix (Agreed)**
- Shared repos: `sigma-core`, `sigma-platform`, `sigma-sdk`, `sigma-packs`, `sigma-infra`, optional `sigma-gateway`.
- Sigma Lab:
  - Brand: Sigma Lab
  - Repos: `sigma-lab-api`, `sigma-lab-ui`
  - Python package: `edge_lab_api`
  - Domain: `sigma-lab.sigmatiq.ai`, API: `api.sigma-lab.sigmatiq.ai`
  - Gateway prefix: `/api/lab`
  - Docker image: `ghcr.io/<org>/sigma-lab-api:<tag>`
- Sigma Sim:
  - Brand: Sigma Sim
  - Repos: `sigma-sim-api`, `sigma-sim-ui`
  - Python package: `edge_sim_api`
  - Domain: `sigma-sim.sigmatiq.ai`, API: `api.sigma-sim.sigmatiq.ai`
  - Gateway prefix: `/api/sim`
  - Docker image: `ghcr.io/<org>/sigma-sim-api:<tag>`
- Sigma Market:
  - Brand: Sigma Market
  - Repos: `sigma-market-api`, `sigma-market-ui`
  - Python package: `edge_market_api`
  - Domain: `sigma-market.sigmatiq.ai`, API: `api.sigma-market.sigmatiq.ai`
  - Gateway prefix: `/api/market`
  - Docker image: `ghcr.io/<org>/sigma-market-api:<tag>`
- Sigma Pilot:
  - Brand: Sigma Pilot
  - Repos: `sigma-pilot-api`, `sigma-pilot-ui`
  - Python package: `edge_pilot_api`
  - Domain: `sigma-pilot.sigmatiq.ai`, API: `api.sigma-pilot.sigmatiq.ai`
  - Gateway prefix: `/api/pilot`
  - Docker image: `ghcr.io/<org>/sigma-pilot-api:<tag>`
