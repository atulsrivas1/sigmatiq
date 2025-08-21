-- Build runs history: records matrix build operations and basic metadata
CREATE TABLE IF NOT EXISTS build_runs (
  id SERIAL PRIMARY KEY,
  pack_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  started_at TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  params JSONB,
  metrics JSONB,
  out_csv_uri TEXT,
  lineage JSONB,
  tag TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_build_runs_pack_model_created
  ON build_runs(pack_id, model_id, created_at DESC);

