-- Add assistant_hints to indicators and indicator_sets
ALTER TABLE IF EXISTS sc.indicators
  ADD COLUMN IF NOT EXISTS assistant_hints JSONB;

ALTER TABLE IF EXISTS sc.indicator_sets
  ADD COLUMN IF NOT EXISTS assistant_hints JSONB;

