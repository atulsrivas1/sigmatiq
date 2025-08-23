-- Reusable backtest sweep presets (grids + guardrails)
BEGIN;

CREATE TABLE IF NOT EXISTS sc.backtest_sweep_presets (
  preset_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  grid JSONB NOT NULL,        -- structure aligned with BacktestSweepGrid
  guardrails JSONB,           -- { max_combos, min_trades, universe_cap, days_cap }
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

DROP TRIGGER IF EXISTS trg_backtest_sweep_presets_updated_at ON sc.backtest_sweep_presets;
CREATE TRIGGER trg_backtest_sweep_presets_updated_at BEFORE UPDATE ON sc.backtest_sweep_presets
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();

COMMIT;

