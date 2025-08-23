# Workflows API — Read‑Only Spec

List
- GET `/catalog/workflows`
  - Query: `persona?`, `goal?`, `category?`, `difficulty?`, `time_lte?`, `q?`, `limit=20`, `offset=0`
  - Response: `{ ok, items: [{ id, version, title, subtitle, persona, difficulty, time_to_complete, media: { cover_uri } }], count, next_offset }`

Detail
- GET `/catalog/workflow/{id}`
  - Response: full WorkflowMeta (see content model), including steps with example API calls.

Notes
- Returns `published` versions by default; `?version=x.y.z` optional.
- Media URIs are included; UI may render or link.

