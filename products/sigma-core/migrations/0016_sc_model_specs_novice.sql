-- Add novice-friendly fields to model registry (model_specs)
BEGIN;

ALTER TABLE sc.model_specs
  ADD COLUMN IF NOT EXISTS novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  ADD COLUMN IF NOT EXISTS beginner_summary TEXT,
  ADD COLUMN IF NOT EXISTS simple_defaults JSONB,   -- e.g., { operation:'preview|subscribe', timeframe:'day', cap:50 }
  ADD COLUMN IF NOT EXISTS explainer_templates JSONB, -- e.g., { summary_tpl, why_tpl, how_to_check_tpl }
  ADD COLUMN IF NOT EXISTS risk_notes JSONB;         -- e.g., { high_vol: 'Choppy regime note', earnings: 'Event risk note' }

COMMIT;

