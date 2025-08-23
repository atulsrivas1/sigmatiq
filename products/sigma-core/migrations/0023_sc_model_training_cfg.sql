-- Training configuration and training runs registry
BEGIN;

-- Attach training configuration JSON to model specs for reproducibility
ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS training_cfg JSONB; -- e.g., { data_window:{start:'2023-01-01',end:'2024-08-01'}, session:{hours:'RTH'}, cv:{method:'rolling',folds:5,gap_bars:5}, filters:{weekdays:[1,2,3,4,5], time:'09:30-16:00', exclude_dates:[], min_dollar_vol:1e6} }

COMMENT ON COLUMN sc.model_specs.training_cfg IS 'Training dataset/time windows, cross-validation, session/time filters, and exclusions for reproducibility.';

-- Model training runs (lineage + metrics)
CREATE TABLE IF NOT EXISTS sc.model_training_runs (
  train_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  model_id TEXT NOT NULL,
  model_version INT NOT NULL,
  status TEXT NOT NULL DEFAULT 'started' CHECK (status IN ('started','success','error','partial')),

  training_cfg JSONB,    -- snapshot of effective training config
  data_window JSONB,     -- actual window used {start,end}
  dataset_hash TEXT,     -- e.g., SHA of feature dataset
  features_hash TEXT,    -- SHA of featureset or config
  git_sha TEXT,

  metrics JSONB,         -- { pr_auc:..., precision_at_k:..., cal_error:..., notes:... }
  error TEXT,

  started_at TIMESTAMPTZ DEFAULT NOW(),
  finished_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS sc_model_training_runs_model_idx ON sc.model_training_runs (model_id, model_version);
CREATE INDEX IF NOT EXISTS sc_model_training_runs_started_idx ON sc.model_training_runs (started_at DESC);

COMMIT;

