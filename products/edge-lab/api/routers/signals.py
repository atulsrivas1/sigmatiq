from __future__ import annotations
from typing import Optional, List
from fastapi import APIRouter, Query
import pandas as pd

try:
    from edge_core.registry.signals_registry import fetch_signals as db_fetch_signals
except Exception:
    db_fetch_signals = None

router = APIRouter()


@router.get("/signals")
def list_signals(
    model_id: Optional[str] = Query(None),
    pack_id: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    tickers: Optional[str] = Query(None),  # comma-separated
    limit: int = Query(200),
    offset: int = Query(0),
):
    if db_fetch_signals is None:
        return {"ok": True, "rows": [], "limit": limit, "offset": offset, "warning": "DB not configured; no rows"}
    tickers_list: Optional[List[str]] = None
    if tickers:
        tickers_list = [t.strip().upper() for t in tickers.split(',') if t.strip()]
    rows = db_fetch_signals(
        model_id=model_id,
        pack_id=pack_id,
        date_eq=date,
        start=start,
        end=end,
        tickers=tickers_list,
        limit=limit,
        offset=offset,
    )
    next_offset = int(offset) + len(rows)
    return {"ok": True, "count": len(rows), "rows": rows, "limit": int(limit), "offset": int(offset), "next_offset": next_offset}


@router.get("/signals/summary")
def signals_summary(
    model_id: str = Query(...),
    risk_profile: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
):
    """Live summary over a period (cost-adjusted metrics). Falls back to CSV if DB not configured."""
    try:
        from api.services.signals_live import load_signals_csv, compute_live_metrics
        from pathlib import Path as _Path
        root = _Path(__file__).resolve().parents[2]
        # Prefer DB if available; fallback to CSV
        df = None
        if db_fetch_signals is not None:
            try:
                rows = db_fetch_signals(model_id=model_id, start=start, end=end, limit=100000, offset=0)
                import pandas as _pd
                df = _pd.DataFrame(rows) if rows else None
            except Exception:
                df = None
        if df is None:
            df = load_signals_csv(root, model_id)
        if df is not None and not df.empty and (start or end) and "ts" in df.columns:
            ts = pd.to_datetime(df["ts"], errors="coerce", utc=True)
            if start:
                df = df[ts >= pd.Timestamp(start).tz_localize("UTC")]
            if end:
                df = df[ts <= pd.Timestamp(end).tz_localize("UTC")]
        metrics = compute_live_metrics(df) if df is not None else None
        out = {
            "ok": True,
            "model_id": model_id,
            "risk_profile": risk_profile,
            "period": {"start": start, "end": end},
            "metrics": ({
                "sharpe": getattr(metrics, 'sharpe', None),
                "sortino": getattr(metrics, 'sortino', None),
                "cum_return": getattr(metrics, 'cum_return', None),
                "win_rate": getattr(metrics, 'win_rate', None),
                "trades": getattr(metrics, 'trades', None),
                "fill_rate": getattr(metrics, 'fill_rate', None),
                "avg_slippage": getattr(metrics, 'avg_slippage', None),
                "max_dd": getattr(metrics, 'max_dd', None),
                "coverage_pct": getattr(metrics, 'coverage_pct', None),
                "freshness_sec": getattr(metrics, 'freshness_sec', None),
            } if metrics is not None else None)
        }
        return out
    except Exception as e:
        return {"ok": False, "error": str(e)}


