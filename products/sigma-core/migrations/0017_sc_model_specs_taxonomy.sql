-- Taxonomy fields for model_specs: horizon/style/tags and instrument/suitability profiles
BEGIN;

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS tags TEXT[];

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS horizon TEXT,
  ADD COLUMN IF NOT EXISTS style TEXT,
  ADD COLUMN IF NOT EXISTS instrument_profile JSONB,
  ADD COLUMN IF NOT EXISTS suitability JSONB;

-- Optional CHECK constraints for common values (non-exhaustive, remains forward-compatible)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'chk_model_specs_horizon'
  ) THEN
    ALTER TABLE sc.model_specs
      ADD CONSTRAINT chk_model_specs_horizon
      CHECK (horizon IS NULL OR horizon IN ('0dte','intraday','swing','position','long_term'));
  END IF;
END$$;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'chk_model_specs_style'
  ) THEN
    ALTER TABLE sc.model_specs
      ADD CONSTRAINT chk_model_specs_style
      CHECK (style IS NULL OR style IN ('momentum','mean_reversion','trend_follow','breakout','volatility','carry','stat_arb'));
  END IF;
END$$;

COMMIT;
