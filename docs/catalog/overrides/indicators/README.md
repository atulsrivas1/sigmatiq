# Indicator Content Overrides — How to Add

Purpose
- These JSON files enrich the auto-generated indicator seed with plain-language guidance for non‑traders. The seeding script merges these into INSERTs for `sc.indicators`.

Where
- Add a file in this folder named exactly as the indicator id (e.g., `rsi.json`, `macd.json`).

Required (for novice readiness)
- `novice_ready: true`
- `beginner_summary`: one‑line plain explainer
- `measures`: include at least `what_it_measures` and `how_to_read`
- `usage.example_conditions`: 1–2 concrete conditions (e.g., `"rsi(period=14) < 30"`)
- `assistant_hints`: 3–4 short bullets (do’s/don’ts)

Recommended
- `data_requirements` (inputs, timeframe, lookback)
- `performance_hints` (cost_band, latency_band, stability)
- `tags`, `media`

Validate + Seed
- Lint indicators/sets: `make -C products/sigma-core lint-catalog` (Issues: 0 expected)
- Regenerate indicator seed: `make -C products/sigma-core gen-indicator-seed`

Notes
- Technical params come from builtin class signatures; use this override to add human-facing context, not to change computation.

