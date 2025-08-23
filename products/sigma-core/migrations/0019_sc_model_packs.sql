-- Model Packs: group multiple models with consensus policy
BEGIN;

-- Registry for model packs (versioned, publishable)
CREATE TABLE IF NOT EXISTS sc.model_packs (
  pack_id TEXT NOT NULL,
  version INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','in_review','published','deprecated')),

  title TEXT NOT NULL,
  description TEXT,

  brand TEXT NOT NULL DEFAULT 'sigmatiq',
  display_name TEXT,

  timeframe TEXT,
  market TEXT DEFAULT 'US',
  instrument TEXT DEFAULT 'equity',

  -- Taxonomy
  horizon TEXT,
  style TEXT,
  tags TEXT[],
  instrument_profile JSONB,
  suitability JSONB,

  -- Novice
  novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  beginner_summary TEXT,
  simple_defaults JSONB,
  explainer_templates JSONB,
  risk_notes JSONB,

  -- Consensus policy
  consensus JSONB, -- e.g., { policy:'majority|weighted|all', min_quorum:2, buy_score:0.7, sell_score:0.7, tie_breaker:'hold' }

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  PRIMARY KEY (pack_id, version)
);
DROP TRIGGER IF EXISTS trg_model_packs_updated_at ON sc.model_packs;
CREATE TRIGGER trg_model_packs_updated_at BEFORE UPDATE ON sc.model_packs
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
CREATE UNIQUE INDEX IF NOT EXISTS sc_model_packs_one_published_per_id
  ON sc.model_packs (pack_id) WHERE status = 'published';

CREATE OR REPLACE VIEW sc.v_model_packs_published AS
SELECT DISTINCT ON (pack_id) *
FROM sc.model_packs
WHERE status = 'published'
ORDER BY pack_id, version DESC;

-- Components of a pack
CREATE TABLE IF NOT EXISTS sc.model_pack_components (
  pack_id TEXT NOT NULL,
  pack_version INT NOT NULL,
  ord INT NOT NULL,
  model_id TEXT NOT NULL,
  model_version INT NOT NULL,
  weight NUMERIC,
  required BOOLEAN DEFAULT FALSE,
  min_score NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (pack_id, pack_version, ord),
  FOREIGN KEY (pack_id, pack_version)
    REFERENCES sc.model_packs(pack_id, version) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS sc_model_pack_components_model_idx
  ON sc.model_pack_components (model_id, model_version);

COMMIT;

