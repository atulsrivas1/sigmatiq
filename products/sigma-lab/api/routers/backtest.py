from __future__ import annotations
from typing import Optional, List, Any, Dict
from fastapi import APIRouter, Query
from pydantic import BaseModel, validator
from datetime import datetime
import pandas as pd

from sigma_core.backtest.engine import run_backtest
from sigma_core.registry.backtest_registry import create_backtest_run, leaderboard as db_leaderboard, create_backtest_folds
from sigma_platform.io import workspace_paths, resolve_indicator_set_path, PACKS_DIR
from sigma_platform.policy import load_policy
try:
    from sigma_platform.lineage import compute_lineage as _compute_lineage
except Exception:
    _compute_lineage = None
try:
    from sigma_platform.model_cards import write_model_card
except Exception:
    write_model_card = None

router = APIRouter()


class BacktestRequest(BaseModel):
    model_id: str
    csv: Optional[str] = None
    target: Optional[str] = None
    thresholds: Optional[str | List[float]] = None
    splits: int = 5
    embargo: float = 0.0
    top_pct: Optional[float] = None
    allowed_hours: Optional[str | List[int]] = None
    slippage_bps: float = 1.0
    size_by_conf: bool = False
    conf_cap: float = 1.0
    per_hour_thresholds: bool = False
    per_hour_select_by: str = 'sharpe'
    calibration: Optional[str] = 'sigmoid'
    pack_id: Optional[str] = 'zerosigma'
    momentum_gate: Optional[bool] = None
    momentum_min: Optional[float] = None
    momentum_column: Optional[str] = None
    save: Optional[bool] = True
    tag: Optional[str] = None

    @validator('allowed_hours', pre=True)
    def _coerce_hours(cls, v):  # type: ignore
        if v is None or isinstance(v, list):
            return v
        if isinstance(v, str) and v.strip():
            try:
                return [int(x) for x in v.split(',') if x.strip()]
            except Exception:
                raise ValueError('allowed_hours must be a list of ints or comma-separated ints')
        return None

    @validator('thresholds', pre=True)
    def _coerce_thresholds(cls, v):  # type: ignore
        if v is None or isinstance(v, list):
            return v
        if isinstance(v, str) and v.strip():
            try:
                return [float(x) for x in v.split(',') if x.strip()]
            except Exception:
                raise ValueError('thresholds must be a list of floats or comma-separated floats')
        return None

    @validator('per_hour_select_by', pre=True)
    def _validate_select_by(cls, v):  # type: ignore
        v = str(v or 'sharpe')
        if v not in ('sharpe','cum_ret','trades'):
            raise ValueError("per_hour_select_by must be one of: sharpe, cum_ret, trades")
        return v

    @validator('calibration', pre=True)
    def _check_calibration(cls, v):  # type: ignore
        if v in (None, 'none', 'sigmoid', 'isotonic'):
            return v
        raise ValueError("calibration must be one of: none, sigmoid, isotonic")


