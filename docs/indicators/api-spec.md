# API Specification — Single Indicator

Base: `/indicators` (existing), focused on single-indicator operations.

List Indicators
- GET `/indicators`
  - Query: `category?`, `live_safe?`
  - Response: `{ ok, indicators: [{ id, version, category, params_schema, outputs, meta }] }`

Validate Indicator Params
- POST `/indicators/validate`
  - Body: `{ id, version?, params }`
  - Response: `{ ok, valid, errors? }`

Compute One Indicator (On-Demand)
- POST `/indicators/compute`
  - Body: `{ symbol, start, end, item: { id, version?, params, alias? }, timeframe?: '1m|5m|15m|hourly|daily', include_inputs?: bool }`
  - Response: `{ ok, columns: [..], rows: N, data_uri?, sample: [{ ts, col1, ... }] }`

Screening (Single-Indicator Conditions)
- POST `/screen`
  - Body: `{ universe: [symbols]|preset_id, at?: ts|bar, condition: { id, params, op, value }, window?: N, timeframe? }`
  - Response: `{ ok, matches: [{ symbol, ts, value }], count }`

Streaming (WebSocket)
- WS `/ws/indicators`
  - Subscribe: `{ action: 'subscribe', symbol, item, timeframe, throttle_ms? }`
  - Screen stream: `{ action: 'screen', universe, condition, timeframe, throttle_ms? }`
  - Server events: `{ type: 'update'|'match'|'heartbeat', payload }`

Artifacts & Lineage
- Responses include `data_uri` (CSV/Parquet) and versions/git sha.

Rate Limits & Guardrails
- Quotas per user; caps on universe size and frequency.
