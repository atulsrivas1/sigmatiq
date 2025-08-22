#!/usr/bin/env python
"""Import existing YAML policies and model configs into the database.

Usage:
  python scripts/migrate_yaml_to_db.py --pack_id zerosigma
  python scripts/migrate_yaml_to_db.py --all
"""
from __future__ import annotations
from pathlib import Path
import argparse
import yaml
from sigma_core.services.io import PACKS_DIR
from api.services.store_db import upsert_policy_db, upsert_model_config_db


def import_pack(pack_id: str):
    pack_dir = PACKS_DIR / pack_id
    pol_dir = pack_dir / 'policy_templates'
    cfg_dir = pack_dir / 'model_configs'
    if cfg_dir.exists():
        for f in sorted(cfg_dir.glob('*.yaml')):
            try:
                cfg = yaml.safe_load(f.read_text(encoding='utf-8')) or {}
                upsert_model_config_db(pack_id, f.stem, cfg)
                print(f"CONFIG → DB: {pack_id}/{f.stem}")
            except Exception as e:
                print(f"CONFIG ERR {f}: {e}")
    if pol_dir.exists():
        for f in sorted(pol_dir.glob('*.yaml')):
            try:
                y = yaml.safe_load(f.read_text(encoding='utf-8')) or {}
                pol = y.get('policy', y) if isinstance(y, dict) else {}
                upsert_policy_db(pack_id, f.stem, pol, bump_version=False)
                print(f"POLICY → DB: {pack_id}/{f.stem}")
            except Exception as e:
                print(f"POLICY ERR {f}: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pack_id')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()

    if args.all:
        for d in sorted(p for p in PACKS_DIR.iterdir() if p.is_dir()):
            import_pack(d.name)
    elif args.pack_id:
        import_pack(args.pack_id)
    else:
        ap.error('Provide --pack_id or --all')


if __name__ == '__main__':
    main()

