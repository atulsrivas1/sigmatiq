-- Enforce guardrails for novice-ready sets and strategies on publish
BEGIN;

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
      IF NEW.guardrails IS NULL THEN
        RAISE EXCEPTION 'sc.indicator_sets: guardrails required when novice_ready and published (set_id=%).', NEW.set_id;
      END IF;
    ELSIF TG_TABLE_NAME = 'strategies' THEN
      IF NEW.beginner_summary IS NULL THEN
        RAISE EXCEPTION 'sc.strategies: beginner_summary required when novice_ready and published (strategy_id=%).', NEW.strategy_id;
      END IF;
      IF NEW.guardrails IS NULL THEN
        RAISE EXCEPTION 'sc.strategies: guardrails required when novice_ready and published (strategy_id=%).', NEW.strategy_id;
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

COMMIT;

