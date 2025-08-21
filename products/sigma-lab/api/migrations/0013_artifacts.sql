-- Artifacts table to normalize produced files/URIs across runs
CREATE TABLE IF NOT EXISTS artifacts (
  id SERIAL PRIMARY KEY,
  pack_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  kind TEXT NOT NULL,              -- matrix|model|plot|report|csv|other
  uri TEXT NOT NULL,               -- file path or object storage URI
  sha256 TEXT NULL,
  size_bytes BIGINT NULL,
  build_run_id INT NULL REFERENCES build_runs(id) ON DELETE SET NULL,
  training_run_id INT NULL REFERENCES training_runs(id) ON DELETE SET NULL,
  backtest_run_id INT NULL REFERENCES backtest_runs(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_artifacts_pack_model_created
  ON artifacts(pack_id, model_id, created_at DESC);

