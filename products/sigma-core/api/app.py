#!/usr/bin/env python3
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Header, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import inspect
import re
from typing import Any, Dict
import json
from datetime import date, timedelta
import pandas as pd
import os
import hashlib

# Load local .env (self-sufficient)
try:
    from dotenv import load_dotenv  # type: ignore
    core_env = Path(__file__).resolve().parents[1] / '.env'
    if core_env.exists():
        load_dotenv(dotenv_path=core_env)
except Exception:
    pass

from sigma_core.storage.relational import get_db
from sigma_core.indicators.registry import get_indicator as get_indicator_cls, get_load_errors as get_indicator_load_errors
from sigma_core.features.sets import IndicatorSet as FBIndicatorSet, IndicatorSpec as FBIndicatorSpec
from sigma_core.features.builder import FeatureBuilder
from sigma_core.data.sources.polygon import (
    get_polygon_daily_bars,
    get_polygon_hourly_bars,
    get_polygon_agg_bars,
)
from sigma_core.labels.hourly_direction import label_next_hour_direction
from sigma_core.labels.forward import label_forward_return_days
from sigma_core.backtest.engine import run_backtest as engine_run_backtest
from datetime import datetime

app = FastAPI(title="Sigma Core Catalog API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- AuthN/AuthZ (placeholder) ---
class User(BaseModel):
    user_id: str
    roles: List[str] = []


def get_current_user(x_user_id: Optional[str] = Header(default=None)) -> User:
    # Placeholder auth: use X-User-Id header if present, else anon
    uid = x_user_id or "anon"
    return User(user_id=uid, roles=["user"])  # no real authz yet


# --- Schemas ---
class IndicatorOut(BaseModel):
    id: str
    version: int
    status: str
    title: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    beginner_summary: Optional[str] = None
    details: Optional[dict] = None


class IndicatorSetOut(BaseModel):
    set_id: str
    version: int
    status: str
    title: str
    purpose: Optional[str] = None
    beginner_summary: Optional[str] = None
    details: Optional[dict] = None


class StrategyOut(BaseModel):
    strategy_id: str
    version: int
    status: str
    title: str
    objective: Optional[str] = None
    beginner_summary: Optional[str] = None
    details: Optional[dict] = None


class WorkflowOut(BaseModel):
    workflow_id: str
    version: int
    status: str
    title: str
    subtitle: Optional[str] = None
    time_to_complete: Optional[int] = None
    beginner_summary: Optional[str] = None
    details: Optional[dict] = None


class RecipeOut(BaseModel):
    recipe_id: str
    version: int
    status: str
    title: str
    beginner_summary: Optional[str] = None
    target_kind: str
    target_id: str
    sort_rank: Optional[int] = None


# --- Indicators (single) ---
class IndicatorValidateIn(BaseModel):
    name: str
    params: Dict[str, Any] | None = None


class IndicatorValidateOut(BaseModel):
    ok: bool
    errors: List[str] = []
    expected_params: List[Dict[str, Any]] = []


class IndicatorComputeIn(BaseModel):
    name: str
    params: Dict[str, Any] | None = None
    data: List[Dict[str, Any]]


class IndicatorComputeOut(BaseModel):
    columns: List[str]
    data: List[Dict[str, Any]]


@app.post("/indicators/validate", response_model=IndicatorValidateOut, summary="Validate indicator params", description="Returns expected parameter list and validates provided params.")
def validate_indicator(payload: IndicatorValidateIn = Body(..., example={"name":"rsi","params":{"period":14}})):
    errors: List[str] = []
    expected: List[Dict[str, Any]] = []
    try:
        cls = get_indicator_cls(payload.name)
    except Exception as e:
        load_errors = get_indicator_load_errors() or []
        errors.append(f"indicator '{payload.name}' not found")
        if load_errors:
            errors.append("loader_errors_present")
        return IndicatorValidateOut(ok=False, errors=errors, expected_params=expected)
    try:
        sig = inspect.signature(cls.__init__)
        for pname, p in list(sig.parameters.items())[1:]:  # skip self
            exp: Dict[str, Any] = {"name": pname}
            if p.default is not inspect._empty:
                exp["default"] = p.default
            if p.annotation is not inspect._empty:
                exp["type"] = str(p.annotation)
            expected.append(exp)
        # Try instantiation to catch bad params
        params = dict(payload.params or {})
        _ = cls(**params)  # type: ignore
        return IndicatorValidateOut(ok=True, errors=[], expected_params=expected)
    except TypeError as te:
        errors.append(str(te))
        return IndicatorValidateOut(ok=False, errors=errors, expected_params=expected)
    except Exception as e:
        errors.append(str(e))
        return IndicatorValidateOut(ok=False, errors=errors, expected_params=expected)


@app.post("/indicators/compute", response_model=IndicatorComputeOut, summary="Compute a single indicator", description="Computes an indicator over supplied rows and returns the computed columns.")
def compute_indicator(payload: IndicatorComputeIn = Body(..., example={"name":"rsi","params":{"period":14},"data":[{"timestamp":"2024-06-01","open":100.0,"high":101.0,"low":99.5,"close":100.5,"volume":1000000}]})):
    try:
        cls = get_indicator_cls(payload.name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"indicator '{payload.name}' not found")
    try:
        params = dict(payload.params or {})
        inst = cls(**params)  # type: ignore
    except TypeError as te:
        raise HTTPException(status_code=400, detail=f"invalid params: {te}")
    try:
        df = pd.DataFrame.from_records(payload.data)
        out = inst.calculate(df)
        # Return only computed columns
        return IndicatorComputeOut(columns=list(out.columns), data=out.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"compute failed: {e}")


class ScreenRule(BaseModel):
    column: str
    op: str  # one of: >, >=, <, <=, ==, !=
    value: float | int


class ScreenRequest(BaseModel):
    name: str
    params: Dict[str, Any] | None = None
    # Provide data per symbol to avoid external data dependencies
    data: Dict[str, List[Dict[str, Any]]]
    rule: ScreenRule


class ScreenResult(BaseModel):
    matched: List[str]
    evaluated: int


@app.post("/screen", response_model=ScreenResult, summary="Screen supplied per-symbol data with a single indicator", description="Caller provides per-symbol time series data; computes indicator and applies a simple rule on the latest value.")
def screen_single_indicator(payload: ScreenRequest = Body(..., example={"name":"rsi","params":{"period":14},"data":{"AAPL":[{"timestamp":"2024-06-01","open":100.0,"high":101.0,"low":99.5,"close":100.5,"volume":1000000}]},"rule":{"column":"rsi_14","op":">","value":70}})):
    try:
        cls = get_indicator_cls(payload.name)
        inst = cls(**(payload.params or {}))  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid indicator: {e}")
    op = payload.rule.op
    if op not in {">", ">=", "<", "<=", "==", "!="}:
        raise HTTPException(status_code=400, detail="unsupported operator in rule")
    matched: List[str] = []
    for sym, rows in payload.data.items():
        try:
            df = pd.DataFrame.from_records(rows)
            out = inst.calculate(df)
            col = payload.rule.column
            if col not in out.columns:
                # Best-effort: if only one column computed, use that
                if len(out.columns) == 1:
                    col = out.columns[0]
                else:
                    continue
            val = out[col].iloc[-1]
            if (
                (op == ">" and val > payload.rule.value)
                or (op == ">=" and val >= payload.rule.value)
                or (op == "<" and val < payload.rule.value)
                or (op == "<=" and val <= payload.rule.value)
                or (op == "==" and val == payload.rule.value)
                or (op == "!=" and val != payload.rule.value)
            ):
                matched.append(sym)
        except Exception:
            continue
    return ScreenResult(matched=sorted(matched), evaluated=len(payload.data))


class AutoScreenRequest(BaseModel):
    # Universe
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    cap: Optional[int] = 50
    # Timeframe and range
    timeframe: str = "day"  # day|hour|<N>m (e.g., 5m)
    start_date: Optional[str] = None  # YYYY-MM-DD
    end_date: Optional[str] = None    # YYYY-MM-DD
    # Indicator
    name: str
    params: Dict[str, Any] | None = None
    rule: ScreenRule


class AutoScreenOut(BaseModel):
    matched: List[str]
    evaluated: int
    fetched: int
    skipped: int


def _default_dates() -> tuple[str, str]:
    ed = date.today()
    sd = ed - timedelta(days=90)
    return (sd.isoformat(), ed.isoformat())


def _fetch_bars(symbol: str, tf: str, start_date: str, end_date: str) -> pd.DataFrame:
    tf_l = tf.lower().strip()
    if tf_l in ("day", "daily"):
        return get_polygon_daily_bars(symbol, start_date, end_date)
    if tf_l in ("hour", "hourly"):
        return get_polygon_hourly_bars(symbol, start_date, end_date)
    # minutes like '5m', '15m', '30m', '1m'
    if tf_l.endswith('m'):
        try:
            n = int(tf_l[:-1])
            return get_polygon_agg_bars(symbol, n, 'minute', start_date, end_date)
        except Exception:
            pass
    # fallback to 5m
    return get_polygon_agg_bars(symbol, 5, 'minute', start_date, end_date)


@app.post("/screen/auto", response_model=AutoScreenOut, summary="Auto-screen a preset/watchlist via Polygon bars", description="Resolves a universe, fetches cached Polygon bars, computes an indicator, and applies a rule on the latest value.")
def screen_auto(payload: AutoScreenRequest, user: User = Depends(get_current_user)):
    if not payload.preset_id and not payload.watchlist_id:
        raise HTTPException(status_code=400, detail="preset_id or watchlist_id required")
    start_date, end_date = payload.start_date, payload.end_date
    if not start_date or not end_date:
        start_date, end_date = _default_dates()
    # Novice cap: 90-day window
    if _days_between(start_date, end_date) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    # Resolve universe
    symbols: List[str] = []
    with get_db() as conn:
        with conn.cursor() as cur:
            if payload.preset_id:
                cur.execute(
                    "SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol",
                    (payload.preset_id,),
                )
                symbols = [r[0] for r in cur.fetchall()]
            else:
                cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id = %s AND user_id = %s", (payload.watchlist_id, user.user_id))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="watchlist not found")
                cur.execute(
                    "SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol",
                    (payload.watchlist_id,),
                )
                symbols = [r[0] for r in cur.fetchall()]
    # Novice caps: 90 days and 50 symbols
    try:
        from datetime import datetime as _dt
        if (_dt.strptime(ed, "%Y-%m-%d") - _dt.strptime(sd, "%Y-%m-%d")).days > 90:
            raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    except Exception:
        pass
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:min(cap, 50)]
    # Prepare indicator
    try:
        cls = get_indicator_cls(payload.name)
        ind = cls(**(payload.params or {}))  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"invalid indicator params: {e}")

    op = payload.rule.op
    if op not in {">", ">=", "<", "<=", "==", "!="}:
        raise HTTPException(status_code=400, detail="unsupported operator in rule")

    matched: List[str] = []
    fetched = 0
    skipped = 0
    # Simple mode defaults
    thresholds_use = payload.thresholds
    top_pct_use = payload.top_pct
    hours_use = payload.allowed_hours
    if (getattr(payload, 'mode', None) or '').lower() == 'simple' and thresholds_use is None and top_pct_use is None:
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT grid FROM sc.backtest_sweep_presets WHERE preset_id = 'rth_thresholds_basic'")
                    rr = cur.fetchone()
                    if rr and rr[0]:
                        grid = rr[0] or {}
                        thr_list = (grid.get('thresholds_list') or [[]])
                        thresholds_use = thr_list[0] if thr_list and thr_list[0] else payload.thresholds
                        hrs_list = (grid.get('allowed_hours_list') or [[]])
                        hours_use = hrs_list[0] if hrs_list and hrs_list[0] else payload.allowed_hours
        except Exception:
            pass
    for sym in symbols:
        try:
            df = _fetch_bars(sym, payload.timeframe, start_date, end_date)
            if df is None or df.empty:
                skipped += 1
                continue
            fetched += 1
            out = ind.calculate(df)
            col = payload.rule.column
            if col not in out.columns:
                if len(out.columns) == 1:
                    col = out.columns[0]
                else:
                    skipped += 1
                    continue
            try:
                val = float(out[col].iloc[-1])
            except Exception:
                skipped += 1
                continue
            if (
                (op == ">" and val > payload.rule.value)
                or (op == ">=" and val >= payload.rule.value)
                or (op == "<" and val < payload.rule.value)
                or (op == "<=" and val <= payload.rule.value)
                or (op == "==" and val == payload.rule.value)
                or (op == "!=" and val != payload.rule.value)
            ):
                matched.append(sym)
        except Exception:
            skipped += 1
            continue
    return AutoScreenOut(matched=sorted(set(matched)), evaluated=len(symbols), fetched=fetched, skipped=skipped)


# --- Auto-build features for an indicator set over a preset/watchlist ---
class AutoSetFeaturesRequest(BaseModel):
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    cap: Optional[int] = 50
    timeframe: str = "day"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    set_id: str
    version: int


class AutoSetFeaturesRow(BaseModel):
    symbol: str
    features: Dict[str, Any]


class AutoSetFeaturesOut(BaseModel):
    evaluated: int
    fetched: int
    skipped: int
    columns: List[str]
    data: List[AutoSetFeaturesRow]


@app.post("/indicator_sets/auto_build", response_model=AutoSetFeaturesOut, summary="Build last-row features for a set", description="Fetches bars via Polygon with caching and computes an indicator set; returns last-row feature values per symbol.")
def indicator_set_auto_build(payload: AutoSetFeaturesRequest, user: User = Depends(get_current_user)):
    if not payload.preset_id and not payload.watchlist_id:
        raise HTTPException(status_code=400, detail="preset_id or watchlist_id required")
    start_date, end_date = payload.start_date, payload.end_date
    if not start_date or not end_date:
        start_date, end_date = _default_dates()
    # Novice cap: 90-day window
    if _days_between(start_date, end_date) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    # Build FBIndicatorSet from DB
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT title FROM sc.indicator_sets WHERE set_id=%s AND version=%s",
                (payload.set_id, payload.version),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="indicator set not found")
            desc = r[0] or ""
            cur.execute(
                "SELECT indicator_id, indicator_version, params FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord",
                (payload.set_id, payload.version),
            )
            comps = cur.fetchall()
            # Resolve universe
            symbols: List[str] = []
            if payload.preset_id:
                cur.execute(
                    "SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol",
                    (payload.preset_id,),
                )
                symbols = [x[0] for x in cur.fetchall()]
            else:
                cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id=%s AND user_id=%s", (payload.watchlist_id, user.user_id))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="watchlist not found")
                cur.execute(
                    "SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol",
                    (payload.watchlist_id,),
                )
                symbols = [x[0] for x in cur.fetchall()]
    # Novice caps: 90 days and 50 symbols
    try:
        from datetime import datetime as _dt
        if (_dt.strptime(ed, "%Y-%m-%d") - _dt.strptime(sd, "%Y-%m-%d")).days > 90:
            raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    except Exception:
        pass
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:min(cap, 50)]
    fb_set = FBIndicatorSet(
        name=str(payload.set_id),
        version=int(payload.version),
        description=str(desc),
        indicators=[FBIndicatorSpec(name=rr[0], version=int(rr[1] or 1), params=(rr[2] or {})) for rr in comps],
    )
    fb = FeatureBuilder(indicator_set=fb_set)

    fetched = 0
    skipped = 0
    cols_union: set[str] = set()
    rows: List[AutoSetFeaturesRow] = []

    for sym in symbols:
        try:
            df = _fetch_bars(sym, payload.timeframe, start_date, end_date)
            if df is None or df.empty:
                skipped += 1
                continue
            fetched += 1
            out_df = fb.add_indicator_features(df)
            new_cols = [c for c in out_df.columns if c not in df.columns]
            if not new_cols:
                skipped += 1
                continue
            cols_union.update(new_cols)
            last = out_df.iloc[-1]
            features = {c: float(last[c]) if c in out_df.columns else None for c in new_cols}
            rows.append(AutoSetFeaturesRow(symbol=sym, features=features))
        except Exception:
            skipped += 1
            continue

    return AutoSetFeaturesOut(
        evaluated=len(symbols),
        fetched=fetched,
        skipped=skipped,
        columns=sorted(cols_union),
        data=rows,
    )


# --- Auto-screen using an indicator set (apply rules to set features) ---
class AutoSetScreenRequest(BaseModel):
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    cap: Optional[int] = 50
    timeframe: str = "day"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    set_id: str
    version: int
    # Either provide a human-readable expression or a rules list (AND semantics)
    rule_expr: Optional[str] = None
    rules: Optional[List[ScreenRule]] = None


def _parse_rules(expr: str) -> List[ScreenRule]:
    parts = [p.strip() for p in re.split(r"(?i)\band\b", expr) if p.strip()]
    out: List[ScreenRule] = []
    pat = re.compile(r"^([A-Za-z0-9_\.]+)\s*(==|!=|>=|<=|>|<)\s*([-+]?[0-9]*\.?[0-9]+)\s*$")
    for p in parts:
        m = pat.match(p)
        if not m:
            raise ValueError(f"invalid condition: '{p}'")
        out.append(ScreenRule(column=m.group(1), op=m.group(2), value=float(m.group(3))))
    return out


