#!/usr/bin/env python3
"""
Run a short preview build for a model and emit NaN stats.

Usage:
  python scripts/preview_model.py --model_id spy_opt_0dte_hourly \
      --pack_id zeroedge --start 2024-07-01 --end 2024-07-03 \
      --out reports/preview_spy_opt_0dte_hourly.json
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import os
import pandas as pd

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from edge_core.data.datasets import build_matrix as build_matrix_range


def resolve_indicator_set_path(pack_id: str, model_id: str) -> Path:
    base = ROOT / 'packs' / pack_id / 'indicator_sets'
    cand = base / f"{model_id}.yaml"
    if cand.exists():
        return cand
    legacy = ROOT / 'packs' / pack_id / 'indicator_set.yaml'
    if legacy.exists():
        return legacy
    # fallback: pack default if present
    default = base / f"{pack_id}_default.yaml"
    return default if default.exists() else legacy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model_id', required=True)
    ap.add_argument('--pack_id', default='zeroedge')
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    paths = {
        'matrices': ROOT / 'matrices' / args.model_id,
        'reports': ROOT / 'reports',
    }
    paths['matrices'].mkdir(parents=True, exist_ok=True)
    paths['reports'].mkdir(parents=True, exist_ok=True)
    out_csv = str(paths['matrices'] / 'preview_matrix.csv')

    ind_path = resolve_indicator_set_path(args.pack_id, args.model_id)
    # Build
    build_matrix_range(
        start_date=args.start,
        end_date=args.end,
        out_csv=out_csv,
        make_real_labels=True,
        distance_max=5,
        ticker=args.model_id.split('_')[0].upper(),
        indicator_set_path=str(ind_path) if ind_path else None,
    )
    df = pd.read_csv(out_csv)
    n = max(1, len(df))
    nan_stats = [{
        'column': c,
        'nan_pct': round(float(pd.to_numeric(df[c], errors='coerce').isna().sum()) * 100.0 / n, 3)
    } for c in df.columns]
    warnings = []
    if not any(str(c).startswith('calls_sold_d') or str(c).startswith('puts_sold_d') for c in df.columns):
        warnings.append('flow features absent in preview')
    # v2 feature thresholds
    v2_cols = ['open_gap_z','atm_iv_open_delta','gamma_density_peak_strike','gamma_skew_left_right']
    v2_cols += [c for c in df.columns if str(c).startswith('first15m_range_z')]
    ns_map = {d['column']: d['nan_pct'] for d in nan_stats}
    warn_cols = [{ 'column': c, 'nan_pct': ns_map.get(c, 0.0)} for c in v2_cols if ns_map.get(c, 0.0) >= 10.0 and ns_map.get(c, 0.0) < 30.0]
    fail_cols = [{ 'column': c, 'nan_pct': ns_map.get(c, 0.0)} for c in v2_cols if ns_map.get(c, 0.0) >= 30.0]
    ok_flag = not bool(fail_cols)
    if warn_cols:
        warnings.append("v2 feature NaNs >10%: " + ", ".join([w['column'] for w in warn_cols]))
    report = {
        'ok': bool(ok_flag),
        'model_id': args.model_id,
        'pack_id': args.pack_id,
        'start': args.start,
        'end': args.end,
        'n_rows': int(len(df)),
        'columns': df.columns.tolist(),
        'nan_stats': nan_stats,
        'warnings': warnings,
        'v2_nan_summary': {'warn': warn_cols, 'fail': fail_cols},
        'csv': out_csv,
    }
    print(json.dumps(report, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
