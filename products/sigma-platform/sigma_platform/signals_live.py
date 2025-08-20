from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict, Any

import math
import pandas as pd


@dataclass
class LiveMetrics:
    sharpe: Optional[float] = None
    sortino: Optional[float] = None
    cum_return: Optional[float] = None
    win_rate: Optional[float] = None
    trades: int = 0
    max_dd: Optional[float] = None
    fill_rate: Optional[float] = None
    avg_slippage: Optional[float] = None
    capacity: Optional[str] = None
    coverage_pct: Optional[float] = None
    freshness_sec: Optional[int] = None


def load_signals_csv(root: Path, model_id: str) -> Optional[pd.DataFrame]:
    csv_path = root / "live_data" / model_id / "signals.csv"
    if not csv_path.exists():
        return None
    try:
        df = pd.read_csv(csv_path)
        df.columns = [c.strip().lower() for c in df.columns]
        if "ts" in df.columns:
            try:
                df["ts"] = pd.to_datetime(df["ts"], errors="coerce", utc=True)
            except Exception:
                pass
        return df
    except Exception:
        return None


def _safe_mean(x: pd.Series) -> Optional[float]:
    if x.empty:
        return None
    v = x.dropna()
    return float(v.mean()) if not v.empty else None


def _compute_sharpe(perf: pd.Series) -> Optional[float]:
    if perf.empty:
        return None
    r = perf.dropna()
    if r.std(ddof=0) == 0 or r.empty:
        return None
    return float(r.mean() / r.std(ddof=0) * math.sqrt(max(1, len(r))))


def _compute_sortino(perf: pd.Series) -> Optional[float]:
    r = perf.dropna()
    dd = r[r < 0]
    if dd.std(ddof=0) == 0 or r.empty:
        return None
    return float(r.mean() / dd.std(ddof=0) * math.sqrt(max(1, len(r))))


def _max_drawdown(equity: pd.Series) -> Optional[float]:
    if equity.empty:
        return None
    roll_max = equity.cummax()
    dd = (equity / roll_max) - 1.0
    try:
        return float(dd.min())
    except Exception:
        return None


def compute_live_metrics(df: pd.DataFrame, *, now_ts: Optional[pd.Timestamp] = None) -> LiveMetrics:
    m = LiveMetrics()
    if df is None or df.empty:
        return m
    dff = df.copy()
    perf = None
    if "pnl" in dff.columns:
        perf = pd.to_numeric(dff["pnl"], errors="coerce")
    elif "rr" in dff.columns:
        perf = pd.to_numeric(dff["rr"], errors="coerce")
    else:
        perf = pd.Series(dtype=float)
    m.trades = int((dff.get("status") == "filled").sum()) if "status" in dff.columns else int(len(dff))
    equity = perf.cumsum() if not perf.empty else pd.Series(dtype=float)
    m.cum_return = float(perf.sum()) if not perf.empty else None
    m.sharpe = _compute_sharpe(perf) if not perf.empty else None
    m.sortino = _compute_sortino(perf) if not perf.empty else None
    m.max_dd = _max_drawdown(equity) if not equity.empty else None
    if "status" in dff.columns:
        st = dff["status"].astype(str).str.lower()
        filled = int((st == "filled").sum())
        considered = int(((st == "filled") | (st == "canceled") | (st == "pending")).sum())
        m.fill_rate = (filled / considered) if considered > 0 else None
    if "slippage" in dff.columns:
        m.avg_slippage = _safe_mean(pd.to_numeric(dff["slippage"], errors="coerce"))
    m.capacity = None
    if "ts" in dff.columns and pd.api.types.is_datetime64_any_dtype(dff["ts"]):
        idx = dff["ts"].sort_values()
        if not idx.empty:
            last_ts = idx.iloc[-1]
            first_ts = idx.iloc[0]
            try:
                uniq_days = idx.dt.date.nunique()
                total_days = max(1, (last_ts.normalize() - first_ts.normalize()).days + 1)
                m.coverage_pct = float(uniq_days) * 100.0 / float(total_days)
            except Exception:
                m.coverage_pct = None
            now_ts = now_ts or (pd.Timestamp.utcnow().tz_localize("UTC") if not pd.Timestamp.utcnow().tzinfo else pd.Timestamp.utcnow())
            m.freshness_sec = int((now_ts - last_ts).total_seconds())
    return m


def leaderboard_from_csv(root: Path, *, pack_filter: Optional[str], risk_profile: Optional[str], start: Optional[str], end: Optional[str], limit: int, offset: int) -> Dict[str, Any]:
    live_dir = root / "live_data"
    rows: List[Dict[str, Any]] = []
    if not live_dir.exists():
        return {"rows": [], "total": 0}

    def _resolve_pack_for_model(mid: str) -> Optional[str]:
        packs_dir = root / "packs"
        if not packs_dir.exists():
            return None
        for pack_dir in packs_dir.iterdir():
            if not pack_dir.is_dir():
                continue
            cfg = pack_dir / "model_configs" / f"{mid}.yaml"
            if cfg.exists():
                return pack_dir.name
        return None

    for model_dir in sorted(live_dir.iterdir()):
        if not model_dir.is_dir():
            continue
        model_id = model_dir.name
        if pack_filter:
            resolved_pack = _resolve_pack_for_model(model_id)
            if resolved_pack != pack_filter:
                continue
        df = load_signals_csv(root, model_id)
        if df is None or df.empty:
            continue
        if start or end:
            if "ts" in df.columns:
                ts = pd.to_datetime(df["ts"], errors="coerce", utc=True)
                if start:
                    ts_start = pd.Timestamp(start).tz_localize("UTC")
                    df = df[ts >= ts_start]
                if end:
                    ts_end = pd.Timestamp(end).tz_localize("UTC")
                    df = df[ts <= ts_end]
        metrics = compute_live_metrics(df)
        rows.append({
            "model_id": model_id,
            "risk_profile": risk_profile or "balanced",
            "period": {"start": start, "end": end},
            "metrics": {
                "sharpe": metrics.sharpe,
                "sortino": metrics.sortino,
                "cum_return": metrics.cum_return,
                "win_rate": metrics.win_rate,
                "trades": metrics.trades,
                "fill_rate": metrics.fill_rate,
                "avg_slippage": metrics.avg_slippage,
                "capacity": metrics.capacity,
                "coverage_pct": metrics.coverage_pct,
                "freshness_sec": metrics.freshness_sec,
            },
            "lineage": {},
        })
    total = len(rows)
    rows = rows[offset: offset + limit]
    return {"rows": rows, "total": total}

