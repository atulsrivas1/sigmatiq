# MLOps & Ops — Alerts AI

Pipelines
- Offline: cohort selection → feature compute (cached Polygon loaders) → label build → train → calibrate → register ModelSpec.
- Online: features via `/indicator_sets/auto_build` → score → plan → explain → guardrails → deliver.

Versioning
- ModelSpec {id, version, featureset_id, label_cfg, thresholds, artifacts_uri}.
- Immutable artifacts; shadow traffic to new versions before switch.

Deployment
- Stateless scoring service; horizontal scale; warm model cache; health probes.
- Blue/green or canary with precision@K watch.

Monitoring
- Precision@K by timeframe; plan hit rates; alert volume; throttling; latency.
- Drift: PSI on features; score calibration checks; retrain triggers.

A/B & Safety
- Threshold variants per cohort; quota and diversity enforced pre-delivery.
- Rollback plan: revert to previous ModelSpec if metrics degrade.
