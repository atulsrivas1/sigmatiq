from __future__ import annotations
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
from pathlib import Path as _Path

router = APIRouter()
PRODUCT_DIR = _Path(__file__).resolve().parents[2]

class CalibrateThresholdsRequest(BaseModel):
    model_id: str
    csv: Optional[str] = None
    pack_id: Optional[str] = None
    metric: Optional[str] = 'sharpe'
    column: Optional[str] = 'score_total'
    grid: Optional[str] = None
    top_n: Optional[int] = None

@router.post('/calibrate_thresholds')
def calibrate_thresholds_ep(payload: CalibrateThresholdsRequest):
    try:
        model_id = payload.model_id
        live_signals = PRODUCT_DIR / 'live_data' / model_id / 'signals.csv'
        csv_path = payload.csv or str(PRODUCT_DIR / 'matrices' / model_id / 'training_matrix_built.csv')
        use_path = str(live_signals if live_signals.exists() else csv_path)
        grid_raw = payload.grid or '0.50,0.55,0.60,0.65,0.70'
        grid_vals = [float(x) for x in grid_raw.split(',') if str(x).strip()]
        df = pd.read_csv(use_path)
        col = payload.column or 'score_total'
        if col not in df.columns:
            raise ValueError(f"column '{col}' not in CSV: {use_path}")
        top_n = int(payload.top_n or 50)
        counts = []
        for thr in grid_vals:
            cnt = int((pd.to_numeric(df[col], errors='coerce') >= thr).sum())
            counts.append((thr, cnt, abs(cnt - top_n)))
        if counts:
            thr_best, cnt_best, _ = sorted(counts, key=lambda t: t[2])[0]
        else:
            thr_best, cnt_best = (grid_vals[0], 0)
        return {
            'ok': True,
            'model_id': model_id,
            'source_csv': use_path,
            'column': col,
            'top_n': top_n,
            'grid': grid_vals,
            'counts': [{'threshold': t, 'count': c} for t, c, _ in counts],
            'recommended_threshold': thr_best,
            'expected_count': cnt_best,
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}


class CalibrateBracketsRequest(BaseModel):
    model_id: str
    pack_id: str | None = 'swingedge'
    desired_rr: float | None = 2.0
    k_stop_grid: str | None = '0.8,1.0,1.2,1.4'
    k_target_grid: str | None = '1.6,2.0,2.4,3.0'
    time_stop_candidates: str | None = '60,90,120,180'


@router.post('/calibrate_brackets')
def calibrate_brackets_ep(payload: CalibrateBracketsRequest):
    """
    Suggest ATR-based bracket parameters to achieve a desired risk:reward.
    Note: Under current ATR bracket model, per-row RR = k_target/k_stop (ATR cancels),
    so RR does not vary per-ticker. This endpoint recommends (k_stop, k_target) pairs
    close to desired_rr and picks a time_stop candidate.
    """
    try:
        desired = float(payload.desired_rr or 2.0)
        ks = [float(x) for x in (payload.k_stop_grid or '0.8,1.0,1.2,1.4').split(',') if x.strip()]
        kt = [float(x) for x in (payload.k_target_grid or '1.6,2.0,2.4,3.0').split(',') if x.strip()]
        times = [int(float(x)) for x in (payload.time_stop_candidates or '60,90,120,180').split(',') if x.strip()]
        cand = []
        for a in ks:
            for b in kt:
                rr = (b / a) if a != 0 else float('inf')
                cand.append({'k_stop': a, 'k_target': b, 'rr': rr, 'delta': abs(rr - desired)})
        cand = sorted(cand, key=lambda r: (r['delta'], r['k_stop']))
        top = cand[:10]
        # Heuristic pick: closest RR, prefer lower k_stop (tighter risk) and moderate time stop
        pick = top[0] if top else {'k_stop': 1.2, 'k_target': 2.0, 'rr': 2.0}
        t_pick = min(times, key=lambda t: abs(t - 120)) if times else 120
        return {
            'ok': True,
            'desired_rr': desired,
            'recommended': {
                'atr_mult_stop': pick['k_stop'],
                'atr_mult_target': pick['k_target'],
                'rr_implied': pick['rr'],
                'time_stop_minutes': t_pick,
            },
            'candidates': top,
            'note': 'RR under ATR brackets is k_target/k_stop (constant per-row). Consider regime-aware adjustments later.'
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}
