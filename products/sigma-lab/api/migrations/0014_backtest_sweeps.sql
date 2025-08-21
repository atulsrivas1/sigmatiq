-- Backtest sweeps master + results tables
CREATE TABLE IF NOT EXISTS backtest_sweeps (
  id SERIAL PRIMARY KEY,
  pack_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  spec JSONB NOT NULL,
  tag TEXT,
  status TEXT DEFAULT 'completed',
  started_at TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_backtest_sweeps_pack_model_created
  ON backtest_sweeps(pack_id, model_id, created_at DESC);

CREATE TABLE IF NOT EXISTS sweep_results (
  id SERIAL PRIMARY KEY,
  sweep_id INT NOT NULL REFERENCES backtest_sweeps(id) ON DELETE CASCADE,
  kind TEXT NOT NULL,              -- thresholds|top_pct|other
  params JSONB NOT NULL,
  metrics JSONB,
  csv_uri TEXT,
  backtest_run_id INT NULL REFERENCES backtest_runs(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_sweep_results_sweep_created
  ON sweep_results(sweep_id, created_at DESC);

