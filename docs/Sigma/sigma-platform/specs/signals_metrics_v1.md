# Signals Metrics v1 — Definitions, Formulas, Acceptance

## Status
Draft — applies to Signals Leaderboard, Model Detail Performance, and Signals Analytics

## Period & Scope
- Metrics are computed over a requested period [start, end] on the signals log after cost adjustments.
- Default period: last 30 calendar days (configurable).
- All metrics are computed per (model_id, risk_profile) unless otherwise specified.

## Cost Adjustments
- Commission: per-trade flat or bps, configured by environment.
- Slippage: measured when fills exist; otherwise modeled (e.g., 50% spread + tick).
- Cost-adjusted PnL: PnL − commissions − slippage.

## Core Metrics (formulas)
- Return (cum_return): sum of PnL / starting capital (or normalized notional); reported as percentage.
- Sharpe: mean(r) / std(r) × sqrt(K), where r is cost-adjusted per-trade or per-period return;
  - K = trades per year if using per-trade r; or K = 252 for daily aggregation.
- Sortino: mean(r) / std(min(r, 0)) × sqrt(K) (downside deviation).
- Win Rate: wins / (wins + losses); ignore open/pending.
- Trades: count of filled trades in period.
- Max Drawdown (live): max peak-to-trough equity decline in the period.
- Fill Rate: filled / (filled + canceled + timed-out) for valid entries.
- Avg Slippage: mean(|fill_px − ref_px|) normalized to asset context (absolute $ for options; bps for equities).
- Capacity (qualitative):
  - Options: derived from median spread %, OI, and volume (thresholds per pack/risk profile).
  - Equities: derived from ADV usage (bps) and realized impact (if measured).
- Coverage %: ratio of timestamps with valid inputs/signals to the period grid (e.g., trading hours bars).
- Freshness (sec): now − latest signal ts within the period.

## Options-Specific Notes (0DTE)
- Reference price: use underlying or premium per strategy; parity/capacity panels surface both.
- Spread %: (ask − bid) / mid; report medians and IQR.
- Delta band / OI/volume thresholds inform Capacity classification.

## Rounding & Display
- Sharpe/Sortino: 2 decimals; Cum Return: 1 decimal (%); Win/Fill: whole %; Trades: integer; Slippage: $0.01 (options) or 1 bps (equities).
- Show N/A when denominator is zero or data is insufficient; surface Coverage % and Freshness.

## Acceptance Criteria — Signals Leaderboard
- Period alignment: all rows computed on identical [start, end] with timezone noted.
- Cost-adjusted: metrics include configured commissions and slippage model where fills are missing.
- Stability: empty or insufficient data yields N/A with Coverage % < 50% highlighted.
- Filters: model/pack/risk_profile/date/tag filter the dataset consistently across tabs.
- Sorting: by Sharpe (desc) defaults; stable when values equal (secondary by Cum Return).
- Lineage: rows include lineage badge when available; clicking opens Model Detail > Performance.

## Acceptance Criteria — Model Detail Performance
- Loads default 30d in ≤ 2s with Coverage % and Freshness visible.
- Cards reflect live period metrics; charts match aggregates (edge cases within rounding tolerance).
- Options models show Parity/Capacity panels.

## References
- Gate & Scoring Spec v1 (for guardrails reapplication in live views)
- Signals API Spec v1 (for endpoint shapes)
