# Model Naming (Auto-generated)

We auto-generate `model_id` from parameters to keep names unambiguous and consistent.

Format
- `<ticker>_<asset>_<horizon>_<cadence>[_<algo>|_<variant>]`
- Lowercase snake_case; allowed chars: `[a-z0-9_]`

Tokens
- `ticker`: underlying, lowercase (e.g., `spy`, `qqq`)
- `asset`: `opt` (options) or `eq` (equity)
- `horizon`: `0dte` | `intraday` | `swing` | `long`
- `cadence`: `5m` | `15m` | `hourly` | `daily`
- `algo` (optional): e.g., `xgb`, `gbm`, `rf`
- `variant` (optional): e.g., `isv1`

Examples
- `spy_opt_0dte_hourly_xgb`
- `spy_eq_swing_daily`
- `tsla_eq_intraday_5m_gbm`

How to create
- Makefile (auto):
  `make init-auto PACK_ID=zeroedge TICKER=SPY ASSET=opt HORIZON=0dte CADENCE=hourly ALGO=xgb`
- Script (direct):
  `python scripts/create_model.py --pack_id zeroedge --ticker SPY --asset opt --horizon 0dte --cadence hourly --algo xgb`

Paths
- Config: `products/edge-lab/packs/<pack_id>/model_configs/<model_id>.yaml`
- Policy: `products/edge-lab/packs/<pack_id>/policy_templates/<model_id>.yaml`
- Artifacts: `products/edge-lab/artifacts/<model_id>/...`
- Matrices: `products/edge-lab/matrices/<model_id>/...`
- Plots: `products/edge-lab/static/backtest_plots/<model_id>/...`
