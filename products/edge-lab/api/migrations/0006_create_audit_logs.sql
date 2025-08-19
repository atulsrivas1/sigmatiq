-- Audit logs for governance and traceability

CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGSERIAL PRIMARY KEY,
  at TIMESTAMPTZ DEFAULT now(),
  path TEXT NOT NULL,
  method TEXT,
  status INTEGER,
  user_id TEXT,
  client TEXT,
  pack_id TEXT,
  model_id TEXT,
  lineage JSONB,
  payload JSONB
);

CREATE INDEX IF NOT EXISTS idx_audit_at ON audit_logs (at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_path_at ON audit_logs (path, at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_model_at ON audit_logs (model_id, at DESC);

