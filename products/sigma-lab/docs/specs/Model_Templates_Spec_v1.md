# Model Templates — Spec v1

## Status
Draft — introduces template-first model creation; no code changes yet

## Goals
- Provide curated, pack-aware starting points so users can create a model in seconds.
- Standardize defaults for indicator sets, policy/risk budgets, hours, and sweep ranges.
- Improve time-to-first-result and reduce configuration errors.

## Template Content (YAML)
```yaml
# products/sigma-lab/packs/<pack>/model_templates/<slug>.yaml
template_id: zeroedge_starter_v1
template_version: 1
name: ZeroSigma Starter (0DTE hourly)
pack: zeroedge
horizon: 0dte
cadence: hourly

indicator_set:
  name: zeroedge_core_v2
  params: {}

policy_defaults:
  risk_profile: balanced   # conservative|balanced|aggressive
  risk_budget:
    allowed_hours: "13,14,15"
    max_drawdown_pct: 0.20
    es95_mult: 2.0
    spread_pct_max: 0.10
    oi_min: 500
    volume_min: 200
    fill_rate_min: 0.85

sweeps_defaults:
  thresholds_variants:
    - "0.50,0.52,0.54"
    - "0.55,0.60,0.65"
  hours_variants:
    - "13,14,15"
  top_pct_variants:
    - "0.10,0.15"

metadata:
  description: Starter template for intraday 0DTE (SPY) with balanced risk.
  tags: [starter, 0dte, hourly]
```

## Catalog
- Path: `configs/templates/catalog.json` (generated or maintained by hand)
- Shape:
```json
{
  "templates": [
    {"template_id": "zeroedge_starter_v1", "name": "ZeroSigma Starter", "pack": "zeroedge", "horizon": "0dte", "cadence": "hourly", "template_version": 1},
    {"template_id": "swing_momentum_daily_v1", "name": "Swing Momentum", "pack": "swingedge", "horizon": "swing", "cadence": "daily", "template_version": 1}
  ]
}
```

## API (docs-only)
- GET `/model_templates?pack=` → catalog entries
- POST `/models` → accepts `{ template_id, name, risk_profile }`
  - Server resolves template → writes per-model config/policy/indicator set using defaults
  - Response includes `model_id` and lineage snapshot

## Lineage
- Add `template_id` and `template_version` to model card and run lineage (see Model_Cards_and_Lineage.md)

## UI Hooks
- Create Model → Template Picker:
  - Step 1: Choose Template (cards)
  - Step 2: Name & Risk Profile
  - Step 3: Create → success screen with [Open Composer] [Open Designer]
- Designer: edit indicator set/policy; saving changes that affect features/labels prompts rebuild in Composer.
- Composer: Build → Sweeps → Leaderboard → Train; gated; lineage shown.

## Acceptance
- Users can create a model by selecting a template, naming it, and choosing a risk profile in ≤ 3 clicks.
- Template details (indicator set, policy defaults, sweeps defaults) are discoverable and applied consistently.
- Lineage displays `template_id` and `template_version`.
