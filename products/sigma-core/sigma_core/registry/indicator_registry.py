from typing import List, Optional
from psycopg2.extras import RealDictCursor
from sigma_core.registry.artifacts import IndicatorSetVersion, IndicatorSpec
from sigma_core.storage.relational import get_db

class IndicatorRegistry:
    def create_indicator_set(self, name: str, version: str, description: str, indicators: List[dict]) -> IndicatorSetVersion:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "INSERT INTO indicator_sets (name, version, description) VALUES (%s, %s, %s) RETURNING id, name, version, description, created_at, updated_at",
                    (name, version, description)
                )
                indicator_set = IndicatorSetVersion(**cur.fetchone())
                
                for ind_spec in indicators:
                    cur.execute(
                        "INSERT INTO indicators (indicator_set_id, name, version, params) VALUES (%s, %s, %s, %s) RETURNING id, indicator_set_id, name, version, params, created_at, updated_at",
                        (indicator_set.id, ind_spec['name'], ind_spec['version'], ind_spec['params'])
                    )
                conn.commit()
                return indicator_set

    def get_indicator_set(self, name: str, version: str) -> Optional[IndicatorSetVersion]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, name, version, description, created_at, updated_at FROM indicator_sets WHERE name = %s AND version = %s",
                    (name, version)
                )
                indicator_set_data = cur.fetchone()
                if indicator_set_data:
                    return IndicatorSetVersion(**indicator_set_data)
                return None

    def list_indicator_sets(self) -> List[IndicatorSetVersion]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT id, name, version, description, created_at, updated_at FROM indicator_sets ORDER BY name, version")
                return [IndicatorSetVersion(**row) for row in cur.fetchall()]

    def get_indicators_by_set_id(self, indicator_set_id: int) -> List[IndicatorSpec]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, indicator_set_id, name, version, params, created_at, updated_at FROM indicators WHERE indicator_set_id = %s ORDER BY name",
                    (indicator_set_id,)
                )
                return [IndicatorSpec(**row) for row in cur.fetchall()]

indicator_registry = IndicatorRegistry()
