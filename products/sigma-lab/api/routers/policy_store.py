from __future__ import annotations
from typing import Optional, Any, Dict
from fastapi import APIRouter, Query
from pydantic import BaseModel

from api.services.store_db import get_policy_db, upsert_policy_db

router = APIRouter()


class PolicyUpsert(BaseModel):
    model_id: str
    pack_id: Optional[str] = 'zerosigma'
    policy: Dict[str, Any]
    bump_version: Optional[bool] = True


@router.get('/policy')
def get_policy(model_id: str = Query(...), pack_id: str = Query('zerosigma')):
    try:
        pol = get_policy_db(pack_id, model_id)
        if pol is None:
            return {"ok": False, "error": "not_found"}
        return {"ok": True, "policy": pol}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@router.put('/policy')
def put_policy(payload: PolicyUpsert):
    try:
        res = upsert_policy_db(payload.pack_id or 'zerosigma', payload.model_id, payload.policy, bool(payload.bump_version))
        return {"ok": True, **res}
    except Exception as e:
        return {"ok": False, "error": str(e)}

