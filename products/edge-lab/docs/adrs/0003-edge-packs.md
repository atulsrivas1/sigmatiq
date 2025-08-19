# ADR 0003: Edge Packs

Status: Accepted

We ship strategies as versioned packs that plug into the shared libraries (`edge_core`, `edge_platform`). Each pack contains indicator sets, model configs, policy templates, and optional backtest templates.

Pack layout (in this workspace): `products/edge-lab/packs/<pack>/`
- `indicator_sets/*.yaml`
- `model_configs/*.yaml` (optional)
- `policy_templates/*.yaml`
- `docs/` (optional)

Conventions
- Names: lowercase with underscores for YAML identifiers; consistent `model_id` format (`ticker_asset_horizon_cadence[_variant]`).
- Versioning: packs can be versioned independently (git tags or a dedicated `edge-packs` repo). Product APIs pin versions.
- Validation: loaders in `edge_core` validate schemas and surface errors via the API.
