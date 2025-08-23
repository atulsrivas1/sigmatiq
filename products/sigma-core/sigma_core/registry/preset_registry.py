from typing import List, Optional
from psycopg2.extras import RealDictCursor

from sigma_core.storage.relational import get_db


class PresetRegistry:
    """Read-only registry for curated universe presets."""

    def list_presets(self) -> List[dict]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT preset_id, title, description, source, version, symbol_count, symbols_uri, created_at, updated_at
                    FROM sc.universe_presets
                    ORDER BY preset_id
                    """
                )
                return [dict(r) for r in cur.fetchall()]

    def get_preset(self, *, preset_id: str) -> Optional[dict]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT preset_id, title, description, source, version, symbol_count, symbols_uri, created_at, updated_at
                    FROM sc.universe_presets WHERE preset_id = %s
                    """,
                    (preset_id,),
                )
                row = cur.fetchone()
                return dict(row) if row else None

    def list_symbols(self, *, preset_id: str, limit: Optional[int] = None) -> List[str]:
        with get_db() as conn:
            with conn.cursor() as cur:
                sql = "SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol"
                if limit is not None:
                    sql += " LIMIT %s"
                    cur.execute(sql, (preset_id, int(limit)))
                else:
                    cur.execute(sql, (preset_id,))
                return [r[0] for r in cur.fetchall()]

