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

def load_recipes():
    items = []
    base = repo_root / 'docs' / 'catalog' / 'recipes'
    if not base.exists():
        return items
    for fp in sorted(base.glob('*.json')):
        try:
            items.append(json.loads(fp.read_text(encoding='utf-8')))
        except Exception:
            continue
    return items

def ver(v):
    if isinstance(v, int):
        return v
    try:
        return int(str(v).split('.')[0])
    except Exception:
        return 1

def main():
    items = load_recipes()
    print('-- AUTO-GENERATED seed for sc.simple_recipes')
    print('BEGIN;')
    for r in items:
        rid = r.get('recipe_id') or r.get('id')
        if not rid:
            continue
        cols = (
            'recipe_id, version, status, title, subtitle, beginner_summary, persona, difficulty, '
            'target_kind, target_id, target_version, defaults, guardrails, risk_profile, universe_preset, sort_rank, tags'
        )
        vals = (
            f"'{rid}', {ver(r.get('version', 1))}, '{r.get('status','published')}', {sql_str(r.get('title'))}, "
            f"{sql_str(r.get('subtitle')) if r.get('subtitle') else 'NULL'}, {sql_str(r.get('beginner_summary')) if r.get('beginner_summary') else 'NULL'}, "
            f"{sql_str(r.get('persona','beginner'))}, {sql_str(r.get('difficulty','beginner'))}, "
            f"{sql_str(r.get('target_kind'))}, {sql_str(r.get('target_id'))}, {ver(r.get('target_version', 1))}, "
            f"{sql_jsonb(r.get('defaults')) if r.get('defaults') else 'NULL'}, {sql_jsonb(r.get('guardrails')) if r.get('guardrails') else 'NULL'}, "
            f"{sql_str(r.get('risk_profile')) if r.get('risk_profile') else 'NULL'}, {sql_str(r.get('universe_preset')) if r.get('universe_preset') else 'NULL'}, "
            f"{int(r.get('sort_rank', 100))}, ARRAY[]::text[]"
        )
        print(f"INSERT INTO sc.simple_recipes ({cols}) VALUES ({vals}) ON CONFLICT (recipe_id, version) DO NOTHING;")
    print('COMMIT;')

if __name__ == '__main__':
    main()
