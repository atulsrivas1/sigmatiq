# Workflows Library — Plain‑Language Recipes

Purpose
- Provide simple, goal‑oriented workflows that non‑traders can follow. Each workflow explains what to do, why it matters, and which indicators, indicator sets, or strategies it uses — all via API/data first. UI can plug in later.

Contents
- `content-models.md` — canonical workflow schema (plain language, steps, deps, media).
- `api-readonly-spec.md` — read‑only endpoints to list and fetch workflows.
- `taxonomy.md` — categories, personas, difficulty, time‑to‑complete, goals.
- `templates.md` — authoring template for clear, consistent workflows.
- `use-cases.md` — catalog of recommended workflows by persona and goal.
- `editorial-workflow.md` — author → review → publish; style and quality gates.
- `seeding-plan.md` — how to seed from our existing docs and examples.
- `examples/` — sample JSON workflows users can consume via API.

Design Principles
- Plain English first; keep steps short and checkable.
- API‑first: include concrete request examples (paths/bodies) but no UI.
- Evidence‑based: link to the explainer docs for indicators/sets/strategies.
- Guardrails: call out prerequisites, caveats, and safety checks.

