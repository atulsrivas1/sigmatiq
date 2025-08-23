# MVP Plan (4 Weeks)

Week 1
- Finalize requirements; select 3 recipes; define labels/targets.
- Build feature pipelines using existing sets; prepare training data.

Week 2
- Train baseline XGBoost; calibrate thresholds for quotas.
- Implement scoring service stub and reason-code extraction.

Week 3
- Add LLM explainer templates; integrate with scoring service.
- Expose `/alerts/preview`; wire to UI prototype; add quotas.

Week 4
- Add `/alerts/subscribe` + `/alerts/feed`; monitoring dashboards.
- Pilot with liquid_etfs/sp500; evaluate precision@K and plan hit rate.
