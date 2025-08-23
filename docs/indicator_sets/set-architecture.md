# Set Architecture Design

Goals
- First-class, versioned, auditable indicator sets with reusable components and rules.
- Prevent redundant/contradictory combinations; optimize compute reuse.

Set Model
- Identity: `set_id`, `name`, `category`, `version`, `description`, `owner`, `tags`.
- Components: 3–7 items `{ id, version?, params, alias?, timeframe?, weight?, depends_on?[] }`.
- Rules: boolean logic/thresholds; conflict resolution (priority/weights); time alignment policies.
- Weights: optional scoring map `{ component_id: weight }`; standardized score 0–100.
- Constraints: universe caps, min liquidity, data completeness, session rules.
- Variants: `base_set_id` + JSON Patch `diff` for overrides; max inheritance depth=1.

Storage & Versioning
- DB JSONB per 0015 migration (`indicator_sets` table with `data` JSONB) for user and pack scope.
- Git-tracked YAML templates for published presets; DB for user-defined sets.
- Semantic versioning; breaking rule changes bump major.

Multi-Timeframe Handling
- Component-level `timeframe` required when differing from set default; explicit resampling rules (up/down-sample + alignment).
- Disallow implicit timeframe mixing.

Computation Reuse
- Build a compute plan (DAG) across requested sets; deduplicate identical indicator computations across sets/symbols.
- Cache key: `(id, version, params, symbol, timeframe)`.

Guardrails
- Redundancy detector (oscillators overlap, duplicated EMAs).
- Conflict detector (momentum + mean reversion at equal priority without gating).
- Cost estimator; warn on SLA/quota breaches.

Lineage & Audit
- Persist resolved set JSON, SHA, indicator versions, timeframes, data windows, and code git sha alongside results/artifacts.

