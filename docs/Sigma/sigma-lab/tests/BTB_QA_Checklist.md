# BTB QA Checklist — Matrix → Sweeps → Leaderboard → Train

Scope: Manual test cases to validate documentation-only design. Use mocks or dry-run endpoints where needed.

## 1) Matrix Build & Profile
- Build matrix with intraday pack (ZeroSigma) and verify:
  - Allowed-hours are applied pre-labeling (e.g., 13–15 rows only).
  - `matrix_sha` present and stable for same inputs.
  - Preview shows: features count, rows, label balance, NaN%.
  - Missingness and correlation heatmaps rendered (or placeholders).
  - Leakage warnings appear if synthetic future-shifted feature is injected.

- Build matrix with daily pack (SwingSigma) and verify:
  - Lookahead = 1d by default; hours filter ignored.
  - `matrix_sha` changes if feature list or date window changes.

Pass if: hours filter precedes labeling (intraday), preview renders, `matrix_sha` stability holds, leakage flags work on synthetic test.

## 2) Sweeps (Run/Results)
- Configure sweep (ZeroSigma): thresholds `0.50,0.52,0.54` and hours `13,14,15`; profile = Balanced.
  - Start sweep; status transitions: queued → running → completed.
  - Results include metrics (Sharpe, return, trades) and lineage (`matrix_sha`, `risk_profile`).
  - Gate evaluation produces pass/fail; failures list reasons (e.g., `min_trades_not_met`).
  - CSV export yields expected columns.

- Re-run identical sweep and verify caching/dedup; should return same `sweep_id` or results immediately.

Pass if: results populate with gate badges, reasons are human-readable, and deduplication works.

## 3) Leaderboard
- Load leaderboard filtered by model and risk profile.
  - "Pass Gate only" hides failing rows.
  - Scatter and table agree on counts and top ranks.
  - Compare modal opens with equity/drawdown/heatmap placeholders.
  - Lineage popover shows `matrix_sha`, `config_sha`, `policy_sha`, `risk_sha`.

Pass if: filtering works, gate filter hides fails, lineage data present.

## 4) Selection Cart
- From Sweeps, add 2 configurations to Selection; verify persistence on page reload and across navigation to Leaderboard and Runs.
- Remove 1 config and confirm it disappears from all pages.

Pass if: cart persists and stays in sync across pages.

## 5) Train Batch (Dry-Run)
- In Runs > Train, ensure only gate-passing rows are enabled to queue.
- Start Training (dry run) with 2 jobs; verify job records created with lineage and profile.
- Concurrency limit enforced (e.g., max 2 jobs) and queued states visible.
- Override a failing row requires confirmation + tag.

Pass if: only pass rows enqueue by default, lineage stamped, concurrency respected.

## 6) 0DTE Parity/Capacity Logic
- Create a test case with spread above limit and OI/volume below min; verify gate fails with `spread_above_limit`, `oi_below_min`, `volume_below_min`.
- Adjust Risk Profile to Aggressive; verify looser limits pass when within profile thresholds.

Pass if: parity/capacity checks reflect profile budgets.

## 7) Idempotency & Keys
- Verify normalized key `(model_id, matrix_sha, kind, value, allowed_hours, splits, tag, risk_profile)` deduplicates sweeps and selections.
- Duplicate train job submission is ignored unless `force=true`.

Pass if: dedup works and duplicate trains are blocked by default.

## 8) Error Handling / Limits
- API returns structured errors with codes (`INVALID_PARAM`, `NOT_FOUND`, `GATE_FAILED`).
- List endpoints enforce `limit<=200` and default `limit=50`.

Pass if: errors are consistent and pagination limits enforced.

## 9) Reproducibility
- Rebuild same matrix, rerun same sweep; verify identical results within tolerance and same lineage shas.

Pass if: deterministic runs produce matching results/lineage.

## 10) Security/Quotas (Policy)
- Ensure per-user quotas for sweeps and training are applied; exceeding limit yields friendly errors.

Pass if: quotas enforced per spec.

