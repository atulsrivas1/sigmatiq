# Assistant API Spec v1

## Status
Draft — complements AI Assistant Spec v1

## Endpoint
- POST `/assistant/query`
  - Request
    ```json
    {
      "message": "string",
      "context": {
        "route": "#/sweeps",
        "model_id": "spy_opt_0dte_hourly",
        "risk_profile": "balanced",
        "matrix_sha": "sha...",
        "selection": [ {"model_id":"...","config":{...},"lineage":{...}} ]
      },
      "allow_execute": false
    }
    ```
  - Response (SSE or chunked)
    - Streams assistant tokens and any tool call requests/responses.
    - Tool calls are mediated server-side (see Tools).

## Tools (server-moderated)
- `docs.search(query: string)` → `{ snippets: [{path, text}], total }`
- `reports.search(glob: string)` → `{ files: [{path, size, modified_at}] }`
- `reports.read_csv(path: string, opts?: { limit?: number, columns?: string[] })` → `{ columns: string[], rows: any[] }`
- `reports.read_xlsx(path: string, opts?: { sheet?: string|number, limit?: number })` → `{ sheets: string[], columns: string[], rows: any[] }`
- `db.leaderboard(params)` → `{ rows: LeaderboardRow[], total }`
- `db.run_detail(id: string)` → `{ run: object }`
- `pipeline.suggest(kind: "build"|"sweep"|"train", payload: object)` → `{ make: string, rest: object }`
- (opt-in) `pipeline.execute(kind, payload)` → `{ job_id|sweep_id }` (requires confirmation)

Notes
- DB methods are allowlisted queries with parameter validation; no free-form SQL.
- File methods are scoped to `products/edge-lab/{reports,static,matrices,artifacts}`; previews capped.
- Execute is disabled unless `allow_execute` is true and a prior explicit confirmation token is present.

## Errors
```json
{
  "error": { "code": "FORBIDDEN|NOT_FOUND|INVALID_PARAM|INTERNAL", "message": "...", "details": {} }
}
```

## Acceptance
- Streams responses; handles tool call round-trips; cites sources in assistant text.
- Enforces read-only by default; execution requires explicit confirmation.
- Validates parameters and blocks unsafe paths/queries.

