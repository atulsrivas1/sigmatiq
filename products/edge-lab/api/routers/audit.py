from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Query

try:
    from api.services.audit import fetch_audit as _fetch_audit
except Exception:
    _fetch_audit = None

router = APIRouter()


@router.get('/audit')
def audit_list(
    path: Optional[str] = Query(None),
    method: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    pack_id: Optional[str] = Query(None),
    model_id: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    limit: int = Query(100),
    offset: int = Query(0),
):
    if _fetch_audit is None:
        return {'ok': True, 'rows': [], 'count': 0, 'limit': int(limit), 'offset': int(offset), 'next_offset': int(offset), 'warning': 'DB not configured'}
    try:
        rows = _fetch_audit(
            path=path,
            method=method,
            status=status,
            pack_id=pack_id,
            model_id=model_id,
            start=start,
            end=end,
            limit=int(limit),
            offset=int(offset),
        )
        return {'ok': True, 'rows': rows, 'count': len(rows), 'limit': int(limit), 'offset': int(offset), 'next_offset': int(offset) + len(rows)}
    except Exception as e:
        msg = str(e)
        if 'Database env vars missing' in msg or 'psycopg2' in msg:
            return {'ok': True, 'rows': [], 'count': 0, 'limit': int(limit), 'offset': int(offset), 'next_offset': int(offset), 'warning': msg}
        return {'ok': False, 'error': msg}
