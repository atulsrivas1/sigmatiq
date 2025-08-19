# Scanner Universe – TODOs

Priority: High for usability; enables one-command scans without manual ticker lists.

- Built-in universes: add CSVs under `data/universe/`
  - Files: `sp100.csv`, `sp500.csv`, `nasdaq100.csv`, `russell1000.csv`
  - Schema: `ticker` (uppercase), optional `name`, `sector` (if available)
  - Source: static snapshot for now; later switch to point-in-time provider

- CLI support: accept a named universe
  - `scripts/scanner_breakout_momentum.py`: add `--universe sp500|sp100|nasdaq100|russell1000`
  - Resolution order: `--universe_csv` > `--universe` (named) > `--tickers`
  - When `--universe` is used, load from `data/universe/<universe>.csv`

- API support: named universes in `/scan`
  - Add `universe` (string) param alongside `universe_csv` and `tickers`
  - Server resolves to `data/universe/<universe>.csv`
  - Validation: 404 if unknown name or file missing

- Universe service (longer-term)
  - Module: `edge_core/data/universe.py` with helpers:
    - `load_universe(name|path)`
    - Filters: price ≥ $5, ADV_20 ≥ 1M, optionability flag
    - Point-in-time memberships (index constituents) when provider available
  - Endpoint: `GET /universe?name=sp500` to preview count and sample
  - Health: extend `/healthz` to include coverage on the chosen universe

- Make targets and docs
  - `make scan UNIVERSE_NAME=sp500` (shortcut to named universes)
  - Update runbooks to show named-universe flows
  - Add small sample universe under `data/universe/sample10.csv` for CI smoke

- UI wizard integration
  - Step to choose universe: named sets or upload CSV; show count and filters applied
  - Persist selection into model config metadata for reproducibility

