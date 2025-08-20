# Risk Profile Schema — v1

## Status
Draft — complements ADR 0005

## Purpose
Describe how risk appetite is encoded in configs and lineage so models can be trained and ranked under multiple profiles without changing `model_id`.

## Schema
```yaml
risk_profile: conservative | balanced | aggressive

risk_budget:
  min_trades: int
  max_drawdown_pct: float
  es95_mult: float            # ES95 ≤ es95_mult × avg_loss
  spread_pct_max: float       # options/overlay
  oi_min: int                 # options/overlay
  volume_min: int             # options/overlay
  fill_rate_min: float        # options/overlay
  adv_bps_max: float          # equities packs
  turnover_max: float         # per year
  allowed_hours: string       # e.g., "13,14,15" (intraday)
  daily_loss_cap_R: float     # per day cap in R

sweep_overrides:
  thresholds_range: [float, float]
  top_pct_range: [float, float]
  hours_variants: [string]

sizing:
  risk_per_trade_R: float     # 0.5 (C), 1.0 (B), 1.5 (A) default
```

## Lineage Fields
```jsonc
{
  "risk_profile": "balanced",
  "risk_sha": "sha256:..."   // hash of risk_budget block
}
```

## Defaults (per pack)
- ZeroSigma (0DTE)
  - C: MaxDD≤15, ES95≤1.5×, spread≤8%, OI≥1000, vol≥400, fill≥0.90, hours 13–15
  - B: MaxDD≤20, ES95≤2.0×, spread≤10%, OI≥500, vol≥200, fill≥0.85, hours 13–15
  - A: MaxDD≤25, ES95≤2.5×, spread≤12%, OI≥300, vol≥100, fill≥0.80, hours 12–15
- SwingSigma
  - C: MaxDD≤20, trades/yr≥40, Sharpe_adj≥1.2, adv_bps≤5, turnover≤150%
  - B: MaxDD≤25, trades/yr≥30, Sharpe_adj≥1.0, adv_bps≤10, turnover≤200%
  - A: MaxDD≤30, trades/yr≥25, Sharpe_adj≥0.8, adv_bps≤15, turnover≤300%
- LongSigma
  - C: Calmar≥0.8, MaxDD≤30
  - B: Calmar≥0.6, MaxDD≤35
  - A: Calmar≥0.4, MaxDD≤40
- MomentumSigma
  - C/B/A: progressively looser IR targets, turnover caps, adv_bps caps
- Overlay
  - Mirrors ZeroSigma for parity/capacity; margin usage caps per profile

## Rationale
- Profiles control guards and search space breadth (sweeps), and optionally position sizing, without rebuilding matrices.
- `risk_sha` ensures reproducibility; badges make profile visible in UI.

