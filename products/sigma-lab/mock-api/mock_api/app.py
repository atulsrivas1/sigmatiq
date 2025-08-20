from __future__ import annotations
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from datetime import datetime

app = FastAPI(title="Sigmatiq Sigma Mock API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {
        "name": "Sigmatiq Sigma Mock API",
        "ok": True,
        "endpoints": [
            "/health", "/models", "/model_detail",
            "/indicator_sets", "/leaderboard", "/signals", "/option_signals",
            "/policy/explain", "/calibrate_thresholds",
            "/scan", "/build_matrix", "/preview_matrix", "/train", "/backtest",
        ],
    }


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "sigma-mock",
        "version": "0.1.0",
        "now": datetime.utcnow().isoformat() + "Z",
        "deps": {"fastapi": "ok", "db": "mock"},
    }


@app.get("/models")
def models():
    return {
        "models": [
            {"id": "spy_opt_0dte_hourly", "config": {"model_id": "spy_opt_0dte_hourly", "ticker": "SPY", "algo": "xgb", "pack": "zerosigma"}},
            {"id": "spy_eq_swing_daily", "config": {"model_id": "spy_eq_swing_daily", "ticker": "SPY", "algo": "xgb", "pack": "swingsigma"}},
        ]
    }


@app.get("/model_detail")
def model_detail(model_id: str = Query(...), pack_id: str = Query("zerosigma")):
    return {
        "ok": True,
        "model_id": model_id,
        "pack_id": pack_id,
        "config": {"model_id": model_id, "ticker": "SPY", "algo": "xgb"},
        "policy_valid": True,
        "policy_source": "model",
        "execution_effective": {"slippage_bps": 1.0, "size_by_conf": False, "conf_cap": 1.0},
        "policy_errors": [],
    }


@app.get("/indicator_sets")
def indicator_sets():
    return {
        "ok": True,
        "groups": [
            {"group": "trend", "indicators": ["ema_20", "ema_50", "adx_14", "lr_r2_20"]},
            {"group": "momentum", "indicators": ["momentum_20", "momentum_63", "rsi_14"]},
            {"group": "volatility", "indicators": ["atr_14", "roll_std_20"]},
        ],
    }


@app.get("/leaderboard")
def leaderboard(
    model_id: Optional[str] = Query(None),
    pack_id: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    risk_profile: Optional[str] = Query(None),
    pass_gate: bool = Query(False),
    limit: int = Query(5),
    offset: int = Query(0),
):
    base_rows = [
        {
            "started_at": "2025-08-16T11:50:00Z",
            "model_id": "spy_opt_0dte_hourly",
            "pack_id": "zerosigma",
            "sharpe": 2.1,
            "trades": 120,
            "win_rate": 0.58,
            "max_drawdown": -0.12,
            "cum_ret": 0.22,
            "gate": {"pass": True, "reasons": []},
            "tag": "demo",
            "lineage": {"matrix_sha": "c7d8e9a", "policy_sha": "e5f6abc", "config_sha": "a1b2c3d", "risk_profile": risk_profile or "Balanced"},
        },
        {
            "started_at": "2025-08-15T16:10:00Z",
            "model_id": "spy_eq_swing_daily",
            "pack_id": "swingsigma",
            "sharpe": 1.4,
            "trades": 80,
            "win_rate": 0.55,
            "max_drawdown": -0.08,
            "cum_ret": 0.12,
            "gate": {"pass": False, "reasons": ["min_trades_not_met"]},
            "tag": "smoke",
            "lineage": {"matrix_sha": "d4e5f6b", "policy_sha": "aa11bb2", "config_sha": "cc33dd4", "risk_profile": risk_profile or "Balanced"},
        },
        {
            "started_at": "2025-08-14T10:20:00Z",
            "model_id": "aapl_eq_intraday_hourly",
            "pack_id": "swingsigma",
            "sharpe": 1.1,
            "trades": 65,
            "win_rate": 0.52,
            "max_drawdown": -0.10,
            "cum_ret": 0.09,
            "gate": {"pass": True, "reasons": []},
            "tag": "demo",
            "lineage": {"matrix_sha": "1122abc", "policy_sha": "3344def", "config_sha": "5566fed", "risk_profile": risk_profile or "Balanced"},
        },
    ]
    # Apply simple filters (mock behavior)
    rows = [r for r in base_rows if (not model_id or r["model_id"] == model_id) and (not pack_id or r["pack_id"] == pack_id) and (not tag or r.get("tag") == tag)]
    if pass_gate:
        rows = [r for r in rows if r.get("gate", {}).get("pass")]
    return {"ok": True, "rows": rows[offset:offset+limit], "limit": limit, "offset": offset, "next_offset": offset+limit}


