# Cost Model — Strategies (Approximate)

Backtesting
- Inputs: universe size U, bars N, parameter combos P, folds F.
- Complexity: O(U * N * P * F) with constants for TX model and order logic.
- Resources: Parallel per-P and per-F; memory for features and trade logs.
- Budget: Standard equity breakout on U=500, N=2y 5m bars, P=20, F=5 → multi-hour on 8 vCPU unless cached.

Live
- Signal eval + policy + sizing per bar; broker round-trips dominate.
- Venue rate limits and throttles; retry/backoff strategies impact latency.

Storage
- Trades, orders, fills logs; artifacts (plots/reports). 1–5 MB per run typical; heavy reports larger.

Guardrails
- Cap P and F by plan; enforce universe limits; queue large jobs.

