Registry & Database

Completed
- Lazy pool init and `@contextmanager` get_db.
- Migrations added for ADR 0002 and backtest runs (`0001`, `0002`, `0003`).
- Backtest runs persisted with normalized columns + per-fold table; `/leaderboard` reads from DB.

Pending
- Optional SSL params for cloud DBs; add Make target for applying migrations.
- Consider storing model artifacts/versions in DB registry (future work per ADR 0002).
