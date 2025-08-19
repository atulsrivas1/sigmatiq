# Policy Schema (YAML)

Each model must have a policy file at `products/sigma-lab/packs/<pack_id>/policy_templates/<model_id>.yaml`.
This file controls risk, execution, and alerting. The API validates presence and
basic types before allowing build/train/backtest.

Minimal example:

```
name: zerosigma_default_v1
version: 1
policy:
  # BTB v1 additions (optional, see Risk_Profile_Schema.md)
  risk_profile: balanced   # conservative|balanced|aggressive
  risk_budget:             # pack-aware guards (used for gates)
    min_trades: 5
    max_drawdown_pct: 0.20
    es95_mult: 2.0
    spread_pct_max: 0.10   # options/overlay only
    oi_min: 500            # options/overlay only
    volume_min: 200        # options/overlay only
    fill_rate_min: 0.85    # options/overlay only
    adv_bps_max: 0.0010    # equities packs (10 bps)
    turnover_max: 2.0      # per year
    allowed_hours: "13,14,15"  # intraday packs
    daily_loss_cap_R: 3.0
  risk:
    max_drawdown: 0.1        # fraction (0..1)
    max_exposure: 10000      # units or notional, app-specific
  execution:
    slippage_bps: 1.0        # basis points
    size_by_conf: false      # bool
    conf_cap: 1.0            # [0..1], cap on confidence sizing
    momentum_gate: false     # if true, zero positions when score below threshold
    momentum_min: 0.0        # min value for the momentum column
    momentum_column: momentum_score_total  # column name to use
  alerting:
    cooldown_minutes: 5      # minutes
    max_trades_per_day: 10   # integer
```

Notes
- Root can be either at top level or nested under `policy:`; validator normalizes this.
- Required sections: `risk`, `execution`, `alerting` (all mappings).
- Numeric fields validated where present (slippage_bps, conf_cap, cooldown_minutes, max_drawdown, max_exposure).
- Extend freely with additional keys used by your runtime (e.g., momentum gates, per-hour thresholds).

BTB v1
- `risk_profile` and `risk_budget` are optional but recommended; values are pack-aware and drive Gate evaluation for sweeps/leaderboard/train (see `specs/Risk_Profile_Schema.md`).
- Include `risk_profile`/`risk_budget` either at root or under `policy:`; validators normalize both forms.

Validation
- Endpoint: `GET /validate_policy?model_id=<id>&pack_id=<pack>` returns `{ ok, path, errors }`.
- Makefile: `make validate-policy MODEL_ID=<id> PACK_ID=<pack>` prints validation result.
