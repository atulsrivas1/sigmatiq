# Indicator Sets & Feature Bundles — Research Package

Scope
- This package covers research and specs for multi-indicator sets (feature bundles). Each use case involves 3–7 indicators working together. Single-indicator cases are documented separately under `docs/indicators/`.

Contents
- `use-cases.md` — 12+ multi-indicator set use cases with persona, components, data, latency, outputs.
- `use-case-matrix.md` — summary matrix of set use cases.
- `set-architecture.md` — structure, storage, inheritance, and rules for sets.
- `technical-requirements.md` — smart combination engine, redundancy/conflict detection, multi-timeframe handling.
- `set-api-spec.md` — endpoints to create/modify/evaluate/backtest/subscribe to set signals.
- `performance-analysis.md` — cost/performance by set type and optimizations.
- `priority-matrix.md` — phased plan and decision gates for sets.
- `feature-specs.md` — top 5 set features with acceptance criteria.
- `interaction-transcript.md` — Engineer A/B whiteboard + critique focused on sets.
- `competitive-analysis.md` (optional) — how platforms handle strategy combos.
- `cost-model.md` (optional) — cost envelope for set workloads.

Note
- Indicators registry and single-indicator APIs are prerequisites; sets build on top with composition and rules.

