from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Query, Depends
from api.services.auth import require_admin

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


def _forbidden():
    # Placeholder payload until specific admin operations are implemented
    return {"ok": False, "error": "Not implemented", "code": "NOT_IMPLEMENTED"}


@router.get("/jobs")
def admin_jobs(status: Optional[str] = Query(None), limit: int = Query(50), offset: int = Query(0)):
    return _forbidden()


@router.post("/jobs/{job_id}/retry")
def admin_jobs_retry(job_id: str):
    return _forbidden()


@router.post("/jobs/{job_id}/cancel")
def admin_jobs_cancel(job_id: str):
    return _forbidden()


@router.get("/quotas")
def admin_quotas(user: Optional[str] = Query(None)):
    return _forbidden()


@router.patch("/quotas")
def admin_quotas_update():
    return _forbidden()


@router.get("/risk-profiles")
def admin_risk_profiles():
    return _forbidden()


@router.patch("/risk-profiles")
def admin_risk_profiles_update():
    return _forbidden()


@router.get("/packs")
def admin_packs():
    return _forbidden()


@router.get("/indicator_sets")
def admin_indicator_sets(pack: Optional[str] = Query(None)):
    return _forbidden()


@router.get("/templates")
def admin_templates():
    return _forbidden()


@router.post("/templates")
def admin_templates_create():
    return _forbidden()


@router.patch("/templates/{template_id}")
def admin_templates_update(template_id: str):
    return _forbidden()


@router.post("/templates/{template_id}/publish")
def admin_templates_publish(template_id: str):
    return _forbidden()


@router.get("/flags")
def admin_flags():
    return _forbidden()


@router.patch("/flags")
def admin_flags_update():
    return _forbidden()


@router.get("/health")
def admin_health():
    return _forbidden()


@router.get("/audit")
def admin_audit(user: Optional[str] = Query(None), action: Optional[str] = Query(None), limit: int = Query(50), offset: int = Query(0)):
    return _forbidden()


@router.get("/users")
def admin_users():
    return _forbidden()


@router.patch("/users/{user_id}")
def admin_users_update(user_id: str):
    return _forbidden()


@router.post("/users/{user_id}/rotate_token")
def admin_users_rotate(user_id: str):
    return _forbidden()
