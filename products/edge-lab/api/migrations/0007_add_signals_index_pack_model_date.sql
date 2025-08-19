-- Optional composite index for frequent filters on (pack_id, model_id, date)
CREATE INDEX IF NOT EXISTS idx_signals_pack_model_date ON signals (pack_id, model_id, date DESC);

