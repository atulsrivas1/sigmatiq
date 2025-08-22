from __future__ import annotations
from typing import Optional, Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel, validator
from pathlib import Path as _Path
import pandas as pd

from sigma_core.data.datasets import build_matrix as build_matrix_range
from sigma_core.data.stocks import build_stock_matrix as build_stock_matrix_range
from sigma_core.services.io import workspace_paths, load_config, resolve_indicator_set_path, sanitize_out_path
from fastapi.responses import JSONResponse
from sigma_core.services.policy import ensure_policy_exists
from sigma_core.storage.relational import get_db
from api.services.store_db import get_model_config_db
from api.services.store_db import get_indicator_set_model_db, get_indicator_set_pack_db
import yaml as _yaml
try:
    from sigma_core.services.model_cards import write_model_card
except Exception:
    write_model_card = None

router = APIRouter()

class BuildMatrixRequest(BaseModel):
    model_id: str
    start: str
    end: str
    out_csv: Optional[str] = None
    pack_id: Optional[str] = 'zerosigma'
    k_sigma: float = 0.3
    fixed_bp: Optional[float] = None
    distance_max: int = 7
    dump_raw: bool = False
    raw_out: Optional[str] = None
    ticker: Optional[str] = None

    @validator('start', 'end', pre=True)
    def _validate_dates(cls, v):  # type: ignore
        from datetime import date
        try:
            date.fromisoformat(str(v))
            return v
        except Exception:
            raise ValueError('start/end must be ISO date YYYY-MM-DD')

    @validator('distance_max', pre=True)
    def _validate_distance(cls, v):  # type: ignore
        try:
            iv = int(v)
            if iv <= 0:
                raise ValueError('distance_max must be > 0')
            return iv
        except Exception:
            raise ValueError('distance_max must be a positive integer')

    @validator('ticker', pre=True)
    def _validate_ticker(cls, v):  # type: ignore
        if v is None:
            return v
        s = str(v).strip().upper()
        if not s or any(ch in s for ch in ('/', '\\', ' ')):
            raise ValueError('ticker must be a simple symbol')
        return s

