## Summary
- What changed and why (1–3 lines).

## Critic Report (Persona: Code Review Critic)
- Risks to novices:
- Safety gaps (caps/guardrails/undo, costs/risks clarity):
- Complexity increases (simpler alternative):
- Defaults & scope (safe & reversible; on/off):
- API & contracts (docs parity; mode:simple; fields:full; consensus echo):
- Data/migrations (idempotent; novice fields; seeds/lints):
- Errors & DX (plain 400s; env/DB gating):
- Tests & Postman (examples copy/paste runnable & safe):

## Status
- Blockers:
- Major issues:
- Nits:

## Checklist
- [ ] Critic pass completed using `docs/personas/code_reviewer.md` and `docs/CODE_REVIEW_GUIDELINES.md`.
- [ ] Safe defaults + caps enforced (≤90 days, ≤50 symbols, ≤50 combos).
- [ ] `mode: simple` (where relevant) + `fields=full` extras documented.
- [ ] Plain-language errors + next steps.
- [ ] Docs, seeds, and Postman updated.
- [ ] Tests added/updated where patterns exist.

## Screenshots / Examples (optional)

