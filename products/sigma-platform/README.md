Sigmatiq Sigma Platform

Scope
- Shared API/server utilities: DB session helpers, migrations tooling, audit, lineage, pagination, policy, IO path helpers.
- No product routes here; imported by product APIs and workers.

Local Dev (placeholder)
- Test: pytest -q
- Lint/Type: ruff check .; black --check .; mypy .
- Build: python -m build (pyproject)

Notes
- In this workspace, sources live at products/sigma-platform/sigma_platform.
- Product Makefiles set PYTHONPATH to include this folder for local runs.

Repo vs Package Naming
- Repo folder uses kebab-case: `sigma-platform` (human-friendly, URLs)
- Python package uses snake_case: `sigma_platform` (import-friendly)
  This is why you see `products/sigma-platform/sigma_platform` — it’s expected.
