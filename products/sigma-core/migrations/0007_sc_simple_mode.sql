-- Simple Mode and Novice-First data model enhancements
-- Goal: enforce beginner-facing summaries, defaults, and guardrails directly in the DB

BEGIN;

-- Shared trigger: ensure beginner requirements when publishing novice-ready content
CREATE OR REPLACE FUNCTION sc.enforce_beginner_requirements()
RETURNS TRIGGER AS $$
BEGIN
  -- Only enforce on publish of novice-ready content
  IF NEW.status = 'published' AND COALESCE(NEW.novice_ready, false) THEN
    IF TG_TABLE_NAME = 'indicators' THEN
      IF NEW.beginner_summary IS NULL THEN
        RAISE EXCEPTION 'sc.indicators: beginner_summary required when novice_ready and published (id=%).', NEW.id;
      END IF;
    ELSIF TG_TABLE_NAME = 'indicator_sets' THEN
      IF NEW.beginner_summary IS NULL THEN
        RAISE EXCEPTION 'sc.indicator_sets: beginner_summary required when novice_ready and published (set_id=%).', NEW.set_id;
      END IF;
      -- simple_defaults encouraged but not strictly required
    ELSIF TG_TABLE_NAME = 'strategies' THEN
      IF NEW.beginner_summary IS NULL THEN
        RAISE EXCEPTION 'sc.strategies: beginner_summary required when novice_ready and published (strategy_id=%).', NEW.strategy_id;
      END IF;
    ELSIF TG_TABLE_NAME = 'workflows' THEN
      IF NEW.beginner_summary IS NULL THEN
        RAISE EXCEPTION 'sc.workflows: beginner_summary required when novice_ready and published (workflow_id=%).', NEW.workflow_id;
      END IF;
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Indicators: novice flags and explainer fields
ALTER TABLE IF EXISTS sc.indicators
  ADD COLUMN IF NOT EXISTS novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  ADD COLUMN IF NOT EXISTS beginner_summary TEXT,
  ADD COLUMN IF NOT EXISTS beginner_examples JSONB;

DROP TRIGGER IF EXISTS trg_indicators_enforce_beginner ON sc.indicators;
CREATE TRIGGER trg_indicators_enforce_beginner
  BEFORE INSERT OR UPDATE ON sc.indicators
  FOR EACH ROW EXECUTE FUNCTION sc.enforce_beginner_requirements();

-- Indicator Sets: novice flags, defaults and guardrails for Simple Mode
ALTER TABLE IF EXISTS sc.indicator_sets
  ADD COLUMN IF NOT EXISTS novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  ADD COLUMN IF NOT EXISTS beginner_summary TEXT,
  ADD COLUMN IF NOT EXISTS simple_defaults JSONB,   -- e.g., { timeframe:'5m', params:{...} }
  ADD COLUMN IF NOT EXISTS guardrails JSONB;        -- e.g., { universe_cap:200, throttle_per_min:2 }

DROP TRIGGER IF EXISTS trg_indicator_sets_enforce_beginner ON sc.indicator_sets;
CREATE TRIGGER trg_indicator_sets_enforce_beginner
  BEFORE INSERT OR UPDATE ON sc.indicator_sets
  FOR EACH ROW EXECUTE FUNCTION sc.enforce_beginner_requirements();

-- Strategies: novice flags, defaults and guardrails for Simple Mode
ALTER TABLE IF EXISTS sc.strategies
  ADD COLUMN IF NOT EXISTS novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  ADD COLUMN IF NOT EXISTS beginner_summary TEXT,
  ADD COLUMN IF NOT EXISTS simple_defaults JSONB,   -- e.g., { operation:'screen|alert|subscribe', params:{...}, timeframe:'5m' }
  ADD COLUMN IF NOT EXISTS guardrails JSONB;        -- e.g., { max_positions:5, max_daily_trades:10, loss_cap_bps:50 }

DROP TRIGGER IF EXISTS trg_strategies_enforce_beginner ON sc.strategies;
CREATE TRIGGER trg_strategies_enforce_beginner
  BEFORE INSERT OR UPDATE ON sc.strategies
  FOR EACH ROW EXECUTE FUNCTION sc.enforce_beginner_requirements();

-- Workflows: novice flags and summaries (used for guided recipes)
ALTER TABLE IF EXISTS sc.workflows
  ADD COLUMN IF NOT EXISTS novice_ready BOOLEAN DEFAULT FALSE NOT NULL,
  ADD COLUMN IF NOT EXISTS beginner_summary TEXT;

DROP TRIGGER IF EXISTS trg_workflows_enforce_beginner ON sc.workflows;
CREATE TRIGGER trg_workflows_enforce_beginner
  BEFORE INSERT OR UPDATE ON sc.workflows
  FOR EACH ROW EXECUTE FUNCTION sc.enforce_beginner_requirements();

-- Curated Simple Recipes: the novice-first surface
-- Each recipe points to a target (indicator|indicator_set|strategy|workflow) with safe defaults and guardrails
CREATE TABLE IF NOT EXISTS sc.simple_recipes (
  recipe_id TEXT NOT NULL,
  version INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','in_review','published')),

  title TEXT NOT NULL,
  subtitle TEXT,
  beginner_summary TEXT NOT NULL,
  persona TEXT DEFAULT 'beginner',
  difficulty TEXT DEFAULT 'beginner',

  target_kind TEXT NOT NULL CHECK (target_kind IN ('indicator','indicator_set','strategy','workflow')),
  target_id TEXT NOT NULL,
  target_version INT,

  defaults JSONB,            -- parameters/timeframe/universe presets for Simple Mode
  guardrails JSONB,          -- hard caps and safety controls
  risk_profile TEXT CHECK (risk_profile IN ('conservative','balanced','aggressive')),
  universe_preset TEXT,      -- e.g., 'sp500', 'watchlist', 'spy_only'
  sort_rank INT DEFAULT 100,

  tags TEXT[],

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  PRIMARY KEY (recipe_id, version)
);
CREATE UNIQUE INDEX IF NOT EXISTS sc_simple_recipes_one_published_per_id
  ON sc.simple_recipes (recipe_id) WHERE status = 'published';
CREATE INDEX IF NOT EXISTS sc_simple_recipes_target_idx
  ON sc.simple_recipes (target_kind, target_id);
CREATE INDEX IF NOT EXISTS sc_simple_recipes_rank_idx
  ON sc.simple_recipes (sort_rank);
DROP TRIGGER IF EXISTS trg_simple_recipes_updated_at ON sc.simple_recipes;
CREATE TRIGGER trg_simple_recipes_updated_at BEFORE UPDATE ON sc.simple_recipes
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();

-- Convenience view: latest published recipes
CREATE OR REPLACE VIEW sc.v_simple_recipes_published AS
SELECT DISTINCT ON (recipe_id) *
FROM sc.simple_recipes
WHERE status = 'published'
ORDER BY recipe_id, version DESC;

COMMIT;