@router.get("/signals/leaderboard")
def signals_leaderboard(
    pack: Optional[str] = Query(None),
    risk_profile: Optional[str] = Query(None),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
    limit: int = Query(50),
    offset: int = Query(0),
):
    """Aggregate live metrics across models. CSV-based fallback when DB is not configured."""
    try:
        from api.services.signals_live import leaderboard_from_csv
        from pathlib import Path as _Path
        root = _Path(__file__).resolve().parents[2]
        # If DB is available, compute over models discovered in packs and aggregate in-memory
        if db_fetch_signals is not None:
            try:
                import os
                import pandas as _pd
                # Discover models
                models: list[str] = []
                packs_dir = root / "packs"
                for pack_dir in packs_dir.iterdir() if packs_dir.exists() else []:
                    if pack and pack_dir.name != pack:
                        continue
                    cfg_dir = pack_dir / "model_configs"
                    for f in cfg_dir.glob("*.yaml") if cfg_dir.exists() else []:
                        models.append(f.stem)
                rows = []
                for mid in models:
                    try:
                        sig = db_fetch_signals(model_id=mid, start=start, end=end, limit=100000, offset=0)
                        df = _pd.DataFrame(sig) if sig else _pd.DataFrame()
                        if df.empty:
                            continue
                        m = compute_live_metrics(df)
                        rows.append({
                            "model_id": mid,
                            "risk_profile": risk_profile or "balanced",
                            "period": {"start": start, "end": end},
                            "metrics": {
                                "sharpe": m.sharpe,
                                "sortino": m.sortino,
                                "cum_return": m.cum_return,
                                "win_rate": m.win_rate,
                                "trades": m.trades,
                                "fill_rate": m.fill_rate,
                                "avg_slippage": m.avg_slippage,
                                "capacity": m.capacity,
                                "coverage_pct": m.coverage_pct,
                                "freshness_sec": m.freshness_sec,
                            },
                            "lineage": {},
                        })
                    except Exception:
                        continue
                total = len(rows)
                rows = rows[int(offset): int(offset)+int(limit)]
                return {"ok": True, "rows": rows, "total": total}
            except Exception:
                pass
        # Fallback to CSV scan
        lb = leaderboard_from_csv(root, pack_filter=pack, risk_profile=risk_profile, start=start, end=end, limit=limit, offset=offset)
        return {"ok": True, **lb}
    except Exception as e:
        return {"ok": False, "rows": [], "total": 0, "error": str(e)}


@router.get("/models/{model_id}/performance")
def model_performance(model_id: str, risk_profile: Optional[str] = Query(None), start: Optional[str] = Query(None), end: Optional[str] = Query(None)):
    """Bundle live metrics (if available) and a lightweight backtest snapshot.
    Backtest snapshot is best-effort (reads leaderboard DB if configured, else omitted).
    """
    try:
        from api.services.signals_live import load_signals_csv, compute_live_metrics
        from pathlib import Path as _Path
        root = _Path(__file__).resolve().parents[2]
        df = load_signals_csv(root, model_id)
        if df is not None and not df.empty and (start or end) and "ts" in df.columns:
            ts = pd.to_datetime(df["ts"], errors="coerce", utc=True)
            if start:
                df = df[ts >= pd.Timestamp(start).tz_localize("UTC")]
            if end:
                df = df[ts <= pd.Timestamp(end).tz_localize("UTC")]
        metrics = compute_live_metrics(df) if df is not None else None
        backtest = None
        # Best-effort: if db_leaderboard exists, fetch latest entry for model
        try:
            from edge_core.registry.backtest_registry import leaderboard as _db_leaderboard
            rows = _db_leaderboard(model_id=model_id, limit=1, offset=0)
            if rows:
                bt = rows[0]
                backtest = {"started_at": bt.get("started_at"), "metrics": bt.get("metrics") or {"best_sharpe_hourly": bt.get("best_sharpe_hourly"), "best_cum_ret": bt.get("best_cum_ret")}}
        except Exception:
            backtest = None
        out = {
            "ok": True,
            "live": {
                "period": {"start": start, "end": end},
                "metrics": ({
                    "sharpe": getattr(metrics, 'sharpe', None),
                    "sortino": getattr(metrics, 'sortino', None),
                    "cum_return": getattr(metrics, 'cum_return', None),
                    "win_rate": getattr(metrics, 'win_rate', None),
                    "trades": getattr(metrics, 'trades', None),
                    "fill_rate": getattr(metrics, 'fill_rate', None),
                    "avg_slippage": getattr(metrics, 'avg_slippage', None),
                    "max_dd": getattr(metrics, 'max_dd', None),
                    "coverage_pct": getattr(metrics, 'coverage_pct', None),
                    "freshness_sec": getattr(metrics, 'freshness_sec', None),
                } if metrics is not None else None)
            },
            "backtest": backtest,
        }
        return out
    except Exception as e:
        return {"ok": False, "error": str(e)}
