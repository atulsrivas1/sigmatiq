Sigmatiq TODOs (Prioritized)

P0 — Must Do Next (Novice safety, correctness)
 - Metrics explained: Add `metrics_explained` in responses when `mode=simple` or `fields=full` (translate Sharpe, win rate, drawdown, etc.).
- Pack consensus echo: Include `policy`, `min_quorum`, `min_score` in `/packs/*/backtest/*` responses.
- Pack compatibility validation: Pre‑run checks that pack component models share compatible `label_cfg` and timeframes; fail fast with guidance.
- Preset visibility guardrails: Filter sweep preset listing by `visibility` and `owner_user_id`; require guardrails on public presets.
- Error mapping coverage: Extend global handler mappings for common DB/network/env failures (e.g., missing `DATABASE_URL`, invalid `POLYGON_API_KEY`) with next steps.
- Postman verification: Ensure simple‑mode examples for `/backtest/run` and model sweep; add consensus examples (pack run: majority, pack sweep: all); keep configs copy/paste‑safe.

P1 — Near Term (Completes flows, guardrails, CI)
 - Pack sweep simple mode: Support `mode: simple` on `/packs/{id}/backtest/sweep`; default to `rth_thresholds_basic` when grid absent. (Partial: simple mode defaults allowed_hours to RTH.)
- Pipeline lineage: Integrate Parquet dataset build; persist `dataset_run_id` and echo it in pipeline responses.
- CI lints: Add `lint-sweep-presets` and wire into CI (`lint-all`); document minimal CI wiring.
- Budgets/limits: Add per‑user soft compute limits for auto endpoints (`/screen/auto`, set `auto_build`) with clear 429/400s and guidance.
- Fail‑safe computes audit: Verify indicators/feature paths return zeros/empties instead of exceptions; expand unit tests where needed.
- Saved Scans schema: Add `sc.saved_scans` (user_id, recipe_id, name, overrides JSONB, visibility, timestamps); basic CRUD; plan for scheduled scans scaffolding.

P2 — Important (Coverage, content, novice surfacing)
 - Leaderboard index: `CREATE INDEX sc_model_backtests_model_tag_idx ON sc.model_backtest_runs (model_id, tag)`.
 - Thin read catalog API: List presets, list user watchlists/symbols, and universe resolution (preset/watchlist) with server‑side guardrails.
 - Sweep preset creation guardrails: Require `visibility` + `owner_user_id`; enforce presence of guardrails (`max_combos`, `min_trades`, caps) on public presets.
 - Curated indicator sets: Add `ema_trend_adx_filter_v1`, `gap_session_context_v1`, `relative_strength_rotation_v1`, `candlestick_confluence_v1` (+ overrides and seeds). (Partial coverage present.)
 - Beginner workflows/recipes: Add the listed beginner workflows and top recipes variants with novice fields and guardrails. (Many added; fill remaining gaps.)
 - Swagger examples: Keep all examples copy/paste runnable; warn on heavy operations; prefer smallest safe configs.
 - Lint coverage (presets): Extend lints to validate sweep presets against novice criteria (guardrails present, RTH hours for intraday, grid size limits).

P3 — Nice to Have (DX, docs, polish)
- Authoring index: Add index page linking authoring guides (Indicators, Indicator Sets, Strategies, Workflows) for onboarding.
- Docs cross‑links: Add short links to new pipeline endpoints in whiteboarding README; keep examples minimal and safe.

Notes
- Many P0 items strengthen novice safety and reduce complexity; prioritize surfaces used by first‑time users.
- After P0/P1, re‑run Postman/Swagger review to ensure examples reflect guardrails and simple defaults.

Verified (Done)
- Dataset build caps: `/models/dataset/build` enforces ≤90 days and ≤50 symbols with plain‑language 400s; symbols also capped by `cap` (hard limit 50).
- Backtest and pack endpoints: enforce 90‑day and 50‑symbol caps; `/backtest/run` returns `summary` and supports simple‑mode defaults.
