# Sigma Workers

## What it is

Sigma Workers is envisioned to handle background jobs for various Sigmatiq products. This includes tasks like running scanners, schedulers, and live loops, and managing queues.

## Why it matters

Sigma Workers will offload computationally intensive or long-running tasks from the main application, ensuring a responsive user interface and efficient processing of background operations.

## Planned Structure

*   **Background Jobs**: Will include scanners, schedulers, live loops, and queue management.
*   **Integration**: Will read/write via product APIs/DBs and share libraries via `sigma-core` and `sigma-platform`.

## Local Development (Placeholder)

*   **Run worker**: `python -m sigma_workers.worker`
*   **Lint/Type**: `ruff check .; black --check .; mypy .`

**Note**: This product is currently a placeholder, and its full implementation is pending. The source code lives at `products/sigma-workers/sigma_workers`.
