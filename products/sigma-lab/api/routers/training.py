from __future__ import annotations
from typing import Optional, List, Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path as _Path
import pandas as pd
import joblib

from sigma_core.features.builder import select_features as select_features_train
from xgboost import XGBClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder
from api.services.io import workspace_paths, load_config
from api.services.policy import ensure_policy_exists
from api.services.io import resolve_indicator_set_path, PACKS_DIR
try:
    from api.services.lineage import compute_lineage as _compute_lineage
except Exception:
    _compute_lineage = None
try:
    from api.services.model_cards import write_model_card
except Exception:
    write_model_card = None

router = APIRouter()


def _train_model(csv_path: str, *, allowed_hours: Optional[List[int]], target: Optional[str], calibration: Optional[str], model_out: _Path, features_list: Optional[List[str]] = None) -> Dict[str, Any]:
    if select_features_train is None or XGBClassifier is None or LabelEncoder is None:
        raise RuntimeError('Training dependencies missing')
    df = pd.read_csv(csv_path)
    if allowed_hours and 'hour_et' in df.columns:
        df = df[df['hour_et'].isin(allowed_hours)].copy()
    y_col = target or ('y' if 'y' in df.columns and df['y'].notna().any() else 'y_syn')
    features = features_list or select_features_train(df)
    missing = [c for c in features if c not in df.columns]
    for c in missing:
        if c.startswith('calls_sold_d') or c.startswith('puts_sold_d'):
            df[c] = 0.0
    X = df[features].fillna(0.0).values
    y_raw = df[y_col].astype(str).values
    le = LabelEncoder(); y = le.fit_transform(y_raw)
    model = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.08, subsample=0.9, colsample_bytree=0.9, eval_metric='mlogloss', tree_method='hist', random_state=2025)
    if calibration in {'sigmoid','isotonic'}:
        try:
            clf = CalibratedClassifierCV(model, method=calibration, cv=3)
            clf.fit(X, y)
            final = clf
        except Exception:
            model.fit(X, y); final = model
    else:
        model.fit(X, y); final = model
    model_out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({'model': final, 'features': features, 'label_encoder': le}, model_out)
    return {'ok': True, 'model_out': str(model_out), 'rows': int(len(df))}

class TrainRequest(BaseModel):
    model_id: str
    csv: Optional[str] = None
    allowed_hours: Optional[str | List[int]] = None
    calibration: Optional[str] = 'sigmoid'
    model_out: Optional[str] = None
    target: Optional[str] = None
    pack_id: Optional[str] = 'zeroedge'

@router.post('/train')
def train_ep(payload: TrainRequest):
    model_id = payload.model_id
    if not model_id:
        return {'ok': False, 'error': 'model_id is required'}
    if select_features_train is None or XGBClassifier is None:
        return {'ok': False, 'error': 'Training deps missing'}
    pol_err = ensure_policy_exists(model_id, payload.pack_id or 'zeroedge')
    if pol_err:
        return {'ok': False, 'error': pol_err}
    paths = workspace_paths(model_id, payload.pack_id or 'zeroedge')
    csv = payload.csv or str(paths['matrices'] / 'training_matrix_built.csv')
    allowed_hours = payload.allowed_hours
    if isinstance(allowed_hours, str) and allowed_hours:
        allowed_hours = [int(x) for x in allowed_hours.split(',')]
    calib = payload.calibration or 'sigmoid'
    out_path = _Path(payload.model_out or (paths['artifacts'] / 'gbm.pkl'))
    cfgm = load_config(model_id, payload.pack_id or 'zeroedge')
    fcfg = cfgm.get('features') or {}
    try:
        df_tmp = pd.read_csv(csv, nrows=1000)
        cols = set(df_tmp.columns)
    except Exception:
        cols = set()
    selected: List[str] = []
    def maybe_add(names: List[str]):
        for n in names:
            if n in cols:
                selected.append(n)
    # If features config is a list, honor it directly (intersection with available columns)
    if isinstance(fcfg, list):
        for n in fcfg:
            if isinstance(n, str) and n in cols:
                selected.append(n)
    else:
        # Dict-based feature flags
        if fcfg.get('flow', {}).get('per_distance', True):
            for c in cols:
                cs = str(c)
                if cs.startswith('calls_sold_d') or cs.startswith('puts_sold_d'):
                    selected.append(cs)
        if fcfg.get('flow', {}).get('totals', True) or fcfg.get('flow', {}).get('ratios', True):
            maybe_add(['calls_sold_total','puts_sold_total','pc_ratio','imbalance'])
        if fcfg.get('flow', {}).get('atm', False):
            maybe_add(['atm_calls','atm_puts','atm_pc_ratio','atm_imbalance'])
        if fcfg.get('dealer', {}).get('mm_profit_dir_simple', False):
            maybe_add(['mm_profit_dir_simple'])
        if fcfg.get('dealer', {}).get('divergence_score', False):
            maybe_add(['divergence_score'])
        if fcfg.get('oi', {}).get('include', False):
            maybe_add(['distance_to_max_pain','oi_concentration'])
        if (cfgm.get('momentum', {}) or {}).get('include', False):
            horizons = (cfgm.get('momentum', {}) or {}).get('hourly_horizons', [1,3])
            for h in horizons:
                maybe_add([f'close_mom_{h}'])
        if (cfgm.get('volatility', {}) or {}).get('include', False):
            horizons = (cfgm.get('volatility', {}) or {}).get('hourly_horizons', [3])
            for h in horizons:
                maybe_add([f'close_vol_{h}'])
    selected = sorted(set(selected))
    try:
        res = _train_model(csv, allowed_hours=allowed_hours, target=payload.target, calibration=calib, model_out=out_path, features_list=(selected or None))
        # Write model card for training
        try:
            feats = None
            try:
                bundle = joblib.load(out_path)
                feats = bundle.get('features') if isinstance(bundle, dict) else None
            except Exception:
                feats = selected or None
            lineage_vals = None
            if _compute_lineage is not None:
                try:
                    ind_path = resolve_indicator_set_path(payload.pack_id or 'zeroedge', model_id)
                    lineage_vals = _compute_lineage(pack_dir=PACKS_DIR / (payload.pack_id or 'zeroedge'), model_id=model_id, indicator_set_path=ind_path)
                except Exception:
                    pass
            if write_model_card is not None:
                write_model_card(
                    pack_id=(payload.pack_id or 'zeroedge'),
                    model_id=model_id,
                    event='train',
                    params={'csv': csv, 'allowed_hours': allowed_hours, 'calibration': calib, 'target': payload.target},
                    metrics={'rows': res.get('rows')},
                    features=feats,
                    lineage=lineage_vals,
                )
        except Exception:
            pass
        return res
    except Exception as e:
        return {'ok': False, 'error': str(e)}
