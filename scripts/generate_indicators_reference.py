#!/usr/bin/env python
"""
Generate a Markdown catalog of available indicators.

Tries to import sigma_core.indicators.registry and introspect indicator classes.
Falls back to listing files under products/sigma-core/sigma_core/indicators/builtins
if imports fail.

Usage:
  python scripts/generate_indicators_reference.py --out docs/INDICATORS_REFERENCE.md
"""
import argparse
import inspect
import sys
from pathlib import Path


def load_registry():
    try:
        here = Path(__file__).resolve()
        repo_root = here.parents[1]
        core_path = repo_root / 'products' / 'sigma-core'
        if str(core_path) not in sys.path:
            sys.path.insert(0, str(core_path))
        from sigma_core.indicators.registry import registry  # type: ignore
        return registry
    except Exception:
        return None


def build_from_registry(registry):
    rows = []
    for name, cls in sorted(registry.indicators.items(), key=lambda x: x[0]):
        try:
            sig = inspect.signature(cls.__init__)
            params = [p.name for p in sig.parameters.values() if p.name != 'self']
        except Exception:
            params = []
        cat = getattr(cls, 'CATEGORY', 'uncategorized')
        sub = getattr(cls, 'SUBCATEGORY', 'general')
        doc = (cls.__doc__ or '').strip().splitlines()[0] if (cls.__doc__ or '').strip() else ''
        rows.append((name, cat, sub, params, doc))
    return rows


def build_from_files(repo_root: Path):
    # Fallback: list builtin filenames; no params/doc available
    builtins_dir = repo_root / 'products' / 'sigma-core' / 'sigma_core' / 'indicators' / 'builtins'
    rows = []
    if builtins_dir.exists():
        for f in sorted(builtins_dir.glob('*.py')):
            if f.name == '__init__.py':
                continue
            name = f.stem
            rows.append((name, 'unknown', 'unknown', [], ''))
    return rows


def write_markdown(rows, out_path: Path):
    lines = [
        '# Indicators Catalog',
        '',
        'This catalog is auto‑generated. It summarizes available indicators with category, subcategory, and constructor parameters.',
        '',
        '| Name | Category | Subcategory | Params | Description |',
        '|------|----------|-------------|--------|-------------|',
    ]
    for name, cat, sub, params, doc in rows:
        pstr = ', '.join(params) if params else ''
        doc = doc.replace('|', '\\|')
        lines.append(f'| {name} | {cat} | {sub} | {pstr} | {doc} |')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    nl = chr(10)
    out_path.write_text(nl.join(lines) + nl, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='docs/INDICATORS_REFERENCE.md')
    args = ap.parse_args()
    out_path = Path(args.out)
    registry = load_registry()
    if registry is not None:
        rows = build_from_registry(registry)
    else:
        rows = build_from_files(Path(__file__).resolve().parents[1])
    write_markdown(rows, out_path)
    print(f'Wrote {out_path} ({len(rows)} indicators)')


if __name__ == '__main__':
    main()

