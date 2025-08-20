from __future__ import annotations
from typing import Any, Dict
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
import os

from sigma_core.storage.relational import get_db
from sigma_core.indicators.registry import registry as indicator_registry
from sigma_core.indicators.registry import get_load_errors as _get_indicator_load_errors
from api.runtime import ROUTER_STATUS
from sigma_core.services.model_cards import list_model_cards
from sigma_core.services.io import workspace_paths
from sigma_core.data.sources.polygon import (
    get_polygon_hourly_bars,
    get_polygon_daily_bars,
    get_polygon_option_chain_snapshot,
)

router = APIRouter()


@router.get("/health")
def health():
    return {"ok": True}


@router.get("/healthz")
def healthz(ticker: str = Query("SPY"), pack_id: str = Query("zerosigma"), model_id: str | None = Query(None)):
    errors: Dict[str, str] = {}
    checks: Dict[str, Any] = {}
    # Routers + indicators quick status
    try:
        checks["routers"] = {k: bool(v) for k, v in ROUTER_STATUS.items()}
    except Exception:
        checks["routers"] = {}
    try:
        checks["indicators_count"] = int(len(indicator_registry.indicators))
        errs = _get_indicator_load_errors()
        if errs:
            errors["indicators_load"] = f"{len(errs)} load errors"
    except Exception:
        pass
    poly = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    checks["polygon_api_key"] = bool(poly)
    today = datetime.now().date()
    start = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")
    try:
        df_d = get_polygon_daily_bars(ticker, start, end)
        checks["daily_bars_rows"] = int(len(df_d))
    except Exception as e:
        errors["daily_bars"] = str(e)
    try:
        df_h = get_polygon_hourly_bars(ticker, start, end)
        checks["hourly_bars_rows"] = int(len(df_h))
    except Exception as e:
        errors["hourly_bars"] = str(e)
    try:
        snap = get_polygon_option_chain_snapshot(ticker, today)
        checks["snapshot_rows"] = int(len(snap))
        checks["snapshot_has_iv"] = bool(("implied_volatility" in snap.columns) and snap["implied_volatility"].notna().any())
    except Exception as e:
        errors["snapshot"] = str(e)
    ok = checks.get("polygon_api_key") and ("daily_bars_rows" in checks) and ("hourly_bars_rows" in checks)
    try:
        with get_db() as conn:  # type: ignore
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                checks["db_ok"] = True
    except Exception as e:
        errors["db"] = str(e)
        checks["db_ok"] = False
    # Coverage hints (optional model awareness)
    try:
        if model_id:
            cards = list_model_cards(pack_id=pack_id, model_id=model_id)
            checks["model_cards_count"] = len(cards)
            live_csv = workspace_paths(model_id, pack_id)["live"] / "signals.csv"
            checks["signals_csv_exists"] = live_csv.exists()
    except Exception as e:
        errors["coverage"] = str(e)
    return {"ok": bool(ok and checks.get("db_ok", False)), "checks": checks, "errors": errors}
