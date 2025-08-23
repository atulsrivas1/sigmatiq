# Model Pipeline — Requirements (Novice‑First)

## Purpose
Provide a one‑tap, novice‑friendly pipeline to: build/reuse a dataset, run safe sweep backtests, surface a leaderboard with plain‑language summaries, and conditionally train a model when guardrails are satisfied — all with conservative defaults and clear, reversible steps.

## Goals (Outcomes)
- Build or reuse a dataset for a model’s scope/timeframe within safe caps.
- Run a curated set of sweep configurations (or a preset) to pick the best config.
- Produce a concise leaderboard, novice summaries, and next steps.
- If a config passes guardrails, kick off a training run (not publish) and record lineage.

## Non‑Goals (MVP)
- No auto‑publish of trained models; a human Critic Gate remains mandatory.
- No unrestricted sweeps or unbounded windows.
- No advanced resource scheduling or multi‑GPU orchestration (future).

## Users & Modes
- Novice user (default): `mode: simple` — minimal inputs; uses curated sweep preset (e.g., `rth_thresholds_basic`).
- Advanced user: explicit grid, custom guardrails; still capped and explained.

## Inputs (API)
- `model_id`, optional `version` (defaults to latest published).
- `timeframe?`, `start_date?`, `end_date?` (else infer from model’s `training_cfg.data_window` or last 90 days).
- `universe`: `{ preset_id | watchlist_id | symbols[], cap }` (cap ≤ 50 enforced).
- `mode`: `simple|advanced`.
- `sweep_preset_id?` (simple default), or `grid?` (advanced): thresholds_list | top_pct_list; hours/label params optional.
- `guardrails?`: `{ min_trades, min_sharpe, max_position_rate }`.
- `persist` (default true), `dry_run?` (default false).

## Outputs (API)
- `{ pipeline_run_id, dataset: { run_id, rows, symbols }, backtests: { run_ids[], leaderboard[] }, chosen?: { config, metrics }, training?: { run_id, status }, summary, next_steps }`.

## Guardrails (Hard Caps)
- Date window ≤ 90 days (all phases); intraday runs default to RTH hours for novices.
- Universe cap ≤ 50 symbols.
- Sweep combinations ≤ 50.
- Simple mode must use a vetted sweep preset with guardrails.

## Guardrails (Quality Gates)
- Pass to training only if:
  - `trades_total ≥ min_trades` (e.g., 50) and `avg_sharpe_hourly ≥ min_sharpe` (e.g., 0.2).
  - `allowed_hours` are RTH for intraday (or explicitly configured).
  - Optional: `max_position_rate` not exceeded.

## Failure Handling (Novice)
- Missing `POLYGON_API_KEY` → plain 400: how to set it in `.env`.
- No symbols resolved → hint to use `sp500`/`liquid_etfs` or add watchlist items.
- Partial data fetch → continue with available symbols; include a warning list.

## Telemetry & Storage
- Record a pipeline run row with dataset/backtest/training references, status, summary, and errors.
- Use existing `sc.model_training_runs` and `sc.model_backtest_runs/folds` for lineage.

## Acceptance Criteria
- A novice can start with `{ model_id, universe: { preset_id } }` and get a clear result within caps.
- Pipeline returns a leaderboard and a plain summary; trains only if guardrails pass.
- All writes are idempotent; dry‑run mode returns plan without side effects.
- Postman examples: simple and advanced flows are copy/paste runnable.

## Risks & Mitigations
- Cost blow‑ups → enforce caps + warn on near‑limit usage; show estimated duration.
- Overfitting on sweeps → limit combos; prefer presets; require minimum trades.
- Inconsistent labels in packs → validate compatibility pre‑run, fail fast with guidance.
