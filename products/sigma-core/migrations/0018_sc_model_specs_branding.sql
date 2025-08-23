-- Branding fields for model_specs and optional guidance for IDs
BEGIN;

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS brand TEXT DEFAULT 'sigmatiq' NOT NULL,
  ADD COLUMN IF NOT EXISTS display_name TEXT; -- user-facing name (can omit brand in UI if desired)

-- Optional (COMMENT) guidance for naming convention:
COMMENT ON COLUMN sc.model_specs.brand IS 'Brand or namespace owner of the model (e.g., sigmatiq).';
COMMENT ON COLUMN sc.model_specs.display_name IS 'User-facing name; keep plain-language. Internal model_id may include brand prefix.';

COMMIT;

