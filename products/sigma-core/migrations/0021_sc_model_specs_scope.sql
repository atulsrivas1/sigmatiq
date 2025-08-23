-- Add explicit scope field to model_specs for cohort vs per-ticker targeting
BEGIN;

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS scope JSONB; -- e.g., { type:'cohort', allow_presets:['sp500'] } or { type:'per_ticker', allow_symbols:['SPY'] }

COMMENT ON COLUMN sc.model_specs.scope IS 'Targeting scope for the model: cohort vs per_ticker plus allowed presets/symbols/filters.';

COMMIT;

