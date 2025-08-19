#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
from sigma_core.data.stocks import build_stock_matrix as build_stock_matrix_range
from packs import __init__ as _p  # noqa: F401


def resolve_indicator_set_path(pack_id: str, model_id: str) -> Path|None:
    base = ROOT / 'packs' / pack_id / 'indicator_sets'
    cand = base / f"{model_id}.yaml"
    if cand.exists():
        return cand
    # named set from model config
    cfg = ROOT / 'packs' / pack_id / 'model_configs' / f"{model_id}.yaml"
    if cfg.exists():
        import yaml
        data = yaml.safe_load(cfg.read_text()) or {}
        name = data.get('indicator_set')
        if name:
            cand2 = base / f"{name}.yaml"
            if cand2.exists():
                return cand2
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model_id', required=True)
    ap.add_argument('--pack_id', default='swingsigma')
    ap.add_argument('--ticker', required=False)
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--label_kind', default='fwd_ret_20d')
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    out_csv = ROOT / 'matrices' / args.model_id / 'preview_stock.csv'
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    ind = resolve_indicator_set_path(args.pack_id, args.model_id)
    build_stock_matrix_range(
        start_date=args.start,
        end_date=args.end,
        out_csv=str(out_csv),
        ticker=(args.ticker or args.model_id.split('_')[0].upper()),
        indicator_set_path=(str(ind) if ind else None),
        label_kind=args.label_kind,
    )
    df = pd.read_csv(out_csv)
    n = max(1, len(df))
    nan_stats = [{ 'column': c, 'nan_pct': round(float(pd.to_numeric(df[c], errors='coerce').isna().sum())*100.0/n, 3)} for c in df.columns]
    report = {
        'ok': True,
        'model_id': args.model_id,
        'pack_id': args.pack_id,
        'n_rows': int(len(df)),
        'nan_stats': nan_stats,
        'csv': str(out_csv),
    }
    print(json.dumps(report, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

