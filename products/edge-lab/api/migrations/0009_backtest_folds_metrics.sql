-- Add optional metrics to backtest_folds for stability and drawdown analysis

ALTER TABLE backtest_folds
  ADD COLUMN IF NOT EXISTS sortino DOUBLE PRECISION,
  ADD COLUMN IF NOT EXISTS max_dd DOUBLE PRECISION;

