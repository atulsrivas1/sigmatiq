import json
import sys as _sys
import os as _os
from pathlib import Path as _Path
# Ensure shared core (parent repo) is importable for data/backtest/train modules
_WS_ROOT = _Path(__file__).resolve().parent.parent
_PARENT = _WS_ROOT.parent
_CORE_ENV = _os.environ.get("ZE_CORE_PATH")
if _CORE_ENV and _CORE_ENV not in _sys.path:
    _sys.path.insert(0, _CORE_ENV)
# Also attempt to add sibling sigma-core if present (monorepo layout)
try:
    _SIGMA_CORE_DIR = _PARENT / 'sigma-core'
    if _SIGMA_CORE_DIR.exists() and str(_SIGMA_CORE_DIR) not in _sys.path:
        _sys.path.insert(0, str(_SIGMA_CORE_DIR))
except Exception:
    pass
if str(_PARENT) not in _sys.path:
    _sys.path.insert(0, str(_PARENT))
if str(_WS_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_WS_ROOT))

# Load .env early so env vars (e.g., POLYGON_API_KEY) are available
try:
    from dotenv import load_dotenv as _load_dotenv
    _load_dotenv(dotenv_path=_WS_ROOT/".env")
except Exception:
    pass
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import shutil

import pandas as pd
import joblib
import yaml
from fastapi import FastAPI, Request, Body, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time as _time

from sigma_core.data.datasets import build_matrix as build_matrix_range
from sigma_core.data.stocks import build_stock_matrix as build_stock_matrix_range
from sigma_core.backtest.engine import run_backtest
from sigma_core.features.builder import select_features as select_features_train
from sigma_core.cv.splits import PurgedEmbargoedWalkForwardSplit
from sigma_core.data.sources.polygon import (
    get_polygon_hourly_bars,
    get_polygon_daily_bars,
    get_polygon_option_chain_snapshot,
)
from sigma_core.indicators.registry import registry as indicator_registry
from sigma_core.registry.backtest_registry import create_backtest_run, leaderboard as db_leaderboard, create_backtest_folds
try:
    from sigma_core.registry.signals_registry import upsert_signals as db_upsert_signals
except Exception:
    db_upsert_signals = None  # optional
from sigma_core.storage.relational import get_db
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import numpy as np
import requests as _requests
import csv as _csv
import uuid as _uuid
import numpy as _np
try:
    from api.services.brackets import apply_stock_brackets
except Exception:
    apply_stock_brackets = None
try:
    from api.services.lineage import compute_lineage as _compute_lineage
except Exception:
    _compute_lineage = None
try:
    from api.services.policy import validate_policy_file as _validate_policy_file
except Exception:
    _validate_policy_file = None


# Workspace is the repository root (Sigmatiq-Sigma)
ROOT_DIR = _Path(__file__).resolve().parent.parent
WS_DIR = ROOT_DIR

app = FastAPI(title="Sigmatiq Sigma API")

# Routers (modular endpoints)
import importlib as _importlib
import logging as _logging
from api import runtime as _runtime

def _include_router(mod_path: str) -> None:
    try:
        mod = _importlib.import_module(mod_path)
        r = getattr(mod, 'router', None)
        if r is not None:
            app.include_router(r)
            _runtime.ROUTER_STATUS[mod_path] = True
        else:
            _runtime.ROUTER_STATUS[mod_path] = False
    except Exception:
        _logging.getLogger(__name__).warning("failed to include router: %s", mod_path)
        _runtime.ROUTER_STATUS[mod_path] = False

_include_router('api.routers.signals')
_include_router('api.routers.health')
_include_router('api.routers.indicators')
_include_router('api.routers.calibration')
_include_router('api.routers.policy')
_include_router('api.routers.training')
_include_router('api.routers.models')
_include_router('api.routers.model_cards')
_include_router('api.routers.audit')
_include_router('api.routers.options')
_include_router('api.routers.backtest')
_include_router('api.routers.datasets')
_include_router('api.routers.sweep')
_include_router('api.routers.admin')
_include_router('api.routers.packs')

# Lightweight audit middleware (DB optional). Logs POST requests to key endpoints.
try:
    from api.services.audit import log_audit as _log_audit
except Exception:
    _log_audit = None

