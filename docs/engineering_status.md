Sigmatiq Products — Engineering Status (Working Notes)

Last Commit
- Branch: main
- Commit: 2e0d240 (plus prior commits in this session)

Scope Completed
- Brand rename
  - Edge → Sigma across repos/folders and Python packages (`edge_*` → `sigma_*`).
  - Sigmatix → Sigmatiq across docs, UI, and assets (non-archive docs).
  - Pack IDs: zeroedge→zerosigma, swingedge→swingsigma, longedge→longsigma, overnightedge→overnightsigma, momentumedge→momentumsigma.
  - Indicator sets: renamed files and references (`zeroedge_*` → `zerosigma_*`).
- Code updates
  - Imports updated to `sigma_core`, `sigma_platform`, `sigma_workers`.
  - API titles and docstrings updated to Sigma.
  - Dynamic imports in indicators registry now use `sigma_core.indicators.builtins.*`.
- UI + Docs
  - UI attributes: `data-edge` → `data-sigma` and selector updates.
  - Branding tokens: moved to `--sigma-*`; asset and token filenames updated (e.g., `edge-pack-themes.css` → `sigma-pack-themes.css`).
  - Branding assets and icons renamed to `*sigma*` variants.
- Tooling
  - Brand sweep script (sigma-lab/ui/scripts/brand_sweep.cjs) + Make target `make -C products/sigma-lab brand-sweep`.
  - Mock API service for UI: products/mock-api (FastAPI) with core endpoints.
  - Git hygiene: added products/.gitignore; removed tracked __pycache__/ and .pyc files.
- Tests
  - pytest.ini added at products/.
  - sigma-core tests: labels, features builder, indicators registry.
  - sigma-lab API tests: endpoints smoke + services (io/policy) basic validation.
  - Manual runner used to validate tests in this environment; all selected tests passed.

How to Run
- Sigma Lab API
  - python products/sigma-lab/api/run_api.py --host 0.0.0.0 --port 8001 --reload
- Mock API (UI dev)
  - pip install -r products/mock-api/requirements.txt
  - make -C products/mock-api dev  (serves on http://localhost:8010; docs at /docs)
- Tests
  - Core: pytest products/sigma-core/tests -q
  - API: pytest products/sigma-lab/api/tests -q
  - All (if environment allows): pytest -q
  - Coverage (if pytest-cov available): pytest --cov=sigma_core --cov=sigma_platform --cov=products/sigma-lab/api --cov-report term-missing
- Brand enforcement
  - make -C products/sigma-lab brand-sweep

Known Reminders / Open Items
- Docs under `products/sigma-lab/docs/_archive/` intentionally untouched (legacy).
- Some plain-English “edge” phrases remain in prose (e.g., “edge cases”); correct usage, not branding.
- Consider wiring CI to run: brand sweep, pytest (core + API), and docs link checks.
- Optional: add pytest-cov to dev requirements and enforce minimum coverage threshold.
- Expand tests: datasets/training/sweep routers happy/err paths; a couple of built-in indicators compute checks on tiny DataFrames.
- Consider top-level Make targets for common dev flows (API start, Mock start, tests).

Next Session Starting Points
- Hook pytest + coverage into CI; set baseline and threshold.
- Add UI integration tests against Mock API for key pages (signals, leaderboard, scanners).
- Review any team-provided TODOs in sigma-lab/docs/BACKLOG.md and docs/todos/.
- If needed: create migration scripts/templates for renamed DBs (`sigma_*`).

Quick Links
- Mock API guide: products/mock-api/README.md
- Sigma Lab docs index: products/sigma-lab/docs/INDEX.md
- Brand sweep script: products/sigma-lab/ui/scripts/brand_sweep.cjs
- Tests entry points: products/sigma-core/tests/, products/sigma-lab/api/tests/

