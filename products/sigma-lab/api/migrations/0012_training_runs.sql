-- Training runs history: records training operations and artifacts
CREATE TABLE IF NOT EXISTS training_runs (
  id SERIAL PRIMARY KEY,
  pack_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  started_at TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  params JSONB,
  metrics JSONB,
  model_out_uri TEXT,
  features JSONB,
  lineage JSONB,
  tag TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_training_runs_pack_model_created
  ON training_runs(pack_id, model_id, created_at DESC);

