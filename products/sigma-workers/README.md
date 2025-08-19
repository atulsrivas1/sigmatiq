Sigmatiq Sigma Workers

Scope
- Background jobs for products: scanners, schedulers, live loops, queues.
- Reads/writes via product APIs/DBs; shares libraries via sigma-core/sigma-platform.

Local Dev (placeholder)
- Run worker: python -m sigma_workers.worker
- Lint/Type: ruff check .; black --check .; mypy .

Notes
- Sources live at products/sigma-workers/sigma_workers.
- Split per product later (e.g., separate workers repos) as needed.

