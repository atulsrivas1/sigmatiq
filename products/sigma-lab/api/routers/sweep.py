from __future__ import annotations
from typing import Optional, List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from datetime import datetime

from api.services.io import workspace_paths, resolve_indicator_set_path, PACKS_DIR
from api.services.policy import load_policy
from api.routers.backtest import _parity_bracket_next_session_open
from sigma_core.backtest.engine import run_backtest
from sigma_core.registry.backtest_registry import create_backtest_run, create_backtest_folds

try:
    from api.services.lineage import compute_lineage as _compute_lineage
except Exception:
    _compute_lineage = None

router = APIRouter()


class BacktestSweepRequest(BaseModel):
    model_id: str
    pack_id: Optional[str] = 'zerosigma'
    start: Optional[str] = None  # reserved for future matrix rebuilds
    end: Optional[str] = None
    thresholds_variants: Optional[List[str]] = None  # each item: "0.55,0.60,0.65"
    allowed_hours_variants: Optional[List[str]] = None  # each item: "13,14,15"
    top_pct_variants: Optional[List[float]] = None
    splits: int = 5
    embargo: float = 0.0
    allowed_hours: Optional[str] = None
    save: bool = True
    tag: Optional[str] = 'sweep'
    # Guardrails
    min_trades: int = 0
    min_sharpe: Optional[float] = None


