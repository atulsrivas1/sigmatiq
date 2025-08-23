# Catalog API — Read-Only Spec

Principles
- Return rich, human-friendly explainers for Indicators, Indicator Sets, and Strategies.
- Default to latest `published` version; include lineage and media URIs.

List Endpoints
- GET `/catalog/indicators`
  - Query: `category?`, `persona?`, `tag?`, `q?`, `limit=20`, `offset=0`
  - Response: `{ ok, items: [{ id, version, title, short_description, category, tags, media: { cover_uri } }], count, next_offset }`

- GET `/catalog/indicator_sets`
  - Same query shape; similar list item fields (`set_id`, `purpose`)

- GET `/catalog/strategies`
  - Query adds `horizon?` and `asset_class?`

Detail Endpoints (Explainers)
- GET `/catalog/indicator/{id}`
  - Response: full IndicatorMeta (see content model)

- GET `/catalog/indicator_set/{set_id}`
  - Response: full IndicatorSetMeta

- GET `/catalog/strategy/{strategy_id}`
  - Response: full StrategyMeta

Auxiliary
- GET `/catalog/glossary?q=` → `{ ok, terms: [...] }`
- GET `/catalog/media/{asset_id}` → media resource or redirect (optional)

Version Selection (optional)
- `?version=x.y.z` returns specific explainer version; 404 if not published unless `include_unpublished=true` with auth.

Errors
- JSON API errors with `{ ok:false, code, message }`; include `hint` when safe.

