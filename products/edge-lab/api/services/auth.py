from __future__ import annotations
import os
from fastapi import Request, HTTPException


def require_admin(request: Request) -> None:
    """Simple RBAC: require ADMIN_TOKEN env match via header or bearer token.

    Accepted:
    - Header: X-Admin-Token: <token>
    - Authorization: Bearer <token>
    """
    admin_token = os.environ.get("ADMIN_TOKEN")
    if not admin_token:
        # Admin disabled if token not set; deny by default
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "admin disabled"})

    # Check headers
    hdr = request.headers.get("x-admin-token")
    if hdr and hdr == admin_token:
        return None

    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
        if token == admin_token:
            return None

    # If header missing, return 401; if provided and wrong, return 403
    if not hdr and not auth:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "missing admin token"})
    raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "invalid admin token"})

