#!/usr/bin/env python3
"""
Parse a Markdown indicator catalog (AlgoTraderAI_Indicators_Polygon_First.md) and produce:
- docs/indicators/catalog.json (normalized rows with category/subcategory)
- docs/indicators/summary.json (counts)
- docs/indicators/missing_vs_repo.json (not in current registry)

Assumptions:
- Category headings use '### <Category>'
- Tables begin with a header row containing 'Indicator |'
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9_]", "_", (s or "").strip().lower())


def parse_md(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows: list[dict] = []
    category = None
    in_table = False
    headers: list[str] = []
    # Normalize headers to keys
    def norm_header(h: str) -> str:
        h = h.strip().lower()
        if "indicator" in h: return "indicator"
        if "param" in h: return "params"
        if "input" in h: return "inputs"
        if "formula" in h: return "formula"
        if "notes" in h: return "notes"
        if "provider" in h: return "provider"
        if "endpoint" in h: return "endpoint"
        return slug(h)

    for ln in lines:
        if ln.startswith("### "):
            category = ln[4:].strip()
            in_table = False
            headers = []
            continue
        if "|" in ln and "Indicator" in ln and "|" in ln.split("Indicator",1)[1]:
            # header row
            parts = [p.strip() for p in ln.strip("|").split("|")]
            headers = [norm_header(p) for p in parts]
            in_table = True
            continue
        if in_table:
            if not ln.strip() or re.match(r"^-+\|", ln):
                # separator or blank
                continue
            if ln.startswith("### "):
                in_table = False
                continue
            parts = [p.strip() for p in ln.strip("|").split("|")]
            if len(parts) < 2:
                continue
            data = {headers[i]: parts[i] for i in range(min(len(headers), len(parts)))}
            name = data.get("indicator") or data.get("name")
            if not name:
                continue
            rows.append({
                "name": name,
                "key": slug(name),
                "category": category or "uncategorized",
                "subcategory": data.get("subcategory") or data.get("type") or "general",
                "params": data.get("params", ""),
                "inputs": data.get("inputs", ""),
                "formula": data.get("formula", ""),
                "provider": data.get("provider", "Polygon"),
                "endpoint": data.get("endpoint", ""),
                "notes": data.get("notes", ""),
            })
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=str(ROOT / "AlgoTraderAI_Indicators_Polygon_First.md"))
    args = ap.parse_args()

    path = Path(args.md)
    if not path.exists():
        raise SystemExit(f"Markdown file not found: {path}")
    rows = parse_md(path)
    out_dir = ROOT / "docs" / "indicators"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "catalog.json").write_text(json.dumps(rows, indent=2))

    # Ensure repo root is on sys.path for edge_core imports
    import sys
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    # Summary
    summary: dict[str, dict[str, int]] = {}
    for it in rows:
        cat = it["category"] or "uncategorized"
        sub = it["subcategory"] or "general"
        summary.setdefault(cat, {})[sub] = summary.get(cat, {}).get(sub, 0) + 1
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    # Missing vs registry
    missing = []
    try:
        from edge_core.indicators.registry import registry
        registered = set(registry.indicators.keys())
        for it in rows:
            if it["key"] not in registered:
                missing.append({"name": it["name"], "key": it["key"], "category": it["category"], "provider": it["provider"], "endpoint": it["endpoint"]})
    except Exception as e:
        missing = [{"error": f"Failed to import registry: {e}"}]
    (out_dir / "missing_vs_repo.json").write_text(json.dumps(missing, indent=2))

    print(f"Parsed {len(rows)} indicators from {path}")
    print(f"Wrote catalog, summary, and missing lists to {out_dir}")


if __name__ == "__main__":
    main()
