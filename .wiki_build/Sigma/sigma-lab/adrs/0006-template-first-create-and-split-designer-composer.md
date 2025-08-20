# ADR 0006: Template‑First Create and Split Designer vs Composer

## Status
Accepted — 2025-08-18

## Context (the issue)
- The initial Create flow asked users to pick indicators and set policy before they had any context, causing decision fatigue and slower time-to-first-result.
- Mixing structural edits (indicators/policy) with the BTB flow (Build → Sweeps → Leaderboard → Train) muddled the mental model and increased errors.
- We need a fast path to a working model, with clear places for structure (edit) vs operations (compose).

## Decision
- Make “Create Model” a template-first picker (templates are pack-aware and opinionated).
- Split workspaces:
  - Designer (noun): edit structure — indicator set, policy, metadata. Save prompts rebuild when needed.
  - Composer (noun): run operations — Build → Sweeps → Leaderboard → Train; gate and lineage-first.
- After Create, deep-link to Composer by default (primary), with an option to open Designer.
- Add `template_id` and `template_version` to lineage and model card.

## Rationale
- Reduces choice overload and gets users to results quickly.
- Keeps BTB focused and self-explanatory; separates editing from experiments/training.
- Improves reproducibility: template, risk profile, and budgets are stamped in lineage.

## Consequences
Positive
- Faster onboarding; fewer invalid configs; clearer IA (Designer vs Composer).
- Assistant can recommend templates and explain differences between risk profiles.

Trade-offs
- Requires maintaining a template catalog per pack.
- Two workspaces to design (Designer, Composer) versus one.

## Implementation Notes
- Templates: `products/sigma-lab/packs/<pack>/model_templates/*.yaml`; catalog under `configs/templates/catalog.json`.
- API (docs-only): `GET /model_templates`, `POST /models { template_id, name, risk_profile }`.
- Lineage: include `template_id`, `template_version` in cards and runs.
- UI: Update Create, Wireframes, and Requirements to use Template Picker; add Designer page; keep Composer tabs.

## Alternatives Considered
- Keep Create as a full wizard (Basics → Indicators → Policy → Preview → Save): slower, higher friction, higher error rate.
- Call the pipeline “Designer”: misleading for an operational flow; we reserve Designer for structure editing.

## References
- Model Templates Spec v1
- Matrix Contract v1, Risk Profile Schema, Gate & Scoring Spec v1
