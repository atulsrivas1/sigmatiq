from __future__ import annotations
from typing import Optional, Any, Dict, List
from fastapi import APIRouter, Query, Path
from psycopg2.extras import RealDictCursor

from sigma_core.storage.relational import get_db

router = APIRouter()


def _page_limit(limit: int) -> int:
    return max(1, min(int(limit), 500))


@router.get('/build_runs')
def list_build_runs(
    pack_id: Optional[str] = Query(None),
    model_id: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    start: Optional[str] = Query(None),  # ISO timestamp
    end: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    try:
        where = []
        params: List[Any] = []
        if pack_id:
            where.append('pack_id = %s'); params.append(pack_id)
        if model_id:
            where.append('model_id = %s'); params.append(model_id)
        if tag:
            where.append("(params->>'tag' = %s OR %s = %s)")
            params.extend([tag, 1, 0])
        if start:
            where.append('created_at >= %s'); params.append(start)
        if end:
            where.append('created_at <= %s'); params.append(end)
        sql = "SELECT id, pack_id, model_id, started_at, finished_at, params, metrics, out_csv_uri, lineage, created_at FROM build_runs"
        if where:
            sql += ' WHERE ' + ' AND '.join(where)
        sql += ' ORDER BY created_at DESC LIMIT %s OFFSET %s'
        params.extend([_page_limit(limit), int(offset)])
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
        return {'ok': True, 'rows': rows, 'limit': _page_limit(limit), 'offset': int(offset), 'next_offset': int(offset) + len(rows)}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@router.get('/training_runs')
def list_training_runs(
    pack_id: Optional[str] = Query(None),
    model_id: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    try:
        where = []
        params: List[Any] = []
        if pack_id:
            where.append('pack_id = %s'); params.append(pack_id)
        if model_id:
            where.append('model_id = %s'); params.append(model_id)
        if tag:
            where.append("(params->>'tag' = %s OR %s = %s)")
            params.extend([tag, 1, 0])
        if start:
            where.append('created_at >= %s'); params.append(start)
        if end:
            where.append('created_at <= %s'); params.append(end)
        sql = "SELECT id, pack_id, model_id, started_at, finished_at, params, metrics, model_out_uri, features, lineage, created_at FROM training_runs"
        if where:
            sql += ' WHERE ' + ' AND '.join(where)
        sql += ' ORDER BY created_at DESC LIMIT %s OFFSET %s'
        params.extend([_page_limit(limit), int(offset)])
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
        return {'ok': True, 'rows': rows, 'limit': _page_limit(limit), 'offset': int(offset), 'next_offset': int(offset) + len(rows)}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@router.get('/sweeps')
def list_sweeps(
    pack_id: Optional[str] = Query(None),
    model_id: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    try:
        where = []
        params: List[Any] = []
        if pack_id:
            where.append('pack_id = %s'); params.append(pack_id)
        if model_id:
            where.append('model_id = %s'); params.append(model_id)
        if tag:
            where.append('tag = %s'); params.append(tag)
        if status:
            where.append('status = %s'); params.append(status)
        sql = "SELECT id, pack_id, model_id, tag, status, spec, started_at, finished_at, created_at FROM backtest_sweeps"
        if where:
            sql += ' WHERE ' + ' AND '.join(where)
        sql += ' ORDER BY created_at DESC LIMIT %s OFFSET %s'
        params.extend([_page_limit(limit), int(offset)])
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params)
                rows = cur.fetchall()
        return {'ok': True, 'rows': rows, 'limit': _page_limit(limit), 'offset': int(offset), 'next_offset': int(offset) + len(rows)}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@router.get('/sweeps/{sweep_id}')
def get_sweep(
    sweep_id: int = Path(..., ge=1),
):
    try:
        with get_db() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT id, pack_id, model_id, tag, status, spec, started_at, finished_at, created_at FROM backtest_sweeps WHERE id = %s",
                    (int(sweep_id),),
                )
                sweep = cur.fetchone()
                if not sweep:
                    return {'ok': False, 'error': f'not found: {sweep_id}'}
                cur.execute(
                    "SELECT id, kind, params, metrics, csv_uri, backtest_run_id, created_at FROM sweep_results WHERE sweep_id = %s ORDER BY created_at DESC",
                    (int(sweep_id),),
                )
                results = cur.fetchall()
        return {'ok': True, 'sweep': sweep, 'results': results}
    except Exception as e:
        return {'ok': False, 'error': str(e)}

