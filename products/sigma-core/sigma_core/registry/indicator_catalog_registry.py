from typing import List, Optional, Sequence
from psycopg2.extras import RealDictCursor

from sigma_core.storage.relational import get_db
from sigma_core.registry.artifacts import IndicatorCatalogEntry


class IndicatorCatalogRegistry:
    """DB-backed read registry for sc.indicators catalog entries."""

    def list_indicators(self, *, status: str = 'published', latest: bool = True) -> List[IndicatorCatalogEntry]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if latest and status == 'published':
                    cur.execute(
                        """
                        SELECT DISTINCT ON (id) id, version, status, title, category, subcategory, created_at, updated_at
                        FROM sc.indicators WHERE status = 'published'
                        ORDER BY id, version DESC
                        """
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, version, status, title, category, subcategory, created_at, updated_at
                        FROM sc.indicators
                        WHERE (%s IS NULL OR status = %s)
                        ORDER BY id, version DESC
                        """,
                        (status, status),
                    )
                return [IndicatorCatalogEntry(**row) for row in cur.fetchall()]

    def get_indicator(self, *, id: str, version: Optional[int] = None) -> Optional[IndicatorCatalogEntry]:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if version is None:
                    cur.execute(
                        """
                        SELECT id, version, status, title, category, subcategory, created_at, updated_at
                        FROM sc.indicators
                        WHERE id = %s
                        ORDER BY version DESC
                        LIMIT 1
                        """,
                        (id,),
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, version, status, title, category, subcategory, created_at, updated_at
                        FROM sc.indicators
                        WHERE id = %s AND version = %s
                        """,
                        (id, int(version)),
                    )
                row = cur.fetchone()
                return IndicatorCatalogEntry(**row) if row else None

    def search(
        self,
        *,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        tags_any: Optional[Sequence[str]] = None,
        text: Optional[str] = None,
        status: str = 'published',
    ) -> List[IndicatorCatalogEntry]:
        where = ["1=1"]
        params: List[object] = []
        if status:
            where.append("status = %s"); params.append(status)
        if category:
            where.append("category = %s"); params.append(category)
        if subcategory:
            where.append("subcategory = %s"); params.append(subcategory)
        if tags_any:
            where.append("tags && %s::text[]"); params.append(list(tags_any))
        if text:
            where.append("(id ILIKE %s OR title ILIKE %s)"); params.extend([f"%{text}%", f"%{text}%"])
        sql = f"SELECT id, version, status, title, category, subcategory, created_at, updated_at FROM sc.indicators WHERE {' AND '.join(where)} ORDER BY id, version DESC"
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                return [IndicatorCatalogEntry(**row) for row in cur.fetchall()]
