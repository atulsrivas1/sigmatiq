Strategies — How To Add (for Codex sessions)

Where
- Add JSON files to `docs/catalog/strategies/strategy_<name>.json`
- Regenerate SQL seed via `make -C products/sigma-core gen-strategy-seed`

Required fields
- `strategy_id`, `version`, `status`, `title`, `objective`
- `entry_logic`, `exit_logic` (plain text expressions)
- `pre_reqs.indicator_sets_used`: ["<set_id>"] (link to at least one indicator set)
- `novice_ready: true`, `beginner_summary`: one‑line, plain language
- `simple_defaults`: `{ operation: 'backtest'|'screen'|'alert'|'subscribe', timeframe: '1m|5m|hourly|daily' }`
- `guardrails`: `{ max_positions, max_daily_trades, loss_cap_bps }`
- `assistant_hints`: 3–4 short do’s/don’ts

Good patterns
- Align each strategy to one curated indicator set (keeps UX simple)
- Default timeframes: 1m/5m for intraday, hourly for swing, daily for IV/regime
- Set conservative guardrails (Simple Mode ethos)

Validate + Seed
- Lint: `make -C products/sigma-core lint-strategies` (Issues: 0 expected)
- Seed: `make -C products/sigma-core gen-strategy-seed` (updates `0004_sc_seed_strategies.sql`)

Naming
- `strategy_<short_name>.json`, `strategy_id: <short_name>`
- Keep `version: "1.0.0"` for content; DB major = 1

