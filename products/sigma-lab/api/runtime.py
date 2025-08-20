from __future__ import annotations

# Shared runtime state for lightweight diagnostics

# Router load status populated at startup by api.app
ROUTER_STATUS: dict[str, bool] = {}

