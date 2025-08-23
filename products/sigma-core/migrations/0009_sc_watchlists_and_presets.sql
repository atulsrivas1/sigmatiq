-- Watchlists and Universe Presets
BEGIN;

-- User watchlists
CREATE TABLE IF NOT EXISTS sc.watchlists (
  watchlist_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  visibility TEXT NOT NULL DEFAULT 'private' CHECK (visibility IN ('private','shared','public')),
  is_default BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE (user_id, name)
);
DROP TRIGGER IF EXISTS trg_watchlists_updated_at ON sc.watchlists;
CREATE TRIGGER trg_watchlists_updated_at BEFORE UPDATE ON sc.watchlists
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();
-- Only one default per user
CREATE UNIQUE INDEX IF NOT EXISTS sc_watchlists_one_default_per_user
  ON sc.watchlists (user_id) WHERE is_default;

CREATE TABLE IF NOT EXISTS sc.watchlist_symbols (
  watchlist_id UUID NOT NULL REFERENCES sc.watchlists(watchlist_id) ON DELETE CASCADE,
  symbol TEXT NOT NULL,
  note TEXT,
  sort INT,
  added_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (watchlist_id, symbol)
);
CREATE INDEX IF NOT EXISTS sc_watchlist_symbols_watchlist_idx ON sc.watchlist_symbols (watchlist_id);

-- Curated universe presets (e.g., sp500, nasdaq100)
CREATE TABLE IF NOT EXISTS sc.universe_presets (
  preset_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  source TEXT,
  version TEXT,
  symbol_count INT,
  symbols_uri TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
DROP TRIGGER IF EXISTS trg_universe_presets_updated_at ON sc.universe_presets;
CREATE TRIGGER trg_universe_presets_updated_at BEFORE UPDATE ON sc.universe_presets
  FOR EACH ROW EXECUTE FUNCTION sc.touch_updated_at();

-- Optional explicit symbol list for smaller presets
CREATE TABLE IF NOT EXISTS sc.universe_preset_symbols (
  preset_id TEXT NOT NULL REFERENCES sc.universe_presets(preset_id) ON DELETE CASCADE,
  symbol TEXT NOT NULL,
  PRIMARY KEY (preset_id, symbol)
);
CREATE INDEX IF NOT EXISTS sc_universe_preset_symbols_preset_idx ON sc.universe_preset_symbols (preset_id);

COMMIT;
