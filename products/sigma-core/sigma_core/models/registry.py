from typing import List, Optional
from psycopg2.extras import RealDictCursor
from sigma_core.registry.artifacts import ModelVersion
from sigma_core.storage.relational import get_db

class ModelRegistry:
    def create_model_version(self, name: str, version: str, description: str, artifact_uri: str, data_hash: str, git_sha: str, metrics: dict) -> ModelVersion:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO model_versions (name, version, description, artifact_uri, data_hash, git_sha, metrics) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id, name, version, description, artifact_uri, data_hash, git_sha, metrics, created_at, updated_at",
                    (name, version, description, artifact_uri, data_hash, git_sha, json.dumps(metrics))
                )
                model_version = ModelVersion(**cur.fetchone())
                conn.commit()
                return model_version

    def get_model_version(self, name: str, version: str) -> Optional[ModelVersion]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, name, version, description, artifact_uri, data_hash, git_sha, metrics, created_at, updated_at FROM model_versions WHERE name = %s AND version = %s",
                    (name, version)
                )
                model_version_data = cur.fetchone()
                if model_version_data:
                    return ModelVersion(**model_version_data)
                return None

    def list_model_versions(self) -> List[ModelVersion]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, name, version, description, artifact_uri, data_hash, git_sha, metrics, created_at, updated_at FROM model_versions ORDER BY name, version")
                return [ModelVersion(**row) for row in cur.fetchall()]

model_registry = ModelRegistry()
