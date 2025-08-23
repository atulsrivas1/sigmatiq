# Cost Model — Indicator Sets (Approximate)

Assumptions
- Universe U up to 200 symbols for RT evaluation; 1–5m bars common.
- 4 components on average per set; mixed timeframes in some cases.

Cold Evaluate (common set)
- Data fetch: 50–150 ms/symbol (amortized via batching)
- Compute: ~0.3–0.8 ms/indicator/symbol for last-window updates
- Total: ~500–1000 ms for U=200, components=4 with cache and batching

Streaming
- Incremental updates per bar; partition universe across workers (e.g., 4x → U=50 each)
- Per update per worker target: <200 ms

Storage
- Cached features: 1–2 MB per symbol per day (Parquet) for common indicators
- Artifacts retention 30–90 days for hot universes

Guardrails impact
- Universe caps, throttling, and dedup reduce worst-case CPU/IO by >60%

