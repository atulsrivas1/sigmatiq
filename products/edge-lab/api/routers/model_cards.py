from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Query

from api.services.model_cards import list_model_cards, load_model_card

router = APIRouter()


@router.get('/model_cards')
def list_cards(pack_id: str = Query('zeroedge'), model_id: str = Query(...), limit: int = Query(200), offset: int = Query(0)):
    rows = list_model_cards(pack_id=pack_id, model_id=model_id)
    start = max(0, int(offset)); end = start + int(limit)
    page = rows[start:end]
    return {'ok': True, 'count': len(page), 'cards': page, 'limit': int(limit), 'offset': start, 'next_offset': start + len(page)}


@router.get('/model_card')
def get_card(pack_id: str = Query('zeroedge'), model_id: str = Query(...), file: Optional[str] = Query(None)):
    try:
        data = load_model_card(pack_id=pack_id, model_id=model_id, file=file)
        return {'ok': True, **data}
    except Exception as e:
        return {'ok': False, 'error': str(e)}
