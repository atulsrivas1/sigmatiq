# ADR 0005: Build → Backtest (Sweeps) → Leaderboard → Select → Train, with Risk Profiles

## Status
Accepted — 2025-08-18

## Context
- We need a clear, reproducible workflow to build feature/target matrices, backtest across configurations (sweeps), select the best configurations, and train models — across multiple packs (ZeroSigma/0DTE, SwingSigma, LongSigma, OvernightSigma, MomentumSigma, Options Overlay).
- The UI must make this pipeline intuitive and guard against common pitfalls (multiple-testing bias, capacity/parity issues, target leakage, compute waste).
- Users have different risk appetites; a single base model should support multiple risk‑tagged variants without duplicating data unnecessarily.

## Decision
1) Workflow sequence and gate
- Sequence: Matrix Build → Backtest (Sweeps) → Leaderboard → User Selection → Train.
- Add a Gate between Leaderboard and Train: hard guards (e.g., min trades, max drawdown, parity/capacity) and a holdout check; only “pass” rows are trainable by default.
- Cache/dedupe repeated sweeps by a normalized key (model_id, date window, sweep params, risk_profile, matrix_sha).

2) Risk budgets and profiles
- Introduce configurable risk budgets per pack; enforce as guards in sweeps and before training.
- Support three user risk profiles: Conservative, Balanced, Aggressive. Profiles adjust guards and behavior (e.g., allowed hours, threshold ranges, position sizing).
- Values are configurable and can be tuned later; models can be trained under multiple profiles and tagged accordingly.

3) Ranking after gates (pack‑aware)
- ZeroSigma/Overlay: Rank by Sortino × sqrt(trades/100) − penalty(MaxDD, fold‑instability); tie by return, win rate, capacity index.
- Swing/Momentum: Cost‑adjusted Sharpe (or IR for momentum) with turnover penalty; tie by MaxDD/Calmar.
- LongSigma: Calmar primary; tie by Sortino and CAGR; light turnover penalty.

4) Naming, lineage, and storage
- Keep `model_id` stable; add first‑class `risk_profile` and `risk_sha` (hash of risk budget) to lineage.
- Reuse matrices across profiles where possible; artifacts stored under `artifacts/<model_id>/<risk_profile>/...`.
- Stamp runs with: `matrix_sha`, `config_sha`, `policy_sha`, `risk_profile`, `risk_sha`.

5) Automation policy
- Default is user‑driven training (explicit selection); optional “auto‑train top N that pass Gate” can be enabled per user/profile with quotas and holdout gating.

6) UI structure updates
- Sweeps: add Risk Profile selector, Risk Envelope (guard controls), pass/fail budget chips with tooltips, selection cart, compare action, small equity sparklines.
- Leaderboard: filter by `risk_profile`, “Pass Gate only” toggle, compare modal (equity, drawdown, hour‑wise performance), batch actions (“Train selected”).
- Runs > Train: grouped by `risk_profile`, concurrency/quotas, matrix reuse indicator, lineage preview.
- Models: risk badges on cards; filter by risk profile; sibling links between risk variants.

## Rationale
- Gates reduce false positives and compute waste; holdout checks mitigate multiple‑testing bias.
- Risk profiles make the same base strategy usable across different appetites without fracturing IDs.
- Pack‑aware ranking aligns selection with instrument/horizon realities (tail risk for 0DTE, costs/turnover for momentum, Calmar for long‑horizon).
- Provenance (shas) and caching ensure reproducibility and performance.
- UI changes keep the pipeline intuitive and transparent (why a row passes/fails; how it uses budgets).

## Consequences
Positive:
- Reproducible, auditable selection; fewer paper alphas; better compute utilization.
- Clear UX for risk appetite and profile‑based variants.
- Easier portfolio‑level governance with standardized budgets.

Negative/Trade‑offs:
- Slightly more configuration surface (profiles + budgets) to manage.
- Added complexity in lineage and UI (badges, filters, gates, compare views).

## Alternatives Considered
- Baking risk into `model_id` (e.g., suffixes): simpler routing but noisier IDs and less flexible metadata.
- Single universal metric (Sharpe only): simpler but misaligned with tails/costs/capacity across packs.
- Gate only at training time: simpler but wastes sweep/leaderboard attention and risks over‑selection.

## Open Questions / Next Steps
- Matrix reuse: default is reuse across profiles; any cases needing per‑profile matrices?
- Allowed‑hours: apply pre‑labeling in matrix build (reduce leakage) vs only in backtests?
- Matrix preview: include label balance, missingness heatmap, feature‑target leakage test, rolling hour coverage?
- Concurrency/quotas: default parallel trainings per user and per profile?
- Finalize default numeric budgets per pack (current defaults are reasonable starting points; all configurable).

