from __future__ import annotations
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query
from pydantic import BaseModel
from pathlib import Path as _Path
import shutil
import yaml
import pandas as pd

from sigma_core.services.io import workspace_paths, load_config, resolve_indicator_set_path, PACKS_DIR
from sigma_core.services.policy import ensure_policy_exists
from sigma_core.indicators.registry import registry as indicator_registry
from sigma_core.data.datasets import build_matrix as build_matrix_range

router = APIRouter()

class CreateModelRequest(BaseModel):
    ticker: str
    asset_type: str | None = 'opt'  # 'opt'|'eq'
    horizon: str | None = '0dte'
    cadence: str | None = 'hourly'
    algo: str | None = 'gbm'
    variant: str | None = None
    pack_id: str | None = 'zerosigma'
    indicator_set_name: str | None = None

@router.post('/models')
def create_model_ep(payload: CreateModelRequest):
    try:
        ticker = str(payload.ticker).upper()
        asset_raw = str(payload.asset_type or 'opt').lower()
        asset = 'opt' if asset_raw in {'opt','options','option'} else ('eq' if asset_raw in {'eq','equity','equities','stock','stocks'} else asset_raw)
        horizon = str(payload.horizon or '0dte').lower()
        cadence = str(payload.cadence or 'hourly').lower()
        algo = str(payload.algo or 'gbm').lower()
        suffix = f"_{payload.variant}" if payload.variant else ''
        model_id = f"{ticker.lower()}_{asset}_{horizon}_{cadence}{suffix}"
        ws = workspace_paths(model_id, payload.pack_id or 'zerosigma')
        cfg_dir = ws['config'].parent
        pol_dir = ws['policy'].parent
        ind_dir = cfg_dir.parent / 'indicator_sets'
        cfg_dir.mkdir(parents=True, exist_ok=True)
        pol_dir.mkdir(parents=True, exist_ok=True)
        ind_dir.mkdir(parents=True, exist_ok=True)
        cfg_path = ws['config']
        if cfg_path.exists():
            return {"ok": False, "error": f"Model config already exists: {cfg_path}"}
        cfg = {
            'model_id': model_id,
            'ticker': ticker,
            'model': algo,
            'task': 'classification',
            'hyperparams': {'n_estimators': 300, 'max_depth': 6, 'learning_rate': 0.05},
            'features': ['rsi__period=14','iv_realized_spread__window=20','sold_flow_ratio__window=5'],
            'label': {'type': 'next_bar_updown', 'horizon': 1},
            'train_window': {'start': '2023-01-01', 'end': '2024-12-31'},
            'asset_type': asset,
            'horizon': horizon,
            'cadence': cadence,
        }
        cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False))
        default_pol = pol_dir / 'default.yaml'
        pol_out = ws['policy']
        if default_pol.exists():
            shutil.copyfile(default_pol, pol_out)
        else:
            pol_out.write_text(yaml.safe_dump({'policy': {'execution': {}, 'risk': {}, 'alerting': {}}}, sort_keys=False))
        if payload.indicator_set_name:
            src = ind_dir / f"{payload.indicator_set_name}.yaml"
            if src.exists():
                dst = ind_dir / f"{model_id}.yaml"
                shutil.copyfile(src, dst)
        return {"ok": True, "model_id": model_id, "paths": {"config": str(cfg_path), "policy": str(pol_out)}, "message": "created"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

class IndicatorSetUpsertRequest(BaseModel):
    pack_id: str
    scope: str  # 'pack' or 'model'
    model_id: Optional[str] = None
    name: str
    indicators: list

@router.post('/indicator_sets')
def upsert_indicator_set_ep(payload: IndicatorSetUpsertRequest):
    try:
        pack_id = payload.pack_id or 'zerosigma'
        scope = (payload.scope or 'pack').lower()
        name = payload.name
        inds = payload.indicators or []
        valid = []
        for it in inds:
            if isinstance(it, dict):
                nm = it.get('name') or it.get('indicator')
                params = it.get('params') or {k:v for k,v in it.items() if k not in {'name','indicator'}}
            else:
                nm = str(it); params = {}
            if not nm or nm not in indicator_registry.indicators:
                raise ValueError(f"unknown indicator: {nm}")
            try:
                indicator_registry.indicators[nm](**params)
            except TypeError as e:
                raise ValueError(f"invalid params for {nm}: {e}")
            d = {'name': nm}; d.update(params)
            valid.append(d)
        base = workspace_paths('dummy', pack_id)['config'].parent / 'indicator_sets'
        base.mkdir(parents=True, exist_ok=True)
        if scope == 'model':
            model_id = payload.model_id or name
            target = base / f"{model_id}.yaml"
        else:
            target = base / f"{name}.yaml"
        data = {'name': name, 'version': 1, 'indicators': valid}
        target.write_text(yaml.safe_dump(data, sort_keys=False))
        return {"ok": True, "path": str(target), "count": len(valid), "message": "written"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

class PreviewMatrixRequest(BaseModel):
    model_id: str
    start: str
    end: str
    pack_id: str | None = 'zerosigma'
    max_rows: int | None = 200

@router.post('/preview_matrix')
def preview_matrix_ep(payload: PreviewMatrixRequest):
    model_id = payload.model_id
    pack_id = payload.pack_id or 'zerosigma'
    pol_err = ensure_policy_exists(model_id, pack_id)
    if pol_err:
        return {"ok": False, "error": pol_err}
    try:
        tmp_csv = workspace_paths(model_id, pack_id)['reports'] / f"preview_matrix_{model_id}.csv"
        workspace_paths(model_id, pack_id)['reports'].mkdir(parents=True, exist_ok=True)
        indicator_set_path = resolve_indicator_set_path(pack_id, model_id)
        build_matrix_range(
            start_date=payload.start,
            end_date=payload.end,
            out_csv=str(tmp_csv),
            make_real_labels=True,
            distance_max=7,
            dump_raw=False,
            ticker=model_id.split('_')[0].upper(),
            indicator_set_path=str(indicator_set_path),
            label_config=None,
        )
        df = pd.read_csv(tmp_csv)
        # --- QA checks ---
        n = max(1, len(df))
        numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
        # NaN stats
        nan_stats = [{'column': c, 'nan_pct': round(float(pd.to_numeric(df[c], errors='coerce').isna().sum())*100.0/n, 3)} for c in numeric_cols]
        warn = [s for s in nan_stats if s['nan_pct'] >= 10.0]
        fail = [s for s in nan_stats if s['nan_pct'] >= 30.0]
        # Monotonic time (by common timestamp columns)
        def _first_existing(cols):
            for c in cols:
                if c in df.columns:
                    return c
            return None
        ts_col = _first_existing(['datetime','date','timestamp','ts','dt'])
        monotonic_ok = None
        monotonic_violations = 0
        if ts_col is not None:
            try:
                ts = pd.to_datetime(df[ts_col])
                monotonic_ok = bool(ts.is_monotonic_increasing)
                if not monotonic_ok:
                    monotonic_violations = int((ts.diff().dt.total_seconds() < 0).sum())
            except Exception:
                monotonic_ok = None
        # Non-negative vol (consider columns containing 'vol' or 'atr')
        vol_cols = [c for c in numeric_cols if ('vol' in str(c).lower()) or str(c).lower().startswith('atr_')]
        neg_vol_count = 0
        vol_checked = 0
        for c in vol_cols:
            s = pd.to_numeric(df[c], errors='coerce')
            vol_checked += int(s.notna().sum())
            neg_vol_count += int((s < 0).sum())
        vol_neg_pct = round(100.0 * (neg_vol_count / max(1, vol_checked)), 3) if vol_checked else 0.0
        # Session alignment (hour_et in reasonable US RTH range)
        sess_ok = None
        sess_off_pct = None
        if 'hour_et' in df.columns:
            try:
                hrs = pd.to_numeric(df['hour_et'], errors='coerce')
                valid = hrs.isin([9,10,11,12,13,14,15,16])
                sess_off_pct = round(100.0 * float((~valid).sum()) / n, 3)
                sess_ok = bool(sess_off_pct <= 5.0)
            except Exception:
                sess_ok = None
        # IV sanity (values in [0, 5] roughly, 0-500%)
        iv_cols = [c for c in numeric_cols if 'iv' in str(c).lower() or 'implied_vol' in str(c).lower()]
        iv_out_count = 0
        iv_checked = 0
        for c in iv_cols:
            s = pd.to_numeric(df[c], errors='coerce')
            iv_checked += int(s.notna().sum())
            iv_out_count += int(((s < 0) | (s > 5.0)).sum())
        iv_out_pct = round(100.0 * (iv_out_count / max(1, iv_checked)), 3) if iv_checked else 0.0
        iv_ok = (iv_checked == 0) or (iv_out_pct <= 5.0)
        qa = {
            'monotonic_time': {'ok': monotonic_ok, 'violations': monotonic_violations},
            'non_negative_vol': {'ok': vol_neg_pct == 0.0, 'neg_pct': vol_neg_pct, 'checked': vol_checked},
            'session_alignment': {'ok': sess_ok, 'off_pct': sess_off_pct},
            'iv_sanity': {'ok': iv_ok, 'out_of_range_pct': iv_out_pct, 'checked': iv_checked},
            'nan': {'warn': warn, 'fail': fail},
        }
        overall_ok = True
        # Determine overall ok with conservative gates
        if monotonic_ok is False:
            overall_ok = False
        if vol_checked and vol_neg_pct > 0.0:
            overall_ok = False
        if sess_ok is False:
            overall_ok = False
        if not iv_ok:
            overall_ok = False
        if any(s['nan_pct'] >= 30.0 for s in fail):
            overall_ok = False
        return {"ok": bool(overall_ok), "rows": int(len(df)), "qa": qa, "nan_stats": nan_stats, "warn": warn, "fail": fail}
    except Exception as e:
        return {"ok": False, "error": str(e)}


class PatchModelRequest(BaseModel):
    pack_id: str | None = 'zerosigma'
    # Provide a partial config to merge into existing config
    config: Dict[str, Any]


@router.patch('/models/{model_id}')
def patch_model_config(model_id: str, payload: PatchModelRequest):
    try:
        pack_id = payload.pack_id or 'zerosigma'
        cfg_path = workspace_paths(model_id, pack_id)['config']
        if not cfg_path.exists():
            return {"ok": False, "error": f"config not found: {cfg_path}"}
        try:
            cur = yaml.safe_load(cfg_path.read_text()) or {}
        except Exception:
            cur = {}
        upd = payload.config or {}
        # shallow merge (by sections); preserve unknown keys
        for k, v in upd.items():
            if isinstance(v, dict) and isinstance(cur.get(k), dict):
                cur[k].update(v)
            else:
                cur[k] = v
        cfg_path.write_text(yaml.safe_dump(cur, sort_keys=False))
        return {"ok": True, "path": str(cfg_path), "config": cur}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@router.get('/model_templates')
def list_model_templates(pack: str | None = Query(None)):
    try:
        out: List[Dict[str, Any]] = []
        packs = [pack] if pack else [p.name for p in PACKS_DIR.iterdir() if p.is_dir()]
        for pid in sorted(packs):
            tpl_dir = PACKS_DIR / pid / 'model_templates'
            if not tpl_dir.exists():
                continue
            for f in sorted(tpl_dir.glob('*.yaml')):
                try:
                    y = yaml.safe_load(f.read_text()) or {}
                except Exception:
                    y = {}
                out.append({
                    'pack': pid,
                    'template_id': y.get('template_id') or f.stem,
                    'name': y.get('name') or f.stem,
                    'horizon': y.get('horizon'),
                    'cadence': y.get('cadence'),
                    'template_version': y.get('template_version'),
                })
        return {"ok": True, "templates": out}
    except Exception as e:
        return {"ok": False, "error": str(e)}
