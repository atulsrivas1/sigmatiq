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

def load_workflow_examples():
    out = []
    ex_dir = repo_root / 'docs' / 'workflows' / 'examples'
    if not ex_dir.exists():
        return out
    for fp in ex_dir.glob('*.json'):
        try:
            out.append(json.loads(fp.read_text(encoding='utf-8')))
        except Exception:
            continue
    return out

def main():
    def ver(v):
        if isinstance(v, int):
            return v
        try:
            return int(str(v).split('.')[0])
        except Exception:
            return 1
    items = load_workflow_examples()
    print('-- AUTO-GENERATED seed for sc.workflows')
    print('BEGIN;')
    for w in items:
        wid = w.get('id') or w.get('workflow_id')
        if not wid:
            continue
        cols = (
            'workflow_id, version, status, title, subtitle, goal, persona, difficulty, time_to_complete, tags, '
            'prerequisites, dependencies, steps, outputs, best_when, avoid_when, caveats, links, novice_ready, beginner_summary'
        )
        vals = (
            f"'{wid}', {ver(w.get('version', 1))}, '{w.get('status','published')}', {sql_str(w.get('title'))}, {sql_str(w.get('subtitle')) if w.get('subtitle') else 'NULL'}, "
            f"{sql_jsonb(w.get('goal')) if w.get('goal') else 'NULL'}, {sql_str(w.get('persona')) if w.get('persona') else 'NULL'}, {sql_str(w.get('difficulty')) if w.get('difficulty') else 'NULL'}, "
            f"{int(w.get('time_to_complete', 5)) if w.get('time_to_complete') is not None else 'NULL'}, ARRAY[]::text[], "
            f"{sql_jsonb(w.get('prerequisites')) if w.get('prerequisites') else 'NULL'}, {sql_jsonb(w.get('dependencies')) if w.get('dependencies') else 'NULL'}, "
            f"{sql_jsonb(w.get('steps')) if w.get('steps') else 'NULL'}, {sql_jsonb(w.get('outputs')) if w.get('outputs') else 'NULL'}, "
            f"{sql_jsonb(w.get('best_when')) if w.get('best_when') else 'NULL'}, {sql_jsonb(w.get('avoid_when')) if w.get('avoid_when') else 'NULL'}, "
            f"{sql_jsonb(w.get('caveats')) if w.get('caveats') else 'NULL'}, {sql_jsonb(w.get('links')) if w.get('links') else 'NULL'}, "
            f"{str(bool(w.get('novice_ready', False))).upper()}, {sql_str(w.get('beginner_summary')) if w.get('beginner_summary') else 'NULL'}"
        )
        print(f"INSERT INTO sc.workflows ({cols}) VALUES ({vals}) ON CONFLICT (workflow_id, version) DO NOTHING;")
    print('COMMIT;')

if __name__ == '__main__':
    main()