@app.post("/indicator_sets/auto_screen", response_model=AutoScreenOut, summary="Screen a set by applying rules", description="Resolves universe, fetches bars via Polygon, computes the set, and applies ANDed rules on the latest features.")
def indicator_set_auto_screen(payload: AutoSetScreenRequest, user: User = Depends(get_current_user)):
    if not payload.preset_id and not payload.watchlist_id:
        raise HTTPException(status_code=400, detail="preset_id or watchlist_id required")
    start_date, end_date = payload.start_date, payload.end_date
    if not start_date or not end_date:
        start_date, end_date = _default_dates()
    # Novice cap: 90-day window
    if _days_between(start_date, end_date) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    # Build rules
    rules: List[ScreenRule] = []
    if payload.rules:
        rules = payload.rules
    elif payload.rule_expr:
        try:
            rules = _parse_rules(payload.rule_expr)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"invalid rule_expr: {e}")
    else:
        raise HTTPException(status_code=400, detail="rules or rule_expr required")
    # Build FBIndicatorSet and resolve universe
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT title FROM sc.indicator_sets WHERE set_id=%s AND version=%s",
                (payload.set_id, payload.version),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="indicator set not found")
            desc = r[0] or ""
            cur.execute(
                "SELECT indicator_id, indicator_version, params FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord",
                (payload.set_id, payload.version),
            )
            comps = cur.fetchall()
            symbols: List[str] = []
            if payload.preset_id:
                cur.execute(
                    "SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol",
                    (payload.preset_id,),
                )
                symbols = [x[0] for x in cur.fetchall()]
            else:
                cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id=%s AND user_id=%s", (payload.watchlist_id, user.user_id))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="watchlist not found")
                cur.execute(
                    "SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol",
                    (payload.watchlist_id,),
                )
                symbols = [x[0] for x in cur.fetchall()]
    # Novice caps: 90 days and 50 symbols
    try:
        from datetime import datetime as _dt
        if (_dt.strptime(ed, "%Y-%m-%d") - _dt.strptime(sd, "%Y-%m-%d")).days > 90:
            raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    except Exception:
        pass
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:min(cap, 50)]
    fb_set = FBIndicatorSet(
        name=str(payload.set_id),
        version=int(payload.version),
        description=str(desc),
        indicators=[FBIndicatorSpec(name=rr[0], version=int(rr[1] or 1), params=(rr[2] or {})) for rr in comps],
    )
    fb = FeatureBuilder(indicator_set=fb_set)

    matched: List[str] = []
    fetched = 0
    skipped = 0

    for sym in symbols:
        try:
            df = _fetch_bars(sym, payload.timeframe, start_date, end_date)
            if df is None or df.empty:
                skipped += 1
                continue
            fetched += 1
            out_df = fb.add_indicator_features(df)
            new_cols = [c for c in out_df.columns if c not in df.columns]
            if not new_cols:
                skipped += 1
                continue
            last = out_df.iloc[-1]
            def check_rule(rule: ScreenRule) -> bool:
                col = rule.column if rule.column in out_df.columns else None
                if col is None:
                    # if only one new column, allow implicit
                    if len(new_cols) == 1:
                        col = new_cols[0]
                    else:
                        return False
                try:
                    val = float(last[col])
                except Exception:
                    return False
                if rule.op == ">":
                    return val > rule.value
                if rule.op == ">=":
                    return val >= rule.value
                if rule.op == "<":
                    return val < rule.value
                if rule.op == "<=":
                    return val <= rule.value
                if rule.op == "==":
                    return val == rule.value
                if rule.op == "!=":
                    return val != rule.value
                return False
            if all(check_rule(r) for r in rules):
                matched.append(sym)
        except Exception:
            skipped += 1
            continue
    return AutoScreenOut(matched=sorted(set(matched)), evaluated=len(symbols), fetched=fetched, skipped=skipped)


# --- Dataset Builder for Models (training/backtest datasets) ---
class DatasetBuildRequest(BaseModel):
    model_id: str
    version: Optional[int] = None  # latest published if not provided
    # Universe overrides (else derive from model scope)
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    symbols: Optional[List[str]] = None
    # Timeframe/date overrides (else use spec.timeframe and training_cfg.data_window)
    timeframe: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    cap: Optional[int] = 50
    include_labels: bool = True
    output: Optional[str] = "summary"  # summary|csv
    out_dir: Optional[str] = "data_dumps"


class DatasetBuildOut(BaseModel):
    run_id: Optional[str] = None
    model_id: str
    version: int
    timeframe: str
    symbols: int
    rows: int
    features: int
    wrote_path: Optional[str] = None


def _get_latest_model_version(cur, model_id: str) -> Optional[int]:
    cur.execute("SELECT version FROM sc.v_model_specs_published WHERE model_id=%s", (model_id,))
    r = cur.fetchone()
    return r[0] if r else None


def _load_model_spec(cur, model_id: str, version: int) -> Dict[str, Any]:
    cur.execute(
        """
        SELECT model_id, version, status, timeframe, market, instrument,
               featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
               scope, training_cfg
        FROM sc.model_specs WHERE model_id=%s AND version=%s
        """,
        (model_id, version),
    )
    r = cur.fetchone()
    if not r:
        raise HTTPException(status_code=404, detail="model not found")
    cols = [d[0] for d in cur.description]
    return dict(zip(cols, r))


def _resolve_symbols_for_model(scope: Optional[Dict[str, Any]], override: Dict[str, Any], user: User) -> List[str]:
    # Priority: explicit symbols > preset_id/watchlist_id > scope.allow_presets/allow_symbols
    if override.get("symbols"):
        return list(dict.fromkeys([str(s).upper() for s in override["symbols"]]))
    sym: List[str] = []
    if override.get("preset_id") or override.get("watchlist_id"):
        # Reuse universe resolver
        req = UniverseRequest(preset_id=override.get("preset_id"), watchlist_id=override.get("watchlist_id"), cap=override.get("cap"))
        return resolve_universe(req, user)  # type: ignore[arg-type]
    if scope:
        t = scope.get("type")
        if t == "cohort" and scope.get("allow_presets"):
            # Take first preset and resolve
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol", (scope["allow_presets"][0],))
                    sym = [r[0] for r in cur.fetchall()]
        elif t == "per_ticker" and scope.get("allow_symbols"):
            sym = [str(s).upper() for s in scope["allow_symbols"]]
    return sym


def _build_fb_for_featureset(cur, featureset: Dict[str, Any]) -> FeatureBuilder:
    # Build FeatureBuilder from featureset config: set_id+version | strategy_id+version | indicators[]
    if featureset.get("set_id"):
        set_id = featureset["set_id"]
        set_version = int(featureset.get("version") or 1)
        # Build from DB set components
        payload = AutoSetFeaturesRequest(set_id=set_id, version=set_version, timeframe="day")  # timeframe unused here
        # reuse code path to load components
        with get_db() as conn:
            with conn.cursor() as cur2:
                cur2.execute(
                    "SELECT indicator_id, indicator_version, params FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord",
                    (set_id, set_version),
                )
                comps = cur2.fetchall()
        fb_set = FBIndicatorSet(name=str(set_id), version=int(set_version), description="from_registry", indicators=[FBIndicatorSpec(name=rr[0], version=int(rr[1] or 1), params=(rr[2] or {})) for rr in comps])
        return FeatureBuilder(indicator_set=fb_set)
    if featureset.get("strategy_id"):
        sid = featureset["strategy_id"]
        sver = int(featureset.get("strategy_version") or 1)
        fb_set = _build_fb_set_for_strategy(sid, sver)
        return FeatureBuilder(indicator_set=fb_set)
    if featureset.get("indicators"):
        inds = [FBIndicatorSpec(name=i.get("id"), version=int(i.get("version") or 1), params=(i.get("params") or {})) for i in featureset.get("indicators") or []]
        fb_set = FBIndicatorSet(name="synthetic", version=1, description="synthetic", indicators=inds)
        return FeatureBuilder(indicator_set=fb_set)
    raise HTTPException(status_code=400, detail="invalid featureset config")


def _compute_labels_stock(df: pd.DataFrame, tp_pct: float, sl_pct: float, max_hold: int) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)
    if not {"close", "high", "low"}.issubset(df.columns):
        out["label"] = None
        out["outcome"] = None
        out["realized_return"] = 0.0
        return out
    close = df["close"].astype(float).values
    high = df["high"].astype(float).values
    low = df["low"].astype(float).values
    n = len(df)
    H = int(max(1, max_hold))
    label = [None]*n
    outcome = [None]*n
    realized = [0.0]*n
    for i in range(n):
        entry = close[i]
        tp = entry * (1.0 + tp_pct/100.0)
        sl = entry * (1.0 - sl_pct/100.0)
        hit_tp_at = None
        hit_sl_at = None
        last = min(n-1, i+H)
        k = i+1
        while k <= last:
            if hit_tp_at is None and high[k] >= tp:
                hit_tp_at = k
            if hit_sl_at is None and low[k] <= sl:
                hit_sl_at = k
            if hit_tp_at is not None or hit_sl_at is not None:
                # if both happened same bar, treat whichever check found first
                break
            k += 1
        if hit_tp_at is not None and (hit_sl_at is None or hit_tp_at <= hit_sl_at):
            label[i] = 1
            outcome[i] = "tp_hit"
            realized[i] = (tp - entry) / entry
        elif hit_sl_at is not None and (hit_tp_at is None or hit_sl_at < hit_tp_at):
            label[i] = 0
            outcome[i] = "sl_hit"
            realized[i] = (sl - entry) / entry
        else:
            label[i] = 0
            outcome[i] = "max_hold"
            realized[i] = (close[last] - entry) / entry
    out["label"] = label
    out["outcome"] = outcome
    out["realized_return"] = realized
    return out


@app.post(
    "/models/dataset/build",
    response_model=DatasetBuildOut,
    summary="Build dataset for a model (training/backtest)",
    description="Resolves cohort, fetches bars, computes features using the model's featureset, and optionally generates stock labels. Writes CSV if requested and records a training run."
)
def build_model_dataset(
    payload: DatasetBuildRequest = Body(
        ..., example={
            "model_id": "sq_macd_trend_pullback_5m",
            "timeframe": "5m",
            "preset_id": "liquid_etfs",
            "start_date": "2024-06-01",
            "end_date": "2024-06-15",
            "cap": 10,
            "include_labels": True,
            "output": "csv",
            "out_dir": "data_dumps"
        }
    ),
    user: User = Depends(get_current_user)
):
    with get_db() as conn:
        with conn.cursor() as cur:
            ver = payload.version
            if ver is None:
                ver = _get_latest_model_version(cur, payload.model_id)
                if ver is None:
                    raise HTTPException(status_code=404, detail="no published version for model")
            spec = _load_model_spec(cur, payload.model_id, int(ver))
    timeframe = payload.timeframe or spec.get("timeframe") or "day"
    # Dates
    if payload.start_date and payload.end_date:
        sd, ed = payload.start_date, payload.end_date
    else:
        tc = spec.get("training_cfg") or {}
        win = tc.get("data_window") or {}
        sd, ed = win.get("start"), win.get("end")
        if not sd or not ed:
            sd, ed = _default_dates()
    # Symbols
    symbols = _resolve_symbols_for_model(spec.get("scope"), payload.dict(), user)
    if not symbols:
        raise HTTPException(status_code=400, detail="no symbols resolved; provide preset/watchlist/symbols or model scope")
    # Novice caps: 90 days and 50 symbols
    try:
        from datetime import datetime as _dt
        if (_dt.strptime(ed, "%Y-%m-%d") - _dt.strptime(sd, "%Y-%m-%d")).days > 90:
            raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    except Exception:
        pass
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:min(cap, 50)]
    # Feature builder
    fb = _build_fb_for_featureset(None, spec.get("featureset") or {})
    rows_total = 0
    feats_cols: set[str] = set()
    frames: List[pd.DataFrame] = []
    # Label cfg
    lc = spec.get("label_cfg") or {}
    tp_pct = float(lc.get("tp_pct") or 0.0)
    sl_pct = float(lc.get("sl_pct") or 0.0)
    max_hold = int(lc.get("max_hold_bars") or 0)
    for sym in symbols:
        df = _fetch_bars(sym, timeframe, sd, ed)
        if df is None or df.empty:
            continue
        # Ensure expected columns
        # df already has 'date','open','high','low','close','volume'
        fdf = fb.add_indicator_features(df)
        new_cols = [c for c in fdf.columns if c not in df.columns]
        feats_cols.update(new_cols)
        res = fdf.copy()
        if payload.include_labels and tp_pct > 0 and sl_pct > 0 and max_hold > 0:
            lbl = _compute_labels_stock(res, tp_pct, sl_pct, max_hold)
            res = pd.concat([res, lbl], axis=1)
        res.insert(0, "symbol", sym)
        rows_total += len(res)
        frames.append(res)
    if not frames:
        raise HTTPException(status_code=400, detail="no data computed for symbols/timeframe/date range")
    out_df = pd.concat(frames, axis=0, ignore_index=True)
    # Optional CV fold assignment
    if payload.fold_count and int(payload.fold_count) > 1:
        try:
            import numpy as _np  # type: ignore
        except Exception:
            raise HTTPException(status_code=400, detail="fold assignment requires numpy; please install it")
        k = int(payload.fold_count)
        gap = int(payload.gap_bars or 0)
        if 'date' in out_df.columns:
            out_df.sort_values(['symbol','date'], inplace=True, kind='mergesort')
        else:
            out_df.sort_values(['symbol'], inplace=True, kind='mergesort')
        folds: List[int] = []
        for _, g in out_df.groupby('symbol', sort=False):
            n = len(g)
            if n <= k:
                f = list(range(min(n, k))) + [k-1]*(max(0, n-k))
            else:
                edges = (_np.linspace(0, n, k+1)).astype(int)
                ff = _np.zeros(n, dtype=int)
                for i in range(k):
                    start = edges[i]
                    end = edges[i+1]
                    ff[start:end] = i
                    if gap > 0 and i < k-1:
                        ff[max(start, end-gap):end] = -1
                f = ff.tolist()
            folds.extend(f)
        out_df['fold'] = folds

    wrote_path = None
    run_id = None
    _out = (payload.output or "").lower()
    if _out == "csv":
        out_dir = payload.out_dir or "data_dumps"
        os.makedirs(out_dir, exist_ok=True)
        fname = f"dataset_{payload.model_id}_v{ver}_{timeframe}_{sd}_{ed}.csv".replace(':','-')
        path = os.path.join(out_dir, fname)
        out_df.to_csv(path, index=False)
        wrote_path = path
        # hash file
        try:
            h = hashlib.sha1(Path(path).read_bytes()).hexdigest()
        except Exception:
            h = None
        # record training run
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO sc.model_training_runs (model_id, model_version, status, training_cfg, data_window, dataset_hash, features_hash, git_sha, metrics, started_at, finished_at)
                        VALUES (%s,%s,'success',%s,%s,%s,%s,%s,%s,NOW(),NOW())
                        RETURNING train_id
                        """,
                        (
                            payload.model_id,
                            int(ver),
                            json.dumps(spec.get("training_cfg") or {}),
                            json.dumps({"start": sd, "end": ed}),
                            h,
                            None,
                            None,
                            json.dumps({"rows": len(out_df), "symbols": len(symbols)}),
                        ),
                    )
                    run_id = cur.fetchone()[0]
                    conn.commit()
        except Exception:
            run_id = None
    elif _out == "parquet":
        try:
            import pyarrow as _pa  # noqa: F401
            import pyarrow.parquet as _pq  # noqa: F401
        except Exception:
            raise HTTPException(status_code=400, detail="parquet output requires pyarrow; please install it")
        out_dir = payload.out_dir or "data_dumps"
        os.makedirs(out_dir, exist_ok=True)
        fname = f"dataset_{payload.model_id}_v{ver}_{timeframe}_{sd}_{ed}.parquet".replace(':','-')
        path = os.path.join(out_dir, fname)
        try:
            out_df.to_parquet(path, index=False)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"failed to write parquet: {e}")
        wrote_path = path
        try:
            h = hashlib.sha1(Path(path).read_bytes()).hexdigest()
        except Exception:
            h = None
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO sc.model_training_runs (model_id, model_version, status, training_cfg, data_window, dataset_hash, features_hash, git_sha, metrics, started_at, finished_at)
                        VALUES (%s,%s,'success',%s,%s,%s,%s,%s,%s,NOW(),NOW())
                        RETURNING train_id
                        """,
                        (
                            payload.model_id,
                            int(ver),
                            json.dumps(spec.get("training_cfg") or {}),
                            json.dumps({"start": sd, "end": ed}),
                            h,
                            None,
                            None,
                            json.dumps({"rows": len(out_df), "symbols": len(symbols)}),
                        ),
                    )
                    run_id = cur.fetchone()[0]
                    conn.commit()
        except Exception:
            run_id = None
    return DatasetBuildOut(
        run_id=str(run_id) if run_id else None,
        model_id=payload.model_id,
        version=int(ver),
        timeframe=timeframe,
        symbols=len(symbols),
        rows=rows_total,
        features=len(feats_cols),
        wrote_path=wrote_path,
    )


