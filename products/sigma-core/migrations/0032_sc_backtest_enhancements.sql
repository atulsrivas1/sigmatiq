-- Enhancements: pack_id, summary on backtest runs; expression indexes; curation fields on sweep presets
BEGIN;

-- Backtest runs: optional pack association and plain-language summary
ALTER TABLE sc.model_backtest_runs
  ADD COLUMN IF NOT EXISTS pack_id TEXT,
  ADD COLUMN IF NOT EXISTS summary TEXT;

-- Useful filter/sort indexes on metrics JSON
CREATE INDEX IF NOT EXISTS sc_model_backtests_sharpe_idx ON sc.model_backtest_runs (((metrics->>'avg_sharpe_hourly')::float));
CREATE INDEX IF NOT EXISTS sc_model_backtests_cumret_idx ON sc.model_backtest_runs (((metrics->>'cum_ret_sum')::float));
CREATE INDEX IF NOT EXISTS sc_model_backtests_trades_idx ON sc.model_backtest_runs (((metrics->>'trades_total')::int));
CREATE INDEX IF NOT EXISTS sc_model_backtests_tag_idx ON sc.model_backtest_runs (tag);
CREATE INDEX IF NOT EXISTS sc_model_backtests_pack_idx ON sc.model_backtest_runs (pack_id);
CREATE INDEX IF NOT EXISTS sc_model_backtests_timeframe_idx ON sc.model_backtest_runs (timeframe);

-- Sweep presets: ownership/visibility/tags for curation
ALTER TABLE sc.backtest_sweep_presets
  ADD COLUMN IF NOT EXISTS owner_user_id TEXT,
  ADD COLUMN IF NOT EXISTS visibility TEXT DEFAULT 'public' CHECK (visibility IN ('public','private','team')),
  ADD COLUMN IF NOT EXISTS tags JSONB DEFAULT '[]'::jsonb;

COMMIT;

