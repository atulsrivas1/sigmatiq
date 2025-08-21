# Getting Started

This page shows basic setup and navigation in plain English.

## Sign in and setup
- Configure `.env` (database and API key). Copy `.env.example` if needed.
- Run `make db-migrate` once to prepare the database.
- Start the API: `uvicorn products.sigma-lab.api.app:app --host 0.0.0.0 --port 8001`.

## Basic navigation (from UI mocks)
- Left sidebar shows: Dashboard, Models, Signals, Packs, Templates, Feature Flags, Users, Options Health, Performance, Admin, Docs.
- Top bar shows the page title and breadcrumbs.
- Cards and tables use clear labels and status badges like Success, Warning, Error, Info.

## Key screens to try first
- Dashboard: recent models, quick actions, health.
- Models: list and search, filters, view toggle (grid/list).
- Performance & Leaderboards: compare backtest runs and choose winners.

Related reading
- [Start Here](./START_HERE.md)
- [Modeling Pipeline Guide](./MODELING_PIPELINE_GUIDE.md)
- [Dashboard](./products/dashboard.md)
