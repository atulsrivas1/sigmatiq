# Whiteboarding — AI Dev Design (Extensible)

Participants
- Dev1 (Lead ML Eng): modeling, feature abstraction, serving
- Dev2 (Data/Platform Eng): data adapters, pipelines, MLOps
- Dev3 (Applied Scientist): labeling, calibration, evaluation

Agenda (60–75 min)
- 0–10m: Scope + non-goals (avoid overbuild)
- 10–25m: Core abstractions (feature, label, model, scorer, plan)
- 25–40m: Extensibility (countries, instruments, regimes)
- 40–55m: Data + pipelines (offline/online parity, cache, adapters)
- 55–70m: Serving + APIs + monitoring + A/B
- 70–75m: Risks, next steps, owners
 - Critic checkpoint (mandatory): challenge complexity, surface novice risks, propose simpler defaults.

Goals
- Produce a modular design spec and interfaces we can implement incrementally.
- Ensure extension to multiple exchanges/markets and instruments without rewrites.
- Keep novice‑first guardrails embedded at every layer.
