# AI Assistant — Explainer Simplification (Future Work)

Goal
- Help non‑traders understand indicators, indicator sets, strategies, and workflows by translating technical terms into plain English, offering tiered explanations, and guiding next actions without overwhelming users.

Scope
- Contextual Q&A over catalog explainers (Indicators, Sets, Strategies, Workflows).
- Progressive disclosure: beginner → intermediate → advanced views.
- Inline definitions and examples (pull from Glossary and Examples).
- Action guidance: suggest workflows, screens, or backtests based on intent.

User Experience
- Modes: Explain (what/why), Read (how to read), Caveats (risks), Try (next step).
- Levels: "Explain like I’m new", "Short summary", "Deep dive".
- Examples: one concrete example per concept; avoid jargon.
- Suggestions: link to workflows (API-first), not UI.

Data Sources
- `sc.*` tables (published views):
  - Indicators: measures, usage, data_requirements
  - Sets: components, rationale, alignment
  - Strategies: entry/exit, risk, policy
  - Workflows: steps with example API calls
- Glossary and references when available.

API (Assistant endpoints; later)
- POST `/assistant/explain`
  - Body: `{ kind: 'indicator'|'set'|'strategy'|'workflow', id, level: 'beginner'|'summary'|'deep', locale?: 'en-US', focus?: 'how_to_read'|'caveats'|'examples' }`
  - Response: `{ ok, text, bullets?, examples?, links? }`
- POST `/assistant/compare`
  - Body: `{ kind, ids: [...], level }` → differences and when to use which.
- POST `/assistant/recommend`
  - Body: `{ goal: 'find_breakouts'|'gate_0dte'|..., persona?, time? }` → workflows/sets/indicators to try.

Prompting Strategy (Server‑side)
- Ground every response in fetched `sc.*` explainer fields; never hallucinate values.
- Use templates per kind + level; include glossary definitions inline.
- Summarize in 3–5 bullets; add one example; end with one suggested next step.

Guardrails
- Keep explanations factual; include caveats; avoid performance promises.
- Respect locale; avoid jargon; define terms at first use.
- Rate limits; length caps (e.g., 120–180 words for beginner level).

Telemetry (Opt‑in)
- Track which fields users ask about; top confusion points; popular workflows after assistant suggestions.
- Feed insights back into explainer edits (editorial workflow).

Editorial Hooks (Content Model Additions — optional)
- `assistant_hints`: short bullets authors can add per entity for the assistant to emphasize/avoid.
- `examples`: curated short examples the assistant can reuse.

Rollout Plan
- Phase 1: Read‑only explainer Q&A for Indicators (beginner + summary).
- Phase 2: Add Sets and Workflows + recommendations.
- Phase 3: Add Strategies + comparisons and guardrails.

