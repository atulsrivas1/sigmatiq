from __future__ import annotations
from typing import Any, Dict, List, Optional

try:
    from sigma_core.storage.relational import get_db
except Exception:
    get_db = None  # type: ignore


def log_audit(
    *,
    path: str,
    method: str,
    status: int,
    user_id: Optional[str] = None,
    client: Optional[str] = None,
    pack_id: Optional[str] = None,
    model_id: Optional[str] = None,
    lineage: Optional[Dict[str, Any]] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> None:
    if get_db is None:
        return
    try:
        with get_db() as conn:  # type: ignore
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO audit_logs (path, method, status, user_id, client, pack_id, model_id, lineage, payload)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        path,
                        method,
                        int(status),
                        user_id,
                        client,
                        pack_id,
                        model_id,
                        lineage,
                        payload,
                    ),
                )
                conn.commit()
    except Exception:
        return


def fetch_audit(
    *,
    path: Optional[str] = None,
    method: Optional[str] = None,
    status: Optional[int] = None,
    pack_id: Optional[str] = None,
    model_id: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    if get_db is None:
        return []
    where = []
    params: List[Any] = []
    if path:
        where.append("path = %s"); params.append(path)
    if method:
        where.append("method = %s"); params.append(method)
    if status is not None:
        where.append("status = %s"); params.append(int(status))
    if pack_id:
        where.append("pack_id = %s"); params.append(pack_id)
    if model_id:
        where.append("model_id = %s"); params.append(model_id)
    if start:
        where.append("at >= %s"); params.append(start)
    if end:
        where.append("at <= %s"); params.append(end)
    sql = "SELECT id, at, path, method, status, user_id, client, pack_id, model_id, lineage, payload FROM audit_logs"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY at DESC LIMIT %s OFFSET %s"
    params.append(int(limit))
    params.append(int(max(0, offset)))
    from psycopg2.extras import RealDictCursor  # type: ignore
    with get_db() as conn:  # type: ignore
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            return [dict(r) for r in rows]

