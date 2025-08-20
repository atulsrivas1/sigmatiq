# Quotas & Rate Limits v1

## Status
Draft — applies to BTB + Assistant endpoints

## Rate Limits (per user)
- Default: 60 requests / minute per IP+user for public GET endpoints
- Burst for streaming endpoints (assistant): 10 concurrent streams
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`

## Quotas (per user)
- Sweeps: max 10 per day; max 2 concurrent running
- Train: max 2 concurrent jobs; max 20 per day
- Assistant execute: disabled by default; when enabled, counts toward sweeps/train quotas

## Profiles & Overrides
- Profiles: `conservative|balanced|aggressive` do not change quotas; they impact Gate only
- Admin overrides: per-user exceptions with expiry; logged in audit trail

## Enforcement & Errors
- 429 RATE_LIMITED with `Retry-After` when rate limit exceeded
- 403 QUOTA_EXCEEDED with quota/usage details when quota exceeded

## Observability
- Metrics: per-endpoint RPS, 429 count, 403 (quota) count, concurrent streams, job concurrency
- Logs: include user_id, request_id, quota snapshot on enforcement

## Examples
- Trying to start 3rd training concurrently → 403 QUOTA_EXCEEDED { train_concurrency: 2 }
- 11th sweep in a day → 403 QUOTA_EXCEEDED { sweeps_per_day: 10 }
