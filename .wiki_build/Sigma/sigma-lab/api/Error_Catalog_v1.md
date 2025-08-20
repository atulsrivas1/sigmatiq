# Error Catalog v1 — Codes, Status, Shape

## Status
Draft — aligns with BTB/Assistant API specs

## Response Shape
```jsonc
{
  "error": {
    "code": "STRING_CODE",
    "message": "Human-friendly message",
    "details": { }
  }
}
```

## Codes & HTTP Mapping
- INVALID_PARAM (400): request validation failed; include field errors in details
- NOT_FOUND (404): resource missing (e.g., sweep_id, run_id)
- CONFLICT (409): duplicate or conflicting state (e.g., duplicate job without force)
- UNPROCESSABLE (422): semantically invalid (e.g., bad config tuple)
- FORBIDDEN (403): disallowed action (e.g., execute without confirmation)
- RATE_LIMITED (429): too many requests; include retry-after header
- QUOTA_EXCEEDED (403): per-user quota exceeded (sweeps/train)
- GATE_FAILED (400): attempted to train a failing config without override
- TIMEOUT (504): upstream/worker timed out; request id included
- INTERNAL (500): unexpected error; request id included

## Details Payload (examples)
- INVALID_PARAM
  - details: { field_errors: [{ field, issue }] }
- RATE_LIMITED
  - details: { limit: 60, window_sec: 60 }
  - headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`
- QUOTA_EXCEEDED
  - details: { quota: { sweeps_per_day: 10, train_concurrency: 2 }, usage: { … } }
- GATE_FAILED
  - details: { reasons: ["min_trades_not_met", "max_dd_exceeded"] }

## Logging & Correlation
- Include `X-Request-ID` in responses; log errors with request id and user id.
- Sanitize payloads in logs (no secrets).

