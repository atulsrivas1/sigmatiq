# Matrix Contract v1

## Status
Accepted — 2025-08-18

## Scope
Defines a reproducible contract for building training matrices across packs (ZeroEdge/0DTE, SwingEdge, LongEdge, OvernightEdge, MomentumEdge, Options Overlay). Covers labels, time rules, feature hygiene, options specifics, versioning, caching, and UI diagnostics.

## Decisions
- Labels are sweep‑friendly (lookahead return vs threshold). Stops/targets remain in backtests.
- Intraday allowed‑hours are applied before labeling to avoid leakage.
- Hygiene favors conservative imputation, train‑only scaling, and automatic leakage checks.
- Strong `matrix_sha` versioning ensures reproducibility; matrices are reused across risk profiles.

## Label & Lookahead
- ZeroEdge (0DTE): target = underlying next‑1h cumulative return (log or pct). Binary label `y=1` if return ≥ threshold (swept later); else `0`.
- SwingEdge (daily): target = next‑1d return; binary label via threshold (swept).
- LongEdge (weekly/position): target = next‑1w return; binary label via threshold (swept).
- MomentumEdge (intraday/daily): horizon‑appropriate next‑window return; binary label via threshold (swept).
- Options Overlay: start with underlying return for label; option premium fields remain features for parity/capacity checks (premium‑based labels may be added in v2).

Notes
- Label thresholds are chosen during sweeps (not fixed in matrix) to support configuration exploration.
- Stops/targets and sizing rules are applied in backtests, not in matrix labeling.

## Time & Hours
- Timezone: US/Eastern; trading session 09:30–16:00.
- Intraday allowed‑hours filter is applied before labeling (e.g., ZeroEdge: 13–15) to avoid leakage.
- No forward‑fill across market closure boundaries.

## Features & NaNs
- Imputation: drop rows with NaN in the target window; forward‑fill features up to 1 bar; add explicit missingness flags. No global/statistical imputes that could leak.
- Scaling: RobustScaler (median/IQR) fit on train split only; transform applied to val/test; scaler params stored with artifacts.
- Leakage checks: automatic shift/leak scan on a holdout slice (e.g., last 10% of window) to flag features with suspicious correlation to future targets; expose warnings in UI (green/yellow/red).

## Options / 0DTE Specifics (as features + parity metadata)
- Contract selection: same‑day expiry; choose nearest‑to‑ATM by |delta| ≈ 0.35 ± 0.05 with highest liquidity (volume, then OI) at decision time.
- Prices captured: bid, ask, mid = (bid+ask)/2, spread, OI, volume, delta, IV. These support parity/capacity guards and cost modeling in backtests.
- Backtest (not matrix) costs: default slippage = 50% of spread + $0.01 tick; commission configurable. Trades can be skipped if parity/capacity guards fail (marked unfilled).

## Versioning & Caching
`matrix_sha = hash(
  datasource_ids,
  universe,
  date_window,
  resample,
  feature_list + params,
  label_def { lookahead, target_source },
  hours_filter,
  imputation_cfg,
  scaling_cfg,
  tz,
  calendar_version
)`

- Matrices are reused across risk profiles (same `matrix_sha`). Sweeps/policy/training vary (`config_sha`, `policy_sha`, `risk_sha`).
- Store `matrix_sha` alongside artifacts and stamp into run lineage.

## Preview & Diagnostics (UI)
- Summary: features count, rows, label balance, NaN%.
- Heatmaps: missingness heatmap; feature correlation heatmap.
- Leakage summary: flagged features with short explanations/tooltips.
- Coverage: counts by hour/day; intraday packs show a per‑hour bar chart.
- Stability: simple drift chart (rolling mean/std of target and key features).

## Defaults (v1)
- Lookahead: ZeroEdge 1h; SwingEdge 1d; LongEdge 1w; Momentum intraday 1h, daily 1d.
- Holdout for leakage/drift checks: last 10% of the matrix date window.
- Scaling: RobustScaler on numerics; one‑hot for categoricals if present; all fit on train split only.
- 0DTE delta band: 0.35 ± 0.05; liquidity tiebreaker: max volume, then max OI.
- Backtest slippage model (not matrix): 50% spread + $0.01; commissions configurable.

## Rationale
- Decoupling labels (simple, sweep‑friendly) from backtest policy enables fast configuration exploration and clear comparisons.
- Pre‑labeling hours filters prevent subtle leakage in intraday workflows.
- Conservative hygiene reduces false positives caused by aggressive imputations or inadvertent lookahead.
- Strong versioning (comprehensive `matrix_sha`) guarantees reproducibility and effective caching.
- 0DTE specifics keep option microstructure available for parity/capacity checks without complicating labels.

## Interactions with Risk Profiles
- Risk profiles (Conservative/Balanced/Aggressive) do not change `matrix_sha` by default; they adjust sweeps, guards, and training policies.
- UI exposes `matrix_sha` and risk badges; leaderboard can filter “Pass Gate only” based on profile‑specific budgets.

## Open Questions
- Any packs requiring per‑profile matrices (e.g., materially different features/hours)? Default is reuse.
- Threshold selection policy: fixed ranges per pack vs dynamic ranges based on label distribution.
- Additional diagnostics to include (e.g., partial dependence on key features) in a future version.

