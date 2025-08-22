from __future__ import annotations
from typing import Optional, Any, Dict
from fastapi import APIRouter, Query
from pydantic import BaseModel

from api.services.store_db import (
    upsert_indicator_set_db,
    get_indicator_set_model_db,
    get_indicator_set_pack_db,
)

router = APIRouter()


class IndicatorSetUpsertDB(BaseModel):
    pack_id: str
    scope: str  # 'pack' | 'model'
    model_id: Optional[str] = None
    name: Optional[str] = None
    data: Dict[str, Any]
    version: Optional[int] = 1


@router.get('/indicator_set')
def get_indicator_set(
    pack_id: str = Query(...),
    model_id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
):
    try:
        if model_id:
            d = get_indicator_set_model_db(pack_id, model_id)
        elif name:
            d = get_indicator_set_pack_db(pack_id, name)
        else:
            return {"ok": False, "error": "provide model_id or name"}
        if d is None:
            return {"ok": False, "error": "not_found"}
        return {"ok": True, "data": d}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@router.put('/indicator_set')
def put_indicator_set(payload: IndicatorSetUpsertDB):
    try:
        res = upsert_indicator_set_db(
            payload.pack_id,
            payload.scope,
            model_id=payload.model_id,
            name=payload.name,
            data=payload.data,
            version=int(payload.version or 1),
        )
        return {"ok": True, **res}
    except Exception as e:
        return {"ok": False, "error": str(e)}

