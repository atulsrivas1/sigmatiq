-- Enforce novice fields on publish for models and packs
BEGIN;

-- For model_specs: when novice_ready and status='published', require non-null beginner_summary, explainer_templates, guardrails
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'chk_model_specs_novice_publish'
  ) THEN
    ALTER TABLE sc.model_specs
      ADD CONSTRAINT chk_model_specs_novice_publish
      CHECK (
        NOT (novice_ready AND status = 'published')
        OR (beginner_summary IS NOT NULL AND explainer_templates IS NOT NULL AND guardrails IS NOT NULL)
      );
  END IF;
END$$;

-- For model_packs: same enforcement
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'chk_model_packs_novice_publish'
  ) THEN
    ALTER TABLE sc.model_packs
      ADD CONSTRAINT chk_model_packs_novice_publish
      CHECK (
        NOT (novice_ready AND status = 'published')
        OR (beginner_summary IS NOT NULL AND explainer_templates IS NOT NULL AND consensus IS NOT NULL)
      );
  END IF;
END$$;

COMMIT;

