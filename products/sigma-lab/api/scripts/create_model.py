#!/usr/bin/env python3
"""
Create a new model scaffold that always includes a policy file.

Usage (auto-name preferred):
  python scripts/create_model.py \
    --pack_id zeroedge --ticker SPY --asset opt --horizon 0dte --cadence hourly \
    [--algo xgb] [--variant isv1]

Legacy (explicit name still accepted):
  python scripts/create_model.py --pack_id zeroedge --model_id spy_opt_0dte_hourly_xgb --ticker SPY

Actions:
  - Generates model_id if not provided: <ticker>_<asset>_<horizon>_<cadence>[_<algo>|_<variant>]
  - Ensures directories (artifacts/, matrices/, live_data/, static/backtest_plots/<model_id>)
  - Creates packs/<pack_id>/model_configs/<model_id>.yaml if missing (with ticker, asset_type, and stubs)
  - Copies packs/<pack_id>/policy_templates/default.yaml to packs/<pack_id>/policy_templates/<model_id>.yaml if missing

Requires:
  - A default policy template exists at packs/<pack_id>/policy_templates/default.yaml
"""

from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys
import yaml
import re

ROOT = Path(__file__).resolve().parents[1]


def _gen_model_id(*, ticker: str, asset: str, horizon: str, cadence: str, algo: str | None = None, variant: str | None = None) -> str:
    t = str(ticker).lower()
    a = str(asset).lower()
    h = str(horizon).lower()
    c = str(cadence).lower()
    parts = [t, a, h, c]
    if algo:
        parts.append(str(algo).lower())
    if variant:
        parts.append(str(variant).lower())
    name = "_".join(parts)
    if not re.fullmatch(r"[a-z0-9_]+", name):
        raise ValueError(f"Generated model_id contains invalid characters: {name}")
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack_id", default="zeroedge")
    ap.add_argument("--model_id", required=False, help="Explicit name; otherwise auto-generated")
    ap.add_argument("--ticker", required=True)
    ap.add_argument("--asset", choices=["opt","eq"], help="Asset type: opt (options) or eq (equity)")
    ap.add_argument("--horizon", choices=["0dte","intraday","swing","long"], help="Strategy horizon")
    ap.add_argument("--cadence", choices=["5m","15m","hourly","daily"], help="Primary data cadence")
    ap.add_argument("--algo", default=None, help="Optional algo token, e.g., xgb, gbm")
    ap.add_argument("--variant", default=None, help="Optional variant token, e.g., isv1")
    args = ap.parse_args()

    pack = ROOT / "packs" / args.pack_id
    if not pack.exists():
        print(f"Pack not found: {pack}")
        sys.exit(1)

    # Determine model_id (prefer auto-generation)
    model_id = args.model_id
    if not model_id:
        missing = [k for k in ("asset","horizon","cadence") if getattr(args, k) is None]
        if missing:
            print(f"Auto-name requires: --asset, --horizon, --cadence (missing: {', '.join(missing)})")
            sys.exit(1)
        try:
            model_id = _gen_model_id(
                ticker=args.ticker,
                asset=args.asset,
                horizon=args.horizon,
                cadence=args.cadence,
                algo=args.algo,
                variant=args.variant,
            )
        except Exception as e:
            print(f"ERROR generating model_id: {e}")
            sys.exit(1)
    else:
        if not re.fullmatch(r"[a-z0-9_]+", model_id):
            print("ERROR: model_id must be lowercase snake_case [a-z0-9_]")
            sys.exit(1)

    # Ensure per-model directories
    for p in [ROOT/"artifacts"/model_id, ROOT/"matrices"/model_id, ROOT/"live_data"/model_id, ROOT/"static"/"backtest_plots"/model_id]:
        p.mkdir(parents=True, exist_ok=True)

    # Ensure model config
    cfg_dir = pack / "model_configs"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    cfg_path = cfg_dir / f"{model_id}.yaml"
    if not cfg_path.exists():
        cfg = {
            "model_id": model_id,
            "description": f"{args.ticker} model {model_id}",
            "ticker": args.ticker,
            "asset_type": (args.asset or ("opt" if args.pack_id == "zeroedge" else None)),
            "features": {
                "flow": {"per_distance": True, "totals": True, "ratios": True, "atm": False},
                "dealer": {"mm_profit_dir_simple": True, "divergence_score": True},
                "oi": {"include": False},
            },
            "momentum": {"include": True, "hourly_horizons": [1,3]},
            "volatility": {"include": True, "hourly_horizons": [3]},
        }
        cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False))
        print(f"Created model config: {cfg_path}")
    else:
        print(f"Model config exists: {cfg_path}")

    # Ensure policy exists (copy from default)
    pol_dir = pack / "policy_templates"
    src_default = pol_dir / "default.yaml"
    dst_policy = pol_dir / f"{model_id}.yaml"
    if not src_default.exists():
        print(f"ERROR: Default policy not found: {src_default}")
        sys.exit(1)
    if not dst_policy.exists():
        shutil.copyfile(src_default, dst_policy)
        print(f"Copied default policy to: {dst_policy}")
    else:
        print(f"Policy already exists: {dst_policy}")

    print("Done.")


if __name__ == "__main__":
    main()
