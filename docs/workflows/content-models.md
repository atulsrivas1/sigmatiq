# Workflow Content Model

WorkflowMeta (explainer payload)
- id: stable identifier (`find_oversold_large_caps_v1`)
- version: semantic content version (not code)
- status: draft | in_review | published
- title: short goal‑oriented title ("Find Oversold Stocks (5 minutes)")
- subtitle: one‑line plain explanation
- goal: outcome the user achieves
- persona: day_trader | swing_trader | investor | options_trader | pm | beginner
- difficulty: beginner | intermediate | advanced
- time_to_complete: minutes estimate (int)
- prerequisites: short bullets (data/API keys, DB, dates)
- dependencies: { indicators: [ids], indicator_sets: [set_ids], strategies: [strategy_ids] }
- steps: ordered list of plain‑language steps; each step may include
  - description: short instruction
  - rationale: why this step matters
  - api: { method, path, query?, body? }  // example only; user can adapt
  - expects: quick check for success (what to see in the response)
- outputs: what the user gets (list entries, alerts, plot URIs, leaderboard rows)
- best_when: conditions when this workflow shines
- avoid_when: conditions to skip or adjust
- caveats: small risks or gotchas
- media: { cover_uri, gallery: [{ uri, alt, caption, kind }] }
- links: references to catalog explainers and docs pages
- research: evidence bullets and references
- lineage: { content_version, generated_from_docs_uri?, reviewed_by?, last_reviewed_at? }

