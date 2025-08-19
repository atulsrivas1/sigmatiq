Sigmatiq Edge Workers

Scope
- Background jobs for products: scanners, schedulers, live loops, queues.
- Reads/writes via product APIs/DBs; shares libraries via edge-core/edge-platform.

Local Dev (placeholder)
- Run worker: python -m edge_workers.worker
- Lint/Type: ruff check .; black --check .; mypy .

Notes
- Sources live at products/edge-workers/edge_workers.
- Split per product later (e.g., separate workers repos) as needed.

