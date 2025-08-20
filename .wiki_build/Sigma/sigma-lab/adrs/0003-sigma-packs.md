# ADR 0003: Sigma Packs

Status: Accepted

We ship strategies as versioned packs that plug into the shared libraries (`sigma_core`, `sigma_platform`). Each pack contains indicator sets, model configs, policy templates, and optional backtest templates.

Pack layout (in this workspace): `products/sigma-lab/packs/<pack>/`
- `indicator_sets/*.yaml`
- `model_configs/*.yaml` (optional)
- `policy_templates/*.yaml`
- `docs/` (optional)

Conventions
- Names: lowercase with underscores for YAML identifiers; consistent `model_id` format (`ticker_asset_horizon_cadence[_variant]`).
- Versioning: packs can be versioned independently (git tags or a dedicated `sigma-packs` repo). Product APIs pin versions.
- Validation: loaders in `sigma_core` validate schemas and surface errors via the API.