# --- Recipes runner (Simple Mode) ---
class RecipeRunRequest(BaseModel):
    recipe_id: str
    # Optional overrides
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    timeframe: Optional[str] = None
    cap: Optional[int] = None
    params_override: Optional[Dict[str, Any]] = None
    rule_expr: Optional[str] = None
    rules: Optional[List[ScreenRule]] = None


@app.post("/recipes/run", response_model=AutoScreenOut, summary="Run a screen recipe", description="Executes a Simple Mode recipe using cached Polygon data and AND rules.")
def run_recipe(payload: RecipeRunRequest = Body(..., example={"recipe_id":"macd_trend_pullback_screen_5m","preset_id":"sp500","rule_expr":"macd_hist_12_26_9 > 0 and rsi_14 < 70","cap":50}), user: User = Depends(get_current_user)):
    # Load recipe definition
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT target_kind, target_id, target_version, defaults, guardrails, universe_preset
                FROM sc.v_simple_recipes_published WHERE recipe_id = %s
                """,
                (payload.recipe_id,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="recipe not found")
            target_kind, target_id, target_version, defaults, guardrails, universe_preset = row
    defaults = defaults or {}
    guardrails = guardrails or {}
    op = (defaults.get("operation") or "screen").lower()
    if op != "screen":
        raise HTTPException(status_code=501, detail="Only screen recipes are supported right now")

    # Resolve universe and settings
    cap = int(payload.cap or guardrails.get("universe_cap") or 50)
    tf = payload.timeframe or defaults.get("timeframe") or "day"
    preset_id = payload.preset_id or universe_preset
    watchlist_id = payload.watchlist_id
    if not preset_id and not watchlist_id:
        raise HTTPException(status_code=400, detail="preset_id or watchlist_id required (or set in recipe)")

    # Merge params
    params = dict(defaults.get("params") or {})
    if payload.params_override:
        params.update(payload.params_override)

    # Build rules
    rules: List[ScreenRule] = []
    if payload.rules:
        rules = payload.rules
    elif payload.rule_expr:
        try:
            rules = _parse_rules(payload.rule_expr)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"invalid rule_expr: {e}")
    # If still no rules, require the caller to provide them (we don't infer generic indicator rules)
    if not rules:
        raise HTTPException(status_code=400, detail="rules or rule_expr required for screening")

    # Dispatch by target_kind
    if target_kind == "indicator":
        # Use auto screen for single indicator
        req = AutoScreenRequest(
            preset_id=preset_id,
            watchlist_id=watchlist_id,
            cap=cap,
            timeframe=tf,
            name=str(target_id),
            params=params,
            rule=rules[0] if len(rules) == 1 else None,  # placeholder; we'll route to set/strategy path below if multiple
        )
        if len(rules) == 1 and req.rule is not None:
            return screen_auto(req, user)  # type: ignore[arg-type]
        else:
            # For multiple conditions, compute indicator into a pseudo set pipeline and AND rules
            # Reuse indicator_set_auto_screen with a synthetic set containing this indicator
            syn_set = FBIndicatorSet(name=str(target_id), version=int(target_version or 1), description="recipe_synth", indicators=[FBIndicatorSpec(name=str(target_id), version=int(target_version or 1), params=params)])
            # Save to local scope only; we will compute inline below
            symbols = _resolve_universe_symbols(preset_id, watchlist_id, user)
            symbols = symbols[:cap]
            fb = FeatureBuilder(indicator_set=syn_set)
            matched: List[str] = []
            fetched = 0
            skipped = 0
            start_date, end_date = _default_dates()
            for sym in symbols:
                try:
                    df = _fetch_bars(sym, tf, start_date, end_date)
                    if df is None or df.empty:
                        skipped += 1
                        continue
                    fetched += 1
                    out_df = fb.add_indicator_features(df)
                    new_cols = [c for c in out_df.columns if c not in df.columns]
                    if not new_cols:
                        skipped += 1
                        continue
                    last = out_df.iloc[-1]
                    def ok(rule: ScreenRule) -> bool:
                        col = rule.column if rule.column in out_df.columns else (new_cols[0] if len(new_cols) == 1 else None)
                        if not col:
                            return False
                        try:
                            val = float(last[col])
                        except Exception:
                            return False
                        return (
                            (rule.op == ">" and val > rule.value)
                            or (rule.op == ">=" and val >= rule.value)
                            or (rule.op == "<" and val < rule.value)
                            or (rule.op == "<=" and val <= rule.value)
                            or (rule.op == "==" and val == rule.value)
                            or (rule.op == "!=" and val != rule.value)
                        )
                    if all(ok(r) for r in rules):
                        matched.append(sym)
                except Exception:
                    skipped += 1
                    continue
            return AutoScreenOut(matched=sorted(set(matched)), evaluated=len(symbols), fetched=fetched, skipped=skipped)

    elif target_kind == "indicator_set":
        return indicator_set_auto_screen(
            AutoSetScreenRequest(
                preset_id=preset_id,
                watchlist_id=watchlist_id,
                cap=cap,
                timeframe=tf,
                start_date=None,
                end_date=None,
                set_id=str(target_id),
                version=int(target_version or 1),
                rules=rules,
            ),
            user,
        )
    elif target_kind == "strategy":
        return strategy_auto_screen(
            AutoStrategyScreenRequest(
                preset_id=preset_id,
                watchlist_id=watchlist_id,
                cap=cap,
                timeframe=tf,
                start_date=None,
                end_date=None,
                strategy_id=str(target_id),
                version=int(target_version or 1),
                rules=rules,
            ),
            user,
        )
    else:
        raise HTTPException(status_code=400, detail=f"unsupported recipe target_kind: {target_kind}")


# --- Workflows runner ---
class WorkflowRunRequest(BaseModel):
    workflow_id: str
    # Shared overrides
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    timeframe: Optional[str] = None
    cap: Optional[int] = None


class WorkflowStepResult(BaseModel):
    index: int
    kind: str
    matched: List[str]
    evaluated: int
    fetched: int
    skipped: int


class WorkflowRunOut(BaseModel):
    workflow_id: str
    results: List[WorkflowStepResult]


@app.post("/workflows/run", response_model=WorkflowRunOut, summary="Run a workflow with screen-style steps", description="Runs indicator, indicator_set, and strategy steps with optional per-step overrides for preset/watchlist, timeframe, and cap.")
def run_workflow(payload: WorkflowRunRequest = Body(..., example={"workflow_id":"breakout_pullback_scan_5m_v1","preset_id":"sp500","timeframe":"5m","cap":50}), user: User = Depends(get_current_user)):
    # Load workflow steps
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT steps FROM sc.v_workflows_published WHERE workflow_id = %s",
                (payload.workflow_id,),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="workflow not found")
            steps = row[0] or []
    if not isinstance(steps, list) or not steps:
        raise HTTPException(status_code=400, detail="workflow has no runnable steps")

    results: List[WorkflowStepResult] = []
    # Defaults
    base_cap = int(payload.cap or 50)
    base_tf = payload.timeframe or "day"
    preset_id = payload.preset_id
    watchlist_id = payload.watchlist_id

    for idx, step in enumerate(steps):
        try:
            if not isinstance(step, dict):
                continue
            kind = str(step.get("kind") or step.get("type") or "").lower()
            tf = str(step.get("timeframe") or base_tf)
            cap = int(step.get("cap") or base_cap)
            # Per-step universe overrides (fallback to request-level overrides)
            step_preset_id = step.get("preset_id") or preset_id
            step_watchlist_id = step.get("watchlist_id") or watchlist_id

            if kind == "indicator":
                name = str(step.get("name") or step.get("indicator") or "")
                if not name:
                    continue
                params = step.get("params") or {}
                # rule can be string or object
                r_expr = step.get("rule_expr") or step.get("rule") if isinstance(step.get("rule"), str) else None
                r_obj = step.get("rule") if isinstance(step.get("rule"), dict) else None
                rule: Optional[ScreenRule] = None
                if r_obj:
                    rule = ScreenRule(**r_obj)
                elif r_expr:
                    rs = _parse_rules(str(r_expr))
                    rule = rs[0] if rs else None
                if not rule:
                    # Skip step if no rule
                    continue
                req = AutoScreenRequest(
                    preset_id=step_preset_id,
                    watchlist_id=step_watchlist_id,
                    cap=cap,
                    timeframe=tf,
                    name=name,
                    params=params,
                    rule=rule,
                )
                out = screen_auto(req, user)  # type: ignore[arg-type]
                results.append(WorkflowStepResult(index=idx, kind="indicator", matched=out.matched, evaluated=out.evaluated, fetched=out.fetched, skipped=out.skipped))
                continue

            if kind in ("indicator_set", "set"):
                set_id = str(step.get("set_id") or step.get("id") or "")
                version = int(step.get("version") or 1)
                # rules: accept rule_expr string or rules list
                r_expr = step.get("rule_expr") or step.get("rules") if isinstance(step.get("rules"), str) else None
                rules_list = step.get("rules") if isinstance(step.get("rules"), list) else None
                rules: List[ScreenRule] = []
                if rules_list:
                    rules = [ScreenRule(**r) for r in rules_list]
                elif r_expr:
                    rules = _parse_rules(str(r_expr))
                if not rules:
                    continue
                out = indicator_set_auto_screen(
                    AutoSetScreenRequest(
                        preset_id=step_preset_id,
                        watchlist_id=step_watchlist_id,
                        cap=cap,
                        timeframe=tf,
                        set_id=set_id,
                        version=version,
                        rules=rules,
                    ),
                    user,
                )
                results.append(WorkflowStepResult(index=idx, kind="indicator_set", matched=out.matched, evaluated=out.evaluated, fetched=out.fetched, skipped=out.skipped))
                continue

            if kind == "strategy":
                strategy_id = str(step.get("strategy_id") or step.get("id") or "")
                version = int(step.get("version") or 1)
                r_expr = step.get("rule_expr") or step.get("rules") if isinstance(step.get("rules"), str) else None
                rules_list = step.get("rules") if isinstance(step.get("rules"), list) else None
                rules: List[ScreenRule] = []
                if rules_list:
                    rules = [ScreenRule(**r) for r in rules_list]
                elif r_expr:
                    rules = _parse_rules(str(r_expr))
                if not rules:
                    continue
                out = strategy_auto_screen(
                    AutoStrategyScreenRequest(
                        preset_id=step_preset_id,
                        watchlist_id=step_watchlist_id,
                        cap=cap,
                        timeframe=tf,
                        strategy_id=strategy_id,
                        version=version,
                        rules=rules,
                    ),
                    user,
                )
                results.append(WorkflowStepResult(index=idx, kind="strategy", matched=out.matched, evaluated=out.evaluated, fetched=out.fetched, skipped=out.skipped))
                continue

            # Unknown kind: skip
            continue
        except Exception:
            # Skip failing steps; continue to next
            continue

    if not results:
        raise HTTPException(status_code=400, detail="no runnable steps with rules found in workflow")
    return WorkflowRunOut(workflow_id=payload.workflow_id, results=results)


# --- Auto features and screening for strategies (merge linked indicator sets) ---
class AutoStrategyBase(BaseModel):
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    cap: Optional[int] = 50
    timeframe: str = "day"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    strategy_id: str
    version: int


class AutoStrategyFeaturesOut(BaseModel):
    evaluated: int
    fetched: int
    skipped: int
    columns: List[str]
    data: List[AutoSetFeaturesRow]


def _build_fb_set_for_strategy(strategy_id: str, version: int) -> FBIndicatorSet:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT title FROM sc.strategies WHERE strategy_id=%s AND version=%s",
                (strategy_id, version),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="strategy not found")
            desc = r[0] or ""
            cur.execute(
                "SELECT set_id, set_version FROM sc.strategy_indicator_sets WHERE strategy_id=%s AND strategy_version=%s",
                (strategy_id, version),
            )
            links = cur.fetchall() or []
            if not links:
                # Strategy without sets is allowed; return empty indicator set
                return FBIndicatorSet(name=strategy_id, version=int(version), description=str(desc), indicators=[])
            # Gather all components from linked sets
            seen: set[tuple[str, int, str]] = set()
            specs: List[FBIndicatorSpec] = []
            for sid, sver in links:
                cur.execute(
                    "SELECT indicator_id, indicator_version, params FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord",
                    (sid, sver),
                )
                for ind_id, ind_ver, params in cur.fetchall():
                    key = (str(ind_id), int(ind_ver or 1), json.dumps(params or {}, sort_keys=True))
                    if key in seen:
                        continue
                    seen.add(key)
                    specs.append(FBIndicatorSpec(name=str(ind_id), version=int(ind_ver or 1), params=(params or {})))
    return FBIndicatorSet(name=strategy_id, version=int(version), description=str(desc), indicators=specs)


def _resolve_universe_symbols(preset_id: Optional[str], watchlist_id: Optional[str], user: User) -> List[str]:
    with get_db() as conn:
        with conn.cursor() as cur:
            if preset_id:
                cur.execute("SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol", (preset_id,))
                return [r[0] for r in cur.fetchall()]
            cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id=%s AND user_id=%s", (watchlist_id, user.user_id))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="watchlist not found")
            cur.execute("SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol", (watchlist_id,))
            return [r[0] for r in cur.fetchall()]


@app.post("/strategies/auto_build", response_model=AutoStrategyFeaturesOut, summary="Build features for a strategy (merged sets)", description="Merges all sets linked to the strategy, fetches bars via Polygon, computes features, and returns last-row values.")
def strategy_auto_build(payload: AutoStrategyBase, user: User = Depends(get_current_user)):
    if not payload.preset_id and not payload.watchlist_id:
        raise HTTPException(status_code=400, detail="preset_id or watchlist_id required")
    start_date, end_date = payload.start_date, payload.end_date
    if not start_date or not end_date:
        start_date, end_date = _default_dates()
    # Novice cap: 90-day window
    if _days_between(start_date, end_date) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    symbols = _resolve_universe_symbols(payload.preset_id, payload.watchlist_id, user)
    # Novice caps: 90 days and 50 symbols
    try:
        from datetime import datetime as _dt
        if (_dt.strptime(ed, "%Y-%m-%d") - _dt.strptime(sd, "%Y-%m-%d")).days > 90:
            raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    except Exception:
        pass
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:min(cap, 50)]

    fb_set = _build_fb_set_for_strategy(payload.strategy_id, payload.version)
    fb = FeatureBuilder(indicator_set=fb_set)

    fetched = 0
    skipped = 0
    cols_union: set[str] = set()
    rows: List[AutoSetFeaturesRow] = []

    for sym in symbols:
        try:
            df = _fetch_bars(sym, payload.timeframe, start_date, end_date)
            if df is None or df.empty:
                skipped += 1
                continue
            fetched += 1
            out_df = fb.add_indicator_features(df)
            new_cols = [c for c in out_df.columns if c not in df.columns]
            if not new_cols:
                skipped += 1
                continue
            cols_union.update(new_cols)
            last = out_df.iloc[-1]
            features = {c: float(last[c]) if c in out_df.columns else None for c in new_cols}
            rows.append(AutoSetFeaturesRow(symbol=sym, features=features))
        except Exception:
            skipped += 1
            continue

    return AutoStrategyFeaturesOut(
        evaluated=len(symbols),
        fetched=fetched,
        skipped=skipped,
        columns=sorted(cols_union),
        data=rows,
    )


class AutoStrategyScreenRequest(AutoStrategyBase):
    rule_expr: Optional[str] = None
    rules: Optional[List[ScreenRule]] = None


@app.post("/strategies/auto_screen", response_model=AutoScreenOut, summary="Screen a strategy by applying rules", description="Resolves universe, fetches bars via Polygon, computes merged strategy features, and applies ANDed rules on the latest values.")
def strategy_auto_screen(payload: AutoStrategyScreenRequest, user: User = Depends(get_current_user)):
    if not payload.preset_id and not payload.watchlist_id:
        raise HTTPException(status_code=400, detail="preset_id or watchlist_id required")
    start_date, end_date = payload.start_date, payload.end_date
    if not start_date or not end_date:
        start_date, end_date = _default_dates()
    # Novice cap: 90-day window
    if _days_between(start_date, end_date) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    rules: List[ScreenRule] = []
    if payload.rules:
        rules = payload.rules
    elif payload.rule_expr:
        try:
            rules = _parse_rules(payload.rule_expr)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"invalid rule_expr: {e}")
    else:
        raise HTTPException(status_code=400, detail="rules or rule_expr required")

    symbols = _resolve_universe_symbols(payload.preset_id, payload.watchlist_id, user)
    # Novice caps: 90 days and 50 symbols
    try:
        from datetime import datetime as _dt
        if (_dt.strptime(ed, "%Y-%m-%d") - _dt.strptime(sd, "%Y-%m-%d")).days > 90:
            raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    except Exception:
        pass
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:min(cap, 50)]

    fb_set = _build_fb_set_for_strategy(payload.strategy_id, payload.version)
    fb = FeatureBuilder(indicator_set=fb_set)

    matched: List[str] = []
    fetched = 0
    skipped = 0

    for sym in symbols:
        try:
            df = _fetch_bars(sym, payload.timeframe, start_date, end_date)
            if df is None or df.empty:
                skipped += 1
                continue
            fetched += 1
            out_df = fb.add_indicator_features(df)
            new_cols = [c for c in out_df.columns if c not in df.columns]
            if not new_cols:
                skipped += 1
                continue
            last = out_df.iloc[-1]
            def check_rule(rule: ScreenRule) -> bool:
                col = rule.column if rule.column in out_df.columns else None
                if col is None:
                    if len(new_cols) == 1:
                        col = new_cols[0]
                    else:
                        return False
                try:
                    val = float(last[col])
                except Exception:
                    return False
                if rule.op == ">":
                    return val > rule.value
                if rule.op == ">=":
                    return val >= rule.value
                if rule.op == "<":
                    return val < rule.value
                if rule.op == "<=":
                    return val <= rule.value
                if rule.op == "==":
                    return val == rule.value
                if rule.op == "!=":
                    return val != rule.value
                return False
            if all(check_rule(r) for r in rules):
                matched.append(sym)
        except Exception:
            skipped += 1
            continue
    return AutoScreenOut(matched=sorted(set(matched)), evaluated=len(symbols), fetched=fetched, skipped=skipped)

# --- Catalog endpoints (read-only) ---
@app.get("/catalog/indicators", response_model=List[IndicatorOut])
def list_indicators(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    search: Optional[str] = Query(default=None, min_length=2),
    novice_only: bool = Query(default=False),
    fields: str = Query(default="summary", regex="^(summary|full)$"),
):
    if fields == "full":
        select_cols = (
            "SELECT id, version, status, title, category, subcategory, beginner_summary, novice_ready, "
            "measures, data_requirements, usage, performance_hints"
        )
    else:
        select_cols = (
            "SELECT id, version, status, title, category, subcategory, beginner_summary, novice_ready"
        )
    sql = [select_cols, "FROM sc.v_indicators_published", "WHERE 1=1"]
    params: List[object] = []
    if category:
        sql.append("AND category = %s"); params.append(category)
    if subcategory:
        sql.append("AND subcategory = %s"); params.append(subcategory)
    if search:
        sql.append("AND (id ILIKE %s OR title ILIKE %s)"); params.extend([f"%{search}%", f"%{search}%"])
    if novice_only:
        sql.append("AND novice_ready = TRUE")
    sql.append("ORDER BY id")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(" ".join(sql), params)
            rows = cur.fetchall()
            out = []
            for r in rows:
                base = {
                    "id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "category": r[4],
                    "subcategory": r[5],
                    "beginner_summary": r[6],
                }
                if fields == "full":
                    base["details"] = {
                        "measures": r[8],
                        "data_requirements": r[9],
                        "usage": r[10],
                        "performance_hints": r[11],
                    }
                out.append(IndicatorOut(**base))
            return out


@app.get("/catalog/indicator/{indicator_id}", response_model=IndicatorOut)
def get_indicator(indicator_id: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, version, status, title, category, subcategory
                FROM sc.v_indicators_published WHERE id = %s
                """,
                (indicator_id,),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="indicator not found")
            return IndicatorOut(id=r[0], version=r[1], status=r[2], title=r[3], category=r[4], subcategory=r[5])


