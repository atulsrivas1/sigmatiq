-- Add normalized columns to backtest_runs and a folds table

ALTER TABLE backtest_runs
  ADD COLUMN IF NOT EXISTS best_sharpe_hourly DOUBLE PRECISION,
  ADD COLUMN IF NOT EXISTS best_cum_ret DOUBLE PRECISION,
  ADD COLUMN IF NOT EXISTS trades_total INTEGER,
  ADD COLUMN IF NOT EXISTS tag VARCHAR(255);

CREATE TABLE IF NOT EXISTS backtest_folds (
  id SERIAL PRIMARY KEY,
  run_id INTEGER NOT NULL REFERENCES backtest_runs(id) ON DELETE CASCADE,
  fold INTEGER NOT NULL,
  thr_used DOUBLE PRECISION,
  cum_ret DOUBLE PRECISION,
  sharpe_hourly DOUBLE PRECISION,
  trades INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_backtest_folds_run ON backtest_folds(run_id);

