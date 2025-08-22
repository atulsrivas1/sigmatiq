-- Config and policy storage in DB (move away from YAML files)

CREATE TABLE IF NOT EXISTS packs (
  id TEXT PRIMARY KEY,
  meta JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS model_configs (
  pack_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  config JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (pack_id, model_id)
);

-- Versioned policies (latest is max(version))
CREATE TABLE IF NOT EXISTS policies (
  pack_id TEXT NOT NULL,
  model_id TEXT NOT NULL,
  version INT NOT NULL DEFAULT 1,
  policy JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (pack_id, model_id, version)
);

CREATE INDEX IF NOT EXISTS idx_policies_latest ON policies (pack_id, model_id, version DESC);

-- Indicator sets (pack or model scope)
CREATE TABLE IF NOT EXISTS indicator_sets (
  id SERIAL PRIMARY KEY,
  pack_id TEXT NOT NULL,
  scope TEXT NOT NULL,             -- 'pack' | 'model'
  model_id TEXT NULL,
  name TEXT NULL,
  data JSONB NOT NULL,
  version INT NOT NULL DEFAULT 1,
  created_at TIMESTAMPTZ DEFAULT now()
);