@router.post('/backtest')
def backtest_ep(payload: BacktestRequest):
    model_id = payload.model_id
    if not model_id:
        return {"ok": False, "error": "model_id is required"}
    if run_backtest is None:
        return {"ok": False, "error": "Backtest dep missing"}
    pack_id = payload.pack_id or 'zerosigma'
    paths = workspace_paths(model_id, pack_id)
    csv = payload.csv or str(paths['matrices'] / 'training_matrix_built.csv')
    started_at = datetime.utcnow()
    try:
        df = pd.read_csv(csv)
        target_col = payload.target or ('y' if 'y' in df.columns and df['y'].notna().any() else 'y_syn')
        thr_raw = payload.thresholds or '0.55,0.60,0.65,0.70'
        if isinstance(thr_raw, str):
            thresholds = [float(x) for x in thr_raw.split(',')]
        else:
            thresholds = [float(x) for x in thr_raw]
        allowed_hours = payload.allowed_hours
        if isinstance(allowed_hours, str) and allowed_hours:
            allowed_hours = [int(x) for x in allowed_hours.split(',')]
        pol = load_policy(model_id, pack_id)
        exec_pol = pol.get('execution', {}) if isinstance(pol.get('execution', {}), dict) else {}
        mgate = payload.momentum_gate if payload.momentum_gate is not None else bool(exec_pol.get('momentum_gate', False))
        mmin = float(payload.momentum_min) if payload.momentum_min is not None else float(exec_pol.get('momentum_min', 0.0))
        mcol = payload.momentum_column if payload.momentum_column is not None else str(exec_pol.get('momentum_column', 'momentum_score_total'))

        res = run_backtest(
            df,
            target_col,
            thresholds,
            splits=int(payload.splits),
            embargo=float(payload.embargo),
            top_pct=(float(payload.top_pct) if payload.top_pct not in (None, '', False) else None),
            plots_dir=str(paths['plots']),
            allowed_hours=allowed_hours,
            slippage_bps=float(payload.slippage_bps),
            size_by_conf=bool(payload.size_by_conf),
            conf_cap=float(payload.conf_cap),
            per_hour_thresholds=bool(payload.per_hour_thresholds),
            per_hour_select_by=str(payload.per_hour_select_by),
            calibration=(None if payload.calibration in (None, 'none') else payload.calibration),
            momentum_gate=bool(mgate),
            momentum_min=float(mmin),
            momentum_column=str(mcol),
        )
        finished_at = datetime.utcnow()
        # Leaderboard convenience
        best_sharpe = None
        best_cum = None
        try:
            th = res.get('threshold_results') or []
            if th:
                best_sharpe = float(max((r.get('sharpe_hourly', 0.0) for r in th)))
                best_cum = float(max((r.get('cum_ret', 0.0) for r in th)))
        except Exception:
            pass
        # --- Parity backtest (stocks) for entry_mode=next_session_open with ATR brackets ---
        parity = None
        try:
            exec_pol = pol.get('execution', {}) if isinstance(pol.get('execution', {}), dict) else {}
            br = exec_pol.get('brackets', {}) if isinstance(exec_pol.get('brackets', {}), dict) else {}
            if br:
                parity = _parity_bracket_next_session_open(df, br)
        except Exception:
            parity = None

        if bool(payload.save):
            try:
                params_store = {
                    'csv': csv,
                    'target': target_col,
                    'thresholds': thresholds,
                    'splits': int(payload.splits),
                    'embargo': float(payload.embargo),
                    'top_pct': (float(payload.top_pct) if payload.top_pct not in (None, '', False) else None),
                    'allowed_hours': allowed_hours,
                    'slippage_bps': float(payload.slippage_bps),
                    'size_by_conf': bool(payload.size_by_conf),
                    'conf_cap': float(payload.conf_cap),
                    'per_hour_thresholds': bool(payload.per_hour_thresholds),
                    'per_hour_select_by': str(payload.per_hour_select_by),
                    'calibration': (None if payload.calibration in (None, 'none') else payload.calibration),
                    'momentum_gate': bool(mgate),
                    'momentum_min': float(mmin),
                    'momentum_column': str(mcol),
                }
                # Attach lineage fingerprints into params
                try:
                    ind_path = resolve_indicator_set_path(pack_id, model_id)
                except Exception:
                    ind_path = None
                lineage_vals = None
                if _compute_lineage is not None:
                    try:
                        pack_dir = PACKS_DIR / pack_id
                        lineage_vals = _compute_lineage(pack_dir=pack_dir, model_id=model_id, indicator_set_path=ind_path)
                        params_store['lineage'] = lineage_vals
                    except Exception:
                        pass
                # attach parity summary into metrics to persist
                metrics_store = {'best_sharpe_hourly': best_sharpe, 'best_cum_ret': best_cum}
                if parity is not None:
                    metrics_store['parity'] = parity
                run_row = create_backtest_run(
                    pack_id=pack_id,
                    model_id=model_id,
                    started_at=started_at,
                    finished_at=finished_at,
                    params=params_store,
                    metrics=metrics_store,
                    plots_uri=str(paths['plots']),
                    data_csv_uri=csv,
                    best_sharpe_hourly=best_sharpe,
                    best_cum_ret=best_cum,
                    trades_total=None,
                    tag=payload.tag,
                )
                folds = res.get('threshold_results') or []
                rows = []
                for i, r in enumerate(folds):
                    rows.append({'fold': i, 'thr': r.get('thr'), 'cum_ret': r.get('cum_ret'), 'sharpe_hourly': r.get('sharpe_hourly'), 'trades': r.get('trades')})
                if rows:
                    create_backtest_folds(int(run_row['id']), rows)
            except Exception:
                pass
        # Write model card for backtest
        try:
            if write_model_card is not None:
                metrics_for_card = {'best_sharpe_hourly': best_sharpe, 'best_cum_ret': best_cum}
                if parity is not None:
                    metrics_for_card['parity'] = parity
                # prefer the lineage we computed above; recompute if missing
                if _compute_lineage is not None and 'lineage' not in locals():
                    try:
                        ind_path = resolve_indicator_set_path(pack_id, model_id)
                        lineage_vals = _compute_lineage(pack_dir=PACKS_DIR / pack_id, model_id=model_id, indicator_set_path=ind_path)
                    except Exception:
                        lineage_vals = None
                write_model_card(
                    pack_id=pack_id,
                    model_id=model_id,
                    event='backtest',
                    params={'thresholds': thresholds, 'allowed_hours': allowed_hours, 'per_hour_thresholds': bool(payload.per_hour_thresholds), 'per_hour_select_by': str(payload.per_hour_select_by), 'calibration': (None if payload.calibration in (None, 'none') else payload.calibration)},
                    metrics=metrics_for_card,
                    lineage=lineage_vals,
                )
        except Exception:
            pass
        return {'ok': True, 'result': res, 'best_sharpe_hourly': best_sharpe, 'best_cum_ret': best_cum, 'parity': parity}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@router.get('/leaderboard')
