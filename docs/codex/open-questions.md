# Open Questions

Areas that need confirmation or tighter specification before finalizing UX/docs.

## Options Health thresholds
- Exact thresholds and pass/fail bands for options health views (batch5). What metrics drive “healthy/at-risk” badges? Is there a baseline per underlying or global?

## Roles, flags, and scope
- Admin vs. user endpoints overlap (e.g., `/leaderboard`, `/audit`). Which are intended for end-user UI vs. admin consoles? Confirm auth scopes and visibility rules for: feature flags, quotas, users, risk profiles.

## Indicators descriptions
- Many indicators lack human-friendly descriptions. Source of truth for 1–2 line explanations, typical ranges, and lookbacks? Should these live in registry docstrings or a YAML metadata file (preferred)?

## Leaderboard fields
- Sort key defaults (`order_by`) and available columns. Are we standardizing on `sharpe_hourly`, `cum_ret`, `trades`, or additional stats?

## Policy validation
- `/validate_policy` currently aliases `/policy/explain`. Do we want strict validation that returns actionable errors and severity codes for UI?

## Parity backtest behavior
- Stock parity logic (ATR/time brackets) is attached to backtests when brackets are configured. Should UI surface this explicitly, and where do the calibrated parameters live?

## Sweeps guardrails
- Default `min_trades` and optional `min_sharpe` for filtering. Confirm values for non-technical presets (e.g., “Conservative”, “Balanced”, “Aggressive”).

## Duplicated routes
- There are overlapping routes in `admin.py` vs dedicated routers (e.g., audit, leaderboard). Plan to consolidate or keep them intentionally separate? Update docs accordingly.

## Artifacts store
- For `artifacts` rows (matrix/model/plot), confirm SHA-256 and size population plan. Is a content-addressable store planned or best-effort metadata only?

