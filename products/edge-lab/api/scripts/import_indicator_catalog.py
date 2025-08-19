#!/usr/bin/env python3
"""
Import indicator research catalog from an Excel file and produce:
- docs/indicators/catalog.json (normalized rows)
- docs/indicators/summary.json (by category/subcategory)
- docs/indicators/missing_vs_repo.json (not implemented yet)

Requires: pandas + openpyxl

Usage:
  python scripts/import_indicator_catalog.py --xlsx AlgoTraderAI_Indicators_Polygon_First.xlsx
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _slug(s: str) -> str:
    return (
        str(s or "")
        .strip()
        .replace("/", "_")
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", default=str(ROOT / "AlgoTraderAI_Indicators_Polygon_First.xlsx"))
    ap.add_argument("--sheet", default=0, help="Sheet index or name (default 0)")
    args = ap.parse_args()

    try:
        df = pd.read_excel(args.xlsx, sheet_name=args.sheet)
    except Exception as e:
        print("ERROR: Failed to read Excel. Install openpyxl (pip install openpyxl) and verify the file path.")
        print(f"Detail: {e}")
        sys.exit(1)

    # Try to normalize common columns
    cols = {c.strip().lower(): c for c in df.columns if isinstance(c, str)}
    def pick(*names):
        for n in names:
            if n in cols:
                return cols[n]
        return None

    col_name = pick("name", "indicator", "indicator name")
    col_cat = pick("category", "type")
    col_sub = pick("subcategory", "sub-category", "sub type")
    col_params = pick("params", "window", "period", "config")
    col_provider = pick("provider", "source")
    col_endpoint = pick("endpoint", "api", "url")
    col_notes = pick("notes", "description", "comments")

    rows = []
    for idx, r in df.iterrows():
        name = str(r.get(col_name, "")).strip()
        if not name:
            continue
        rows.append({
            "name": name,
            "key": _slug(name),
            "category": str(r.get(col_cat, "")).strip(),
            "subcategory": str(r.get(col_sub, "")).strip(),
            "params": str(r.get(col_params, "")).strip(),
            "provider": str(r.get(col_provider, "")).strip(),
            "endpoint": str(r.get(col_endpoint, "")).strip(),
            "notes": str(r.get(col_notes, "")).strip(),
        })

    out_dir = ROOT / "docs" / "indicators"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "catalog.json").write_text(json.dumps(rows, indent=2))

    # Summary by category/subcategory
    summary: dict[str, dict[str, int]] = {}
    for it in rows:
        cat = it["category"] or "uncategorized"
        sub = it["subcategory"] or "general"
        summary.setdefault(cat, {})[sub] = summary.get(cat, {}).get(sub, 0) + 1
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    # Ensure repo root is on sys.path for edge_core imports
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    # Compare against registered indicators in our repo
    missing = []
    try:
        from edge_core.indicators.registry import registry
        registered = set(registry.indicators.keys())
        for it in rows:
            key = it["key"]
            # heuristic: if exact key not in registry, mark missing
            if key not in registered:
                missing.append({"name": it["name"], "key": key, "category": it["category"], "provider": it["provider"], "endpoint": it["endpoint"]})
    except Exception as e:
        missing = [{"error": f"Failed to import registry: {e}"}]
    (out_dir / "missing_vs_repo.json").write_text(json.dumps(missing, indent=2))

    print(f"Wrote {len(rows)} indicators to {out_dir/'catalog.json'}")
    print(f"Summary at {out_dir/'summary.json'}; Missing vs repo at {out_dir/'missing_vs_repo.json'}")


if __name__ == "__main__":
    main()
