# Packs API Spec v1

## Status
Draft — implemented in backend (routers/packs.py)

## Endpoints
- GET `/packs`
  - Resp: `{ ok, packs: [{ id, meta }] }`
  - Notes: `meta` is parsed from `packs/<id>/pack.yaml` when present.

- GET `/packs/{pack_id}`
  - Resp: `{ ok, pack: { id, meta, indicator_sets: [{name}], templates: [{ template_id, name, template_version }], models: [model_id] } }`
  - Notes: `indicator_sets` from `indicator_sets/*.yaml`; `templates` from `model_templates/*.yaml`; `models` from `model_configs/*.yaml`.

- GET `/packs/{pack_id}/templates`
  - Resp: `{ ok, templates: [{ template_id, name, pack, horizon, cadence, template_version }] }`

- GET `/packs/{pack_id}/indicator_sets`
  - Resp: `{ ok, indicator_sets: [{ name }] }`

## Acceptance
- Returns 200 with `{ ok: true }` when pack exists; error `{ ok: false, error }` when not found.
- Handles missing pack.yaml gracefully.
- Lists are stable and sorted by filename.

