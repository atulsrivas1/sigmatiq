# Content Models — Indicators, Sets, Strategies

Overview
- Define explainer payload fields returned by the Catalog API. Content is authored/reviewed, versioned, and published.

Common Fields (all)
- `id`/`set_id`/`strategy_id`: stable identifier
- `version`: semantic version for the explainer content (not code)
- `status`: `draft | in_review | published`
- `title`, `subtitle`, `short_description`, `long_description`
- `tags`: `[category, persona, difficulty, risk, use_case, ...]`
- `media`: `{ cover_uri, gallery: [{ uri, alt, caption, kind }], diagram_uri? }`
- `research`: `{ references: [{ title, url, note }], reviewed_by, last_reviewed_at, confidence_score }`
- `i18n?`: localized variants per field (future)
- `lineage`: `{ code_version?, git_sha?, generated_from_docs_uri?, content_version }`

IndicatorMeta
- `id`, `version`, `status`
- `title`, `subtitle`, `short_description`, `long_description`
- `category`, `subcategory`, `tags[]`
- `parameters[]`: `{ name, label, description, type, default, min?, max?, typical_range? }`
- `measures`: `{ what_it_measures, how_to_read, typical_ranges, caveats }`
- `data_requirements`: `{ inputs, timeframe, lookback, dependencies? }`
- `usage`: `{ best_when: [], avoid_when: [], example_conditions: [], step_by_step: [] }`
- `performance_hints`: `{ cost_band: low|med|high, latency_band: rt_ultra|rt_fast|near_rt|batch, stability: low|med|high }`
- `assistant_hints?`: `[]` (3–5 short bullets to emphasize in assistant responses)
- `media`, `research`, `i18n?`, `lineage`

IndicatorSetMeta
- `set_id`, `version`, `status`, `title`, `purpose`
- `components[]`: `{ indicator_id, params, role, weight?, timeframe? }`
- `rationale`: `why_these_work_together`
- `reading_guide`: `{ signal_logic, weighting_rules?, timeframe_alignment }`
- `risk_notes?`, `anti_patterns[]`, `redundancy_notes?`, `conflict_notes?`
- `data_requirements`, `performance_hints`, `media`, `research`, `i18n?`, `lineage`
- `assistant_hints?`: `[]` (top takeaways the assistant should surface)

StrategyMeta
- `strategy_id`, `version`, `status`, `title`, `objective`
- `entry_logic`, `exit_logic`, `filters?`, `examples[]`
- `risk`: `{ position_sizing, stops_targets, daily_loss_limit?, exposure_caps? }`
- `execution_policy`: `{ slippage_model, order_types, hours, liquidity_rules }`
- `pre_reqs`: `{ datasets, indicator_sets_used }`
- `performance_snapshot`: `{ sharpe_range?, dd_range?, winrate_range? }`
- `caveats`, `compliance_note`, `how_to_evaluate[]`
- `media`, `research`, `i18n?`, `lineage`
- `assistant_hints?`: `[]` (simple bullets the assistant can use to coach users)

WorkflowMeta (addition)
- Add optional `assistant_hints?`: `[]` (plain tips and “what to focus on” for users).

Shared Aux
- MediaAsset: `{ id, uri, alt, caption, kind, width?, height?, sha256? }`
- GlossaryTerm: `{ term, plain_definition, longer_explainer?, media_refs?[] }`
- Reference: `{ title, url|doi, note?, relevance_tag? }`
- Tag: `{ id, kind: category|persona|difficulty|risk|use_case, label, description? }`

Field Ownership and Non-Overlap
- Purpose: avoid duplicated meaning across Indicators vs Indicator Sets. Keep single ownership per concept.
- Ownership rules
  - Indicator-only fields: `parameters[]`, `measures` (what_it_measures, how_to_read, typical_ranges, caveats).
  - Set-only fields: `components[]`, `rationale`, `reading_guide` (signal_logic, weighting_rules, timeframe_alignment), `anti_patterns`.
  - Shared fields with scoped meaning:
    - `data_requirements`: Indicator = required inputs/lookback for that indicator. Set = union/summary of component inputs and timeframe guidance; never restate per-indicator details.
    - `performance_hints`: Indicator = cost/latency/stability for computing one indicator. Set = aggregated/worst-case across components (author-provided today; may be auto-derived later).
    - `assistant_hints`: Indicator = how to read/use this indicator. Set = how to combine components safely; pitfalls of the combo.
    - `beginner_summary` (novice-only): Indicator = “what it means” in plain language. Set = “why these together” and “how to use” in one sentence.
  - Prohibited overlaps:
    - Do not include `parameters` or `measures` in indicator set JSON.
    - Do not restate component-level logic in set `measures`; use `reading_guide.signal_logic` instead.
    - Do not copy indicator docstrings into set descriptions; keep set content about combination logic and usage.

Validation guidance (authoring/linting)
- Indicator JSON must include: `category`, `subcategory`, `parameters[]` (or inferred), `measures`, `data_requirements`. If `novice_ready=true`, must include `beginner_summary`.
- Indicator Set JSON must include: `components[]`, `rationale`, `reading_guide.timeframe_alignment`. If `novice_ready=true`, include `beginner_summary` and prefer providing `simple_defaults` and `guardrails`.
- If a set JSON includes indicator-only fields (`parameters`, `measures`), they will be ignored by generators and should be removed in review.
