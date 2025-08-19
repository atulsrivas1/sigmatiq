-- Admin quotas and feature flags tables

CREATE TABLE IF NOT EXISTS admin_quotas (
  user_id TEXT PRIMARY KEY,
  sweeps_per_day INTEGER DEFAULT 10,
  sweeps_concurrent INTEGER DEFAULT 2,
  train_per_day INTEGER DEFAULT 20,
  train_concurrent INTEGER DEFAULT 2,
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feature_flags (
  key TEXT PRIMARY KEY,
  enabled BOOLEAN NOT NULL DEFAULT FALSE,
  updated_at TIMESTAMPTZ DEFAULT now(),
  updated_by TEXT
);