@app.get("/catalog/indicator_sets", response_model=List[IndicatorSetOut])
def list_indicator_sets(
    search: Optional[str] = Query(default=None, min_length=2),
    novice_only: bool = Query(default=False),
    fields: str = Query(default="summary", regex="^(summary|full)$"),
):
    if fields == "full":
        select_cols = (
            "SELECT set_id, version, status, title, purpose, beginner_summary, novice_ready, "
            "reading_guide, data_requirements, performance_hints, anti_patterns"
        )
    else:
        select_cols = (
            "SELECT set_id, version, status, title, purpose, beginner_summary, novice_ready"
        )
    sql = [select_cols, "FROM sc.v_indicator_sets_published", "WHERE 1=1"]
    params: List[object] = []
    if search:
        sql.append("AND (set_id ILIKE %s OR title ILIKE %s)"); params.extend([f"%{search}%", f"%{search}%"])
    if novice_only:
        sql.append("AND novice_ready = TRUE")
    sql.append("ORDER BY set_id")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(" ".join(sql), params)
            rows = cur.fetchall()
            out = []
            for r in rows:
                base = {
                    "set_id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "purpose": r[4],
                    "beginner_summary": r[5],
                }
                if fields == "full":
                    base["details"] = {
                        "reading_guide": r[7],
                        "data_requirements": r[8],
                        "performance_hints": r[9],
                        "anti_patterns": r[10],
                    }
                out.append(IndicatorSetOut(**base))
            return out


@app.get("/catalog/indicator_set/{set_id}", response_model=IndicatorSetOut)
def get_indicator_set(set_id: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT set_id, version, status, title, purpose, beginner_summary, novice_ready FROM sc.v_indicator_sets_published WHERE set_id = %s",
                (set_id,),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="indicator set not found")
            return IndicatorSetOut(set_id=r[0], version=r[1], status=r[2], title=r[3], purpose=r[4])


@app.get("/catalog/strategies", response_model=List[StrategyOut])
def list_strategies(
    search: Optional[str] = Query(default=None, min_length=2),
    novice_only: bool = Query(default=False),
    fields: str = Query(default="summary", regex="^(summary|full)$"),
):
    if fields == "full":
        select_cols = (
            "SELECT strategy_id, version, status, title, objective, beginner_summary, novice_ready, "
            "entry_logic, exit_logic, risk, execution_policy, performance_snapshot"
        )
    else:
        select_cols = (
            "SELECT strategy_id, version, status, title, objective, beginner_summary, novice_ready"
        )
    sql = [select_cols, "FROM sc.v_strategies_published", "WHERE 1=1"]
    params: List[object] = []
    if search:
        sql.append("AND (strategy_id ILIKE %s OR title ILIKE %s)"); params.extend([f"%{search}%", f"%{search}%"])
    if novice_only:
        sql.append("AND novice_ready = TRUE")
    sql.append("ORDER BY strategy_id")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(" ".join(sql), params)
            rows = cur.fetchall()
            out: List[StrategyOut] = []
            for r in rows:
                base = {
                    "strategy_id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "objective": r[4],
                    "beginner_summary": r[5],
                }
                if fields == "full":
                    base["details"] = {
                        "entry_logic": r[7],
                        "exit_logic": r[8],
                        "risk": r[9],
                        "execution_policy": r[10],
                        "performance_snapshot": r[11],
                    }
                out.append(StrategyOut(**base))
            return out


@app.get("/catalog/strategy/{strategy_id}", response_model=StrategyOut)
def get_strategy(strategy_id: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT strategy_id, version, status, title, objective, beginner_summary, novice_ready FROM sc.v_strategies_published WHERE strategy_id = %s",
                (strategy_id,),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="strategy not found")
            return StrategyOut(strategy_id=r[0], version=r[1], status=r[2], title=r[3], objective=r[4])


@app.get("/catalog/workflows", response_model=List[WorkflowOut])
def list_workflows(
    search: Optional[str] = Query(default=None, min_length=2),
    persona: Optional[str] = None,
    novice_only: bool = Query(default=False),
    fields: str = Query(default="summary", regex="^(summary|full)$"),
):
    if fields == "full":
        select_cols = (
            "SELECT workflow_id, version, status, title, subtitle, time_to_complete, beginner_summary, novice_ready, "
            "goal, persona, steps, outputs"
        )
    else:
        select_cols = (
            "SELECT workflow_id, version, status, title, subtitle, time_to_complete, beginner_summary, novice_ready"
        )
    sql = [select_cols, "FROM sc.v_workflows_published", "WHERE 1=1"]
    params: List[object] = []
    if persona:
        sql.append("AND persona = %s"); params.append(persona)
    if search:
        sql.append("AND (workflow_id ILIKE %s OR title ILIKE %s)"); params.extend([f"%{search}%", f"%{search}%"])
    if novice_only:
        sql.append("AND novice_ready = TRUE")
    sql.append("ORDER BY workflow_id")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(" ".join(sql), params)
            rows = cur.fetchall()
            out: List[WorkflowOut] = []
            for r in rows:
                base = {
                    "workflow_id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "subtitle": r[4],
                    "time_to_complete": r[5],
                    "beginner_summary": r[6],
                }
                if fields == "full":
                    base["details"] = {
                        "goal": r[8],
                        "persona": r[9],
                        "steps": r[10],
                        "outputs": r[11],
                    }
                out.append(WorkflowOut(**base))
            return out


@app.get("/catalog/workflow/{workflow_id}", response_model=WorkflowOut)
def get_workflow(workflow_id: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT workflow_id, version, status, title, subtitle, time_to_complete FROM sc.v_workflows_published WHERE workflow_id = %s",
                (workflow_id,),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="workflow not found")
            return WorkflowOut(workflow_id=r[0], version=r[1], status=r[2], title=r[3], subtitle=r[4], time_to_complete=r[5])


@app.get("/recipes", response_model=List[RecipeOut])
def list_recipes(persona: Optional[str] = None, limit: int = 50):
    with get_db() as conn:
        with conn.cursor() as cur:
            if persona:
                cur.execute(
                    """
                    SELECT recipe_id, version, status, title, beginner_summary, target_kind, target_id, sort_rank
                    FROM sc.v_simple_recipes_published
                    WHERE persona = %s
                    ORDER BY sort_rank NULLS LAST, recipe_id
                    LIMIT %s
                    """,
                    (persona, limit),
                )
            else:
                cur.execute(
                    """
                    SELECT recipe_id, version, status, title, beginner_summary, target_kind, target_id, sort_rank
                    FROM sc.v_simple_recipes_published
                    ORDER BY sort_rank NULLS LAST, recipe_id
                    LIMIT %s
                    """,
                    (limit,),
                )
            rows = cur.fetchall()
            return [RecipeOut(recipe_id=r[0], version=r[1], status=r[2], title=r[3], beginner_summary=r[4], target_kind=r[5], target_id=r[6], sort_rank=r[7]) for r in rows]


@app.get("/recipes/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT recipe_id, version, status, title, beginner_summary, target_kind, target_id, sort_rank
                FROM sc.v_simple_recipes_published WHERE recipe_id = %s
                """,
                (recipe_id,),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="recipe not found")
            return RecipeOut(recipe_id=r[0], version=r[1], status=r[2], title=r[3], beginner_summary=r[4], target_kind=r[5], target_id=r[6], sort_rank=r[7])


# --- Presets & Watchlists ---
class WatchlistCreate(BaseModel):
    name: str
    description: Optional[str] = None
    visibility: Optional[str] = "private"
    is_default: Optional[bool] = False


class SymbolsIn(BaseModel):
    symbols: List[str]


@app.get("/presets")
def list_presets():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT preset_id, title, description, source, version, symbol_count FROM sc.universe_presets ORDER BY preset_id"
            )
            out = []
            for r in cur.fetchall():
                out.append({
                    "preset_id": r[0],
                    "title": r[1],
                    "description": r[2],
                    "source": r[3],
                    "version": r[4],
                    "symbol_count": r[5],
                })
            return out


@app.get("/presets/{preset_id}/symbols", response_model=List[str])
def list_preset_symbols(preset_id: str, limit: Optional[int] = Query(default=None, ge=1, le=5000)):
    with get_db() as conn:
        with conn.cursor() as cur:
            if limit is not None:
                cur.execute("SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol LIMIT %s", (preset_id, int(limit)))
            else:
                cur.execute("SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol", (preset_id,))
            return [r[0] for r in cur.fetchall()]


@app.get("/watchlists")
def list_watchlists(user: User = Depends(get_current_user)):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT watchlist_id, name, description, visibility, is_default, created_at, updated_at
                FROM sc.watchlists WHERE user_id = %s ORDER BY is_default DESC, name
                """,
                (user.user_id,),
            )
            out = []
            for r in cur.fetchall():
                out.append({
                    "watchlist_id": str(r[0]),
                    "name": r[1],
                    "description": r[2],
                    "visibility": r[3],
                    "is_default": r[4],
                    "created_at": r[5],
                    "updated_at": r[6],
                })
            return out


@app.post("/watchlists", status_code=201, summary="Create or update a watchlist")
def create_watchlist(payload: WatchlistCreate = Body(..., example={"name":"starter","description":"demo list","visibility":"private","is_default":True}), user: User = Depends(get_current_user)):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sc.watchlists (user_id, name, description, visibility, is_default)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id, name) DO UPDATE SET description=EXCLUDED.description, visibility=EXCLUDED.visibility, is_default=EXCLUDED.is_default
                RETURNING watchlist_id
                """,
                (user.user_id, payload.name, payload.description, payload.visibility or "private", bool(payload.is_default)),
            )
            wid = cur.fetchone()[0]; conn.commit()
            return {"watchlist_id": str(wid)}


@app.get("/watchlists/{watchlist_id}/symbols", response_model=List[str])
def get_watchlist_symbols(watchlist_id: str, user: User = Depends(get_current_user)):
    with get_db() as conn:
        with conn.cursor() as cur:
            # ownership check
            cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id = %s AND user_id = %s", (watchlist_id, user.user_id))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="watchlist not found")
            cur.execute("SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol", (watchlist_id,))
            return [r[0] for r in cur.fetchall()]


@app.post("/watchlists/{watchlist_id}/symbols", status_code=204, summary="Add symbols to a watchlist")
def add_watchlist_symbols(watchlist_id: str, payload: SymbolsIn = Body(..., example={"symbols":["AAPL","MSFT","SPY"]}), user: User = Depends(get_current_user)):
    if not payload.symbols:
        return
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id = %s AND user_id = %s", (watchlist_id, user.user_id))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="watchlist not found")
            for sym in payload.symbols:
                cur.execute("INSERT INTO sc.watchlist_symbols (watchlist_id, symbol) VALUES (%s, %s) ON CONFLICT DO NOTHING", (watchlist_id, sym))
            conn.commit()


@app.delete("/watchlists/{watchlist_id}/symbols/{symbol}", status_code=204)
def remove_watchlist_symbol(watchlist_id: str, symbol: str, user: User = Depends(get_current_user)):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id = %s AND user_id = %s", (watchlist_id, user.user_id))
            if not cur.fetchone():
                raise HTTPException(status_code=404, detail="watchlist not found")
            cur.execute("DELETE FROM sc.watchlist_symbols WHERE watchlist_id = %s AND symbol = %s", (watchlist_id, symbol))
            conn.commit()


class UniverseRequest(BaseModel):
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    cap: Optional[int] = None


@app.post("/universe/resolve", response_model=List[str], summary="Resolve a universe", description="Returns symbols for a preset or a user watchlist with optional cap.")
def resolve_universe(req: UniverseRequest = Body(..., example={"preset_id":"sp500","cap":50}), user: User = Depends(get_current_user)):
    if not req.preset_id and not req.watchlist_id:
        raise HTTPException(status_code=400, detail="preset_id or watchlist_id required")
    symbols: List[str] = []
    with get_db() as conn:
        with conn.cursor() as cur:
            if req.preset_id:
                cur.execute("SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol", (req.preset_id,))
                symbols = [r[0] for r in cur.fetchall()]
            else:
                cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id = %s AND user_id = %s", (req.watchlist_id, user.user_id))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="watchlist not found")
                cur.execute("SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol", (req.watchlist_id,))
                symbols = [r[0] for r in cur.fetchall()]
    cap = req.cap if req.cap and req.cap > 0 else None
    return symbols[:cap] if cap else symbols


@app.get("/healthz")
def healthz():
    # Simple DB connectivity check
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Indicator Sets (CRUD, versioning) ---
class IndicatorSetComponentIn(BaseModel):
    indicator_id: str
    indicator_version: Optional[int] = None
    params: Dict[str, Any] | None = None
    role: Optional[str] = None
    weight: Optional[float] = None
    timeframe: Optional[str] = None


class IndicatorSetCreateIn(BaseModel):
    set_id: str
    version: int
    status: str = "draft"  # draft|in_review|published
    title: str
    purpose: Optional[str] = None
    novice_ready: bool = False
    beginner_summary: Optional[str] = None
    simple_defaults: Optional[Dict[str, Any]] = None
    guardrails: Optional[Dict[str, Any]] = None
    components: List[IndicatorSetComponentIn]


@app.post("/indicator_sets", status_code=201, summary="Create an indicator set version")
def create_indicator_set(payload: IndicatorSetCreateIn = Body(..., example={"set_id":"demo_set","version":1,"status":"draft","title":"Demo Set","purpose":"Testing","novice_ready":False,"components":[{"indicator_id":"rsi","indicator_version":1,"params":{"period":14}}]})):
    if payload.novice_ready and payload.status == "published" and not payload.guardrails:
        raise HTTPException(status_code=400, detail="guardrails required for novice_ready published sets")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sc.indicator_sets
                (set_id, version, status, title, purpose, novice_ready, beginner_summary, simple_defaults, guardrails)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    payload.set_id,
                    payload.version,
                    payload.status,
                    payload.title,
                    payload.purpose,
                    payload.novice_ready,
                    payload.beginner_summary,
                    json_or_none(payload.simple_defaults),
                    json_or_none(payload.guardrails),
                ),
            )
            # components
            ord_idx = 0
            for comp in payload.components:
                cur.execute(
                    """
                    INSERT INTO sc.indicator_set_components
                    (set_id, set_version, ord, indicator_id, indicator_version, params, role, weight, timeframe)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        payload.set_id,
                        payload.version,
                        ord_idx,
                        comp.indicator_id,
                        comp.indicator_version,
                        json_or_none(comp.params),
                        comp.role,
                        comp.weight,
                        comp.timeframe,
                    ),
                )
                ord_idx += 1
            conn.commit()
            return {"ok": True}