@app.get("/signals")
def signals(limit: int = Query(20), offset: int = Query(0)):
    rows = [
        {"ts": "2025-08-19T15:30:00Z", "ticker": "SPY", "side": "Long", "model_id": "spy_opt_0dte_hourly", "conf": 0.78, "pack_id": "zerosigma"},
        {"ts": "2025-08-19T15:31:00Z", "ticker": "AAPL", "side": "Short", "model_id": "spy_eq_swing_daily", "conf": 0.61, "pack_id": "swingsigma"},
    ]
    return {"ok": True, "rows": rows[offset:offset+limit], "limit": limit, "offset": offset, "next_offset": offset+limit}


@app.get("/option_signals")
def option_signals(limit: int = Query(20), offset: int = Query(0)):
    rows = [
        {"ts": "2025-08-19T15:30:00Z", "ticker": "SPY", "symbol": "SPY250819C00500000", "side": "BuyCall", "conf": 0.72, "pack_id": "zerosigma"},
        {"ts": "2025-08-19T15:45:00Z", "ticker": "TSLA", "symbol": "TSLA250819P00200000", "side": "BuyPut", "conf": 0.66, "pack_id": "zerosigma"},
    ]
    return {"ok": True, "rows": rows[offset:offset+limit], "limit": limit, "offset": offset, "next_offset": offset+limit}


@app.get("/policy/explain")
def policy_explain(model_id: str = Query(...), pack_id: str = Query("zerosigma")):
    return {
        "ok": True,
        "schema_ok": True,
        "schema_errors": [],
        "execution_effective": {"slippage_bps": 1.0, "size_by_conf": False, "conf_cap": 1.0,
                                  "brackets": {"enabled": True, "atr_mult_stop": 1.2, "atr_mult_target": 2.0, "time_stop_minutes": 120}},
        "checks": {"risk": {"max_drawdown": {"ok": True}}, "lint": []},
    }


class CalibrateThresholdsRequest(BaseModel):
    model_id: str
    csv: Optional[str] = None
    pack_id: Optional[str] = None
    metric: Optional[str] = 'sharpe'
    column: Optional[str] = 'score_total'
    grid: Optional[str] = '0.50,0.55,0.60,0.65,0.70'
    top_n: Optional[int] = 50


@app.post("/calibrate_thresholds")
def calibrate_thresholds_ep(payload: CalibrateThresholdsRequest):
    grid_vals = [float(x) for x in (payload.grid or '0.50,0.55,0.60').split(',')]
    counts = [{"threshold": t, "count": 50 - int(abs(0.6 - t) * 100)} for t in grid_vals]
    rec = max(counts, key=lambda r: r["count"]) if counts else {"threshold": 0.6, "count": 40}
    return {
        "ok": True,
        "model_id": payload.model_id,
        "source_csv": payload.csv or "mock://matrix.csv",
        "column": payload.column or "score_total",
        "top_n": payload.top_n or 50,
        "grid": grid_vals,
        "counts": counts,
        "recommended_threshold": rec["threshold"],
        "expected_count": rec["count"],
    }


class ScanRequest(BaseModel):
    pack_id: Optional[str] = 'swingsigma'
    model_id: Optional[str] = 'universe_eq_swing_daily_scanner'
    indicator_set: Optional[str] = 'swing_eq_breakout_scanner'
    start: str
    end: str
    tickers: Optional[str] = None
    universe_csv: Optional[str] = None
    universe_col: Optional[str] = 'ticker'
    top_n: Optional[int] = 50


@app.post("/scan")
def scan_ep(payload: ScanRequest):
    rows = [
        {"ticker": "AAPL", "score_total": 0.82, "bos_derived": 0.6, "score_breakout": 0.9, "score_momentum": 0.7, "score_alignment": 0.8},
        {"ticker": "MSFT", "score_total": 0.76, "bos_derived": 0.5, "score_breakout": 0.8, "score_momentum": 0.6, "score_alignment": 0.7},
    ]
    return {"ok": True, "rows": rows, "top_n": payload.top_n or 50}


@app.post("/build_matrix")
def build_matrix(model_id: str = Body(..., embed=True), pack_id: str = Body("zerosigma", embed=True), start: str = Body(...), end: str = Body(...)):
    # Provide additional fields used by UI
    return {
        "ok": True,
        "model_id": model_id,
        "pack_id": pack_id,
        "path": f"mock://matrices/{model_id}/training_matrix_built.csv",
        "rows": 12345,
        "matrix_sha": "c7d8e9a",
        "profile": {
            "features": 128,
            "rows": 12345,
            "label_balance": {"pos": 0.48, "neg": 0.52},
            "nan_pct": 0.012
        }
    }


