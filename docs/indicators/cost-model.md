# Cost Model (Optional, Approximate)

Assumptions
- Universe U up to 200 symbols for RT scans; 1–5m bars.
- Indicator set K ~ 5–10 per screen; window sizes 14–50.

On-Demand Screen (Cold)
- Data fetch: ~50–150 ms per symbol (amortized via batching)
- Compute: ~0.2–0.6 ms per indicator per symbol for last-window updates
- Total: ~400–900 ms for U=200, K=6 with caching and batching

Streaming Scanner
- Incremental updates only per new bar; CPU dominated by window updates
- With partitioning across 4 workers, per-worker U~50 ⇒ sub-200 ms updates

Storage
- Cached materializations in Parquet: ~1–2 MB per symbol per day for common features
- Artifacts retention policy: 30–90 days for hot universes

Costs
- CPU: 2–4 vCPU for scanner MVP; scales linearly with U and K
- Memory: 2–8 GB per worker for rolling windows and caches
- Network: dependent on data source; prefer local cache

Guardrails impact
- Universe caps and throttle reduce worst-case costs by >60%

