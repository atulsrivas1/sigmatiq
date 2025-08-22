from __future__ import annotations
from typing import Optional, Any, Dict
from fastapi import APIRouter, Query
from pydantic import BaseModel

from api.services.store_db import get_model_config_db, upsert_model_config_db

router = APIRouter()


class ModelConfigUpsert(BaseModel):
    pack_id: str
    model_id: str
    config: Dict[str, Any]


@router.get('/model_config')
def get_model_config(model_id: str = Query(...), pack_id: str = Query('zerosigma')):
    try:
        cfg = get_model_config_db(pack_id, model_id)
        if cfg is None:
            return {"ok": False, "error": "not_found"}
        return {"ok": True, "config": cfg}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@router.put('/model_config')
def put_model_config(payload: ModelConfigUpsert):
    try:
        upsert_model_config_db(payload.pack_id, payload.model_id, payload.config)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

