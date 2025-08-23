-- Add plan_template column to model_specs (missed in initial create)
BEGIN;

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS plan_template JSONB; -- { stop_atr, tp_atr, max_hold_bars, sizing_hint }

COMMENT ON COLUMN sc.model_specs.plan_template IS 'Default plan template for novice-friendly SL/TP/max-hold and sizing hints.';

COMMIT;

