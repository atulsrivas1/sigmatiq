# Critic Checklist (Mandatory for All Sessions)

Use this checklist before accepting designs, changes, or publishing content/models. If any item fails, stop and propose a simpler, safer alternative.

- Novice-first
  - Plain language (no jargon) and clear beginner summary.
  - One-tap/one-screen where possible; hide advanced under “Advanced”.
  - Defaults are safe, reversible, and clearly explained.
- Safety & Guardrails
  - Quotas and diversity caps in place; throttle bursty behavior.
  - Undo/mute/snooze paths; no hidden state changes.
  - Guardrails persisted in DB (sets/strategies/models/packs) and enforced at publish.
- Scope & Simplicity
  - Is there a preset/story-driven path instead of parameters?
  - Are we avoiding new toggles/flags unless they benefit novices?
  - Can a first-time user succeed in 60 seconds?
- Transparency
  - Risks, costs, and delays explained up front.
  - Preview available before subscribe/commit; clear opt-out.
- Data & Reproducibility
  - Feature/label parity between training and serving; avoid “today” cache.
  - Training config captured (`training_cfg`) with windows, session, CV, filters.
- Branding & Naming
  - Model IDs/packs use `sq_` prefix; display_name user-friendly.
  - Taxonomy (horizon/style) and scope (cohort/per-ticker) declared.

Record findings in the PR or session notes and link to mitigations.
