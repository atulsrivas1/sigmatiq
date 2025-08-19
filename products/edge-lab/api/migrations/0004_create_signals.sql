-- Signals table for actionable alerts (stocks)
-- id uses bigserial to avoid uuid extension dependency

CREATE TABLE IF NOT EXISTS signals (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL,
  model_id TEXT NOT NULL,
  ticker TEXT NOT NULL,

  -- Core execution fields
  side TEXT,
  entry_mode TEXT,
  entry_ref_px DOUBLE PRECISION,
  stop_px DOUBLE PRECISION,
  target_px DOUBLE PRECISION,
  time_stop_minutes INTEGER,
  rr DOUBLE PRECISION,

  -- Scoring fields (optional depending on source)
  score_total DOUBLE PRECISION,
  rank INTEGER,
  score_breakout DOUBLE PRECISION,
  score_momentum DOUBLE PRECISION,
  score_trend_quality DOUBLE PRECISION,
  score_alignment DOUBLE PRECISION,

  -- Metadata & lineage (optional)
  pack_id TEXT,
  policy_version TEXT,
  pack_sha TEXT,
  indicator_set_sha TEXT,
  model_config_sha TEXT,
  policy_sha TEXT,

  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(date, model_id, ticker)
);

CREATE INDEX IF NOT EXISTS idx_signals_date_model ON signals (date, model_id);
CREATE INDEX IF NOT EXISTS idx_signals_model_date ON signals (model_id, date DESC);
CREATE INDEX IF NOT EXISTS idx_signals_model_ticker_date ON signals (model_id, ticker, date DESC);

