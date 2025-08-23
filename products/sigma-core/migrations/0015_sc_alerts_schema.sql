-- Alerts AI schema: models, subscriptions, runs, alerts, deliveries, outcomes, settings
BEGIN;

-- ---------------------------------------------------------------------------
-- Model specifications (registry)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sc.model_specs (
  model_id TEXT NOT NULL,
  version INT NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft','in_review','published','deprecated')),

  title TEXT NOT NULL,
  description TEXT,

  target_kind TEXT CHECK (target_kind IN ('indicator_set','strategy','recipe')),
  target_id TEXT,
  target_version INT,
  timeframe TEXT,
  market TEXT DEFAULT 'US',
  instrument TEXT DEFAULT 'equity',

  featureset JSONB,      -- e.g., { set_id:'macd_trend_pullback_v1', version:1 }
  label_cfg JSONB,       -- TP/SL/max_hold config, horizons
  thresholds JSONB,      -- buy/sell thresholds, precision targets
  guardrails JSONB,      -- quotas, exposure caps, DTE mins
  artifacts JSONB,       -- { model_uri, calibration_uri, notes }

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  PRIMARY KEY (model_id, version)
);
DROP TRIGGER IF EXISTS trg_model_specs_updated_at ON sc.model_specs;
CREATE TRIGGER trg_model_specs_updated_at BEFORE UPDATE ON sc.model_specs
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
CREATE UNIQUE INDEX IF NOT EXISTS sc_model_specs_one_published_per_id
  ON sc.model_specs (model_id) WHERE status = 'published';

CREATE OR REPLACE VIEW sc.v_model_specs_published AS
SELECT DISTINCT ON (model_id) *
FROM sc.model_specs
WHERE status = 'published'
ORDER BY model_id, version DESC;

-- ---------------------------------------------------------------------------
-- User alert settings and subscriptions
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sc.user_alert_settings (
  user_id TEXT PRIMARY KEY,
  defaults JSONB,
  daily_budget INT,
  hourly_budget INT,
  mute_until TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
DROP TRIGGER IF EXISTS trg_user_alert_settings_updated_at ON sc.user_alert_settings;
CREATE TRIGGER trg_user_alert_settings_updated_at BEFORE UPDATE ON sc.user_alert_settings
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();

CREATE TABLE IF NOT EXISTS sc.alert_subscriptions (
  subscription_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT NOT NULL,
  target_kind TEXT NOT NULL CHECK (target_kind IN ('model','indicator_set','strategy','recipe')),
  target_id TEXT NOT NULL,
  target_version INT,
  model_id TEXT,
  model_version INT,
  timeframe TEXT NOT NULL,
  preset_id TEXT REFERENCES sc.universe_presets(preset_id) ON DELETE SET NULL,
  watchlist_id UUID REFERENCES sc.watchlists(watchlist_id) ON DELETE SET NULL,
  budgets JSONB,     -- { daily:5, hourly:0 }
  channels JSONB,    -- { email:true, push:true, inapp:true }
  active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS sc_alert_subscriptions_user_idx ON sc.alert_subscriptions (user_id);
DROP TRIGGER IF EXISTS trg_alert_subscriptions_updated_at ON sc.alert_subscriptions;
CREATE TRIGGER trg_alert_subscriptions_updated_at BEFORE UPDATE ON sc.alert_subscriptions
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
-- Prevent duplicate subscriptions for the same scope
CREATE UNIQUE INDEX IF NOT EXISTS sc_alert_subs_unique_scope
  ON sc.alert_subscriptions (user_id, target_kind, target_id, timeframe, COALESCE(preset_id, ''), COALESCE(watchlist_id::text, ''));

-- ---------------------------------------------------------------------------
-- Runs and alerts
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sc.alert_runs (
  run_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  triggered_by TEXT NOT NULL CHECK (triggered_by IN ('system','user','preview')),
  subscription_id UUID REFERENCES sc.alert_subscriptions(subscription_id) ON DELETE SET NULL,
  user_id TEXT,
  model_id TEXT,
  model_version INT,
  target_kind TEXT,
  target_id TEXT,
  target_version INT,
  timeframe TEXT,
  universe_kind TEXT CHECK (universe_kind IN ('preset','watchlist')),
  preset_id TEXT REFERENCES sc.universe_presets(preset_id) ON DELETE SET NULL,
  watchlist_id UUID REFERENCES sc.watchlists(watchlist_id) ON DELETE SET NULL,
  cap INT,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  finished_at TIMESTAMPTZ,
  status TEXT CHECK (status IN ('started','success','error','partial')),
  error TEXT
);
CREATE INDEX IF NOT EXISTS sc_alert_runs_started_idx ON sc.alert_runs (started_at DESC);
CREATE INDEX IF NOT EXISTS sc_alert_runs_user_idx ON sc.alert_runs (user_id);

CREATE TABLE IF NOT EXISTS sc.alerts (
  alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  run_id UUID NOT NULL REFERENCES sc.alert_runs(run_id) ON DELETE CASCADE,
  subscription_id UUID REFERENCES sc.alert_subscriptions(subscription_id) ON DELETE SET NULL,
  user_id TEXT,
  symbol TEXT NOT NULL,
  market TEXT,
  instrument TEXT,
  timeframe TEXT,
  decision TEXT CHECK (decision IN ('buy','sell','hold')),
  score NUMERIC,
  plan JSONB,     -- { stop_pct, take_profit_pct, max_hold_bars, sizing_hint }
  reasons JSONB,
  model_id TEXT,
  model_version INT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  delivered_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS sc_alerts_user_created_idx ON sc.alerts (user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS sc_alerts_symbol_idx ON sc.alerts (symbol, created_at DESC);
CREATE UNIQUE INDEX IF NOT EXISTS sc_alerts_unique_per_run_symbol ON sc.alerts (run_id, symbol);

CREATE TABLE IF NOT EXISTS sc.alert_delivery (
  alert_id UUID NOT NULL REFERENCES sc.alerts(alert_id) ON DELETE CASCADE,
  channel TEXT NOT NULL CHECK (channel IN ('email','push','inapp')),
  status TEXT NOT NULL CHECK (status IN ('pending','sent','opened','failed')),
  provider_msg_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (alert_id, channel)
);
DROP TRIGGER IF EXISTS trg_alert_delivery_updated_at ON sc.alert_delivery;
CREATE TRIGGER trg_alert_delivery_updated_at BEFORE UPDATE ON sc.alert_delivery
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();

CREATE TABLE IF NOT EXISTS sc.alert_outcomes (
  alert_id UUID PRIMARY KEY REFERENCES sc.alerts(alert_id) ON DELETE CASCADE,
  outcome TEXT CHECK (outcome IN ('tp_hit','sl_hit','max_hold','expired','cancelled')),
  realized_return NUMERIC,
  resolved_at TIMESTAMPTZ,
  meta JSONB
);
CREATE INDEX IF NOT EXISTS sc_alert_outcomes_resolved_idx ON sc.alert_outcomes (resolved_at DESC);

COMMIT;