@app.middleware("http")
async def audit_mw(request, call_next):
    # basic request logging with duration
    _t0 = _time.time()
    response = await call_next(request)
    try:
        dur_ms = int((_time.time() - _t0) * 1000)
        _logging.getLogger(__name__).info("%s %s -> %s (%dms)", request.method, request.url.path, getattr(response, 'status_code', '?'), dur_ms)
    except Exception:
        pass
    try:
        if _log_audit is not None and request.method in {"POST"}:
            path = str(request.url.path)
            # Only log key mutating routes
            if path in {"/scan","/options_overlay","/build_matrix","/train","/backtest"}:
                try:
                    body = await request.body()
                    payload = None
                    if body:
                        import json as _json
                        try:
                            payload = _json.loads(body.decode('utf-8'))
                        except Exception:
                            payload = None
                except Exception:
                    payload = None
                # best-effort model/pack extraction
                model_id = None; pack_id = None
                if isinstance(payload, dict):
                    model_id = payload.get('model_id')
                    pack_id = payload.get('pack_id')
                # lineage (best-effort)
                lineage_vals = None
                try:
                    if _compute_lineage is not None and model_id and pack_id:
                        pack_dir = WS_DIR / 'packs' / str(pack_id)
                        # Try to resolve indicator set file if present
                        ind_path = None
                        try:
                            ind_cand = pack_dir / 'indicator_sets' / f"{model_id}.yaml"
                            ind_path = ind_cand if ind_cand.exists() else (pack_dir / 'indicator_set.yaml')
                        except Exception:
                            ind_path = None
                        lineage_vals = _compute_lineage(pack_dir=pack_dir, model_id=str(model_id), indicator_set_path=ind_path)
                except Exception:
                    lineage_vals = None
                _log_audit(
                    path=path,
                    method=request.method,
                    status=int(getattr(response, 'status_code', 0)),
                    user_id=None,
                    client=str(request.client.host) if getattr(request, 'client', None) else None,
                    pack_id=pack_id,
                    model_id=model_id,
                    lineage=lineage_vals,
                    payload=payload,
                )
    except Exception as e:
        _logging.getLogger(__name__).warning("audit middleware error: %s", e)
    return response


# Optional simple in-memory rate limit (dev scaffold)
try:
    import os as _os
    _RATE_ENABLED = (_os.getenv('RATELIMIT_ENABLED', 'false').lower() == 'true')
    _RATE_PER_MIN = int(_os.getenv('RATELIMIT_PER_MIN', '120'))
except Exception:
    _RATE_ENABLED = False
    _RATE_PER_MIN = 120

_rate_counters: dict[tuple[str,str,int], int] = {}