@app.get("/indicator_sets/all")
def list_indicator_sets_all():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT set_id, version, status, title, purpose, novice_ready, beginner_summary FROM sc.indicator_sets ORDER BY set_id, version DESC"
            )
            out = []
            for r in cur.fetchall():
                out.append({
                    "set_id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "purpose": r[4],
                    "novice_ready": r[5],
                    "beginner_summary": r[6],
                })
            return out


@app.get("/indicator_sets/{set_id}/{version}")
def get_indicator_set_full(set_id: str, version: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT set_id, version, status, title, purpose, novice_ready, beginner_summary, simple_defaults, guardrails FROM sc.indicator_sets WHERE set_id=%s AND version=%s",
                (set_id, version),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="indicator set not found")
            cur.execute(
                """
                SELECT ord, indicator_id, indicator_version, params, role, weight, timeframe
                FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord
                """,
                (set_id, version),
            )
            comps = [
                {
                    "ord": rr[0],
                    "indicator_id": rr[1],
                    "indicator_version": rr[2],
                    "params": rr[3],
                    "role": rr[4],
                    "weight": rr[5],
                    "timeframe": rr[6],
                }
                for rr in cur.fetchall()
            ]
            return {
                "set": {
                    "set_id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "purpose": r[4],
                    "novice_ready": r[5],
                    "beginner_summary": r[6],
                    "simple_defaults": r[7],
                    "guardrails": r[8],
                },
                "components": comps,
            }


@app.post("/indicator_sets/{set_id}/{version}/publish", status_code=204)
def publish_indicator_set(set_id: str, version: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            # enforce guardrails if novice_ready
            cur.execute(
                "SELECT novice_ready, guardrails FROM sc.indicator_sets WHERE set_id=%s AND version=%s",
                (set_id, version),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="indicator set not found")
            novice_ready, guardrails = row[0], row[1]
            if novice_ready and not guardrails:
                raise HTTPException(status_code=400, detail="guardrails required for novice_ready published sets")
            cur.execute(
                "UPDATE sc.indicator_sets SET status='published', published_at=NOW() WHERE set_id=%s AND version=%s",
                (set_id, version),
            )
            conn.commit()
            return


def json_or_none(v: Any):
    return v if v is not None else None


# --- Strategies (CRUD minimal + validate) ---
class StrategyCreateIn(BaseModel):
    strategy_id: str
    version: int
    status: str = "draft"
    title: str
    objective: Optional[str] = None
    novice_ready: bool = False
    beginner_summary: Optional[str] = None
    simple_defaults: Optional[Dict[str, Any]] = None
    guardrails: Optional[Dict[str, Any]] = None
    entry_logic: Optional[Dict[str, Any]] = None
    exit_logic: Optional[Dict[str, Any]] = None
    risk: Optional[Dict[str, Any]] = None
    execution_policy: Optional[Dict[str, Any]] = None
    indicator_sets: Optional[List[Dict[str, Any]]] = None  # [{set_id, set_version}]


@app.post("/strategies", status_code=201, summary="Create a strategy version")
def create_strategy(payload: StrategyCreateIn = Body(..., example={"strategy_id":"trend_follow_alignment","version":1,"status":"draft","title":"Trend Follow Alignment","novice_ready":False,"indicator_sets":[{"set_id":"macd_trend_pullback_v1","set_version":1}]})):
    if payload.novice_ready and payload.status == "published" and not payload.guardrails:
        raise HTTPException(status_code=400, detail="guardrails required for novice_ready published strategies")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sc.strategies
                (strategy_id, version, status, title, objective, novice_ready, beginner_summary, simple_defaults, guardrails,
                 entry_logic, exit_logic, risk, execution_policy)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    payload.strategy_id,
                    payload.version,
                    payload.status,
                    payload.title,
                    payload.objective,
                    payload.novice_ready,
                    payload.beginner_summary,
                    json_or_none(payload.simple_defaults),
                    json_or_none(payload.guardrails),
                    json_or_none(payload.entry_logic),
                    json_or_none(payload.exit_logic),
                    json_or_none(payload.risk),
                    json_or_none(payload.execution_policy),
                ),
            )
            if payload.indicator_sets:
                for link in payload.indicator_sets:
                    cur.execute(
                        """
                        INSERT INTO sc.strategy_indicator_sets (strategy_id, strategy_version, set_id, set_version)
                        VALUES (%s,%s,%s,%s)
                        """,
                        (
                            payload.strategy_id,
                            payload.version,
                            link.get("set_id"),
                            int(link.get("set_version")),
                        ),
                    )
            conn.commit()
            return {"ok": True}


@app.get("/strategies/all")
def list_strategies_all():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT strategy_id, version, status, title, objective, novice_ready, beginner_summary FROM sc.strategies ORDER BY strategy_id, version DESC"
            )
            out = []
            for r in cur.fetchall():
                out.append({
                    "strategy_id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "objective": r[4],
                    "novice_ready": r[5],
                    "beginner_summary": r[6],
                })
            return out


