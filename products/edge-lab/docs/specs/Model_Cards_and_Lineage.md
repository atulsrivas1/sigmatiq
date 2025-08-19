# Model Cards & Lineage — Specification (Edge Lab)

## Goals
- Transparency: Every model/run ships a standardized model card and data sheet.
- Reproducibility: Every output carries lineage fingerprints for pack/config/policy.
- Discoverability: Cards and lineage can be fetched via API and surfaced in UI.

## Artifacts & Locations
- Model card (human-readable):
  - Path (under product root): `products/edge-lab/packs/<pack_id>/model_cards/<model_id>.md`
  - Generated on: build/train/backtest; latest card reflects latest config + evaluation.
- Model card (machine-readable):
  - Path (under product root): `products/edge-lab/packs/<pack_id>/model_cards/<model_id>.json`
  - Schema mirrors the Markdown fields for API consumption.
- Lineage fingerprints:
  - CSV outputs: add columns: `pack_sha, indicator_set_sha, model_config_sha, policy_sha, risk_sha, risk_profile`.
  - Signals DB (signals table): add same columns (already planned); populate on upsert.
  - Backtest runs: store lineage in `backtest_runs.params` and normalized columns; include optional `tag` for grouping sweeps/smoke.

## Model Card Schema (YAML/JSON)
```yaml
model_id: <string>
pack_id: <string>
version: <string|semver>            # optional model version
created_at: <iso8601>
updated_at: <iso8601>

# Data & Evaluation
data:
  ticker: <string>
  asset_type: <eq|opt>
  cadence: <5m|15m|hourly|daily>
  window:
    train_start: <YYYY-MM-DD>
    train_end: <YYYY-MM-DD>
    test_start: <YYYY-MM-DD>
    test_end: <YYYY-MM-DD>
  point_in_time: true

evaluation:
  method: walk_forward|cv
  splits: <int>
  embargo: <float>
  metrics:
    sharpe_hourly: <float>
    cum_ret: <float>
    hit_rate: <float>
    mdd: <float>
  costs:
    slippage_bps: <float>
    commission_bps: <float>

# Features & Labels
features:
  indicator_set: <name>
  indicators: [ {name: rsi, period: 14}, ... ]
label:
  kind: next_bar_updown|fwd_ret_<Nd>|close_to_open|none

# Assumptions & Risks
assumptions:
  - Uses ATR(14) for brackets; entry=next_session_open.
  - ...
risks:
  - Sensitive to earnings gaps.
  - ...

# Outputs & Policy Envelope
outputs:
  alerts:
    entry_mode: next_session_open
    brackets: { atr_period: 14, atr_mult_stop: 1.2, atr_mult_target: 2.0, time_stop_minutes: 120 }
  recommended_risk:
    min_rr: 1.5
    max_daily_loss: <float|optional>

lineage:
  pack_sha: <sha1>
  indicator_set_sha: <sha1>
  model_config_sha: <sha1>
  policy_sha: <sha1>
  template_id: <string>
  template_version: <int>
  risk_profile: conservative|balanced|aggressive
  risk_sha: <sha1>
```

## Lineage — How to Compute
- Compute SHA-1 (or SHA-256) of the content of:
  - `products/edge-lab/packs/<pack_id>/indicator_sets/<model_id or named>.yaml`
  - `products/edge-lab/packs/<pack_id>/model_configs/<model_id>.yaml`
  - `products/edge-lab/packs/<pack_id>/policy_templates/<model_id>.yaml`
  - Optionally include pack-level `pack.yaml` when available.
  - `risk_sha`: hash over the serialized `risk_budget` block and `risk_profile` used for the run.
  - Include `template_id` and `template_version` as-is when the model was created from a template.
- Store these SHAs in memory during a run and stamp into CSV rows/DB writes/backtest params.

## API Additions
- `GET /model_card?model_id=...&pack_id=...`
  - Returns latest JSON card (and a link to Markdown).
- `GET /model_cards?model_id=...&pack_id=...`
  - Lists available cards (JSON/MD) with timestamps.
- Extend `/signals` rows with lineage fields (if not already present).
- Extend `/backtest` response with lineage snapshot and persist lineage on runs/folds.

## Generation Triggers
- On `POST /build_matrix`, `POST /train`, `POST /backtest`:
  - Load configs, compute lineage; generate or update model card Markdown/JSON with new evaluation window + metrics.
  - Write under `products/edge-lab/packs/<pack_id>/model_cards/`.

## UI Hooks (future)
- Show card summary in model detail; link to full card.
- In preview pane, display QA/NaN summary and top assumptions.
- In signals view, show lineage diff vs previous day.

## Acceptance Criteria
- Every model has a persisted model card (MD+JSON) updated on build/train/backtest.
- CSV / DB outputs include lineage fields; `/signals` exposes them.
- API `GET /model_card` returns the JSON card; Markdown is viewable in repo/docs.

## Rollout
- Sprint 1–2: implement generator + API; stamp lineage in outputs; docs update.
- Sprint 3: wire parity reporting to reference entry_mode+brackets from card.
