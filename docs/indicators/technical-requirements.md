# Technical Requirements — Indicator Engine (Single)

Scope
- Define the indicator computation engine, caching, validation, and versioning for single-indicator evaluation. Chaining and sets are out of scope here.

Engine Contracts
- Indicator registry entry
  - id (name), version (semver), category, description
  - params_schema (Pydantic/JSON Schema) with defaults and ranges
  - inputs: required columns and lookback
  - outputs: list of columns with dtypes
  - compute(df, params) -> DataFrame or dict of Series
  - metadata: cost_estimate, live_safe (bool), examples

Column naming
- Default: `<name>__<param_sig>__<out>` (collision-safe)
- Alias: optional `alias` replaces `<name>` in outputs
- Multi-output: append `__<out>` per column

Caching Strategy
- Key: hash(name, version, params, symbol, timeframe, range)
- Store: artifacts table + object storage path
- Modes: in-memory LRU for last-window, on-disk/object-store for bulk
- Invalidation: on version/param change; TTL for live

QA & Validation
- Pre: params validation
- Post: NaN ratios, monotonic timestamps, session alignment, iv sanity
- Report: structured QA report (warn/fail)

Data Abstraction
- Fetchers: bars (1m/5m/15m/hourly/daily), options IV/eod, VIX
- Unified schema: `timestamp`, `open/high/low/close/volume`, `session_flags`

Performance
- Vectorized ops; incremental updates; reuse windows
- Batch micro-batching per universe; safe parallelism by symbol

Versioning & Lineage
- Track indicator version and git sha in artifacts/runs
- Compatibility: additive only; breaking → version bump

Security & Sandbox (custom indicators)
- Optional user-defined indicators: restricted Python/DSL with time/memory limits
- Manual review to publish into registry