@app.get("/strategies/{strategy_id}/{version}")
def get_strategy_full(strategy_id: str, version: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT strategy_id, version, status, title, objective, novice_ready, beginner_summary,
                       simple_defaults, guardrails, entry_logic, exit_logic, risk, execution_policy
                FROM sc.strategies WHERE strategy_id=%s AND version=%s
                """,
                (strategy_id, version),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="strategy not found")
            cur.execute(
                "SELECT set_id, set_version FROM sc.strategy_indicator_sets WHERE strategy_id=%s AND strategy_version=%s",
                (strategy_id, version),
            )
            links = [{"set_id": rr[0], "set_version": rr[1]} for rr in cur.fetchall()]
            return {
                "strategy": {
                    "strategy_id": r[0],
                    "version": r[1],
                    "status": r[2],
                    "title": r[3],
                    "objective": r[4],
                    "novice_ready": r[5],
                    "beginner_summary": r[6],
                    "simple_defaults": r[7],
                    "guardrails": r[8],
                    "entry_logic": r[9],
                    "exit_logic": r[10],
                    "risk": r[11],
                    "execution_policy": r[12],
                },
                "indicator_sets": links,
            }


@app.post("/strategies/{strategy_id}/{version}/publish", status_code=204)
def publish_strategy(strategy_id: str, version: int):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT novice_ready, guardrails FROM sc.strategies WHERE strategy_id=%s AND version=%s",
                (strategy_id, version),
            )
            row = cur.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="strategy not found")
            novice_ready, guardrails = row[0], row[1]
            if novice_ready and not guardrails:
                raise HTTPException(status_code=400, detail="guardrails required for novice_ready published strategies")
            cur.execute(
                "UPDATE sc.strategies SET status='published', published_at=NOW() WHERE strategy_id=%s AND version=%s",
                (strategy_id, version),
            )
            conn.commit()
            return


class StrategyValidateIn(BaseModel):
    strategy: StrategyCreateIn


class StrategyValidateOut(BaseModel):
    ok: bool
    errors: List[str]


@app.post("/strategies/validate", response_model=StrategyValidateOut, summary="Validate a strategy payload")
def validate_strategy(payload: StrategyValidateIn = Body(..., example={"strategy":{"strategy_id":"trend_follow_alignment","version":1,"status":"draft","title":"Trend Follow Alignment","novice_ready":False,"indicator_sets":[{"set_id":"macd_trend_pullback_v1","set_version":1}]}})):
    errs: List[str] = []
    s = payload.strategy
    if s.novice_ready and (s.status == "published") and not s.guardrails:
        errs.append("guardrails required for novice_ready published strategies")
    # verify linked sets exist
    if s.indicator_sets:
        with get_db() as conn:
            with conn.cursor() as cur:
                for link in s.indicator_sets:
                    cur.execute(
                        "SELECT 1 FROM sc.indicator_sets WHERE set_id=%s AND version=%s",
                        (link.get("set_id"), int(link.get("set_version"))),
                    )
                    if not cur.fetchone():
                        errs.append(f"indicator_set not found: {link}")
    return StrategyValidateOut(ok=(len(errs) == 0), errors=errs)


# --- FeatureBuilder convenience for sets ---
class BuildSetFeaturesIn(BaseModel):
    set_id: str
    version: int
    data: List[Dict[str, Any]]


class BuildSetFeaturesOut(BaseModel):
    columns: List[str]
    data: List[Dict[str, Any]]


@app.post("/indicator_sets/build_features", response_model=BuildSetFeaturesOut, summary="Compute set features for supplied rows")
def build_set_features(payload: BuildSetFeaturesIn = Body(..., example={"set_id":"macd_trend_pullback_v1","version":1,"data":[{"timestamp":"2024-06-01","open":100.0,"high":101.0,"low":99.5,"close":100.5,"volume":1000000}]})):
    # Map DB set and components into FeatureBuilder's models and compute features for provided data
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT set_id, version, title FROM sc.indicator_sets WHERE set_id=%s AND version=%s",
                (payload.set_id, payload.version),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="indicator set not found")
            cur.execute(
                "SELECT indicator_id, indicator_version, params FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord",
                (payload.set_id, payload.version),
            )
            comps = cur.fetchall()
    fb_set = FBIndicatorSet(
        name=str(payload.set_id),
        version=int(payload.version),
        description=str(r[2]) if len(r) > 2 and r[2] is not None else "",
        indicators=[
            FBIndicatorSpec(name=rr[0], version=int(rr[1] or 1), params=(rr[2] or {})) for rr in comps
        ],
    )
    fb = FeatureBuilder(indicator_set=fb_set)
    df = pd.DataFrame.from_records(payload.data)
    out_df = fb.add_indicator_features(df)
    cols_new = [c for c in out_df.columns if c not in df.columns]
    return BuildSetFeaturesOut(columns=cols_new, data=out_df[cols_new].to_dict(orient="records"))


# --- Backtest Runner ---
class BacktestLabelCfg(BaseModel):
    kind: str  # 'hourly_direction' | 'forward_days'
    params: Dict[str, Any] | None = None


class BacktestFeaturesCfg(BaseModel):
    set_id: str
    version: int


class BacktestUniverseIn(BaseModel):
    preset_id: Optional[str] = None
    watchlist_id: Optional[str] = None
    symbols: Optional[List[str]] = None
    cap: Optional[int] = 50


class BacktestRequest(BaseModel):
    timeframe: str = "hour"  # hour|day|<N>m
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    universe: BacktestUniverseIn
    features: BacktestFeaturesCfg
    label: BacktestLabelCfg
    # Engine params
    thresholds: Optional[List[float]] = [0.55, 0.6, 0.65, 0.7]
    top_pct: Optional[float] = None
    splits: int = 5
    embargo: float = 0.0
    size_by_conf: bool = False
    conf_cap: float = 1.0
    allowed_hours: Optional[List[int]] = None
    momentum_gate: bool = False
    momentum_min: float = 0.0
    momentum_column: str = 'momentum_score_total'


class BacktestSymbolResult(BaseModel):
    symbol: str
    threshold_results: List[Dict[str, Any]]
    top_pct_result: Optional[Dict[str, Any]] = None
    rows: int


class BacktestRunOut(BaseModel):
    scope: str
    timeframe: str
    symbols_evaluated: int
    symbols_skipped: int
    per_symbol: List[BacktestSymbolResult]
    pooled_result: Optional[Dict[str, Any]] = None
    warnings: Optional[List[str]] = None
    summary: Optional[str] = None


def _resolve_symbols_from_universe(u: BacktestUniverseIn, user: User) -> List[str]:
    if u.symbols:
        syms = [str(s).upper() for s in u.symbols]
        cap = max(1, int(u.cap or len(syms)))
        return syms[:cap]
    syms: List[str] = []
    if not u.preset_id and not u.watchlist_id:
        return syms
    with get_db() as conn:
        with conn.cursor() as cur:
            if u.preset_id:
                cur.execute(
                    "SELECT symbol FROM sc.universe_preset_symbols WHERE preset_id = %s ORDER BY symbol",
                    (u.preset_id,),
                )
                syms = [r[0] for r in cur.fetchall()]
            else:
                cur.execute("SELECT 1 FROM sc.watchlists WHERE watchlist_id = %s AND user_id = %s", (u.watchlist_id, user.user_id))
                if not cur.fetchone():
                    raise HTTPException(status_code=404, detail="watchlist not found")
                cur.execute(
                    "SELECT symbol FROM sc.watchlist_symbols WHERE watchlist_id = %s ORDER BY sort NULLS LAST, symbol",
                    (u.watchlist_id,),
                )
                syms = [r[0] for r in cur.fetchall()]
    cap = max(1, int(u.cap or 50))
    return syms[:cap]


def _build_fb_set_from_db(set_id: str, version: int) -> FBIndicatorSet:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT title FROM sc.indicator_sets WHERE set_id=%s AND version=%s",
                (set_id, version),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="indicator set not found")
            desc = r[0] or ""
            cur.execute(
                "SELECT indicator_id, indicator_version, params FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord",
                (set_id, version),
            )
            comps = cur.fetchall()
    return FBIndicatorSet(
        name=str(set_id),
        version=int(version),
        description=str(desc),
        indicators=[FBIndicatorSpec(name=rr[0], version=int(rr[1] or 1), params=(rr[2] or {})) for rr in comps],
    )


def _maybe_add_hour_et(df: pd.DataFrame) -> pd.DataFrame:
    if 'date' in df.columns and 'hour_et' not in df.columns:
        try:
            dt = pd.to_datetime(df['date'])
            try:
                df['hour_et'] = dt.dt.tz_convert('US/Eastern').dt.hour
            except Exception:
                df['hour_et'] = dt.dt.hour
        except Exception:
            pass
    return df


def _apply_label(df: pd.DataFrame, label: BacktestLabelCfg) -> pd.DataFrame:
    kind = (label.kind or '').lower().strip()
    params = dict(label.params or {})
    if kind in ('hour', 'hourly', 'hourly_direction'):
        return label_next_hour_direction(df, **params)
    if kind in ('forward_days', 'fwd_days', 'fwd'):
        return label_forward_return_days(df, **params)
    # Default: passthrough
    return df


@app.post(
    "/backtest/run",
    response_model=BacktestRunOut,
    summary="Run cross-validated backtest over a set of symbols",
    description="Fetches bars for a universe, builds features from an indicator set, applies labels, and runs a CV backtest per symbol with an optional pooled summary."
)
def run_backtest(
    payload: BacktestRequest = Body(
        ..., example={
            "timeframe": "hour",
            "start_date": "2024-06-01",
            "end_date": "2024-06-15",
            "universe": {"preset_id": "liquid_etfs", "cap": 5},
            "features": {"set_id": "macd_trend_pullback_v1", "version": 1},
            "label": {"kind": "hourly_direction", "params": {"k_sigma": 0.3}},
            "thresholds": [0.55, 0.6, 0.65],
            "splits": 5,
            "embargo": 0.1,
            "size_by_conf": False,
            "conf_cap": 1.0
        }
    ),
    user: User = Depends(get_current_user),
    persist: bool = Query(False, description="Persist backtest summary and folds to DB"),
    tag: Optional[str] = Query(None, description="Optional tag for persisted run"),
    pack_id: Optional[str] = Query(None, description="Optional pack_id to associate this run with")
):
    start_date = payload.start_date
    end_date = payload.end_date
    if not start_date or not end_date:
        start_date, end_date = _default_dates()
    # Novice cap: 90-day window
    if _days_between(start_date, end_date) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    symbols = _resolve_symbols_from_universe(payload.universe, user)
    if not symbols:
        raise HTTPException(status_code=400, detail="no symbols resolved; provide universe (preset/watchlist/symbols)")
    # Novice cap: 50 symbols
    symbols = symbols[:50]
    fb_set = _build_fb_set_from_db(payload.features.set_id, int(payload.features.version))
    fb = FeatureBuilder(indicator_set=fb_set)

    per_symbol: List[BacktestSymbolResult] = []
    skipped = 0
    frames_all: List[pd.DataFrame] = []
    for sym in symbols:
        try:
            df = _fetch_bars(sym, payload.timeframe, start_date, end_date)
            if df is None or df.empty:
                skipped += 1
                continue
            df = _maybe_add_hour_et(df)
            fdf = fb.add_indicator_features(df)
            ldf = _apply_label(fdf, payload.label)
            # Ensure target column
            target_col = 'y' if 'y' in ldf.columns else ('y_syn' if 'y_syn' in ldf.columns else None)
            if not target_col:
                skipped += 1
                continue
            res = engine_run_backtest(
                ldf,
                target_col=target_col,
                thresholds=thresholds_use or [],
                splits=int(payload.splits or 5),
                embargo=float(payload.embargo or 0.0),
                top_pct=top_pct_use,
                allowed_hours=hours_use,
                slippage_bps=1.0,
                size_by_conf=bool(payload.size_by_conf),
                conf_cap=float(payload.conf_cap or 1.0),
                momentum_gate=bool(payload.momentum_gate),
                momentum_min=float(payload.momentum_min or 0.0),
                momentum_column=str(payload.momentum_column or 'momentum_score_total'),
            )
            per_symbol.append(BacktestSymbolResult(symbol=sym, threshold_results=res.get('threshold_results') or [], top_pct_result=res.get('top_pct_result'), rows=len(ldf)))
            frames_all.append(ldf)
        except Exception:
            skipped += 1
            continue
    pooled_result: Optional[Dict[str, Any]] = None
    if frames_all:
        try:
            pooled_df = pd.concat(frames_all, axis=0, ignore_index=True)
            target_col = 'y' if 'y' in pooled_df.columns else ('y_syn' if 'y_syn' in pooled_df.columns else None)
            if target_col:
                pooled_result = engine_run_backtest(
                    pooled_df,
                    target_col=target_col,
                    thresholds=thresholds_use or [],
                    splits=int(payload.splits or 5),
                    embargo=float(payload.embargo or 0.0),
                    top_pct=top_pct_use,
                    allowed_hours=hours_use,
                    slippage_bps=1.0,
                    size_by_conf=bool(payload.size_by_conf),
                    conf_cap=float(payload.conf_cap or 1.0),
                    momentum_gate=bool(payload.momentum_gate),
                    momentum_min=float(payload.momentum_min or 0.0),
                    momentum_column=str(payload.momentum_column or 'momentum_score_total'),
                )
        except Exception:
            pooled_result = None
    # Optional: persist run
    if persist:
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    start_dt = datetime.utcnow()
                    metrics = {}
                    folds = []
                    if pooled_result:
                        folds = pooled_result.get('threshold_results') or []
                        # compute simple aggregates
                        try:
                            import numpy as _np  # type: ignore
                            if folds:
                                sh = [float(r.get('sharpe_hourly', 0.0)) for r in folds]
                                tr = [int(r.get('trades', 0)) for r in folds]
                                cr = [float(r.get('cum_ret', 0.0)) for r in folds]
                                metrics = {
                                    'avg_sharpe_hourly': float(_np.mean(sh)),
                                    'trades_total': int(sum(tr)),
                                    'cum_ret_sum': float(sum(cr)),
                                }
                        except Exception:
                            metrics = {}
                    cur.execute(
                        """
                        INSERT INTO sc.model_backtest_runs
                          (model_id, model_version, pack_id, timeframe, data_window, universe, featureset, label_cfg, params, metrics, best_config, summary, git_sha, tag, started_at, finished_at)
                        VALUES
                          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        RETURNING run_id
                        """,
                        (
                            None, None, pack_id, payload.timeframe,
                            json.dumps({'start': start_date, 'end': end_date}),
                            json.dumps(payload.universe.dict() if hasattr(payload.universe, 'dict') else {}),
                            json.dumps({'set_id': payload.features.set_id, 'version': int(payload.features.version)}),
                            json.dumps(payload.label.dict() if hasattr(payload.label, 'dict') else {}),
                            json.dumps({'thresholds': payload.thresholds, 'top_pct': payload.top_pct, 'splits': payload.splits, 'embargo': payload.embargo}),
                            json.dumps(metrics),
                            json.dumps(None),
                            (f"Backtest on {len(symbols)} symbols ({payload.timeframe}) — avg_sharpe={metrics.get('avg_sharpe_hourly',0):.3f}, trades={metrics.get('trades_total',0)}" if metrics else None),
                            None,
                            tag,
                        ),
                    )
                    rid = cur.fetchone()[0]
                    # persist folds
                    if folds:
                        for r in folds:
                            cur.execute(
                                """
                                INSERT INTO sc.model_backtest_folds (run_id, fold, thr_used, cum_ret, sharpe_hourly, trades)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """,
                                (
                                    rid,
                                    int(r.get('fold', 0)),
                                    (float(r.get('thr')) if r.get('thr') is not None else None),
                                    float(r.get('cum_ret', 0.0)),
                                    float(r.get('sharpe_hourly', 0.0)),
                                    int(r.get('trades', 0)),
                                ),
                            )
                    conn.commit()
        except Exception:
            pass
    # Novice summary
    summary = f"Backtested {len(symbols)} symbols ({payload.timeframe}) from {start_date} to {end_date}. Skipped {skipped}."
    return BacktestRunOut(
        scope="per_symbol",
        timeframe=payload.timeframe,
        symbols_evaluated=len(symbols),
        symbols_skipped=skipped,
        per_symbol=per_symbol,
        pooled_result=pooled_result,
        warnings=[],
    )


# --- Backtest sweep for a model ---
class BacktestSweepGrid(BaseModel):
    thresholds_list: Optional[List[List[float]]] = None
    top_pct_list: Optional[List[float]] = None
    allowed_hours_list: Optional[List[List[int]]] = None
    label_params_list: Optional[List[Dict[str, Any]]] = None
    size_by_conf_list: Optional[List[bool]] = None
    conf_cap_list: Optional[List[float]] = None
    max_combos: int = 50
    min_trades: int = 50


class BacktestSweepRequest(BaseModel):
    mode: Optional[str] = None  # simple|advanced
    version: Optional[int] = None
    timeframe: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    universe: BacktestUniverseIn
    sweep_preset_id: Optional[str] = None
    grid: BacktestSweepGrid
    persist: bool = True
    tag: Optional[str] = None
    pack_id: Optional[str] = None


class BacktestSweepOut(BaseModel):
    run_id: Optional[str] = None
    best_config: Dict[str, Any]
    metrics: Dict[str, Any]
    summary: str


# --- Model Pipeline (build -> sweep/backtest -> leaderboard -> conditional train)
class PipelineGuardrails(BaseModel):
    min_trades: Optional[int] = 50
    min_sharpe: Optional[float] = 0.2
    max_position_rate: Optional[float] = None


class PipelineUniverse(BacktestUniverseIn):
    pass


class ModelPipelineRunRequest(BaseModel):
    version: Optional[int] = None
    timeframe: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    universe: PipelineUniverse
    mode: Optional[str] = 'simple'
    sweep_preset_id: Optional[str] = None
    grid: Optional[BacktestSweepGrid] = None
    guardrails: Optional[PipelineGuardrails] = None
    persist: Optional[bool] = True
    dry_run: Optional[bool] = False


class ModelPipelineRunOut(BaseModel):
    pipeline_run_id: str
    status: str
    dataset: Optional[Dict[str, Any]] = None
    backtests: Optional[Dict[str, Any]] = None
    chosen: Optional[Dict[str, Any]] = None
    training: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    next_steps: Optional[List[str]] = None


def _cap_dates_and_symbols(sd: str, ed: str, symbols: List[str]) -> tuple[str, str, List[str]]:
    # Enforce 90-day and 50-symbol caps
    if _days_between(sd, ed) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    cap_syms = symbols[:50]
    return sd, ed, cap_syms


@app.post("/models/{model_id}/pipeline/run", response_model=ModelPipelineRunOut, summary="Run model pipeline: dataset -> sweep/backtest -> conditional train")
def model_pipeline_run(model_id: str, payload: ModelPipelineRunRequest = Body(...), user: User = Depends(get_current_user)):
    # Resolve model version and defaults
    with get_db() as conn:
        with conn.cursor() as cur:
            ver = payload.version
            if ver is None:
                cur.execute("SELECT version FROM sc.v_model_specs_published WHERE model_id=%s", (model_id,))
                r = cur.fetchone(); ver = int(r[0]) if r else None
            if ver is None:
                raise HTTPException(status_code=404, detail="no published version for model")
            cur.execute("SELECT timeframe, featureset, label_cfg, scope FROM sc.model_specs WHERE model_id=%s AND version=%s", (model_id, int(ver)))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="model not found")
            m_timeframe, m_featureset, m_label, m_scope = r[0], r[1] or {}, r[2] or {}, r[3] or {}
    timeframe = payload.timeframe or m_timeframe or 'day'
    sd, ed = payload.start_date, payload.end_date
    if not sd or not ed:
        sd, ed = _default_dates()
    # Resolve universe and apply caps
    symbols = _resolve_symbols_from_universe(payload.universe, user)
    if not symbols:
        raise HTTPException(status_code=400, detail="no symbols resolved; choose a preset like 'sp500' or add a watchlist")
    sd, ed, symbols = _cap_dates_and_symbols(sd, ed, symbols)

    # Create pipeline run row (running)
    pipeline_run_id = None
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sc.model_pipeline_runs (model_id, model_version, timeframe, universe, sweep, guardrails, status, summary)
                    VALUES (%s,%s,%s,%s,%s,%s,'running',%s) RETURNING pipeline_run_id
                    """,
                    (
                        model_id,
                        int(ver),
                        timeframe,
                        json.dumps(payload.universe.dict() if hasattr(payload.universe,'dict') else {}),
                        json.dumps({'preset': payload.sweep_preset_id, 'mode': payload.mode}),
                        json.dumps(payload.guardrails.dict() if payload.guardrails else {}),
                        f"Starting pipeline for {model_id}@{ver} on {len(symbols)} symbols ({timeframe}) over {sd}..{ed}",
                    ),
                )
                pipeline_run_id = str(cur.fetchone()[0]); conn.commit()
    except Exception:
        pipeline_run_id = pipeline_run_id or ""

    # Phase: Dataset (simple: optional summary only)
    dataset_info: Dict[str, Any] = { 'rows': None, 'symbols': len(symbols) }
    # Keep this phase lightweight for now to avoid heavy writes; sweeps will fetch data too

    # Phase: Sweep/backtest
    # Build BacktestSweepRequest using simple or provided preset/grid
    grid = payload.grid or BacktestSweepGrid()
    sweep_req = BacktestSweepRequest(
        version=int(ver),
        timeframe=timeframe,
        start_date=sd,
        end_date=ed,
        universe=BacktestUniverseIn(**payload.universe.dict()),
        sweep_preset_id=(payload.sweep_preset_id or ('rth_thresholds_basic' if (payload.mode or 'simple').lower()=='simple' else None)),
        grid=grid,
        persist=True,
        tag="pipeline"
    )
    try:
        sweep_res = model_backtest_sweep(model_id, sweep_req, user)  # reuse internal function
    except HTTPException as e:
        # Update pipeline run and bubble a novice-friendly message
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE sc.model_pipeline_runs SET status='error', errors=%s, finished_at=NOW() WHERE pipeline_run_id=%s", (json.dumps({'error': e.detail}), pipeline_run_id)); conn.commit()
        raise
    backtests_info = { 'run_ids': [sweep_res.run_id] if sweep_res.run_id else [], 'leaderboard': [] }

    # Evaluate guardrails and optionally "train"
    gr = payload.guardrails or PipelineGuardrails()
    metrics = sweep_res.metrics or {}
    chosen_ok = (
        (metrics.get('trades_total', 0) >= int(gr.min_trades or 50)) and
        (metrics.get('avg_sharpe_hourly', 0.0) >= float(gr.min_sharpe or 0.2))
    )
    training_info = None
    if chosen_ok and not payload.dry_run:
        # Record a training run stub (no auto-publish)
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO sc.model_training_runs (model_id, model_version, status, training_cfg, data_window, dataset_hash, features_hash, git_sha, metrics, started_at, finished_at)
                        VALUES (%s,%s,'success',%s,%s,%s,%s,%s,%s,NOW(),NOW())
                        RETURNING train_id
                        """,
                        (
                            model_id,
                            int(ver),
                            json.dumps({'selection': sweep_res.best_config}),
                            json.dumps({'start': sd, 'end': ed}),
                            None, None, None,
                            json.dumps({'note': 'pipeline training stub'}),
                        ),
                    )
                    train_id = cur.fetchone()[0]; conn.commit()
                    training_info = { 'run_id': str(train_id), 'status': 'success' }
        except Exception:
            training_info = { 'run_id': None, 'status': 'error' }

    # Compose summary and next steps
    summary = (
        f"Tried safe configurations across {len(symbols)} symbols ({timeframe}) from {sd} to {ed}. "
        f"Best avg_sharpe={metrics.get('avg_sharpe_hourly',0):.3f}, trades={metrics.get('trades_total',0)}. "
        + ("Training started." if training_info else "Guardrails not met; review leaderboard and adjust.")
    )
    next_steps = [
        "Review best backtest metrics",
        "Apply training config (Critic Gate)",
        "Optionally rerun with a different preset or date window"
    ]

    # Update pipeline run row
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE sc.model_pipeline_runs
                    SET backtest_run_ids = %s, training_run_id = %s, status = 'success', summary = %s, finished_at = NOW()
                    WHERE pipeline_run_id = %s
                    """,
                    (
                        json.dumps(backtests_info['run_ids']),
                        (training_info or {}).get('run_id'),
                        summary,
                        pipeline_run_id,
                    ),
                ); conn.commit()
    except Exception:
        pass

    return ModelPipelineRunOut(
        pipeline_run_id=pipeline_run_id,
        status='success',
        dataset=dataset_info,
        backtests=backtests_info,
        chosen={'config': sweep_res.best_config, 'metrics': metrics},
        training=training_info,
        summary=summary,
        next_steps=next_steps,
    )


class ModelPipelineGetOut(BaseModel):
    pipeline_run_id: str
    model_id: str
    version: int
    timeframe: Optional[str] = None
    status: str
    dataset_run_id: Optional[str] = None
    backtest_run_ids: List[str] = []
    training_run_id: Optional[str] = None
    summary: Optional[str] = None
    created_at: Optional[str] = None
    finished_at: Optional[str] = None


@app.get("/models/pipeline/runs/{pipeline_run_id}", response_model=ModelPipelineGetOut, summary="Get pipeline run status")
def get_model_pipeline_run(pipeline_run_id: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT pipeline_run_id, model_id, model_version, timeframe, status, dataset_run_id, backtest_run_ids, training_run_id, summary, created_at, finished_at FROM sc.model_pipeline_runs WHERE pipeline_run_id = %s",
                (pipeline_run_id,),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="pipeline run not found")
            return ModelPipelineGetOut(
                pipeline_run_id=str(r[0]), model_id=r[1], version=int(r[2] or 0), timeframe=r[3], status=r[4],
                dataset_run_id=(str(r[5]) if r[5] else None), backtest_run_ids=(list(r[6]) if r[6] else []), training_run_id=(str(r[7]) if r[7] else None),
                summary=r[8], created_at=str(r[9]) if r[9] else None, finished_at=str(r[10]) if r[10] else None,
            )


def _days_between(sd: str, ed: str) -> int:
    try:
        from datetime import datetime as _dt
        s = _dt.strptime(sd, '%Y-%m-%d'); e = _dt.strptime(ed, '%Y-%m-%d')
        return (e - s).days
    except Exception:
        return 0


