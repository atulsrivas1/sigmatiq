#!/usr/bin/env python3
import json
from pathlib import Path

repo_root = Path(__file__).resolve().parents[3]
import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

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

def load_set_examples():
    """Load base set definitions from examples and overrides directories.
    If a set_id appears in both, the overrides version will take precedence via merge later.
    """
    items = {}
    # examples dir
    ex_dir = repo_root / 'docs' / 'catalog' / 'examples'
    if ex_dir.exists():
        for fp in ex_dir.glob('indicator_set_*.json'):
            try:
                data = json.loads(fp.read_text(encoding='utf-8'))
                sid = data.get('set_id')
                if sid:
                    items[sid] = data
            except Exception:
                continue
    # overrides directory may also contain full definitions
    ovr_dir = repo_root / 'docs' / 'catalog' / 'overrides' / 'indicator_sets'
    if ovr_dir.exists():
        for fp in ovr_dir.glob('*.json'):
            try:
                data = json.loads(fp.read_text(encoding='utf-8'))
                sid = data.get('set_id') or fp.stem
                if sid and sid not in items:
                    items[sid] = data
            except Exception:
                continue
    return list(items.values())

def load_overrides():
    """Load optional overrides for indicator sets to enrich metadata."""
    out = {}
    ovr_dir = repo_root / 'docs' / 'catalog' / 'overrides' / 'indicator_sets'
    if not ovr_dir.exists():
        return out
    for fp in ovr_dir.glob('*.json'):
        try:
            data = json.loads(fp.read_text(encoding='utf-8'))
            out[fp.stem] = data
        except Exception:
            continue
    return out

def deep_merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out

def main():
    def ver(v):
        if isinstance(v, int):
            return v
        try:
            return int(str(v).split('.')[0])
        except Exception:
            return 1
    sets = load_set_examples()
    overrides = load_overrides()
    print('-- AUTO-GENERATED seed for sc.indicator_sets & sc.indicator_set_components')
    print('BEGIN;')
    for s in sets:
        set_id = s.get('set_id')
        if not set_id:
            continue
        # Apply override if present
        if set_id in overrides:
            s = deep_merge(s, overrides[set_id])
        cols = (
            'set_id, version, status, title, purpose, tags, rationale, reading_guide, '
            'risk_notes, anti_patterns, data_requirements, performance_hints, assistant_hints, '
            'novice_ready, beginner_summary, simple_defaults, guardrails'
        )
        vals = (
            f"'{set_id}', {ver(s.get('version', 1))}, 'published', {sql_str(s.get('title'))}, {sql_str(s.get('purpose'))}, "
            f"ARRAY[]::text[], {sql_jsonb(s.get('rationale')) if s.get('rationale') else 'NULL'}, "
            f"{sql_jsonb(s.get('reading_guide')) if s.get('reading_guide') else 'NULL'}, "
            f"{sql_jsonb(s.get('risk_notes')) if s.get('risk_notes') else 'NULL'}, "
            f"{sql_jsonb(s.get('anti_patterns')) if s.get('anti_patterns') else 'NULL'}, "
            f"{sql_jsonb(s.get('data_requirements')) if s.get('data_requirements') else 'NULL'}, "
            f"{sql_jsonb(s.get('performance_hints')) if s.get('performance_hints') else 'NULL'}, "
            f"{sql_jsonb(s.get('assistant_hints')) if s.get('assistant_hints') else 'NULL'}, "
            f"{str(bool(s.get('novice_ready', False))).upper()}, {sql_str(s.get('beginner_summary')) if s.get('beginner_summary') else 'NULL'}, "
            f"{sql_jsonb(s.get('simple_defaults')) if s.get('simple_defaults') else 'NULL'}, {sql_jsonb(s.get('guardrails')) if s.get('guardrails') else 'NULL'}"
        )
        print(f"INSERT INTO sc.indicator_sets ({cols}) VALUES ({vals}) ON CONFLICT (set_id, version) DO NOTHING;")
        comps = s.get('components') or []
        for i, comp in enumerate(comps, start=1):
            c_cols = 'set_id, set_version, ord, indicator_id, indicator_version, params, role, weight, timeframe'
            c_vals = (
                f"'{set_id}', {ver(s.get('version', 1))}, {i}, {sql_str(comp.get('indicator_id'))}, "
                f"{int(comp.get('indicator_version', 0)) if comp.get('indicator_version') else 'NULL'}, "
                f"{sql_jsonb(comp.get('params')) if comp.get('params') else 'NULL'}, "
                f"{sql_str(comp.get('role')) if comp.get('role') else 'NULL'}, "
                f"{float(comp.get('weight')) if comp.get('weight') is not None else 'NULL'}, "
                f"{sql_str(comp.get('timeframe')) if comp.get('timeframe') else 'NULL'}"
            )
            print(f"INSERT INTO sc.indicator_set_components ({c_cols}) VALUES ({c_vals}) ON CONFLICT DO NOTHING;")
    print('COMMIT;')

if __name__ == '__main__':
    main()
