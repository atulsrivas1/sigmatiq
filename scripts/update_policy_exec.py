#!/usr/bin/env python
import os
import argparse
import yaml
from pathlib import Path


def load_yaml(p: Path):
    try:
        return yaml.safe_load(p.read_text(encoding='utf-8')) or {}
    except Exception:
        return {}


def ensure_exec(doc: dict) -> dict:
    # policy may be at root or under 'policy'
    root = doc
    if 'policy' in doc and isinstance(doc['policy'], dict):
        root = doc['policy']
    if 'execution' not in root or not isinstance(root.get('execution'), dict):
        root['execution'] = {}
    return doc


def main():
    ap = argparse.ArgumentParser(description='Update execution policy fields')
    ap.add_argument('--pack_id', required=True)
    ap.add_argument('--model_id', required=True)
    ap.add_argument('--packs_dir', default=os.environ.get('PACKS_DIR', 'products/sigma-lab/packs'))
    ap.add_argument('--size_by_conf', choices=['true','false'], help='Enable/disable size_by_conf')
    ap.add_argument('--conf_cap', type=float, help='Confidence cap (0..1)')
    ap.add_argument('--slippage_bps', type=float, help='Slippage in basis points')
    ap.add_argument('--momentum_gate', choices=['true','false'], help='Enable/disable momentum_gate')
    ap.add_argument('--momentum_min', type=float, help='Minimum momentum for gate')
    ap.add_argument('--momentum_column', type=str, help='Momentum column name')
    args = ap.parse_args()

    pol_path = Path(args.packs_dir) / args.pack_id / 'policy_templates' / f'{args.model_id}.yaml'
    if not pol_path.exists():
        raise SystemExit(f'Policy file not found: {pol_path}')
    doc = load_yaml(pol_path)
    doc = ensure_exec(doc)

    root = doc['policy'] if 'policy' in doc and isinstance(doc['policy'], dict) else doc
    execd = root['execution']

    def as_bool(s):
        return True if str(s).lower() in ('1','true','yes','on') else False

    if args.size_by_conf is not None:
        execd['size_by_conf'] = as_bool(args.size_by_conf)
    if args.conf_cap is not None:
        execd['conf_cap'] = float(args.conf_cap)
    if args.slippage_bps is not None:
        execd['slippage_bps'] = float(args.slippage_bps)
    if args.momentum_gate is not None:
        execd['momentum_gate'] = as_bool(args.momentum_gate)
    if args.momentum_min is not None:
        execd['momentum_min'] = float(args.momentum_min)
    if args.momentum_column is not None:
        execd['momentum_column'] = str(args.momentum_column)

    pol_path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding='utf-8')
    print(f'UPDATED {pol_path}')


if __name__ == '__main__':
    main()

