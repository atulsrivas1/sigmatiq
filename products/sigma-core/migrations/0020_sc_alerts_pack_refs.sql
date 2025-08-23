-- Add optional pack references to runs and alerts
BEGIN;

ALTER TABLE sc.alert_runs
  ADD COLUMN IF NOT EXISTS pack_id TEXT,
  ADD COLUMN IF NOT EXISTS pack_version INT;

ALTER TABLE sc.alerts
  ADD COLUMN IF NOT EXISTS pack_id TEXT,
  ADD COLUMN IF NOT EXISTS pack_version INT;

COMMIT;