@router.post('/build_matrix')
def build_matrix_ep(payload: BuildMatrixRequest):
    model_id = payload.model_id
    if not model_id:
        return {"ok": False, "error": "model_id is required"}
    if build_matrix_range is None:
        return {"ok": False, "error": "Shared core missing: data.datasets"}
    pol_err = ensure_policy_exists(model_id, payload.pack_id or 'zerosigma')
    if pol_err:
        return {"ok": False, "error": pol_err}
    start = payload.start; end = payload.end
    if not start or not end:
        return {"ok": False, "error": "start and end are required"}
    paths = workspace_paths(model_id, payload.pack_id or 'zerosigma')
    cfgm = (get_model_config_db(payload.pack_id or 'zerosigma', model_id) or load_config(model_id, payload.pack_id or 'zerosigma'))
    from datetime import datetime
    started_at = datetime.utcnow()
    try:
        out_csv = str(sanitize_out_path(payload.out_csv, paths['matrices'] / 'training_matrix_built.csv'))
    except ValueError as ve:
        return JSONResponse({"ok": False, "error": str(ve)}, status_code=400)
    # Prefer indicator set from DB; fallback to filesystem path
    ind_data = (get_indicator_set_model_db(payload.pack_id or 'zerosigma', model_id) or None)
    if ind_data is None and cfgm:
        # If config references a named set, attempt to fetch pack-level by name
        name = None
        try:
            name = (cfgm.get('indicator_set_name') or cfgm.get('indicator_set') or cfgm.get('features', {}).get('indicator_set'))
        except Exception:
            name = None
        if name:
            ind_data = get_indicator_set_pack_db(payload.pack_id or 'zerosigma', str(name))
    if ind_data is not None:
        # Write temp YAML for the core to consume
        tmp_ind = paths['reports'] / f"indicator_set_db_{model_id}.yaml"
        paths['reports'].mkdir(parents=True, exist_ok=True)
        to_write = ind_data if ('indicators' in ind_data) else {'name': model_id, 'version': 1, 'indicators': ind_data}
        tmp_ind.write_text(_yaml.safe_dump(to_write, sort_keys=False), encoding='utf-8')
        indicator_set_path = str(tmp_ind)
    else:
        indicator_set_path = str(resolve_indicator_set_path(payload.pack_id or 'zerosigma', model_id))
    try:
        paths['matrices'].mkdir(parents=True, exist_ok=True)
        build_matrix_range(
            start_date=start,
            end_date=end,
            out_csv=out_csv,
            make_real_labels=True,
            k_sigma=float(payload.k_sigma),
            fixed_bp=payload.fixed_bp,
            distance_max=int(payload.distance_max),
            dump_raw=bool(payload.dump_raw),
            raw_out=(str(sanitize_out_path(payload.raw_out, _Path(out_csv).with_name(_Path(out_csv).stem + '_raw.csv'))) if payload.dump_raw else None),
            ticker=str((payload.ticker) or cfgm.get('ticker', 'SPY')),
            indicator_set_path=str(indicator_set_path),
            label_config=(cfgm.get('labels') or cfgm.get('label') or None),
        )
        # Write model card for build
        # Basic metrics for model card and DB row
        cols = []
        try:
            if write_model_card is not None:
                # Basic metrics: rows and columns
                import pandas as _pd
                _df = _pd.read_csv(out_csv, nrows=5)
                cols = list(_df.columns)
                write_model_card(
                    pack_id=(payload.pack_id or 'zerosigma'),
                    model_id=model_id,
                    event='build',
                    params={
                        'start': start,
                        'end': end,
                        'k_sigma': float(payload.k_sigma),
                        'fixed_bp': payload.fixed_bp,
                        'distance_max': int(payload.distance_max),
                        'dump_raw': bool(payload.dump_raw),
                        'ticker': (payload.ticker or cfgm.get('ticker', 'SPY')),
                    },
                    metrics={
                        'columns_count': len(cols),
                    },
                )
        except Exception:
            pass
        # Store build run in DB (best-effort)
        try:
            metrics_store = {'columns_count': len(cols)}
            # lineage
            lineage_vals = None
            try:
                if write_model_card is not None:
                    from sigma_core.services.lineage import compute_lineage as _compute_lineage  # type: ignore
                    ind_path = resolve_indicator_set_path(payload.pack_id or 'zerosigma', model_id)
                    from sigma_core.services.io import PACKS_DIR as _PACKS_DIR  # type: ignore
                    lineage_vals = _compute_lineage(pack_dir=_PACKS_DIR / (payload.pack_id or 'zerosigma'), model_id=model_id, indicator_set_path=ind_path)
            except Exception:
                pass
            # snapshot policy for reproducibility
            try:
                from sigma_core.services.policy import load_policy as _load_policy  # type: ignore
                pol_snap = _load_policy(model_id, payload.pack_id or 'zerosigma')
            except Exception:
                pol_snap = None
            params_store = {
                'start': start,
                'end': end,
                'k_sigma': float(payload.k_sigma),
                'fixed_bp': payload.fixed_bp,
                'distance_max': int(payload.distance_max),
                'dump_raw': bool(payload.dump_raw),
                'ticker': (payload.ticker or cfgm.get('ticker', 'SPY')),
                'policy_snapshot': pol_snap,
            }
            finished_at = datetime.utcnow()
            build_run_id = None
            with get_db() as conn:  # type: ignore
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO build_runs (pack_id, model_id, started_at, finished_at, params, metrics, out_csv_uri, lineage)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                        RETURNING id
                        """,
                        (
                            (payload.pack_id or 'zerosigma'),
                            model_id,
                            started_at,
                            finished_at,
                            params_store,
                            metrics_store,
                            out_csv,
                            lineage_vals,
                        ),
                    )
                    row = cur.fetchone()
                    build_run_id = int(row[0]) if row else None
                    # Insert artifact for matrix CSV
                    try:
                        cur.execute(
                            """
                            INSERT INTO artifacts (pack_id, model_id, kind, uri, sha256, size_bytes, build_run_id)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """,
                            (
                                (payload.pack_id or 'zerosigma'),
                                model_id,
                                'matrix',
                                out_csv,
                                None,
                                None,
                                build_run_id,
                            ),
                        )
                    except Exception:
                        pass
                conn.commit()
        except Exception:
            pass
        return {"ok": True, "out_csv": out_csv}
    except Exception as e:
        return {"ok": False, "error": str(e)}

class BuildStockMatrixRequest(BaseModel):
    ticker: str
    start: str
    end: str
    out_csv: Optional[str] = None
    pack_id: Optional[str] = None
    model_id: Optional[str] = None
    label_kind: Optional[str] = None

    @validator('start', 'end', pre=True)
    def _validate_dates(cls, v):  # type: ignore
        from datetime import date
        try:
            date.fromisoformat(str(v))
            return v
        except Exception:
            raise ValueError('start/end must be ISO date YYYY-MM-DD')

@router.post('/build_stock_matrix')
def build_stock_matrix_ep(payload: BuildStockMatrixRequest):
    try:
        ind_path = None
        if payload.pack_id and payload.model_id:
            ind_path = resolve_indicator_set_path(payload.pack_id, payload.model_id)
        paths = workspace_paths(payload.model_id or payload.ticker.lower(), payload.pack_id or 'swingsigma')
        out_csv = payload.out_csv or str(paths['matrices'] / 'stock_matrix.csv')
        try:
            out_csv = str(sanitize_out_path(payload.out_csv, _Path(out_csv)))
        except ValueError as ve:
            return JSONResponse({"ok": False, "error": str(ve)}, status_code=400)
        build_stock_matrix_range(
            start_date=payload.start,
            end_date=payload.end,
            out_csv=out_csv,
            ticker=payload.ticker,
            indicator_set_path=str(ind_path) if ind_path else None,
            label_kind=payload.label_kind,
        )
        return {"ok": True, "out_csv": out_csv}
    except Exception as e:
        return {"ok": False, "error": str(e)}