def leaderboard_api(
    pack_id: Optional[str] = Query(None),
    model_id: Optional[str] = Query(None),
    limit: int = Query(20),
    order_by: str = Query('sharpe_hourly'),
    offset: int = Query(0),
    tag: Optional[str] = Query(None),
):
    try:
        # fetch a bit more when filtering by tag to avoid empty pages
        base_limit = int(limit) * (2 if tag else 1)
        rows = db_leaderboard(pack_id=pack_id, model_id=model_id, limit=base_limit, order_by=order_by, offset=int(offset))
        if tag:
            try:
                rows = [r for r in rows if (r.get('tag') == tag)]
            except Exception:
                rows = rows
        rows = rows[: int(limit)]
        return {
            'ok': True,
            'rows': rows,
            'limit': int(limit),
            'offset': int(offset),
            'next_offset': int(offset) + len(rows),
            'tag': tag,
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}
def _parity_bracket_next_session_open(df: pd.DataFrame, br: Dict[str, Any]) -> Dict[str, Any]:
    try:
        d = df.copy()
        # Ensure datetime and date columns
        ts_col = None
        for c in ('datetime','timestamp','ts','dt'):
            if c in d.columns:
                ts_col = c; break
        if ts_col is None:
            # try to compose from date + hour
            if 'date' in d.columns and 'hour_et' in d.columns:
                d['_ts'] = pd.to_datetime(d['date'].astype(str)) + pd.to_timedelta(pd.to_numeric(d['hour_et'], errors='coerce').fillna(0).astype(int), unit='h')
                ts_col = '_ts'
            else:
                d['_ts'] = pd.to_datetime(d.index)
                ts_col = '_ts'
        d['_date'] = pd.to_datetime(d[ts_col]).dt.date
        # Identify last index of each session and first index of next session
        groups = d.groupby('_date')
        last_idx = groups.tail(1).index
        # map from a date to first index of that date
        first_idx_by_date = groups.head(1).reset_index().set_index('_date')['index'].to_dict() if hasattr(groups, 'head') else {r['_date']: r.name for _, r in d.groupby('_date')}
        # Bracket params
        atr_period = int(br.get('atr_period', 14))
        atr_mult_stop = float(br.get('atr_mult_stop', 1.5))
        atr_mult_target = float(br.get('atr_mult_target', 3.0))
        time_stop_minutes = int(br.get('time_stop_minutes', 120))
        bars_stop = max(1, int(round(time_stop_minutes / 60.0)))
        # ATR source
        if any(d.columns.str.startswith('atr_')):
            atr_series = pd.to_numeric(d.filter(like='atr_').iloc[:,0], errors='coerce')
        else:
            # simple ATR proxy from high-low
            hi = pd.to_numeric(d.get('high', d.get('close')), errors='coerce')
            lo = pd.to_numeric(d.get('low', d.get('close')), errors='coerce')
            atr_series = (hi - lo).abs().rolling(atr_period, min_periods=1).mean()

        opens = pd.to_numeric(d.get('open', d.get('close')), errors='coerce')
        highs = pd.to_numeric(d.get('high', d.get('close')), errors='coerce')
        lows = pd.to_numeric(d.get('low', d.get('close')), errors='coerce')

        trades = 0
        hits = 0
        pnl_sum = 0.0
        rr_sum = 0.0
        # Build dates once
        dates = sorted(d['_date'].unique())
        date_to_pos = {dt: k for k, dt in enumerate(dates)}
        for i in last_idx:
            cur_date = d.loc[i, '_date']
            pos = date_to_pos.get(cur_date, None)
            if pos is None or pos+1 >= len(dates):
                continue
            next_date = dates[pos+1]
            j = first_idx_by_date.get(next_date)
            if j is None:
                continue
            entry = float(opens.loc[j]) if pd.notna(opens.loc[j]) else None
            if entry is None:
                continue
            atr = float(atr_series.loc[j]) if pd.notna(atr_series.loc[j]) else None
            if atr is None:
                continue
            stop = entry - atr_mult_stop * atr
            target = entry + atr_mult_target * atr
            # iterate bars of next_date only, or up to bars_stop
            k = j
            bars = 0
            hit = None
            while k < len(d) and d.loc[k, '_date'] == next_date and bars < bars_stop:
                h = float(highs.loc[k]) if pd.notna(highs.loc[k]) else entry
                l = float(lows.loc[k]) if pd.notna(lows.loc[k]) else entry
                if h >= target:
                    hit = True; break
                if l <= stop:
                    hit = False; break
                bars += 1
                k += 1
            trades += 1
            if hit is True:
                hits += 1
                rr = (target - entry) / max(1e-9, entry - stop)
                rr_sum += rr
                pnl_sum += (target - entry) / max(1e-9, entry)
            elif hit is False:
                rr = (target - entry) / max(1e-9, entry - stop)
                rr_sum += -1.0
                pnl_sum += (stop - entry) / max(1e-9, entry)
            else:
                # time stop without hit: close at last available close of session window
                lastk = min(k, len(d)-1)
                close_last = float(d.get('close', opens).loc[lastk])
                rr = (close_last - entry) / max(1e-9, entry - stop)
                rr_sum += rr
                pnl_sum += (close_last - entry) / max(1e-9, entry)
        if trades == 0:
            return {'ok': False, 'trades': 0}
        hit_rate = hits / trades
        avg_rr = rr_sum / trades
        avg_ret = pnl_sum / trades
        return {
            'ok': True,
            'trades': int(trades),
            'hit_rate': float(hit_rate),
            'avg_rr': float(avg_rr),
            'avg_return_pct': float(avg_ret*100.0),
            'entry_mode': 'next_session_open',
            'atr_mult_stop': float(br.get('atr_mult_stop', 1.5)),
            'atr_mult_target': float(br.get('atr_mult_target', 3.0)),
            'time_stop_minutes': int(br.get('time_stop_minutes', 120)),
        }
    except Exception:
        return {'ok': False}
