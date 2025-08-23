#!/usr/bin/env python3
"""
Generate SQL seed for sc.indicators by introspecting sigma_core indicator builtins
and augmenting with docs/INDICATORS_REFERENCE.md where possible.

Outputs INSERT statements to stdout for use in migrations.
"""
import json
import re
import inspect
from pathlib import Path

# Import registry from local path
import sys
repo_root = Path(__file__).resolve().parents[3]
sigma_core_pkg = repo_root / 'products' / 'sigma-core' / 'sigma_core'
sys.path.insert(0, str(sigma_core_pkg.parent))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass
from sigma_core.indicators.registry import IndicatorRegistry  # type: ignore





def parse_docs_catalog():
    """Parse docs/INDICATORS_REFERENCE.md table to map name->(category, subcategory, params, description)."""
    catalog_path = repo_root / 'docs' / 'INDICATORS_REFERENCE.md'
    mapping = {}
    if not catalog_path.exists():
        return mapping
    in_table = False
    with catalog_path.open('r', encoding='utf-8') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if line.startswith('| Name'):
                in_table = True
                continue
            if not in_table:
                continue
            if not line or line.startswith('|------'):
                continue
            # | rsi | oscillator | rsi | column, period |  |
            parts = [p.strip() for p in line.strip('|').split('|')]
            if len(parts) < 5:
                continue
            name, category, subcategory, params, desc = parts[:5]
            mapping[name] = {
                'category': category or None,
                'subcategory': subcategory or None,
                'params_list': [p.strip() for p in params.split(',')] if params else [],
                'description': desc or ''
            }
    return mapping


def load_overrides():
    """Load JSON override files for indicators to enrich non-technical fields."""
    import json
    overrides_dir = repo_root / 'docs' / 'catalog' / 'overrides' / 'indicators'
    mapping = {}
    if not overrides_dir.exists():
        return mapping
    for fp in overrides_dir.glob('*.json'):
        try:
            with fp.open('r', encoding='utf-8') as fh:
                data = json.load(fh)
                mapping[fp.stem] = data
        except Exception:
            continue
    return mapping


def deep_merge(a: dict, b: dict) -> dict:
    """Shallow copy of a, merged with b (dict values merged recursively). Lists and scalars from b override a."""
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out



def snake_case(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def param_list_from_signature(cls):
    try:
        sig = inspect.signature(cls.__init__)
        params = []
        for name, p in sig.parameters.items():
            if name == 'self':
                continue
            entry = {
                'name': name,
                'type': str(p.annotation) if p.annotation is not inspect._empty else 'any',
            }
            if p.default is not inspect._empty:
                entry['default'] = p.default
            params.append(entry)
        return params
    except Exception:
        return []


def sql_str(val):
    if val is None:
        return 'NULL'
    s = str(val)
    return "'" + s.replace("'", "''") + "'"


def sql_jsonb(obj):
    if obj is None:
        return 'NULL'
    js = json.dumps(obj, ensure_ascii=False)
    js = js.replace("'", "''")
    return f"'{js}'::jsonb"


def main():
    reg = IndicatorRegistry()
    overrides = load_overrides()
    docs_map = parse_docs_catalog()
    rows = []
    for key, cls in sorted(reg.indicators.items()):
        id_ = key
        title = key.replace('_', ' ').title()
        category = getattr(cls, 'CATEGORY', None)
        subcategory = getattr(cls, 'SUBCATEGORY', None)
        if (not category or not subcategory) and id_ in docs_map:
            category = category or docs_map[id_]['category']
            subcategory = subcategory or docs_map[id_]['subcategory']
        doc = inspect.getdoc(cls) or ''
        short_desc = doc.strip().splitlines()[0] if doc else ''
        params = param_list_from_signature(cls)
        if not params and id_ in docs_map and docs_map[id_]['params_list']:
            params = [{ 'name': n, 'type': 'any' } for n in docs_map[id_]['params_list'] if n]
        measures = {
            'what_it_measures': short_desc or (docs_map.get(id_, {}).get('description') if docs_map else ''),
            'how_to_read': '',
            'typical_ranges': '',
            'caveats': ''
        }
        data_requirements = {'inputs': [], 'timeframe': '', 'lookback': None}
        usage = {'best_when': [], 'avoid_when': [], 'example_conditions': [], 'step_by_step': []}
        performance = {'cost_band': 'low', 'latency_band': 'rt_fast', 'stability': 'medium'}

        # Optional novice-first fields (from overrides)
        novice_ready = False
        beginner_summary = None
        if id_ in overrides:
            novice_ready = bool(overrides[id_].get('novice_ready', False))
            beginner_summary = overrides[id_].get('beginner_summary')

        base = {
            'id': id_,
            'version': 1,
            'status': 'published',
            'title': title,
            'subtitle': None,
            'category': category,
            'subcategory': subcategory,
            'tags': [],
            'short_description': short_desc,
            'long_description': doc,
            'parameters': params,
            'measures': measures,
            'data_requirements': data_requirements,
            'usage': usage,
            'performance_hints': performance,
            'assistant_hints': None,
            'novice_ready': novice_ready,
            'beginner_summary': beginner_summary,
        }
        row = base
        if id_ in overrides:
            try:
                row = deep_merge(base, overrides[id_])
            except Exception:
                row = base
        rows.append(row)

    print('-- AUTO-GENERATED seed for sc.indicators')
    print('BEGIN;')
    for r in rows:
        cols = (
            'id, version, status, title, subtitle, category, subcategory, tags, short_description, '
            'long_description, parameters, measures, data_requirements, usage, performance_hints, assistant_hints, '
            'novice_ready, beginner_summary'
        )
        vals = (
            f"'{r['id']}', {r['version']}, '{r['status']}', "
            f"{sql_str(r['title'])}, NULL, {sql_str(r['category']) if r['category'] else 'NULL'}, "
            f"{sql_str(r['subcategory']) if r['subcategory'] else 'NULL'}, "
            f"ARRAY[]::text[], {sql_str(r['short_description']) if r['short_description'] else 'NULL'}, "
            f"{sql_str(r['long_description']) if r['long_description'] else 'NULL'}, "
            f"{sql_jsonb(r['parameters'])}, {sql_jsonb(r['measures'])}, {sql_jsonb(r['data_requirements'])}, "
            f"{sql_jsonb(r['usage'])}, {sql_jsonb(r['performance_hints'])}, "
            f"{sql_jsonb(r.get('assistant_hints')) if r.get('assistant_hints') else 'NULL'}, "
            f"{str(bool(r.get('novice_ready', False))).upper()}, {sql_str(r.get('beginner_summary')) if r.get('beginner_summary') else 'NULL'}"
        )
        print(f"INSERT INTO sc.indicators ({cols}) VALUES ({vals}) ON CONFLICT (id, version) DO NOTHING;")
    print('COMMIT;')


if __name__ == '__main__':
    main()
