#!/usr/bin/env python3
"""
Sigma Core Runner

Lightweight CLI to apply indicators and indicator sets to market data from CSVs,
and to run a simple screen across multiple symbols. No external data fetching.

Commands:
  - indicator-compute: run a single indicator on an input CSV
  - set-build-features: compute features from an indicator set
  - screen: screen a universe (in one CSV with a symbol column) by indicator rule

Examples:
  python scripts/runner.py indicator-compute \
      --name rsi --params '{"period":14}' \
      --input ./examples/ohlcv.csv --output ./out.csv

  python scripts/runner.py set-build-features \
      --set-json ./examples/indicator_set.json \
      --input ./examples/ohlcv.csv --output ./features.csv

  python scripts/runner.py screen \
      --name rsi --params '{"period":14}' --rule 'rsi_14 > 70' \
      --input ./examples/multi_symbol_ohlcv.csv --symbol-col symbol --output ./matches.txt

Notes:
  - CSV must contain time series columns required by the indicator(s) (e.g., open, high, low, close, volume).
  - For screening, the CSV must include a symbol column (default: symbol) to group series per symbol.
  - For set-build-features, either provide --set-json (preferred, no DB needed) or --set-id/--version (requires DB env + psycopg2).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from sigma_core.indicators.registry import get_indicator
from sigma_core.features.sets import IndicatorSet as FBIndicatorSet, IndicatorSpec as FBIndicatorSpec
from sigma_core.features.builder import FeatureBuilder


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"input file not found: {path}")
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise SystemExit(f"failed to read CSV {path}: {e}")
    # Normalize timestamp column if present
    for c in ("timestamp", "date", "time"):
        if c in df.columns:
            try:
                df[c] = pd.to_datetime(df[c])
            except Exception:
                pass
    return df


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def parse_params(s: Optional[str]) -> Dict[str, Any]:
    if not s:
        return {}
    try:
        return json.loads(s)
    except Exception as e:
        raise SystemExit(f"invalid JSON in --params: {e}")


def parse_rule(s: str) -> tuple[str, str, float]:
    # format: "column op value", e.g., "rsi_14 > 70"
    m = re.match(r"^\s*([A-Za-z0-9_\.]+)\s*(==|!=|>=|<=|>|<)\s*([-+]?[0-9]*\.?[0-9]+)\s*$", s)
    if not m:
        raise SystemExit("invalid --rule; expected format like: rsi_14 > 70")
    col, op, val = m.group(1), m.group(2), float(m.group(3))
    return col, op, val


def cmd_indicator_compute(args: argparse.Namespace) -> None:
    df = load_csv(Path(args.input))
    params = parse_params(args.params)
    cls = get_indicator(args.name)
    try:
        ind = cls(**params)  # type: ignore
    except TypeError as te:
        raise SystemExit(f"invalid params for {args.name}: {te}")
    out = ind.calculate(df)
    merged = pd.concat([df, out], axis=1)
    write_csv(merged, Path(args.output))
    print(f"computed {len(out.columns)} column(s): {list(out.columns)}")


def _load_set_from_json(path: Path) -> FBIndicatorSet:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise SystemExit(f"failed to read set JSON: {e}")
    try:
        inds = [FBIndicatorSpec(name=i["name"], version=int(i.get("version", 1)), params=i.get("params", {})) for i in data["indicators"]]
        return FBIndicatorSet(name=str(data.get("name") or data.get("set_id") or "custom_set"), version=int(data.get("version", 1)), description=str(data.get("description", "")), indicators=inds)
    except Exception as e:
        raise SystemExit(f"invalid set JSON: {e}")


def _load_set_from_db(set_id: str, version: int) -> FBIndicatorSet:
    # Lazy import DB only if needed
    try:
        from sigma_core.storage.relational import get_db
    except Exception as e:
        raise SystemExit("DB dependencies not available. Provide --set-json instead.")
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT title FROM sc.indicator_sets WHERE set_id=%s AND version=%s", (set_id, version))
            r = cur.fetchone()
            if not r:
                raise SystemExit("indicator set not found in DB")
            desc = r[0] or ""
            cur.execute(
                "SELECT indicator_id, indicator_version, params FROM sc.indicator_set_components WHERE set_id=%s AND set_version=%s ORDER BY ord",
                (set_id, version),
            )
            comps = cur.fetchall()
    inds = [FBIndicatorSpec(name=rr[0], version=int(rr[1] or 1), params=(rr[2] or {})) for rr in comps]
    return FBIndicatorSet(name=set_id, version=version, description=desc, indicators=inds)


def cmd_set_build_features(args: argparse.Namespace) -> None:
    df = load_csv(Path(args.input))
    if args.set_json:
        fb_set = _load_set_from_json(Path(args.set_json))
    else:
        if not args.set_id or not args.version:
            raise SystemExit("provide either --set-json, or both --set-id and --version")
        fb_set = _load_set_from_db(args.set_id, int(args.version))
    fb = FeatureBuilder(indicator_set=fb_set)
    out = fb.add_indicator_features(df)
    new_cols = [c for c in out.columns if c not in df.columns]
    write_csv(pd.concat([df, out[new_cols]], axis=1), Path(args.output))
    print(f"built {len(new_cols)} feature column(s): {new_cols}")


def cmd_screen(args: argparse.Namespace) -> None:
    df = load_csv(Path(args.input))
    symbol_col = args.symbol_col or "symbol"
    if symbol_col not in df.columns:
        raise SystemExit(f"--symbol-col '{symbol_col}' not found in input CSV")
    params = parse_params(args.params)
    col, op, val = parse_rule(args.rule)
    cls = get_indicator(args.name)
    try:
        ind = cls(**params)  # type: ignore
    except TypeError as te:
        raise SystemExit(f"invalid params for {args.name}: {te}")
    matched: List[str] = []
    for sym, g in df.groupby(symbol_col):
        try:
            out = ind.calculate(g)
            use_col = col if col in out.columns else (out.columns[0] if len(out.columns) == 1 else None)
            if not use_col:
                continue
            last = out[use_col].iloc[-1]
            ok = (
                (op == ">" and last > val)
                or (op == ">=" and last >= val)
                or (op == "<" and last < val)
                or (op == "<=" and last <= val)
                or (op == "==" and last == val)
                or (op == "!=" and last != val)
            )
            if ok:
                matched.append(str(sym))
        except Exception:
            # Skip bad symbols silently (novice-friendly default)
            continue
    matched = sorted(set(matched))
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text("\n".join(matched), encoding="utf-8")
    print(f"matched {len(matched)} symbols")
    for s in matched:
        print(s)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="Sigma Core Runner")
    sp = ap.add_subparsers(dest="cmd", required=True)

    p1 = sp.add_parser("indicator-compute", help="run a single indicator on a CSV")
    p1.add_argument("--name", required=True, help="indicator name (registry key)")
    p1.add_argument("--params", default="{}", help="JSON params for indicator")
    p1.add_argument("--input", required=True, help="input CSV path")
    p1.add_argument("--output", required=True, help="output CSV path")
    p1.set_defaults(func=cmd_indicator_compute)

    p2 = sp.add_parser("set-build-features", help="compute features from an indicator set")
    p2.add_argument("--set-json", help="indicator set JSON file (preferred; no DB needed)")
    p2.add_argument("--set-id", help="indicator set_id (DB-required if no --set-json)")
    p2.add_argument("--version", type=int, help="indicator set version (DB-required if no --set-json)")
    p2.add_argument("--input", required=True, help="input CSV path")
    p2.add_argument("--output", required=True, help="output CSV path")
    p2.set_defaults(func=cmd_set_build_features)

    p3 = sp.add_parser("screen", help="screen symbols in a CSV using an indicator rule")
    p3.add_argument("--name", required=True, help="indicator name (registry key)")
    p3.add_argument("--params", default="{}", help="JSON params for indicator")
    p3.add_argument("--rule", required=True, help="rule like 'rsi_14 > 70'")
    p3.add_argument("--input", required=True, help="input CSV path with a symbol column")
    p3.add_argument("--symbol-col", default="symbol", help="symbol column name (default: symbol)")
    p3.add_argument("--output", help="optional output file for matched symbols (one per line)")
    p3.set_defaults(func=cmd_screen)

    return ap


def main() -> None:
    ap = build_parser()
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