@app.post("/preview_matrix")
def preview_matrix(model_id: str = Body(..., embed=True), pack_id: str = Body("zerosigma", embed=True), start: str = Body(...), end: str = Body(...)):
    return {
        "ok": True, "model_id": model_id, "pack_id": pack_id,
        "nan_stats": [{"column": "close", "nan_pct": 0.0}, {"column": "ema_20", "nan_pct": 1.23}],
        "columns": ["date","close","ema_20","rsi_14"],
        "rows": 200,
    }


@app.post("/train")
def train(model_id: str = Body(..., embed=True), pack_id: str = Body("zerosigma", embed=True), csv: str = Body(None), calibration: str = Body("sigmoid")):
    return {"ok": True, "model_out": f"mock://artifacts/{model_id}/gbm.pkl", "rows": 9876, "calibration": calibration}


@app.post("/backtest")
def backtest(model_id: str = Body(..., embed=True), pack_id: str = Body("zerosigma", embed=True)):
    return {
        "ok": True,
        "model_id": model_id,
        "pack_id": pack_id,
        "summary": {"sharpe": 1.92, "trades": 234, "win_rate": 0.57, "max_dd": -0.12},
        "artifacts": {"report_csv": f"mock://reports/{model_id}_bt.csv", "plots": [f"mock://plots/{model_id}_eq_curve.png"]},
    }


class CreateModelRequest(BaseModel):
    template_id: str
    name: str
    risk_profile: Optional[str] = "Balanced"


@app.post("/models")
def create_model(payload: CreateModelRequest):
    # Minimal success response with new model_id
    return {
        "ok": True,
        "model_id": payload.name,
        "template_id": payload.template_id,
        "risk_profile": payload.risk_profile or "Balanced",
    }


class BacktestSweepSpec(BaseModel):
    thresholds_variants: Optional[List[List[float]]] = None
    hours_variants: Optional[List[List[int]]] = None
    top_pct_variants: Optional[List[List[float]]] = None


class BacktestSweepBody(BaseModel):
    model_id: str
    risk_profile: Optional[str] = "Balanced"
    sweep: BacktestSweepSpec
    tag: Optional[str] = None


@app.post("/backtest_sweep")
def backtest_sweep(payload: BacktestSweepBody):
    rows: List[Dict[str, Any]] = []
    tag = payload.tag or "demo"
    # Build a few mock combinations from provided variants or fallbacks
    thr_sets = payload.sweep.thresholds_variants or [[0.50, 0.55, 0.60]]
    hr_sets = payload.sweep.hours_variants or [[13, 14], [13, 14, 15]]
    top_sets = payload.sweep.top_pct_variants or [[0.10, 0.15]]

    # thresholds-based rows
    for hs in hr_sets:
        for t in thr_sets[0][:2]:
            rows.append({
                "kind": "thr",
                "value": t,
                "allowed_hours": hs,
                "sharpe": round(0.3 + (t - 0.5) * 1.2, 2),
                "cum_ret": 1.0 + round((t - 0.5) * 0.2, 4),
                "trades": 50 + int((t - 0.5) * 100),
                "gate": {"pass": True if t >= 0.55 else False, "reasons": [] if t >= 0.55 else ["min_trades_not_met"]},
                "parity": "ok",
                "capacity": "medium" if len(hs) == 3 else "high",
                "tag": tag,
                "lineage": {"matrix_sha": "c7d8e9a", "policy_sha": "e5f6abc", "config_sha": "a1b2c3d", "risk_profile": payload.risk_profile},
                "csv": f"mock://reports/{payload.model_id}_thr_{t:.2f}_hours_{'-'.join(map(str,hs))}.csv",
            })

    # top_pct-based rows
    for tp in top_sets[0][:2]:
        hs = hr_sets[0]
        rows.append({
            "kind": "top_pct",
            "value": tp,
            "allowed_hours": hs,
            "sharpe": 0.41,
            "cum_ret": 0.9999,
            "trades": 60,
            "gate": {"pass": False, "reasons": ["min_trades_not_met"]},
            "parity": "—",
            "capacity": "high",
            "tag": tag,
            "lineage": {"matrix_sha": "c7d8e9a", "policy_sha": "e5f6abc", "config_sha": "a1b2c3d", "risk_profile": payload.risk_profile},
            "csv": f"mock://reports/{payload.model_id}_top_{tp:.2f}_hours_{'-'.join(map(str,hs))}.csv",
        })

    return {"ok": True, "rows": rows}

