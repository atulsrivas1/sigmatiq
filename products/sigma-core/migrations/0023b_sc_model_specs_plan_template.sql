-- Add plan_template column to model_specs before seeding
BEGIN;

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS plan_template JSONB; -- { stop_atr, tp_atr, max_hold_bars, sizing_hint }

COMMIT;

