-- Model Pipeline runs for dataset+sweep+training orchestration
BEGIN;

CREATE TABLE IF NOT EXISTS sc.model_pipeline_runs (
  pipeline_run_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  model_id TEXT NOT NULL,
  model_version INT,
  timeframe TEXT,
  universe JSONB,
  sweep JSONB,
  guardrails JSONB,
  dataset_run_id UUID,
  backtest_run_ids JSONB,
  training_run_id UUID,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','running','success','stopped','error')),
  summary TEXT,
  errors JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  finished_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS sc_model_pipeline_runs_model_idx ON sc.model_pipeline_runs (model_id, created_at DESC);
CREATE INDEX IF NOT EXISTS sc_model_pipeline_runs_status_idx ON sc.model_pipeline_runs (status);

COMMIT;

