# Indicators Research Package (Single-Indicator Only)

Scope
- This package covers research and specs for individual indicators only.
- Use cases here each involve exactly one indicator. Combinations and sets are out of scope and will be handled in a separate exercise.

Contents
- `use-cases.md` — 12 single-indicator use cases with persona, workflow, data, latency, outputs.
- `use-case-matrix.md` — summary table of the single-indicator use cases.
- `system-architecture.md` — per-indicator compute and delivery flow.
- `technical-requirements.md` — indicator registry contract, caching, QA, lineage.
- `api-spec.md` — endpoints to validate and compute one indicator; screening supports single-indicator conditions.
- `performance-analysis.md` — costs and optimizations for single-indicator evaluation.
- `priority-matrix.md` — rollout plan for single-indicator features.
- `feature-specs.md` — top 5 single-indicator features with acceptance criteria.
- `interaction-transcript.md` — Engineer A/B whiteboard + critique focused on single-indicator use cases.
- `competitive-analysis.md` (optional) — platform handling of single indicators.
- `cost-model.md` (optional) — cost envelope for single-indicator workloads.

Notes
- Combinatorial logic, sets, and multi-indicator scoring belong in `indicator-sets` (to be created later).
