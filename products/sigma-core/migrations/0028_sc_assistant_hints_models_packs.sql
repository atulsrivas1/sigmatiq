-- Add AI Assistant hints to model_specs and model_packs
BEGIN;

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS assistant_hints JSONB; -- e.g., [ "Verify liquidity before acting", "Reduce size in high vol" ]

ALTER TABLE sc.model_packs
  ADD COLUMN IF NOT EXISTS assistant_hints JSONB;

COMMIT;

