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

def load_strategy_examples():
    out = []
    # Prefer canonical strategies folder; fall back to legacy examples if present
    strat_dir = repo_root / 'docs' / 'catalog' / 'strategies'
    if strat_dir.exists():
        for fp in strat_dir.glob('strategy_*.json'):
            try:
                out.append(json.loads(fp.read_text(encoding='utf-8')))
            except Exception:
                continue
    else:
        ex_dir = repo_root / 'docs' / 'catalog' / 'examples'
        if ex_dir.exists():
            for fp in ex_dir.glob('strategy_*.json'):
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
    items = load_strategy_examples()
    print('-- AUTO-GENERATED seed for sc.strategies & sc.strategy_indicator_sets')
    print('BEGIN;')
    for s in items:
        sid = s.get('strategy_id')
        if not sid:
            continue
        cols = (
            'strategy_id, version, status, title, objective, tags, entry_logic, exit_logic, filters, risk, '
            'execution_policy, pre_reqs, performance_snapshot, caveats, compliance_note, how_to_evaluate, '
            'novice_ready, beginner_summary, simple_defaults, guardrails'
        )
        vals = (
            f"'{sid}', {ver(s.get('version', 1))}, 'published', {sql_str(s.get('title'))}, {sql_str(s.get('objective'))}, "
            f"ARRAY[]::text[], {sql_jsonb(s.get('entry_logic')) if s.get('entry_logic') else 'NULL'}, "
            f"{sql_jsonb(s.get('exit_logic')) if s.get('exit_logic') else 'NULL'}, "
            f"{sql_jsonb(s.get('filters')) if s.get('filters') else 'NULL'}, "
            f"{sql_jsonb(s.get('risk')) if s.get('risk') else 'NULL'}, "
            f"{sql_jsonb(s.get('execution_policy')) if s.get('execution_policy') else 'NULL'}, "
            f"{sql_jsonb(s.get('pre_reqs')) if s.get('pre_reqs') else 'NULL'}, "
            f"{sql_jsonb(s.get('performance_snapshot')) if s.get('performance_snapshot') else 'NULL'}, "
            f"{sql_jsonb(s.get('caveats')) if s.get('caveats') else 'NULL'}, "
            f"{sql_jsonb(s.get('compliance_note')) if s.get('compliance_note') else 'NULL'}, "
            f"{sql_jsonb(s.get('how_to_evaluate')) if s.get('how_to_evaluate') else 'NULL'}, "
            f"{str(bool(s.get('novice_ready', False))).upper()}, {sql_str(s.get('beginner_summary')) if s.get('beginner_summary') else 'NULL'}, "
            f"{sql_jsonb(s.get('simple_defaults')) if s.get('simple_defaults') else 'NULL'}, {sql_jsonb(s.get('guardrails')) if s.get('guardrails') else 'NULL'}"
        )
        print(f"INSERT INTO sc.strategies ({cols}) VALUES ({vals}) ON CONFLICT (strategy_id, version) DO NOTHING;")
        # Link to indicator sets if present
        pre = s.get('pre_reqs') or {}
        link_sets = pre.get('indicator_sets_used') or []
        for set_id in link_sets:
            lcols = 'strategy_id, strategy_version, set_id, set_version'
            lvals = f"'{sid}', {ver(s.get('version', 1))}, '{set_id}', 1"
            print(f"INSERT INTO sc.strategy_indicator_sets ({lcols}) VALUES ({lvals}) ON CONFLICT DO NOTHING;")
    print('COMMIT;')

if __name__ == '__main__':
    main()