@app.post("/models/{model_id}/backtest/sweep", response_model=BacktestSweepOut, summary="Grid-search backtest to pick best config")
def model_backtest_sweep(
    model_id: str,
    payload: BacktestSweepRequest = Body(
        ..., example={
            "universe": {"preset_id": "liquid_etfs", "cap": 20},
            "grid": {
                "thresholds_list": [[0.55, 0.6, 0.65, 0.7]],
                "allowed_hours_list": [[9,10,11,12,13,14,15]],
                "max_combos": 20,
                "min_trades": 50
            },
            "persist": True,
            "tag": "sweep-demo"
        }
    ),
    user: User = Depends(get_current_user)
):
    # Load model spec
    with get_db() as conn:
        with conn.cursor() as cur:
            ver = payload.version
            if ver is None:
                cur.execute("SELECT version FROM sc.v_model_specs_published WHERE model_id=%s", (model_id,))
                r = cur.fetchone()
                if not r:
                    raise HTTPException(status_code=404, detail="no published version for model")
                ver = int(r[0])
            cur.execute(
                "SELECT timeframe, featureset, label_cfg FROM sc.model_specs WHERE model_id=%s AND version=%s",
                (model_id, int(ver)),
            )
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="model not found")
            m_timeframe, m_featureset, m_label = r[0], r[1] or {}, r[2] or {}
    timeframe = payload.timeframe or m_timeframe or 'day'
    # Dates guardrail (<= 90 days)
    sd, ed = payload.start_date, payload.end_date
    if not sd or not ed:
        sd, ed = _default_dates()
    if _days_between(sd, ed) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    # Resolve universe
    symbols = _resolve_symbols_from_universe(payload.universe, user)
    if not symbols:
        raise HTTPException(status_code=400, detail="no symbols resolved for sweep")
    if len(symbols) > 50:
        raise HTTPException(status_code=400, detail="universe too large; cap to 50 symbols")
    # Build features
    fb = _build_fb_for_featureset(None, m_featureset)
    frames: List[pd.DataFrame] = []
    for sym in symbols:
        try:
            df = _fetch_bars(sym, timeframe, sd, ed)
            if df is None or df.empty:
                continue
            df = _maybe_add_hour_et(df)
            fdf = fb.add_indicator_features(df)
            frames.append(fdf)
        except Exception:
            continue
    if not frames:
        raise HTTPException(status_code=400, detail="no data for sweep")
    pooled = pd.concat(frames, axis=0, ignore_index=True)
    # Label with model's default
    label_cfg = BacktestLabelCfg(kind=(m_label.get('kind') or 'hourly_direction'), params=m_label.get('params') or {})
    pooled = _apply_label(pooled, label_cfg)
    target_col = 'y' if 'y' in pooled.columns else ('y_syn' if 'y_syn' in pooled.columns else None)
    if not target_col:
        raise HTTPException(status_code=400, detail="labels not available for pooled dataset")
    # Build grid (optionally from preset)
    g = payload.grid
    if payload.sweep_preset_id:
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT grid, guardrails FROM sc.backtest_sweep_presets WHERE preset_id = %s", (payload.sweep_preset_id,))
                    r = cur.fetchone()
                    if r:
                        pg, guard = r[0] or {}, r[1] or {}
                        if not g or not any([g.thresholds_list, g.top_pct_list, g.allowed_hours_list, g.label_params_list, g.size_by_conf_list, g.conf_cap_list]):
                            # adopt entire preset grid
                            g = BacktestSweepGrid(**pg)
                        # adopt guardrails if present
                        if guard.get('max_combos') and not (payload.grid and payload.grid.max_combos):
                            g.max_combos = int(guard.get('max_combos'))
                        if guard.get('min_trades') and not (payload.grid and payload.grid.min_trades):
                            g.min_trades = int(guard.get('min_trades'))
        except Exception:
            pass
    candidates = []
    thresholds_list = g.thresholds_list or []
    top_pct_list = g.top_pct_list or []
    if thresholds_list and top_pct_list:
        raise HTTPException(status_code=400, detail="provide thresholds_list or top_pct_list, not both")
    if not thresholds_list and not top_pct_list:
        thresholds_list = [[0.55,0.6,0.65,0.7]]
    allowed_hours_list = g.allowed_hours_list or [[]]
    label_params_list = g.label_params_list or [{}]
    size_by_conf_list = g.size_by_conf_list or [False]
    conf_cap_list = g.conf_cap_list or [1.0]
    for thrs in thresholds_list or [None]:
        for tpct in top_pct_list or [None]:
            for hrs in allowed_hours_list:
                for lp in label_params_list:
                    for sbc in size_by_conf_list:
                        for cc in conf_cap_list:
                            candidates.append({'thresholds': thrs, 'top_pct': tpct, 'allowed_hours': hrs, 'label_params': lp, 'size_by_conf': sbc, 'conf_cap': cc})
    if len(candidates) > int(g.max_combos or 50):
        raise HTTPException(status_code=400, detail=f"too many grid combos ({len(candidates)}); cap to {g.max_combos}")
    # Evaluate
    best = None
    best_metrics = None
    for cfg in candidates:
        # relabel if label params vary
        if cfg['label_params']:
            pooled_l = _apply_label(pooled.copy(), BacktestLabelCfg(kind=label_cfg.kind, params=cfg['label_params']))
        else:
            pooled_l = pooled
        res = engine_run_backtest(
            pooled_l,
            target_col=target_col,
            thresholds=(cfg['thresholds'] or []),
            top_pct=cfg['top_pct'],
            splits=5,
            embargo=0.0,
            allowed_hours=(cfg['allowed_hours'] or None),
            size_by_conf=bool(cfg['size_by_conf']),
            conf_cap=float(cfg['conf_cap'] or 1.0),
        )
        folds = res.get('threshold_results') or []
        try:
            import numpy as _np
            sh = [float(r.get('sharpe_hourly', 0.0)) for r in folds]
            tr = [int(r.get('trades', 0)) for r in folds]
            avg_sh = float(_np.mean(sh)) if sh else 0.0
            trades_total = int(sum(tr))
        except Exception:
            avg_sh = 0.0; trades_total = 0
        if trades_total < int(g.min_trades or 50):
            continue
        score = avg_sh
        if (best is None) or (score > best[0]):
            best = (score, cfg, folds)
            best_metrics = {'avg_sharpe_hourly': avg_sh, 'trades_total': trades_total}
    if not best:
        raise HTTPException(status_code=400, detail="no configuration met the minimum trades or produced metrics")
    _, best_cfg, best_folds = best
    summary = f"Best config: {'top_pct='+str(best_cfg['top_pct']) if best_cfg.get('top_pct') is not None else 'thresholds'} with avg_sharpe_hourly={best_metrics['avg_sharpe_hourly']:.3f}, trades_total={best_metrics['trades_total']} over {len(symbols)} symbols."
    run_id = None
    if payload.persist:
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO sc.model_backtest_runs
                          (model_id, model_version, pack_id, timeframe, data_window, universe, featureset, label_cfg, params, metrics, best_config, summary, git_sha, tag, started_at, finished_at)
                        VALUES
                          (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        RETURNING run_id
                        """,
                        (
                            model_id,
                            int(ver),
                            payload.pack_id,
                            timeframe,
                            json.dumps({'start': sd, 'end': ed}),
                            json.dumps(payload.universe.dict() if hasattr(payload.universe, 'dict') else {}),
                            json.dumps(m_featureset or {}),
                            json.dumps(label_cfg.dict() if hasattr(label_cfg, 'dict') else {}),
                            json.dumps({'grid': payload.grid.dict() if hasattr(payload.grid, 'dict') else {}, 'chosen': best_cfg}),
                            json.dumps(best_metrics or {}),
                            json.dumps(best_cfg),
                            summary,
                            None,
                            payload.tag,
                        ),
                    )
                    rid = cur.fetchone()[0]
                    for r in (best_folds or []):
                        cur.execute(
                            """
                            INSERT INTO sc.model_backtest_folds (run_id, fold, thr_used, cum_ret, sharpe_hourly, trades)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (
                                rid,
                                int(r.get('fold', 0)),
                                (float(r.get('thr')) if r.get('thr') is not None else None),
                                float(r.get('cum_ret', 0.0)),
                                float(r.get('sharpe_hourly', 0.0)),
                                int(r.get('trades', 0)),
                            ),
                        )
                    conn.commit()
                    run_id = str(rid)
        except Exception:
            run_id = None
    return BacktestSweepOut(run_id=run_id, best_config=best_cfg, metrics=best_metrics or {}, summary=summary)


# --- Leaderboard endpoint (top backtest runs) ---
class LeaderboardRow(BaseModel):
    run_id: str
    model_id: Optional[str] = None
    model_version: Optional[int] = None
    timeframe: str
    metrics: Dict[str, Any]
    best_config: Dict[str, Any] | None = None
    tag: Optional[str] = None
    started_at: Optional[str] = None
    pack_id: Optional[str] = None
    summary: Optional[str] = None


@app.get("/backtests/leaderboard", response_model=List[LeaderboardRow], summary="Top backtest runs")
def backtests_leaderboard(
    model_id: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    timeframe: Optional[str] = Query(None),
    pack_id: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=200),
    order_by: str = Query("avg_sharpe_hourly", description="one of: avg_sharpe_hourly|cum_ret_sum|trades_total"),
):
    # Build SQL
    order_expr = "(metrics->>'avg_sharpe_hourly')::float DESC"
    if order_by == 'cum_ret_sum':
        order_expr = "(metrics->>'cum_ret_sum')::float DESC"
    elif order_by == 'trades_total':
        order_expr = "(metrics->>'trades_total')::int DESC"
    where = []
    params: List[Any] = []
    if model_id:
        where.append("model_id = %s"); params.append(model_id)
    if tag:
        where.append("tag = %s"); params.append(tag)
    if timeframe:
        where.append("timeframe = %s"); params.append(timeframe)
    if pack_id:
        where.append("pack_id = %s"); params.append(pack_id)
    sql = "SELECT run_id, model_id, model_version, timeframe, metrics, best_config, tag, started_at, pack_id, summary FROM sc.model_backtest_runs"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += f" ORDER BY {order_expr}, started_at DESC LIMIT %s"
    params.append(int(limit))
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            out: List[LeaderboardRow] = []
            for r in rows:
                out.append(LeaderboardRow(
                    run_id=str(r[0]),
                    model_id=r[1],
                    model_version=r[2],
                    timeframe=r[3],
                    metrics=r[4] or {},
                    best_config=r[5] or None,
                    tag=r[6],
                    started_at=str(r[7]) if r[7] else None,
                    pack_id=r[8],
                    summary=r[9],
                ))
            return out


# --- Sweep preset CRUD ---
class SweepPresetIn(BaseModel):
    preset_id: str
    title: str
    description: Optional[str] = None
    grid: Dict[str, Any]
    guardrails: Optional[Dict[str, Any]] = None


@app.post("/backtests/sweep_presets", status_code=201)
def create_sweep_preset(payload: SweepPresetIn = Body(...)):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO sc.backtest_sweep_presets (preset_id, title, description, grid, guardrails)
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (preset_id) DO UPDATE SET title=EXCLUDED.title, description=EXCLUDED.description, grid=EXCLUDED.grid, guardrails=EXCLUDED.guardrails, updated_at=NOW()
                RETURNING preset_id
                """,
                (payload.preset_id, payload.title, payload.description, json.dumps(payload.grid or {}), json.dumps(payload.guardrails or {})),
            )
            rid = cur.fetchone()[0]; conn.commit(); return {"preset_id": str(rid)}


@app.get("/backtests/sweep_presets", response_model=List[SweepPresetIn])
def list_sweep_presets():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT preset_id, title, description, grid, guardrails FROM sc.backtest_sweep_presets ORDER BY preset_id")
            rows = cur.fetchall()
            return [SweepPresetIn(preset_id=r[0], title=r[1], description=r[2], grid=r[3] or {}, guardrails=r[4] or {}) for r in rows]


@app.get("/backtests/sweep_presets/{preset_id}", response_model=SweepPresetIn)
def get_sweep_preset(preset_id: str):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT preset_id, title, description, grid, guardrails FROM sc.backtest_sweep_presets WHERE preset_id=%s", (preset_id,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="preset not found")
            return SweepPresetIn(preset_id=r[0], title=r[1], description=r[2], grid=r[3] or {}, guardrails=r[4] or {})


class ApplyBestCfgRequest(BaseModel):
    run_id: str
    confirm: bool = False


@app.post("/models/{model_id}/training_cfg/apply_best", summary="Apply best config from a backtest run to the model's training_cfg")
def apply_best_training_cfg(
    model_id: str,
    payload: ApplyBestCfgRequest = Body(..., example={"run_id": "00000000-0000-0000-0000-000000000000", "confirm": True})
):
    if not payload.confirm:
        raise HTTPException(status_code=400, detail="confirmation required; set confirm=true to proceed")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT model_version, best_config FROM sc.model_backtest_runs WHERE run_id = %s AND model_id = %s", (payload.run_id, model_id))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="backtest run not found for model")
            ver, best_cfg = r[0], r[1]
            if not ver:
                # default to latest published
                cur.execute("SELECT version FROM sc.v_model_specs_published WHERE model_id=%s", (model_id,))
                rr = cur.fetchone()
                if not rr:
                    raise HTTPException(status_code=404, detail="model has no published version to update")
                ver = int(rr[0])
            # Merge best_cfg into training_cfg.selection
            cur.execute("SELECT training_cfg FROM sc.model_specs WHERE model_id=%s AND version=%s", (model_id, int(ver)))
            rr = cur.fetchone()
            tc = rr[0] or {}
            sel = tc.get('selection', {}) if isinstance(tc, dict) else {}
            sel.update(best_cfg or {})
            tc['selection'] = sel
            cur.execute("UPDATE sc.model_specs SET training_cfg = %s, updated_at = NOW() WHERE model_id=%s AND version=%s", (json.dumps(tc), model_id, int(ver)))
            conn.commit()
            return {"model_id": model_id, "version": int(ver), "training_cfg": tc}


# --- Consensus backtest for model packs ---
class PackBacktestRequest(BaseModel):
    timeframe: str = "hour"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    universe: BacktestUniverseIn
    thresholds: Optional[List[float]] = [0.55, 0.6, 0.65]
    top_pct: Optional[float] = None
    splits: int = 5
    embargo: float = 0.0
    size_by_conf: bool = False
    conf_cap: float = 1.0
    allowed_hours: Optional[List[int]] = None
    mode: Optional[str] = None  # simple|advanced
    consensus_override: Optional[Dict[str, Any]] = None


def _combine_probs_weighted(y_proba_list: List[Dict[str, Any]], weights: List[float]) -> Dict[str, Any]:
    import numpy as np
    w = np.array(weights, dtype=float)
    w = np.where(w > 0, w, 0.0)
    wsum = w.sum() if w.sum() > 0 else 1.0
    p_up_acc = None; p_down_acc = None
    for i, fo in enumerate(y_proba_list):
        classes = fo['classes']
        c2i = {c: idx for idx, c in enumerate(classes)}
        arr = np.array(fo['y_proba'], dtype=float)
        p_up = arr[:, c2i.get('UP', 0)] if 'UP' in c2i else np.zeros(arr.shape[0])
        p_down = arr[:, c2i.get('DOWN', 1)] if 'DOWN' in c2i else np.zeros(arr.shape[0])
        if p_up_acc is None:
            p_up_acc = w[i] * p_up
            p_down_acc = w[i] * p_down
        else:
            p_up_acc += w[i] * p_up
            p_down_acc += w[i] * p_down
    p_up_comb = (p_up_acc / wsum) if p_up_acc is not None else np.zeros_like(y_proba_list[0]['y_proba'])
    p_down_comb = (p_down_acc / wsum) if p_down_acc is not None else np.zeros_like(y_proba_list[0]['y_proba'])
    return { 'p_up': p_up_comb, 'p_down': p_down_comb }


def _positions_from_probs(p_up, p_down, *, thresholds: Optional[List[float]], top_pct: Optional[float], size_by_conf: bool, conf_cap: float):
    import numpy as np
    sign_dir = np.where(p_up >= p_down, 1.0, -1.0)
    if top_pct is not None and top_pct != "":
        conf = np.maximum(p_up, p_down)
        n = len(conf)
        k = max(1, int(np.floor(float(top_pct) * n)))
        idx = np.argsort(-conf)[:k]
        pos = np.zeros(n, dtype=float)
        pos[idx] = sign_dir[idx]
        if size_by_conf:
            conf_sel = np.maximum(0.0, 2.0 * conf[idx] - 1.0)
            pos[idx] = pos[idx] * np.minimum(conf_sel, float(conf_cap))
        return pos, None
    best = None
    for thr in (thresholds or []):
        long = (p_up >= thr) & (p_up > p_down)
        short = (p_down >= thr) & (p_down > p_up)
        pos = np.where(long, 1.0, np.where(short, -1.0, 0.0)).astype(float)
        if size_by_conf:
            conf = np.maximum(p_up, p_down)
            size = np.minimum(np.maximum(0.0, 2.0 * conf - 1.0), float(conf_cap))
            pos = pos * size
        sc = float(np.mean(pos != 0.0))
        if best is None or sc > best[0]:
            best = (sc, float(thr), pos)
    return (best[2] if best else (np.zeros_like(p_up))), (best[1] if best else None)


def _positions_from_policy(yps: List[Dict[str, Any]], weights: List[float], consensus: Dict[str, Any] | None, *, thresholds: Optional[List[float]], top_pct: Optional[float], size_by_conf: bool, conf_cap: float):
    import numpy as np
    policy = (consensus or {}).get('policy', 'weighted')
    if policy == 'weighted':
        comb = _combine_probs_weighted(yps, weights)
        return _positions_from_probs(comb['p_up'], comb['p_down'], thresholds=thresholds, top_pct=top_pct, size_by_conf=size_by_conf, conf_cap=conf_cap)
    # Voting policies
    min_score = float((consensus or {}).get('min_score') or 0.5)
    quorum = (consensus or {}).get('min_quorum')
    # Determine total weight for normalization/quorum default
    w = np.array(weights, dtype=float)
    w = np.where(w > 0, w, 0.0)
    W = float(w.sum() if w.sum() > 0 else len(weights))
    if quorum is None:
        quorum = 0.5 * W
    else:
        try:
            quorum = float(quorum)
        except Exception:
            quorum = 0.5 * W
    # Build votes per model
    n = len(yps[0]['y_proba']) if yps else 0
    vote_sum = np.zeros(n, dtype=float)
    agree_all = np.ones(n, dtype=bool)
    for i, fo in enumerate(yps):
        classes = fo['classes']; c2i = {c: idx for idx, c in enumerate(classes)}
        arr = np.array(fo['y_proba'], dtype=float)
        p_up = arr[:, c2i.get('UP', 0)] if 'UP' in c2i else np.zeros(n)
        p_down = arr[:, c2i.get('DOWN', 1)] if 'DOWN' in c2i else np.zeros(n)
        conf = np.maximum(p_up, p_down)
        sign = np.where((p_up > p_down) & (conf >= min_score), 1.0, np.where((p_down > p_up) & (conf >= min_score), -1.0, 0.0))
        vote_sum += w[i] * sign
        agree_all &= (sign != 0) & (sign == np.sign(vote_sum))
    policy_l = policy.lower()
    if policy_l == 'all':
        pos = np.where(agree_all, np.sign(vote_sum), 0.0).astype(float)
    else:  # majority or others
        pos = np.where(np.abs(vote_sum) >= float(quorum), np.sign(vote_sum), 0.0).astype(float)
    if size_by_conf:
        # scale by normalized vote strength
        scale = np.minimum(np.abs(vote_sum) / (W + 1e-9), float(conf_cap))
        pos = pos * scale
    return pos, None


@app.post("/packs/{pack_id}/backtest/run", summary="Consensus backtest for a model pack")
def pack_backtest_run(
    pack_id: str,
    payload: PackBacktestRequest = Body(
        ..., example={
            "timeframe": "hour",
            "universe": {"preset_id": "liquid_etfs", "cap": 10},
            "thresholds": [0.55, 0.6, 0.65],
            "consensus_override": {"policy": "majority", "min_quorum": 1.5, "min_score": 0.6}
        }
    ),
    user: User = Depends(get_current_user),
    persist: bool = Query(False),
    tag: Optional[str] = Query(None)
):
    # Load pack and components
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version, consensus FROM sc.v_model_packs_published WHERE pack_id=%s", (pack_id,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="pack not found")
            pver, consensus = int(r[0]), r[1] or {}
            cur.execute("SELECT model_id, model_version, weight FROM sc.model_pack_components WHERE pack_id=%s AND pack_version=%s ORDER BY ord", (pack_id, pver))
            comps = cur.fetchall()
            if not comps:
                raise HTTPException(status_code=400, detail="pack has no components")
            models = [(c[0], int(c[1] or 1), float(c[2] or 1.0)) for c in comps]
            model_specs = {}
            for mid, mver, _w in models:
                cur.execute("SELECT featureset, label_cfg FROM sc.model_specs WHERE model_id=%s AND version=%s", (mid, mver))
                rr = cur.fetchone()
                if not rr:
                    raise HTTPException(status_code=404, detail=f"model {mid}@{mver} not found")
                model_specs[(mid, mver)] = { 'featureset': rr[0] or {}, 'label_cfg': rr[1] or {} }
    # Apply optional consensus override
    if payload.consensus_override:
        try:
            consensus = {**(consensus or {}), **(payload.consensus_override or {})}
        except Exception:
            pass
    # Dates/universe
    sd, ed = payload.start_date, payload.end_date
    if not sd or not ed:
        sd, ed = _default_dates()
    if _days_between(sd, ed) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    symbols = _resolve_symbols_from_universe(payload.universe, user)
    if not symbols:
        raise HTTPException(status_code=400, detail="no symbols resolved for pack backtest")
    symbols = symbols[:max(1, int(payload.universe.cap or 50))]
    # Base data + label
    frames = []
    for sym in symbols:
        df = _fetch_bars(sym, payload.timeframe, sd, ed)
        if df is None or df.empty:
            continue
        df = _maybe_add_hour_et(df)
        frames.append(df)
    if not frames:
        raise HTTPException(status_code=400, detail="no data fetched for pack backtest")
    base = pd.concat(frames, axis=0, ignore_index=True)
    first_mid, first_ver, _ = models[0]
    first_label = model_specs[(first_mid, first_ver)]['label_cfg'] or {}
    label_def = BacktestLabelCfg(kind=(first_label.get('kind') or 'hourly_direction'), params=first_label.get('params') or {})
    base_l = _apply_label(base, label_def)
    target_col = 'y' if 'y' in base_l.columns else ('y_syn' if 'y_syn' in base_l.columns else None)
    if not target_col:
        raise HTTPException(status_code=400, detail="labels not available for pack dataset")
    # Determine effective thresholds/top_pct/allowed_hours (simple mode)
    thresholds_use = payload.thresholds
    top_pct_use = payload.top_pct
    hours_use = payload.allowed_hours
    if (payload.mode or '').lower() == 'simple' and thresholds_use is None and top_pct_use is None:
        # Try preset 'rth_thresholds_basic'
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT grid FROM sc.backtest_sweep_presets WHERE preset_id = 'rth_thresholds_basic'")
                    rr = cur.fetchone()
                    if rr and rr[0]:
                        grid = rr[0] or {}
                        thr_list = (grid.get('thresholds_list') or [[]])
                        thresholds_use = thr_list[0] if thr_list and thr_list[0] else [0.55, 0.6, 0.65]
                        hrs_list = (grid.get('allowed_hours_list') or [[]])
                        hours_use = hrs_list[0] if hrs_list and hrs_list[0] else [9,10,11,12,13,14,15]
        except Exception:
            thresholds_use = thresholds_use or [0.55, 0.6, 0.65]
            hours_use = hours_use or [9,10,11,12,13,14,15]
    # Per-model fold outputs
    fold_outputs_per_model: List[List[Dict[str, Any]]] = []
    weights: List[float] = []
    for mid, mver, w in models:
        fb = _build_fb_for_featureset(None, model_specs[(mid, mver)]['featureset'])
        dfm = fb.add_indicator_features(base_l)
        res = engine_run_backtest(
            dfm,
            target_col=target_col,
            thresholds=thresholds_use or [],
            splits=int(payload.splits or 5),
            embargo=float(payload.embargo or 0.0),
            top_pct=top_pct_use,
            allowed_hours=hours_use,
            size_by_conf=bool(payload.size_by_conf),
            conf_cap=float(payload.conf_cap or 1.0),
            return_fold_outputs=True,
        )
        fold_outputs_per_model.append(res.get('fold_outputs') or [])
        weights.append(float(w))
    # Combine per-fold
    import numpy as np
    threshold_results: List[Dict[str, Any]] = []
    for k in range(len(fold_outputs_per_model[0])):
        yps = [fold_outputs_per_model[i][k] for i in range(len(fold_outputs_per_model))]
        pos, thr_used = _positions_from_policy(yps, weights, consensus, thresholds=thresholds_use, top_pct=top_pct_use, size_by_conf=bool(payload.size_by_conf), conf_cap=float(payload.conf_cap or 1.0))
        test_idx = yps[0]['test_idx']
        y_all = base_l[target_col].astype(str).values
        y_dir = np.where(y_all == 'UP', 1.0, np.where(y_all == 'DOWN', -1.0, 0.0))
        pnl = (pos * y_dir[test_idx]); pnl -= np.where(pos != 0, 1.0/10000.0, 0.0)
        threshold_results.append({ 'fold': k, 'thr': thr_used, 'cum_ret': float(np.sum(pnl)), 'sharpe_hourly': float(np.mean(pnl)/(np.std(pnl)+1e-9)), 'trades': int(np.sum(np.abs(pos)>0)) })
    # Aggregate + persist
    try:
        import numpy as _np
        sh = [float(r.get('sharpe_hourly', 0.0)) for r in threshold_results]
        tr = [int(r.get('trades', 0)) for r in threshold_results]
        cr = [float(r.get('cum_ret', 0.0)) for r in threshold_results]
        metrics = { 'avg_sharpe_hourly': float(_np.mean(sh)), 'trades_total': int(sum(tr)), 'cum_ret_sum': float(sum(cr)) }
    except Exception:
        metrics = {}
    summary = f"Pack {pack_id} on {len(symbols)} symbols ({payload.timeframe}) — avg_sharpe={metrics.get('avg_sharpe_hourly',0):.3f}, trades={metrics.get('trades_total',0)}"
    if persist:
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO sc.model_backtest_runs (pack_id, timeframe, data_window, universe, featureset, label_cfg, params, metrics, best_config, summary, tag, started_at, finished_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW()) RETURNING run_id
                        """,
                        (
                            pack_id,
                            payload.timeframe,
                            json.dumps({'start': sd, 'end': ed}),
                            json.dumps(payload.universe.dict() if hasattr(payload.universe, 'dict') else {}),
                            json.dumps({'pack_version': pver, 'models': [{'model_id': mid, 'version': mver} for mid, mver, _ in models]}),
                            json.dumps(label_def.dict() if hasattr(label_def, 'dict') else {}),
                            json.dumps({'thresholds': payload.thresholds, 'top_pct': payload.top_pct, 'splits': payload.splits, 'embargo': payload.embargo, 'policy': consensus}),
                            json.dumps(metrics or {}),
                            json.dumps({'consensus': consensus}),
                            summary,
                            tag,
                        ),
                    )
                    rid = cur.fetchone()[0]
                    for r in threshold_results:
                        cur.execute("INSERT INTO sc.model_backtest_folds (run_id, fold, thr_used, cum_ret, sharpe_hourly, trades) VALUES (%s,%s,%s,%s,%s,%s)", (rid, int(r.get('fold',0)), (float(r.get('thr')) if r.get('thr') is not None else None), float(r.get('cum_ret',0.0)), float(r.get('sharpe_hourly',0.0)), int(r.get('trades',0))))
                    conn.commit()
        except Exception:
            pass
    return { 'threshold_results': threshold_results, 'metrics': metrics, 'summary': summary }


