-- Backtest runs and folds for models and generic feature-set runs
BEGIN;

CREATE TABLE IF NOT EXISTS sc.model_backtest_runs (
  run_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  model_id TEXT,
  model_version INT,
  timeframe TEXT NOT NULL,
  data_window JSONB,        -- { start: 'YYYY-MM-DD', end: 'YYYY-MM-DD' }
  universe JSONB,           -- { preset_id|watchlist_id|symbols[], cap }
  featureset JSONB NOT NULL,
  label_cfg JSONB,
  params JSONB,             -- engine params used for the run
  metrics JSONB,            -- summary metrics (avg_sharpe_hourly, trades_total, cum_ret, etc.)
  best_config JSONB,        -- chosen best threshold/top_pct and other knobs
  git_sha TEXT,
  tag TEXT,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  finished_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS sc_model_backtests_model_idx ON sc.model_backtest_runs (model_id, model_version);
CREATE INDEX IF NOT EXISTS sc_model_backtests_started_idx ON sc.model_backtest_runs (started_at DESC);

CREATE TABLE IF NOT EXISTS sc.model_backtest_folds (
  run_id UUID REFERENCES sc.model_backtest_runs(run_id) ON DELETE CASCADE,
  fold INT NOT NULL,
  thr_used NUMERIC,
  cum_ret NUMERIC,
  sharpe_hourly NUMERIC,
  trades INT,
  PRIMARY KEY (run_id, fold)
);

COMMIT;

