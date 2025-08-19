**Edge Family Repositories**
- Purpose: Define the set of repos, folder structures, naming conventions, and CI/CD guardrails for the Edge product family.

**Recommended Model (Polyrepo per Product UI/API)**
- Separate repository for each product API and each product UI.
- Common shared repositories for platform/core, SDK, infra, and packs.
- Optional gateway repository to provide a unified ingress across products.

Note: In this workspace, Edge Lab is organized as a product under `products/edge-lab/` and the shared libraries are packaged as `edge_core` and `edge_platform` within the same repo for development convenience. The repo split described below is the target long-term polyrepo model.

**Repo Overview**
- Common repos (shared by all products):
  - **edge-core**: Core Python libs (data, features, indicators, models, backtests, registry, storage).
  - **edge-platform**: API/platform utilities (db sessions, migrations tooling, audit, lineage, pagination, policy, IO helpers). Can be a separate repo or a subpackage inside `edge-core`.
  - **edge-sdk-py**: Python SDK with typed client, paginated iterators, lineage helpers, and contract tests.
  - **edge-infra**: Infra as code (Helm/Terraform), GH Actions reusable workflows, base Helm charts.
  - **edge-packs**: Strategy content (indicator sets, model configs, policy templates) versioned independently of runtime code.
- Product API repos (one per product):
  - **edge-lab-api**, **edge-sim-api**, **edge-market-api**, **edge-pilot-api**
- Product UI repos (one per product):
  - **edge-lab-ui**, **edge-sim-ui**, **edge-market-ui**, **edge-pilot-ui**
- Optional:
  - **edge-gateway**: Mounts `/api/{product}` to route requests to product APIs.

**Naming Conventions**
- **Repos**: lowercase with hyphens (e.g., `edge-core`, `edge-apis`, `edge-ui`).
- **Python packages**: lowercase with underscores (e.g., `edge_core`, `edge_platform`).
- **Docker images**: `ghcr.io/<org>/<repo>[:tag]`, hyphens preferred (e.g., `ghcr.io/org/edge-zeroedge-api`).
- **PyPI vs import**: Project names may use hyphens (e.g., `edge-sdk`), import uses underscore (`edge_sdk`).

**edge-core (repo)**
- **Purpose**: Shareable core logic across products; no API server code.
- **Top-level**:
  - `edge_core/`: datasets, features, indicators, models, backtests, evaluation, storage, registry
  - `tests/`: unit and integration tests
  - `pyproject.toml` / `setup.cfg`: build metadata
  - `README.md`, `CHANGELOG.md`
- **CI/CD**:
  - Lint, type check, tests, coverage, SAST, dep scan
  - Publish package on tag to private PyPI (SemVer)
- **Contracts**:
  - Stable function signatures for critical utilities
  - Backward-compatible changes preferred

**edge-platform (repo or subpackage in edge-core)**
- **Purpose**: Shared API/server utilities used by product apps and workers.
- **Top-level**:
  - `edge_platform/`: db session, config, audit, lineage, pagination, policy, IO helpers
  - `migrations/core/`: shared DB schema (signals, option_signals, backtests, audit)
  - `scripts/`: `apply_migrations.py`, `seed_data.py`
  - `tests/`, build files, docs
- **CI/CD**:
  - Same as `edge-core`, publish package on tag
  - Migration dry-run job (checks SQL syntax/orders)

**Product API repos (per product)**
- **Purpose**: Own the API server and product-specific workers for one product.
- **Top-level (example: edge-lab-api)**:
  - `edge_api/`: FastAPI app package
    - `app.py`: ASGI app entrypoint (or `apps/<product>/app.py`)
    - `routers/`: group by area; may include `common/` (if duplicated) and product-specific modules
    - `services/`: thin wrappers calling `edge_platform`
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
- **Top-level (example: edge-lab-ui)**:
  - `src/`: routes, components, brand tokens, product-specific features
  - `public/`: index.html, favicons
  - `vite.config.ts` (or Next.js config): API base pointing to the product API
  - `Makefile` / npm scripts: install/dev/build/preview
- **CI/CD**:
  - Lint, type check, unit/e2e (Playwright), build
  - Deploy independently (CDN/static hosting or container)
- **Config**:
  - Env-driven API base (e.g., `VITE_API_BASE_URL`) targeting the matching product API

**edge-sdk-py (repo, optional but recommended)**
- **Purpose**: Stable SDK for apps and notebooks; enforces API contracts in CI.
- **Top-level**:
  - `edge_sdk/`: typed client, paginated iterators, lineage helpers
  - `tests/`: contract tests against stub/golden schemas
  - Build files, README
- **CI/CD**:
  - Lint, type check, tests
  - Publish on tag (SemVer)

**edge-infra (repo, optional)**
- **Purpose**: Shared infra/ops tooling and reusable workflows.
- **Top-level**:
  - `helm/`: base charts or umbrella charts per app
  - `terraform/`: cluster, networking, databases, secrets
  - `.github/workflows/`: reusable Actions (build-python, build-node, docker-scan, deploy)
- **CI/CD**:
  - Validate Helm templates, Terraform plan, policy checks; no app builds here

**edge-packs (repo, optional)**
- **Purpose**: Versioned strategy content independent of runtime code.
- **Top-level**:
  - `{pack_id}/`: `indicator_sets/`, `model_configs/`, `policy_templates/`
  - `tools/`: validators, lints, schema checks
- **CI/CD**:
  - Validate pack schemas and policies; optionally publish pack bundles

