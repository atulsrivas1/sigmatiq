# Indicator Sets — How to Add / Enrich

Purpose
- Provide curated, beginner‑friendly sets of indicators with clear signal logic and guardrails. Files here are merged into seed SQL for `sc.indicator_sets`.

Where
- Add `<set_id>.json` in this folder (e.g., `momentum_breakout_v1.json`).

Minimum fields (novice‑first)
- `set_id`, `version`, `title`, `purpose`
- `components[]`: `{ indicator_id, params, role, timeframe? }` (3–7 components max)
- `reading_guide.signal_logic` and `reading_guide.timeframe_alignment`
- `novice_ready: true`, `beginner_summary`: one‑line plain explainer
- `simple_defaults`: `{ timeframe: '1m|5m|hourly|daily' }`
- `guardrails`: `{ universe_cap, throttle_per_min }` (use conservative defaults)
- `assistant_hints`: 3–4 bullets (how to combine safely; pitfalls)

Recommended
- `rationale`, `anti_patterns`, `data_requirements`, `performance_hints`, `tags`

Validate + Seed
- Lint indicators/sets: `make -C products/sigma-core lint-catalog` (Issues: 0 expected)
- Regenerate set seed: `make -C products/sigma-core gen-set-seed`

Notes
- Keep signal logic simple and outcome‑focused; avoid parameter soup.
- Prefer linking strategies to sets one‑to‑one for clarity.
