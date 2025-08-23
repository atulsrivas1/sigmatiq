# Risks & Guardrails

- Over-alerting → Budgets per user/timeframe; hard caps; diversity heuristic.
- Misinterpretation → Plain-language; disclaimers; preview before subscribe; no advice.
- Data/latency → Use Polygon cache; limit universes; backoff and degrade gracefully.
- Model drift → Monitor precision@K; recalibrate thresholds; retrain cadence.
- Options risk → Default ATM, min DTE, small size; show premium band; SL/TP conservative.
- Compliance → Audit logs for alerts; transparent criteria; easy opt-out.
