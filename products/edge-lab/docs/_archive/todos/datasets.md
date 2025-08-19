Datasets & Data Adapters

Completed
- Polygon-only adapters for hourly/daily bars; option chain snapshot (IV/Greeks) and OI snapshot.
- `data_cache` used only for historical requests; today’s data never cached.
- Prev-close anchoring logic in dataset builder with hourly fallback.

Pending
- Expose retries/timeouts/backoff via env; structured logging on cache vs API.
- Add a stocks-only dataset builder (equities pipeline) under `swingedge`.
