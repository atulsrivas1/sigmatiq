from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Query

from sigma_core.registry.backtest_registry import leaderboard as db_leaderboard

router = APIRouter()


@router.get('/leaderboard')
def leaderboard_api(
    pack_id: Optional[str] = Query(None),
    model_id: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=500),
    offset: int = Query(0, ge=0),
    order_by: str = Query('sharpe'),  # 'sharpe' | 'cum_ret'
):
    try:
        ob = 'sharpe_hourly' if str(order_by) not in ('cum_ret',) else 'cum_ret'
        rows = db_leaderboard(pack_id=pack_id, model_id=model_id, limit=int(limit), offset=int(offset), order_by=ob)
        return {
            'ok': True,
            'rows': rows,
            'limit': int(limit),
            'offset': int(offset),
            'next_offset': int(offset) + len(rows),
            'order_by': ob,
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}

