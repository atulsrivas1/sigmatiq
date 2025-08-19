# Universe Lists

Curated CSV universes for scanning. Each file has a `ticker` header and one symbol per line.

- `sample10.csv`: small demo set for quick checks.
- `nasdaq100.csv`: large‑cap, tech‑heavy list (approx. NASDAQ‑100 style; maintain as needed).
- `nasdaq200.csv`: expanded tech/growth universe (~200 names) for broader scans.

Notes
- These lists are convenience presets, not point‑in‑time index memberships.
- Update periodically or replace with your own CSVs for production.
- Use with scanners by passing `UNIVERSE_CSV=...` to Make targets or `--universe_csv` to scripts.

