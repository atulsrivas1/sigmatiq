-- Backtest runs persistence

CREATE TABLE IF NOT EXISTS backtest_runs (
  id SERIAL PRIMARY KEY,
  pack_id VARCHAR(255) NOT NULL,
  model_id VARCHAR(255) NOT NULL,
  started_at TIMESTAMP DEFAULT NOW(),
  finished_at TIMESTAMP DEFAULT NOW(),
  params JSONB,
  metrics JSONB,
  plots_uri VARCHAR(1024),
  data_csv_uri VARCHAR(1024),
  git_sha VARCHAR(64),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_pack_model ON backtest_runs(pack_id, model_id);
CREATE INDEX IF NOT EXISTS idx_backtest_runs_created ON backtest_runs(created_at DESC);

