# Options Overlay — TODOs

Priority: Medium-high (after stock bracket rollout). Enables fully actionable options alerts and richer strategies.

- Credit verticals support
  - Add `option_mode: credit_vertical` with `spread_width`, `credit_tp_pct` (e.g., 50%), `credit_loss_multiple` (e.g., 2.0x credit).
  - Compute net credit from short - long mid; estimate stop/target values and bracket logic.
  - Policy hooks under `execution.options` for defaults.

- CSV examples and runbook updates
  - Provide a minimal POST body example for `/options_overlay` in runbooks.
  - Document single-leg and vertical flows (fields, side override, dte_target, min_oi).
  - Add example outputs for `options_signals.csv` (CSV fallback) and DB table columns.

- Expirations helper (UI/CLI)
  - Helper to list available expirations from Polygon for a ticker and suggest closest to `dte_target`.
  - Add a CLI `scripts/list_expirations.py` and optional API `GET /options/expirations?ticker=...`.
  - Integrate into the overlay endpoint: if only `dte_target` provided, pick and echo the chosen expiry.

- Pricing improvements
  - Use quotes mid fallback when snapshot mid is missing (done), extend to BS estimate with IV if both missing; flag `pricing_estimate=true`.
  - Optional: include vega/theta-aware adjustments for premium bracket mapping (beyond delta-only).

- Spreads generalization
  - Support put verticals (downside bias) and iron spreads (later).
  - Encode legs in `legs_json` for auditing.

- Testing & validation
  - Unit tests for overlay selection and premium mapping.
  - Integration smoke against a small ticker set (ENV-guarded for Polygon).