class PackBacktestSweepGrid(BaseModel):
    thresholds_list: Optional[List[List[float]]] = None
    top_pct_list: Optional[List[float]] = None
    max_combos: int = 50
    min_trades: int = 50


class PackBacktestSweepRequest(BaseModel):
    mode: Optional[str] = None  # simple|advanced
    timeframe: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    universe: BacktestUniverseIn
    grid: PackBacktestSweepGrid
    persist: bool = True
    tag: Optional[str] = None
    consensus_override: Optional[Dict[str, Any]] = None


@app.post("/packs/{pack_id}/backtest/sweep", summary="Grid-search consensus backtest for a model pack")
def pack_backtest_sweep(
    pack_id: str,
    payload: PackBacktestSweepRequest = Body(
        ..., example={
            "universe": {"preset_id": "liquid_etfs", "cap": 20},
            "grid": {"thresholds_list": [[0.55, 0.6, 0.65]]},
            "persist": True,
            "tag": "pack-sweep-demo",
            "consensus_override": {"policy": "all", "min_score": 0.6}
        }
    ),
    user: User = Depends(get_current_user)
):
    # Load pack and models
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version, consensus, timeframe FROM sc.v_model_packs_published WHERE pack_id=%s", (pack_id,))
            r = cur.fetchone()
            if not r:
                raise HTTPException(status_code=404, detail="pack not found")
            pver, consensus, p_tf = int(r[0]), (r[1] or {}), (r[2] or None)
            cur.execute("SELECT model_id, model_version, weight FROM sc.model_pack_components WHERE pack_id=%s AND pack_version=%s ORDER BY ord", (pack_id, pver))
            comps = cur.fetchall()
            if not comps:
                raise HTTPException(status_code=400, detail="pack has no components")
            models = [(c[0], int(c[1] or 1), float(c[2] or 1.0)) for c in comps]
            model_specs = {}
            for mid, mver, _w in models:
                cur.execute("SELECT featureset, label_cfg FROM sc.model_specs WHERE model_id=%s AND version=%s", (mid, mver))
                rr = cur.fetchone()
                if not rr:
                    raise HTTPException(status_code=404, detail=f"model {mid}@{mver} not found")
                model_specs[(mid, mver)] = { 'featureset': rr[0] or {}, 'label_cfg': rr[1] or {} }
    # Apply optional consensus override
    if payload.consensus_override:
        try:
            consensus = {**(consensus or {}), **(payload.consensus_override or {})}
        except Exception:
            pass
    timeframe = payload.timeframe or p_tf or 'day'
    sd, ed = payload.start_date, payload.end_date
    if not sd or not ed:
        sd, ed = _default_dates()
    if _days_between(sd, ed) > 90:
        raise HTTPException(status_code=400, detail="date window too large; limit to <= 90 days")
    symbols = _resolve_symbols_from_universe(payload.universe, user)
    if not symbols:
        raise HTTPException(status_code=400, detail="no symbols resolved for sweep")
    symbols = symbols[:max(1, int(payload.universe.cap or 50))]
    # Base + label
    frames = []
    for sym in symbols:
        df = _fetch_bars(sym, timeframe, sd, ed)
        if df is None or df.empty:
            continue
        df = _maybe_add_hour_et(df)
        frames.append(df)
    if not frames:
        raise HTTPException(status_code=400, detail="no data for sweep")
    base = pd.concat(frames, axis=0, ignore_index=True)
    first_mid, first_ver, _ = models[0]
    first_label = model_specs[(first_mid, first_ver)]['label_cfg'] or {}
    label_def = BacktestLabelCfg(kind=(first_label.get('kind') or 'hourly_direction'), params=first_label.get('params') or {})
    base_l = _apply_label(base, label_def)
    target_col = 'y' if 'y' in base_l.columns else ('y_syn' if 'y_syn' in base_l.columns else None)
    if not target_col:
        raise HTTPException(status_code=400, detail="labels unavailable for sweep")
    # Fold outputs per model (one pass)
    fold_outputs_per_model: List[List[Dict[str, Any]]] = []
    weights: List[float] = []
    for mid, mver, w in models:
        fb = _build_fb_for_featureset(None, model_specs[(mid, mver)]['featureset'])
        dfm = fb.add_indicator_features(base_l)
        # Simple mode: default to RTH hours
        hours_use = [9,10,11,12,13,14,15] if ((payload.mode or 'advanced').lower()=='simple') else None
        res = engine_run_backtest(dfm, target_col=target_col, thresholds=[0.5], splits=5, embargo=0.0, allowed_hours=hours_use, return_fold_outputs=True)
        fold_outputs_per_model.append(res.get('fold_outputs') or [])
        weights.append(float(w))
    # Grid
    g = payload.grid
    thresholds_list = g.thresholds_list or []
    top_pct_list = g.top_pct_list or []
    if thresholds_list and top_pct_list:
        raise HTTPException(status_code=400, detail="provide thresholds_list or top_pct_list, not both")
    if not thresholds_list and not top_pct_list:
        thresholds_list = [[0.55, 0.6, 0.65]]
    candidates = []
    for thrs in thresholds_list or [None]:
        for tpct in top_pct_list or [None]:
            candidates.append({'thresholds': thrs, 'top_pct': tpct})
    if len(candidates) > int(g.max_combos or 50):
        raise HTTPException(status_code=400, detail=f"too many grid combos ({len(candidates)})")
    # Evaluate
    import numpy as np
    best = None; best_metrics = None
    for cfg in candidates:
        threshold_results = []
        for k in range(len(fold_outputs_per_model[0])):
            yps = [fold_outputs_per_model[i][k] for i in range(len(fold_outputs_per_model))]
            pos, thr_used = _positions_from_policy(yps, weights, consensus, thresholds=cfg['thresholds'], top_pct=cfg['top_pct'], size_by_conf=False, conf_cap=1.0)
            test_idx = yps[0]['test_idx']
            y_all = base_l[target_col].astype(str).values
            y_dir = np.where(y_all == 'UP', 1.0, np.where(y_all == 'DOWN', -1.0, 0.0))
            pnl = (pos * y_dir[test_idx]); pnl -= np.where(pos != 0, 1.0/10000.0, 0.0)
            threshold_results.append({'fold': k, 'thr': thr_used, 'cum_ret': float(np.sum(pnl)), 'sharpe_hourly': float(np.mean(pnl)/(np.std(pnl)+1e-9)), 'trades': int(np.sum(np.abs(pos)>0))})
        try:
            import numpy as _np
            sh = [float(r.get('sharpe_hourly', 0.0)) for r in threshold_results]
            tr = [int(r.get('trades', 0)) for r in threshold_results]
            avg_sh = float(_np.mean(sh)) if sh else 0.0
            trades_total = int(sum(tr))
        except Exception:
            avg_sh = 0.0; trades_total = 0
        if trades_total < int(g.min_trades or 50):
            continue
        score = avg_sh
        if (best is None) or (score > best[0]):
            best = (score, cfg, threshold_results)
            best_metrics = {'avg_sharpe_hourly': avg_sh, 'trades_total': trades_total}
    if not best:
        raise HTTPException(status_code=400, detail="no configuration met minimum trades or produced metrics")
    _, best_cfg, best_folds = best
    summary = f"Pack {pack_id} best: {'top_pct='+str(best_cfg['top_pct']) if best_cfg.get('top_pct') is not None else 'thresholds'} avg_sharpe={best_metrics['avg_sharpe_hourly']:.3f}, trades_total={best_metrics['trades_total']}"
    run_id = None
    if payload.persist:
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO sc.model_backtest_runs (pack_id, timeframe, data_window, universe, featureset, label_cfg, params, metrics, best_config, summary, tag, started_at, finished_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW()) RETURNING run_id
                        """,
                        (
                            pack_id,
                            timeframe,
                            json.dumps({'start': sd, 'end': ed}),
                            json.dumps(payload.universe.dict() if hasattr(payload.universe, 'dict') else {}),
                            json.dumps({'pack_version': pver, 'models': [{'model_id': mid, 'version': mver} for mid, mver, _ in models]}),
                            json.dumps(label_def.dict() if hasattr(label_def, 'dict') else {}),
                            json.dumps({'grid': payload.grid.dict() if hasattr(payload.grid, 'dict') else {}, 'chosen': best_cfg}),
                            json.dumps(best_metrics or {}),
                            json.dumps(best_cfg),
                            summary,
                            payload.tag,
                        ),
                    )
                    rid = cur.fetchone()[0]
                    for r in (best_folds or []):
                        cur.execute("INSERT INTO sc.model_backtest_folds (run_id, fold, thr_used, cum_ret, sharpe_hourly, trades) VALUES (%s,%s,%s,%s,%s,%s)", (rid, int(r.get('fold',0)), (float(r.get('thr')) if r.get('thr') is not None else None), float(r.get('cum_ret',0.0)), float(r.get('sharpe_hourly',0.0)), int(r.get('trades',0))))
                    conn.commit(); run_id = str(rid)
        except Exception:
            run_id = None
    return { 'run_id': run_id, 'best_config': best_cfg, 'metrics': best_metrics or {}, 'summary': summary }
