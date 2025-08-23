-- Sigma Core database schema and entities (schema: sc)
-- Branding via dedicated schema `sc` (sigma-core)

-- Optional: enable useful extensions (safe if already installed)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Schema namespace
CREATE SCHEMA IF NOT EXISTS sc;

-- Utility: auto-update updated_at timestamps
CREATE OR REPLACE FUNCTION sc.touch_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ---------------------------------------------------------------------------
-- Shared tables
-- ---------------------------------------------------------------------------

-- Controlled vocabulary for tags (optional but recommended)
CREATE TABLE IF NOT EXISTS sc.tags (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL CHECK (kind IN ('category','persona','difficulty','risk','use_case')),
  label TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
DROP TRIGGER IF EXISTS trg_tags_updated_at ON sc.tags;
CREATE TRIGGER trg_tags_updated_at BEFORE UPDATE ON sc.tags
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();

-- Media assets referenced by explainers
CREATE TABLE IF NOT EXISTS sc.media_assets (
  asset_id TEXT PRIMARY KEY,
  uri TEXT NOT NULL,
  alt TEXT,
  caption TEXT,
  kind TEXT,
  width INT,
  height INT,
  sha256 TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
DROP TRIGGER IF EXISTS trg_media_assets_updated_at ON sc.media_assets;
CREATE TRIGGER trg_media_assets_updated_at BEFORE UPDATE ON sc.media_assets
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();

-- Optional: link arbitrary entities to tags (governance over free-form arrays)
CREATE TABLE IF NOT EXISTS sc.entity_tags (
  entity_kind TEXT NOT NULL CHECK (entity_kind IN ('indicator','indicator_set','strategy','workflow')),
  id TEXT NOT NULL,
  version INT NOT NULL,
  tag_id TEXT NOT NULL REFERENCES sc.tags(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (entity_kind, id, version, tag_id)
);

-- ---------------------------------------------------------------------------
-- Indicators
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sc.indicators (
  id TEXT NOT NULL,
  version INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','in_review','published')),

  title TEXT NOT NULL,
  subtitle TEXT,
  category TEXT,
  subcategory TEXT,
  tags TEXT[],
  short_description TEXT,
  long_description TEXT,

  parameters JSONB,           -- array of param objects
  measures JSONB,             -- what_it_measures, how_to_read, typical_ranges, caveats
  data_requirements JSONB,    -- inputs, timeframe, lookback, dependencies
  usage JSONB,                -- best_when, avoid_when, example_conditions, step_by_step
  performance_hints JSONB,    -- cost_band, latency_band, stability

  -- Assistant/editorial hints and novice-first columns (present from day 1 so seeds work)
  assistant_hints JSONB,
  novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  beginner_summary TEXT,

  cover_asset_id TEXT REFERENCES sc.media_assets(asset_id) ON DELETE SET NULL,
  gallery JSONB,              -- optional additional media refs

  "references" JSONB,           -- research refs [{title,url,note}]
  reviewed_by TEXT,
  confidence_score INT,
  code_version TEXT,
  git_sha TEXT,
  docs_uri TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  PRIMARY KEY (id, version)
);
CREATE INDEX IF NOT EXISTS sc_indicators_cat_idx ON sc.indicators (category, subcategory);
CREATE INDEX IF NOT EXISTS sc_indicators_tags_gin ON sc.indicators USING GIN (tags);
DROP TRIGGER IF EXISTS trg_indicators_updated_at ON sc.indicators;
CREATE TRIGGER trg_indicators_updated_at BEFORE UPDATE ON sc.indicators
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
-- Ensure only one published version per id
CREATE UNIQUE INDEX IF NOT EXISTS sc_indicators_one_published_per_id
ON sc.indicators (id) WHERE status = 'published';

-- Latest published view
CREATE OR REPLACE VIEW sc.v_indicators_published AS
SELECT DISTINCT ON (id) *
FROM sc.indicators
WHERE status = 'published'
ORDER BY id, version DESC;

-- ---------------------------------------------------------------------------
-- Indicator Sets
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sc.indicator_sets (
  set_id TEXT NOT NULL,
  version INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','in_review','published')),

  title TEXT NOT NULL,
  purpose TEXT,
  tags TEXT[],

  rationale TEXT,
  reading_guide JSONB,        -- signal_logic, weighting_rules, timeframe_alignment
  risk_notes TEXT,
  anti_patterns JSONB,
  data_requirements JSONB,
  performance_hints JSONB,
  assistant_hints JSONB,

  -- Novice-first columns present from day 1 so seeds work
  novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  beginner_summary TEXT,
  simple_defaults JSONB,   -- e.g., { timeframe:'5m', params:{...} }
  guardrails JSONB,        -- e.g., { universe_cap:200, throttle_per_min:2 }
  cover_asset_id TEXT REFERENCES sc.media_assets(asset_id) ON DELETE SET NULL,
  gallery JSONB,

  "references" JSONB,
  reviewed_by TEXT,
  confidence_score INT,
  code_version TEXT,
  git_sha TEXT,
  docs_uri TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  PRIMARY KEY (set_id, version)
);
CREATE INDEX IF NOT EXISTS sc_indicator_sets_tags_gin ON sc.indicator_sets USING GIN (tags);
DROP TRIGGER IF EXISTS trg_indicator_sets_updated_at ON sc.indicator_sets;
CREATE TRIGGER trg_indicator_sets_updated_at BEFORE UPDATE ON sc.indicator_sets
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
CREATE UNIQUE INDEX IF NOT EXISTS sc_indicator_sets_one_published_per_id
ON sc.indicator_sets (set_id) WHERE status = 'published';

CREATE OR REPLACE VIEW sc.v_indicator_sets_published AS
SELECT DISTINCT ON (set_id) *
FROM sc.indicator_sets
WHERE status = 'published'
ORDER BY set_id, version DESC;

-- Components for each set (normalized)
CREATE TABLE IF NOT EXISTS sc.indicator_set_components (
  set_id TEXT NOT NULL,
  set_version INT NOT NULL,
  ord INT NOT NULL,
  indicator_id TEXT NOT NULL,
  indicator_version INT,
  params JSONB,
  role TEXT,
  weight NUMERIC,
  timeframe TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (set_id, set_version, ord),
  FOREIGN KEY (set_id, set_version)
    REFERENCES sc.indicator_sets(set_id, version) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS sc_set_components_indicator_idx
  ON sc.indicator_set_components (indicator_id);

-- ---------------------------------------------------------------------------
-- Strategies
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sc.strategies (
  strategy_id TEXT NOT NULL,
  version INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','in_review','published')),

  title TEXT NOT NULL,
  objective TEXT,
  tags TEXT[],

  entry_logic JSONB,
  exit_logic JSONB,
  filters JSONB,
  risk JSONB,                 -- sizing, stops/targets, loss limits
  execution_policy JSONB,     -- slippage, order types, hours, liquidity rules
  pre_reqs JSONB,             -- datasets, indicator_sets_used (redundant with link table)
  performance_snapshot JSONB, -- curated ranges, not promises
  caveats TEXT,
  compliance_note TEXT,
  how_to_evaluate JSONB,

  cover_asset_id TEXT REFERENCES sc.media_assets(asset_id) ON DELETE SET NULL,
  gallery JSONB,

  "references" JSONB,
  reviewed_by TEXT,
  confidence_score INT,
  code_version TEXT,
  git_sha TEXT,
  docs_uri TEXT,

  -- Novice-first columns present from day 1 so seeds work
  novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  beginner_summary TEXT,
  simple_defaults JSONB,   -- e.g., { operation:'screen|alert|subscribe', params:{...}, timeframe:'5m' }
  guardrails JSONB,        -- e.g., { max_positions:5, max_daily_trades:10, loss_cap_bps:50 }

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  PRIMARY KEY (strategy_id, version)
);
CREATE INDEX IF NOT EXISTS sc_strategies_tags_gin ON sc.strategies USING GIN (tags);
DROP TRIGGER IF EXISTS trg_strategies_updated_at ON sc.strategies;
CREATE TRIGGER trg_strategies_updated_at BEFORE UPDATE ON sc.strategies
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
CREATE UNIQUE INDEX IF NOT EXISTS sc_strategies_one_published_per_id
ON sc.strategies (strategy_id) WHERE status = 'published';

CREATE OR REPLACE VIEW sc.v_strategies_published AS
SELECT DISTINCT ON (strategy_id) *
FROM sc.strategies
WHERE status = 'published'
ORDER BY strategy_id, version DESC;

-- Link strategies to indicator sets (normalized)
CREATE TABLE IF NOT EXISTS sc.strategy_indicator_sets (
  strategy_id TEXT NOT NULL,
  strategy_version INT NOT NULL,
  set_id TEXT NOT NULL,
  set_version INT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (strategy_id, strategy_version, set_id, set_version),
  FOREIGN KEY (strategy_id, strategy_version)
    REFERENCES sc.strategies(strategy_id, version) ON DELETE CASCADE,
  FOREIGN KEY (set_id, set_version)
    REFERENCES sc.indicator_sets(set_id, version) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------------
-- Workflows
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sc.workflows (
  workflow_id TEXT NOT NULL,
  version INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','in_review','published')),

  title TEXT NOT NULL,
  subtitle TEXT,
  goal TEXT,
  persona TEXT,
  difficulty TEXT,
  time_to_complete INT,
  tags TEXT[],

  prerequisites JSONB,
  dependencies JSONB,         -- { indicators:[], indicator_sets:[], strategies:[] }
  steps JSONB,                -- array of step objects
  outputs JSONB,
  best_when JSONB,
  avoid_when JSONB,
  caveats JSONB,
  links JSONB,

  cover_asset_id TEXT REFERENCES sc.media_assets(asset_id) ON DELETE SET NULL,
  gallery JSONB,

  "references" JSONB,
  reviewed_by TEXT,
  confidence_score INT,
  docs_uri TEXT,

  -- Novice-first columns present from day 1 so seeds work
  novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  beginner_summary TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  PRIMARY KEY (workflow_id, version)
);
CREATE INDEX IF NOT EXISTS sc_workflows_persona_time_idx ON sc.workflows (persona, time_to_complete);
CREATE INDEX IF NOT EXISTS sc_workflows_tags_gin ON sc.workflows USING GIN (tags);
DROP TRIGGER IF EXISTS trg_workflows_updated_at ON sc.workflows;
CREATE TRIGGER trg_workflows_updated_at BEFORE UPDATE ON sc.workflows
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
CREATE UNIQUE INDEX IF NOT EXISTS sc_workflows_one_published_per_id
ON sc.workflows (workflow_id) WHERE status = 'published';

CREATE OR REPLACE VIEW sc.v_workflows_published AS
SELECT DISTINCT ON (workflow_id) *
FROM sc.workflows
WHERE status = 'published'
ORDER BY workflow_id, version DESC;
