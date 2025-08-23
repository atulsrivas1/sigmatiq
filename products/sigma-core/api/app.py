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
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:cap]
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
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:cap]
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
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:cap]
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
    symbols = _resolve_universe_symbols(payload.preset_id, payload.watchlist_id, user)
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:cap]

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
    cap = max(1, int(payload.cap or 50))
    symbols = symbols[:cap]

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
def create_watchlist(payload: WatchlistCreate = Body(..., example={"name":"starter","description":"demo list","visibility":"private","is_default":true}), user: User = Depends(get_current_user)):
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
def create_indicator_set(payload: IndicatorSetCreateIn = Body(..., example={"set_id":"demo_set","version":1,"status":"draft","title":"Demo Set","purpose":"Testing","novice_ready":false,"components":[{"indicator_id":"rsi","indicator_version":1,"params":{"period":14}}]})):
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
def create_strategy(payload: StrategyCreateIn = Body(..., example={"strategy_id":"trend_follow_alignment","version":1,"status":"draft","title":"Trend Follow Alignment","novice_ready":false,"indicator_sets":[{"set_id":"macd_trend_pullback_v1","set_version":1}]})):
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
def validate_strategy(payload: StrategyValidateIn = Body(..., example={"strategy":{"strategy_id":"trend_follow_alignment","version":1,"status":"draft","title":"Trend Follow Alignment","novice_ready":false,"indicator_sets":[{"set_id":"macd_trend_pullback_v1","set_version":1}]}})):
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

