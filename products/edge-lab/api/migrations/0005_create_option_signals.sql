-- Option signals (overlay on top of base signals), phase 2

CREATE TABLE IF NOT EXISTS option_signals (
  id BIGSERIAL PRIMARY KEY,
  signal_id BIGINT NOT NULL REFERENCES signals(id) ON DELETE CASCADE,

  -- Contract identification
  occ_symbol TEXT,
  expiry DATE,
  strike DOUBLE PRECISION,
  type TEXT, -- 'call' | 'put'
  delta DOUBLE PRECISION,
  iv_used DOUBLE PRECISION,

  -- Premium brackets / values
  entry_premium_est DOUBLE PRECISION,
  stop_premium_est DOUBLE PRECISION,
  target_premium_est DOUBLE PRECISION,
  pricing_estimate BOOLEAN,

  -- Spreads (optional, for future)
  legs_json JSONB,
  net_debit_credit DOUBLE PRECISION,
  stop_value DOUBLE PRECISION,
  target_value DOUBLE PRECISION,

  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_option_signals_signal ON option_signals (signal_id);
CREATE INDEX IF NOT EXISTS idx_option_signals_expiry ON option_signals (expiry);
CREATE INDEX IF NOT EXISTS idx_option_signals_occ ON option_signals (occ_symbol);

