-- Add lineage and gate columns to backtest_runs; add useful indexes

ALTER TABLE backtest_runs
  ADD COLUMN IF NOT EXISTS matrix_sha TEXT,
  ADD COLUMN IF NOT EXISTS config_sha TEXT,
  ADD COLUMN IF NOT EXISTS policy_sha TEXT,
  ADD COLUMN IF NOT EXISTS risk_profile TEXT,
  ADD COLUMN IF NOT EXISTS risk_sha TEXT,
  ADD COLUMN IF NOT EXISTS gate_pass BOOLEAN,
  ADD COLUMN IF NOT EXISTS gate_reasons TEXT[],
  ADD COLUMN IF NOT EXISTS median_spread_pct NUMERIC,
  ADD COLUMN IF NOT EXISTS fill_rate NUMERIC,
  ADD COLUMN IF NOT EXISTS oi_min_observed INTEGER,
  ADD COLUMN IF NOT EXISTS volume_min_observed INTEGER;

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_backtest_runs_model_time
  ON backtest_runs(model_id, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_profile_gate_time
  ON backtest_runs(risk_profile, gate_pass, started_at DESC);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_tag
  ON backtest_runs(tag);