@router.post('/backtest_sweep')
def backtest_sweep_ep(payload: BacktestSweepRequest):
    model_id = payload.model_id
    pack_id = payload.pack_id or 'zerosigma'
    paths = workspace_paths(model_id, pack_id)
    csv = str(paths['matrices'] / 'training_matrix_built.csv')
    try:
        df = pd.read_csv(csv)
    except Exception as e:
        return {"ok": False, "error": f"failed to read matrix: {e}", "csv": csv}

    variants_thr = list(payload.thresholds_variants or [])
    variants_hours = list(payload.allowed_hours_variants or ([] if payload.allowed_hours is None else [payload.allowed_hours]))
    variants_top = list(payload.top_pct_variants or [])
    if not variants_thr and not variants_top:
        variants_thr = ['0.50,0.52,0.54', '0.55,0.60,0.65']
    if not variants_hours:
        variants_hours = ['13,14,15']

    # Load policy once for gates
    pol = load_policy(model_id, pack_id)
    exec_pol = pol.get('execution', {}) if isinstance(pol.get('execution', {}), dict) else {}
    mgate = bool(exec_pol.get('momentum_gate', False))
    mmin = float(exec_pol.get('momentum_min', 0.0))
    mcol = str(exec_pol.get('momentum_column', 'momentum_score_total'))

    started_global = datetime.utcnow()
    runs: List[Dict[str, Any]] = []

    def run_one(params: Dict[str, Any]) -> Dict[str, Any]:
        res = run_backtest(
            df,
            params['target_col'],
            params.get('thresholds'),
            splits=int(params.get('splits', payload.splits)),
            embargo=float(params.get('embargo', payload.embargo)),
            top_pct=params.get('top_pct'),
            plots_dir=str(paths['plots']),
            allowed_hours=params.get('allowed_hours'),
            slippage_bps=float(exec_pol.get('slippage_bps', 1.0)),
            size_by_conf=bool(exec_pol.get('size_by_conf', False)),
            conf_cap=float(exec_pol.get('conf_cap', 1.0)),
            per_hour_thresholds=False,
            per_hour_select_by='sharpe',
            calibration='sigmoid',
            momentum_gate=bool(mgate),
            momentum_min=float(mmin),
            momentum_column=str(mcol),
        )
        # parity (if brackets enabled)
        parity = None
        try:
            br = exec_pol.get('brackets', {}) if isinstance(exec_pol.get('brackets', {}), dict) else {}
            if br:
                parity = _parity_bracket_next_session_open(df, br)
        except Exception:
            parity = None

        # store in DB (optional)
        if bool(payload.save):
            try:
                params_store = {k: v for k, v in params.items() if k not in ('target_col',)}
                lineage_vals = None
                if _compute_lineage is not None:
                    try:
                        ind_path = resolve_indicator_set_path(pack_id, model_id)
                        lineage_vals = _compute_lineage(pack_dir=PACKS_DIR / pack_id, model_id=model_id, indicator_set_path=ind_path)
                        params_store['lineage'] = lineage_vals
                    except Exception:
                        pass
                th = res.get('threshold_results') or []
                best_sharpe = None
                best_cum = None
                try:
                    if th:
                        best_sharpe = float(max((r.get('sharpe_hourly', 0.0) for r in th)))
                        best_cum = float(max((r.get('cum_ret', 0.0) for r in th)))
                except Exception:
                    pass
                run_row = create_backtest_run(
                    pack_id=pack_id,
                    model_id=model_id,
                    started_at=started_global,
                    finished_at=datetime.utcnow(),
                    params=params_store,
                    metrics={'best_sharpe_hourly': best_sharpe, 'best_cum_ret': best_cum, 'parity': parity},
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
        # attach quick summary fields for the client
        try:
            th = res.get('threshold_results') or []
            total_trades = int(sum(int(r.get('trades') or 0) for r in th)) if th else None
        except Exception:
            total_trades = None
        res['_summary'] = {
            'best_sharpe_hourly': res.get('best_sharpe_hourly'),
            'best_cum_ret': res.get('best_cum_ret'),
            'total_trades': total_trades,
            'parity': parity,
        }
        return res

    # Determine target column once
    try:
        target_col = 'y' if 'y' in df.columns and df['y'].notna().any() else 'y_syn'
    except Exception:
        target_col = 'y'

    # threshold variants
    for th in variants_thr:
        for hours in variants_hours:
            allowed = [int(x) for x in hours.split(',')] if hours else None
            params = {'target_col': target_col, 'thresholds': [float(x) for x in th.split(',')], 'allowed_hours': allowed, 'splits': payload.splits, 'embargo': payload.embargo}
            res = run_one(params)
            runs.append({'kind': 'thresholds', 'thresholds': th, 'allowed_hours': hours, 'result': res})

    # top-pct variants
    for tp in variants_top:
        for hours in variants_hours:
            allowed = [int(x) for x in hours.split(',')] if hours else None
            params = {'target_col': target_col, 'top_pct': float(tp), 'allowed_hours': allowed, 'splits': payload.splits, 'embargo': payload.embargo}
            res = run_one(params)
            runs.append({'kind': 'top_pct', 'top_pct': float(tp), 'allowed_hours': hours, 'result': res})

    # Best summary
    def best_of(res: Dict[str, Any]) -> float:
        try:
            v = res.get('best_sharpe_hourly')
            return float(v) if v is not None else -1e9
        except Exception:
            return -1e9

    # Apply guardrails to outgoing list
    def passes_guards(r: Dict[str, Any]) -> bool:
        res = r.get('result', {})
        summ = res.get('_summary', {}) if isinstance(res, dict) else {}
        total_tr = summ.get('total_trades')
        if total_tr is not None and int(total_tr) < int(payload.min_trades):
            return False
        if payload.min_sharpe is not None:
            try:
                bs = float(summ.get('best_sharpe_hourly') if summ.get('best_sharpe_hourly') is not None else res.get('best_sharpe_hourly'))
                if bs < float(payload.min_sharpe):
                    return False
            except Exception:
                return False
        return True

    filtered = [r for r in runs if passes_guards(r)]
    ranked = sorted(filtered, key=lambda r: best_of(r['result']), reverse=True)

    # Persist a sweep summary report
    try:
        from pathlib import Path as _P
        import json as _json
        out_dir = _P('products/sigma-lab/reports'); out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        out_path = out_dir / f'backtest_sweep_{model_id}_{ts}.json'
        # only keep top 50 to avoid huge files
        data = {"ok": True, "count": len(runs), "filtered": len(filtered), "runs": ranked[:50]}
        out_path.write_text(_json.dumps(data, indent=2), encoding='utf-8')
        report_path = str(out_path)
    except Exception:
        report_path = None

    return {"ok": True, "runs": ranked[:10], "count": len(runs), "filtered": len(filtered), "report_path": report_path}