@app.middleware("http")
async def _rate_limit_mw(request, call_next):
    if not _RATE_ENABLED:
        return await call_next(request)
    try:
        import time as _t
        now_min = int(_t.time() // 60)
        key = (str(request.client.host) if request.client else 'unknown', str(request.url.path), now_min)
        cnt = _rate_counters.get(key, 0) + 1
        _rate_counters[key] = cnt
        if cnt > _RATE_PER_MIN:
            from fastapi.responses import JSONResponse as _JR
            return _JR({"ok": False, "error": "rate_limited"}, status_code=429)
    except Exception:
        pass
    return await call_next(request)

 

@app.get("/")
def index():
    return {
        "name": "Sigmatiq Sigma API",
        "ok": True,
        "endpoints": [
            "/health", "/models", "/model_detail",
            "/build_matrix", "/train", "/backtest",
            "/build_stock_matrix", "/preview_matrix", "/indicator_sets",
            "/validate_policy", "/leaderboard", "/calibrate_thresholds", "/scan", "/signals",
        ],
    }

def _model_paths(model_id: str, pack_id: str = "zerosigma") -> Dict[str, Path]:
    art = WS_DIR / "artifacts" / model_id / "gbm.pkl"
    pol = WS_DIR / "packs" / pack_id / "policy_templates" / f"{model_id}.yaml"
    live = WS_DIR / "live_data" / model_id
    return {"model": art, "policy": pol, "live": live}


def _load_config(model_id: str, pack_id: str = "zerosigma") -> Dict[str, Any]:
    p = WS_DIR / "packs" / pack_id / "model_configs" / f"{model_id}.yaml"
    if p.exists():
        try:
            return yaml.safe_load(p.read_text()) or {}
        except Exception:
            return {}
    return {}


@app.get("/models")
def list_models(pack_id: str = Query("zerosigma")):
    cfg_dir = WS_DIR / "packs" / pack_id / "model_configs"
    out = []
    for p in sorted(cfg_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(p.read_text())
            out.append({"id": data.get("model_id") or p.stem, "config": data})
        except Exception:
            out.append({"id": p.stem})
    return {"models": out}


def _workspace_paths(model_id: str, pack_id: str = "zerosigma") -> Dict[str, Path]:
    base = WS_DIR
    return {
        "matrices": base / "matrices" / model_id,
        "live": base / "live_data" / model_id,
        "artifacts": base / "artifacts" / model_id,
        "reports": base / "reports",
        "plots": base / "static" / "backtest_plots" / model_id,
        "policy": base / "packs" / pack_id / "policy_templates" / f"{model_id}.yaml",
        "config": base / "packs" / pack_id / "model_configs" / f"{model_id}.yaml",
    }

def _ensure_policy_exists(model_id: str, pack_id: str) -> Optional[str]:
    """Return None if policy exists; otherwise return an error message with required path."""
    pol = _workspace_paths(model_id, pack_id)["policy"]
    if not pol.exists():
        return f"Policy file missing for model '{model_id}'. Please create: {pol}"
    # Validate policy schema
    ok, errs = (True, []) if _validate_policy_file is None else _validate_policy_file(pol)
    if not ok:
        return f"Policy file invalid for model '{model_id}': {', '.join(errs)} (path: {pol})"
    return None

## policy validation now imported from api.services.policy



def _train_model(csv_path: str, *, allowed_hours: Optional[List[int]], target: Optional[str], calibration: Optional[str], model_out: Path, features_list: Optional[List[str]] = None) -> Dict[str, Any]:
    if select_features_train is None or XGBClassifier is None or LabelEncoder is None:
        raise RuntimeError(f"Training dependencies missing")
    df = pd.read_csv(csv_path)
    if allowed_hours and "hour_et" in df.columns:
        df = df[df["hour_et"].isin(allowed_hours)].copy()
    y_col = target or ("y" if "y" in df.columns and df["y"].notna().any() else "y_syn")
    features = features_list or select_features_train(df)
    missing = [c for c in features if c not in df.columns]
    for c in missing:
        if c.startswith("calls_sold_d") or c.startswith("puts_sold_d"):
            df[c] = 0.0
    X = df[features].fillna(0.0).values
    y_raw = df[y_col].astype(str).values
    le = LabelEncoder(); y = le.fit_transform(y_raw)
    model = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.08, subsample=0.9, colsample_bytree=0.9, eval_metric="mlogloss", tree_method="hist", random_state=2025)
    if calibration in {"sigmoid", "isotonic"}:
        try:
            clf = CalibratedClassifierCV(model, method=calibration, cv=3)
            clf.fit(X, y)
            final = clf
        except Exception:
            model.fit(X, y); final = model
    else:
        model.fit(X, y); final = model
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": final, "features": features, "label_encoder": le}, model_out)
    return {"ok": True, "model_out": str(model_out), "rows": int(len(df))}



    # NOTE: backtest endpoint and leaderboard are implemented in routers/backtest.py


@app.get("/model_detail")
def model_detail(model_id: str = Query(...), pack_id: str = Query("zerosigma")):
    cfg = _load_config(model_id, pack_id)
    pol_path = _workspace_paths(model_id, pack_id)["policy"]
    policy = {}
    policy_source = "missing"
    policy_valid = False
    policy_errors: List[str] = []
    execution_effective: Dict[str, Any] = {}
    if pol_path.exists():
        try:
            policy = yaml.safe_load(pol_path.read_text()) or {}
            ok, errs = _validate_policy_file(pol_path)
            policy_valid = bool(ok)
            policy_errors = list(errs)
            policy_source = "model"
            # Resolve effective execution params
            pol_norm = policy.get("policy") if isinstance(policy.get("policy"), dict) else policy
            exec_pol = pol_norm.get("execution", {}) if isinstance(pol_norm.get("execution", {}), dict) else {}
            execution_effective = {
                "slippage_bps": exec_pol.get("slippage_bps", 1.0),
                "size_by_conf": exec_pol.get("size_by_conf", False),
                "conf_cap": exec_pol.get("conf_cap", 1.0),
                "momentum_gate": exec_pol.get("momentum_gate", False),
                "momentum_min": exec_pol.get("momentum_min", 0.0),
                "momentum_column": exec_pol.get("momentum_column", "momentum_score_total"),
            }
        except Exception as e:
            policy = {}
            policy_valid = False
            policy_errors = [str(e)]
    # Renderable strings
    cfg_yaml = ""
    try:
        cfg_yaml = yaml.safe_dump(cfg or {}, sort_keys=False)
    except Exception:
        cfg_yaml = ""
    pol_json = json.dumps(policy, indent=2) if policy else "{}"
    return {
        "ok": True,
        "config": cfg,
        "config_yaml": cfg_yaml,
        "policy": policy,
        "policy_json": pol_json,
        "policy_source": policy_source,
        "policy_valid": policy_valid,
        "policy_errors": policy_errors,
        "execution_effective": execution_effective,
    }

def _load_policy(model_id: str, pack_id: str) -> Dict[str, Any]:
    pol_path = _workspace_paths(model_id, pack_id)["policy"]
    data: Dict[str, Any] = {}
    try:
        raw = yaml.safe_load(pol_path.read_text()) if pol_path.exists() else {}
        if isinstance(raw, dict):
            data = raw.get("policy", raw)
    except Exception:
        data = {}
    return data or {}


def _to_float(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        v = float(x)
        import numpy as _np
        if _np.isfinite(v):
            return v
    except Exception:
        pass
    return None


@app.get("/validate_policy")
def validate_policy(model_id: str = Query(...), pack_id: str = Query("zerosigma")):
    pol_path = _workspace_paths(model_id, pack_id)["policy"]
    if not pol_path.exists():
        return JSONResponse({"ok": False, "error": f"Policy file missing: {pol_path}"}, status_code=400)
    ok, errs = _validate_policy_file(pol_path)
    return {"ok": bool(ok), "path": str(pol_path), "errors": errs}





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
    # Scoring params (optional overrides)
    epsilon: Optional[float] = 0.002
    bos_min: Optional[float] = 0.25
    rsi_min: Optional[float] = 55.0
    adx_min: Optional[float] = 18.0
    # Brackets toggle (optional override)
    brackets_enabled: Optional[bool] = None


def _resolve_indicator_set_path_api(pack_id: str, model_id: str, indicator_set_name: Optional[str]) -> Path:
    return _resolve_indicator_set_path(pack_id, model_id, indicator_set_name)


def _compute_breakout_momentum_score_inline(
    df: pd.DataFrame,
    *,
    epsilon: float = 0.002,
    bos_min: float = 0.25,
    rsi_min: float = 55.0,
    adx_min: float = 18.0,
) -> pd.DataFrame:
    out = df.copy()
    w_break, w_momo, w_trendq, w_align = 40.0, 30.0, 15.0, 15.0
    w_sum = max(1e-6, w_break + w_momo + w_trendq + w_align)
    close = pd.to_numeric(out.get('close', pd.Series(index=out.index)), errors='coerce')
    # Bands & Donchian + ATR
    upper = pd.to_numeric(out.filter(like='upper_').iloc[:,0] if any(out.columns.str.startswith('upper_')) else pd.Series(_np.nan, index=out.index), errors='coerce')
    donch_cols = [c for c in out.columns if c.startswith('donchian_high_')]
    donch_high = pd.to_numeric(out[donch_cols[0]] if donch_cols else pd.Series(_np.nan, index=out.index), errors='coerce')
    atr = pd.to_numeric(out.filter(like='atr_').iloc[:,0] if any(out.columns.str.startswith('atr_')) else pd.Series(_np.nan, index=out.index), errors='coerce')
    # BoS and breakout pass
    bos = (close - donch_high) / atr.replace(0.0, _np.nan)
    bos = bos.replace([_np.inf, -_np.inf], _np.nan).fillna(0.0)
    breakout_pass = ((close > upper * (1.0 + epsilon)) | (close > donch_high * (1.0 + epsilon)) | (bos >= bos_min)).astype(float)
    score_breakout = _np.clip(bos / 0.50, 0.0, 1.0)
    # Momentum 20/63
    m20 = pd.to_numeric((out.filter(like='momentum_20').iloc[:,0] if any(out.columns.str.contains('momentum_20')) else out.get('ret_20', pd.Series(_np.nan, index=out.index))), errors='coerce')
    m63 = pd.to_numeric((out.filter(like='momentum_63').iloc[:,0] if any(out.columns.str.contains('momentum_63')) else out.get('ret_63', pd.Series(_np.nan, index=out.index))), errors='coerce')
    momentum_score = (m20.rank(pct=True) * 0.5 + m63.rank(pct=True) * 0.5).fillna(0.0)
    # Trend quality: ADX scaled; fallback to r2
    adx = pd.to_numeric((out.filter(like='adx_').iloc[:,0] if any(out.columns.str.startswith('adx_')) else pd.Series(_np.nan, index=out.index)), errors='coerce')
    r2 = pd.to_numeric((out.filter(like='lr_r2_').iloc[:,0] if any(out.columns.str.startswith('lr_r2_')) else pd.Series(_np.nan, index=out.index)), errors='coerce').fillna(0.0)
    trend_quality = _np.clip((adx - 20.0) / 15.0, 0.0, 1.0)
    trend_quality = _np.where(adx.notna(), trend_quality, r2)
    # Alignment
    ema20 = pd.to_numeric((out.filter(like='ema_20').iloc[:,0] if any(out.columns.str.startswith('ema_20')) else pd.Series(_np.nan, index=out.index)), errors='coerce')
    ema50 = pd.to_numeric((out.filter(like='ema_50').iloc[:,0] if any(out.columns.str.startswith('ema_50')) else pd.Series(_np.nan, index=out.index)), errors='coerce')
    rsi = pd.to_numeric((out.filter(like='rsi_').iloc[:,0] if any(out.columns.str.startswith('rsi_')) else pd.Series(_np.nan, index=out.index)), errors='coerce')
    align_trend = (ema20 > ema50).astype(float)
    align_rsi = (rsi >= rsi_min).astype(float)
    align_adx = (adx >= adx_min).astype(float) if adx.notna().any() else 1.0
    score_alignment = (align_trend + align_rsi + align_adx) / 3.0
    # Compose
    out['bos_derived'] = bos
    out['score_breakout'] = score_breakout
    out['score_momentum'] = momentum_score
    out['score_trend_quality'] = pd.to_numeric(trend_quality, errors='coerce').fillna(0.0)
    out['score_alignment'] = score_alignment
    out['score_total'] = (w_break * out['score_breakout'] + w_momo * out['score_momentum'] + w_trendq * out['score_trend_quality'] + w_align * out['score_alignment']) / w_sum
    out['_gates_pass'] = ((breakout_pass >= 1.0) & (align_rsi >= 1.0) & (align_adx >= 1.0))
    return out


@app.post("/scan")
def scan_ep(payload: ScanRequest):
    try:
        pack_id = payload.pack_id or 'swingsigma'
        model_id = payload.model_id or 'universe_eq_swing_daily_scanner'
        ind_path = _resolve_indicator_set_path_api(pack_id, model_id, payload.indicator_set)
        # Resolve universe
        tickers: list[str] = []
        if payload.universe_csv:
            u = pd.read_csv(payload.universe_csv)
            col = payload.universe_col or 'ticker'
            if col not in u.columns:
                return JSONResponse({"ok": False, "error": f"Universe CSV missing column: {col}"}, status_code=400)
            tickers = [str(x).strip().upper() for x in u[col].dropna().tolist() if str(x).strip()]
        elif payload.tickers:
            tickers = [x.strip().upper() for x in str(payload.tickers).split(',') if x.strip()]
        else:
            return JSONResponse({"ok": False, "error": "Provide tickers or universe_csv"}, status_code=400)

        # Build and collect latest rows
        latest_rows: list[pd.DataFrame] = []
        base_dir = WS_DIR / 'matrices' / model_id
        base_dir.mkdir(parents=True, exist_ok=True)
        for t in tickers:
            out_csv = base_dir / f"{t}_scan.csv"
            build_stock_matrix_range(
                start_date=payload.start,
                end_date=payload.end,
                out_csv=str(out_csv),
                ticker=t,
                indicator_set_path=str(ind_path) if ind_path else None,
                label_kind='none',
            )
            df = pd.read_csv(out_csv)
            if len(df) == 0:
                continue
            last = df.iloc[[-1]].copy(); last['ticker'] = t
            latest_rows.append(last)
        if not latest_rows:
            return JSONResponse({"ok": False, "error": "No data built for provided universe"}, status_code=400)

        latest = pd.concat(latest_rows, ignore_index=True)
        scored = _compute_breakout_momentum_score_inline(
            latest,
            epsilon=float(payload.epsilon or 0.002),
            bos_min=float(payload.bos_min or 0.25),
            rsi_min=float(payload.rsi_min or 55.0),
            adx_min=float(payload.adx_min or 18.0),
        )
        if '_gates_pass' in scored.columns:
            scored = scored[scored['_gates_pass']].copy()
        
        # Bracket computation (stocks)
        pol = _load_policy(model_id, pack_id)
        exec_pol = pol.get('execution', {}) if isinstance(pol.get('execution', {}), dict) else {}
        br_pol = exec_pol.get('brackets', {}) if isinstance(exec_pol.get('brackets', {}), dict) else {}
        br_enabled = bool(payload.brackets_enabled if payload.brackets_enabled is not None else br_pol.get('enabled', True))
        if br_enabled and apply_stock_brackets is not None:
            scored = apply_stock_brackets(scored, br_pol)
        scored = scored.sort_values('score_total', ascending=False)
        scored['rank'] = _np.arange(1, len(scored) + 1)
        picked = scored.head(int(payload.top_n or 50)).copy()

        # Lineage stamping (CSV + DB)
        policy_version = ''
        try:
            policy_version = str((_load_policy(model_id, pack_id) or {}).get('version', ''))
        except Exception:
            policy_version = ''
        lineage_vals = {'pack_sha': None, 'indicator_set_sha': None, 'model_config_sha': None, 'policy_sha': None}
        if _compute_lineage is not None:
            try:
                pack_dir = WS_DIR / 'packs' / pack_id
                lineage_vals = _compute_lineage(pack_dir=pack_dir, model_id=model_id, indicator_set_path=ind_path)
            except Exception:
                pass
        # Attach lineage & meta columns to picked for CSV persistence
        picked['pack_id'] = pack_id
        picked['policy_version'] = policy_version
        picked['pack_sha'] = lineage_vals.get('pack_sha')
        picked['indicator_set_sha'] = lineage_vals.get('indicator_set_sha')
        picked['model_config_sha'] = lineage_vals.get('model_config_sha')
        picked['policy_sha'] = lineage_vals.get('policy_sha')

        live_dir = _workspace_paths(model_id, pack_id)["live"]
        live_dir.mkdir(parents=True, exist_ok=True)
        out_csv = live_dir / 'signals.csv'
        keep_cols = [c for c in [
            'ticker', 'date', 'close', 'side', 'entry_mode', 'entry_ref_px', 'stop_px', 'target_px', 'time_stop_minutes', 'rr',
            'score_total', 'score_breakout', 'score_momentum', 'score_trend_quality', 'score_alignment', 'rank',
            'pack_id', 'policy_version', 'pack_sha', 'indicator_set_sha', 'model_config_sha', 'policy_sha'
        ] if c in picked.columns]
        picked.to_csv(out_csv, index=False, columns=keep_cols)
        # Optional DB upsert
        if db_upsert_signals is not None:
            try:
                # shape rows for DB
                records = []
                for _, r in picked.iterrows():
                    rec = {
                        'date': pd.to_datetime(r.get('date')).date() if pd.notna(r.get('date')) else None,
                        'model_id': model_id,
                        'ticker': r.get('ticker'),
                        'side': r.get('side', 'buy'),
                        'entry_mode': r.get('entry_mode'),
                        'entry_ref_px': _to_float(r.get('entry_ref_px')),
                        'stop_px': _to_float(r.get('stop_px')),
                        'target_px': _to_float(r.get('target_px')),
                        'time_stop_minutes': int(r.get('time_stop_minutes')) if pd.notna(r.get('time_stop_minutes')) else None,
                        'rr': _to_float(r.get('rr')),
                        'score_total': _to_float(r.get('score_total')),
                        'rank': int(r.get('rank')) if pd.notna(r.get('rank')) else None,
                        'score_breakout': _to_float(r.get('score_breakout')),
                        'score_momentum': _to_float(r.get('score_momentum')),
                        'score_trend_quality': _to_float(r.get('score_trend_quality')),
                        'score_alignment': _to_float(r.get('score_alignment')),
                        'pack_id': pack_id,
                        'policy_version': policy_version,
                        'pack_sha': lineage_vals.get('pack_sha'),
                        'indicator_set_sha': lineage_vals.get('indicator_set_sha'),
                        'model_config_sha': lineage_vals.get('model_config_sha'),
                        'policy_sha': lineage_vals.get('policy_sha'),
                    }
                    records.append(rec)
                if records:
                    db_upsert_signals(records)
            except Exception:
                pass
        return {
            'ok': True,
            'model_id': model_id,
            'pack_id': pack_id,
            'count': int(len(picked)),
            'signals_csv': str(out_csv),
            'top': picked[keep_cols].head(min(5, len(picked))).to_dict(orient='records'),
        }
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)



# --- Model creation & indicator set management & preview ---


def _resolve_indicator_set_path(pack_id: str, model_id: str, indicator_set_name: Optional[str] = None) -> Path:
    base = WS_DIR / 'packs' / pack_id
    cand = base / 'indicator_sets' / f"{model_id}.yaml"
    if cand.exists():
        return cand
    if indicator_set_name:
        cand2 = base / 'indicator_sets' / f"{indicator_set_name}.yaml"
        if cand2.exists():
            return cand2
    legacy = base / 'indicator_set.yaml'
    return legacy


class PreviewMatrixRequest(BaseModel):
    model_id: str
    start: str
    end: str
    pack_id: str | None = 'zerosigma'
    max_rows: int | None = 200


@app.post("/preview_matrix")
def preview_matrix_ep(payload: PreviewMatrixRequest):
    model_id = payload.model_id
    pack_id = payload.pack_id or 'zerosigma'
    pol_err = _ensure_policy_exists(model_id, pack_id)
    if pol_err:
        return JSONResponse({"ok": False, "error": pol_err}, status_code=400)
    try:
        tmp_csv = WS_DIR / 'reports' / f"preview_matrix_{model_id}.csv"
        (WS_DIR / 'reports').mkdir(parents=True, exist_ok=True)
        indicator_set_path = _resolve_indicator_set_path(pack_id, model_id)
        # Lightweight build
        build_matrix_range(
            start_date=payload.start,
            end_date=payload.end,
            out_csv=str(tmp_csv),
            make_real_labels=True,
            distance_max=5,
            ticker=str((_load_config(model_id, pack_id) or {}).get('ticker', 'SPY')),
            indicator_set_path=str(indicator_set_path),
        )
        df = pd.read_csv(tmp_csv)
        # Basic NaN stats as list with percent
        nan_stats_list = []
        n = max(1, len(df))
        for c in df.columns:
            nan_pct = float(pd.to_numeric(df[c], errors='ignore').isna().sum()) * 100.0 / n
            nan_stats_list.append({"column": c, "nan_pct": round(nan_pct, 3)})
        warnings = []
        has_flow_cols = any(str(c).startswith('calls_sold_d') or str(c).startswith('puts_sold_d') for c in df.columns)
        if not has_flow_cols:
            warnings.append("flow features absent in preview")
        # Stricter thresholds for v2 features
        v2_cols = [
            'open_gap_z',
            'atm_iv_open_delta',
            'gamma_density_peak_strike',
            'gamma_skew_left_right',
        ]
        # include first15m_range_z_* variants
        v2_match = []
        for c in df.columns:
            if c in v2_cols or str(c).startswith('first15m_range_z'):
                v2_match.append(str(c))
        warn_cols = []
        fail_cols = []
        if v2_match:
            ns_map = {d['column']: d['nan_pct'] for d in nan_stats_list}
            for c in v2_match:
                pct = float(ns_map.get(c, 0.0))
                if pct >= 30.0:
                    fail_cols.append({"column": c, "nan_pct": pct})
                elif pct >= 10.0:
                    warn_cols.append({"column": c, "nan_pct": pct})
        if warn_cols:
            warnings.append(f"v2 feature NaNs >10%: {[w['column'] for w in warn_cols]}")
        ok_flag = True
        err = None
        if fail_cols:
            ok_flag = False
            err = {"message": "v2 feature NaNs exceed 30%", "columns": fail_cols}
        return {"ok": bool(ok_flag), "n_rows": int(len(df)), "columns": df.columns.tolist(), "nan_stats": nan_stats_list, "warnings": warnings, "v2_nan_summary": {"warn": warn_cols, "fail": fail_cols}, "error": err}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)