**Routing & Deployment Patterns**
- **Direct mode (recommended)**: Each UI points to its matching product API base URL; deploy independently.
- **Gateway mode (optional)**: `edge-gateway` mounts `/api/{product}` → simplifies unified ingress; UIs can target gateway paths.

**Product Scope Summaries**
- **Edge Lab (edge-lab-api / edge-lab-ui)**: Pack and model authoring and management. Create/validate packs (indicator sets, model configs, policies), orchestrate build/train/backtest, lineage/model cards, QA gates, publish to `edge-packs`, audit/governance.
- **Edge Sim (edge-sim-api / edge-sim-ui)**: Simulation and scenario engines. Define scenarios, run batch sims/backtests, compare outcomes, manage artifacts and reports.
- **Edge Market (edge-market-api / edge-market-ui)**: Marketplace and subscriptions. List packs/models, manage subscriptions/entitlements, catalog search, product metadata.
- **Edge Pilot (edge-pilot-api / edge-pilot-ui)**: Automation/execution. Playbooks, guardrails, schedulers, live hooks; approvals and audit for actions.
- **Environments**: dev/staging/prod via GitHub Environments; secrets per env; manual prod approvals.

**Release & Versioning**
- **edge-core/platform**: SemVer with release notes; dependabot/renovate to bump downstream pins.
- **Product APIs**: Per-repo tags (e.g., `zeroedge-api:vX.Y.Z`) plus `:sha` images; Helm chart appVersion sync.
- **Product UIs**: SemVer per repo; Changesets or conventional commits.

**Security & Quality Gates**
- SAST (Bandit), pip-audit, Trivy scans, Gitleaks, license checks.
- Contract tests: ensure response envelopes and pagination remain stable.
- DB migration strategy: expand → backfill → contract; migration dry-run in CI.

**Decision Points**
- **edge-platform placement**: separate repo vs `edge_core.edge_platform` subpackage.
- **Gateway adoption**: use gateway from day one vs introduce later.
- **Packs coupling**: keep in `edge-apis` vs separate `edge-packs` repo for curated content.

**Migration (From Current Repo)**
- Phase 1: Create new repos: `edge-core`, `edge-platform`, `edge-lab-api`, `edge-lab-ui` (start with Edge Lab). Extract shared libs into `edge-core`/`edge-platform` with compatibility shims.
- Phase 2: Move current API into `edge-lab-api` (pack/model authoring, training/backtest orchestration), move UI into `edge-lab-ui` (retain branding/assets). Update Make targets and docs accordingly.
- Phase 3: Split migrations: keep shared schema in `edge-platform` (or duplicate in product repos) and product-specific migrations in `edge-lab-api`.
- Phase 4: Add `edge-sim-api/ui`, `edge-market-api/ui`, `edge-pilot-api/ui` as they come online; establish CI templates across repos.
- Phase 5: Stand up per-repo CI/CD; publish `edge-core/platform`; pin versions in product APIs; add optional `edge-gateway` if needed.

**Review Checklist**
- **Ownership**: CODEOWNERS assigned per repo/path; branch protections in place.
- **Isolation**: UI builds independently; product apps deploy independently or via gateway.
- **Contracts**: SDK + CI contract tests wired; pagination/envelope stability documented.
- **DB**: Migrations gated and reversible; seeds available; env secrets configured.
- **Security**: Scans enabled; dependency pinning and update automation configured.

**Next Steps**
- Confirm polyrepo model and repository names.
- Decide whether `edge-platform` lives standalone or inside `edge-core`.
- I can scaffold initial READMEs and GitHub Actions templates for each repo on approval.

**Alternative (Monorepo options, for reference)**
- APIs monorepo (`edge-apis`) and single UI (`edge-ui`) can be used if you later prefer cross-product atomic changes and path-filtered CI. Not the current recommendation but documented for completeness.
**Final Naming Matrix (Agreed)**
- Shared repos: `edge-core`, `edge-platform`, `edge-sdk`, `edge-packs`, `edge-infra`, optional `edge-gateway`.
- Edge Lab:
  - Brand: Edge Lab
  - Repos: `edge-lab-api`, `edge-lab-ui`
  - Python package: `edge_lab_api`
  - Domain: `edge-lab.sigmatiq.ai`, API: `api.edge-lab.sigmatiq.ai`
  - Gateway prefix: `/api/lab`
  - Docker image: `ghcr.io/<org>/edge-lab-api:<tag>`
- Edge Sim:
  - Brand: Edge Sim
  - Repos: `edge-sim-api`, `edge-sim-ui`
  - Python package: `edge_sim_api`
  - Domain: `edge-sim.sigmatiq.ai`, API: `api.edge-sim.sigmatiq.ai`
  - Gateway prefix: `/api/sim`
  - Docker image: `ghcr.io/<org>/edge-sim-api:<tag>`
- Edge Market:
  - Brand: Edge Market
  - Repos: `edge-market-api`, `edge-market-ui`
  - Python package: `edge_market_api`
  - Domain: `edge-market.sigmatiq.ai`, API: `api.edge-market.sigmatiq.ai`
  - Gateway prefix: `/api/market`
  - Docker image: `ghcr.io/<org>/edge-market-api:<tag>`
- Edge Pilot:
  - Brand: Edge Pilot
  - Repos: `edge-pilot-api`, `edge-pilot-ui`
  - Python package: `edge_pilot_api`
  - Domain: `edge-pilot.sigmatiq.ai`, API: `api.edge-pilot.sigmatiq.ai`
  - Gateway prefix: `/api/pilot`
  - Docker image: `ghcr.io/<org>/edge-pilot-api:<tag>`
