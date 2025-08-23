# Pull Request

- Title:
- Summary (plain language, 1–2 sentences):
- Related Issue/Doc link(s):

## What’s Changing
- 

## Critic Gate (Mandatory)
Refer to docs/CRITIC_CHECKLIST.md. If any item fails, do not merge.

- [ ] Critic pass completed; notes/mitigations linked here: <!-- link to doc/comment -->
- [ ] Beginner summary: plain language (no jargon); user understands outcome in seconds
- [ ] Defaults: safe, reversible, obvious off switch; advanced options hidden
- [ ] Guardrails: quotas/diversity/undo enforced (DB + code where applicable)
- [ ] Scope & simplicity: preset/story-driven path; no parameter soup; ≤ 1 screen where feasible
- [ ] Transparency: risks/costs/delays explained; preview before subscribe/commit; clear opt-out
- [ ] Data & reproducibility: training-serving parity; avoid caching today; training_cfg captured (if models)
- [ ] Branding & naming: `sq_` prefix for model/pack IDs; `display_name` set; clear user-facing names
- [ ] Taxonomy & scope: horizon/style/tags set; scope (cohort/per-ticker) declared if models
- [ ] Novice publish readiness: beginner_summary + explainer_templates + guardrails/consensus present (models/packs)
- [ ] Docs updated (agents.md, requirements/whiteboarding, API examples) where applicable

## Testing
- How was this tested? Include commands, datasets, and results.

## DB Migrations (if any)
- [ ] New migrations listed and applied locally
- List: 

## API & Backwards Compatibility
- [ ] No breaking changes OR documented migration path
- Details:

## Screenshots / API Examples (optional)
- 
