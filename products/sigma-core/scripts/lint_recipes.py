#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
REC_DIR = REPO / 'docs' / 'catalog' / 'recipes'


def load_jsons(dir_path: Path):
    out = []
    if not dir_path.exists():
        return out
    for fp in sorted(dir_path.glob('*.json')):
        try:
            out.append((fp, json.loads(fp.read_text(encoding='utf-8'))))
        except Exception:
            out.append((fp, {'__error__': 'invalid_json'}))
    return out


def lint() -> list[str]:
    issues: list[str] = []
    for fp, r in load_jsons(REC_DIR):
        if '__error__' in r:
            issues.append(f'recipe:{fp.name}: invalid_json'); continue
        if not r.get('recipe_id'):
            issues.append(f'recipe:{fp.name}: recipe_id missing')
        if not r.get('title'):
            issues.append(f'recipe:{fp.name}: title missing')
        if not r.get('beginner_summary'):
            issues.append(f'recipe:{fp.name}: beginner_summary missing')
        if not r.get('persona') or not r.get('difficulty'):
            issues.append(f'recipe:{fp.name}: persona/difficulty missing')
        if not r.get('target_kind') or not r.get('target_id'):
            issues.append(f'recipe:{fp.name}: target_kind/target_id missing')
        defaults = r.get('defaults') or {}
        if not defaults.get('operation') or not defaults.get('timeframe'):
            issues.append(f'recipe:{fp.name}: defaults.operation/timeframe missing')
        guard = r.get('guardrails') or {}
        if guard.get('universe_cap') is None or guard.get('throttle_per_min') is None:
            issues.append(f'recipe:{fp.name}: guardrails.universe_cap/throttle_per_min missing')
        if not r.get('risk_profile'):
            issues.append(f'recipe:{fp.name}: risk_profile missing')
        if r.get('sort_rank') is None:
            issues.append(f'recipe:{fp.name}: sort_rank missing')
    return issues


def main():
    issues = lint()
    print(f'Issues: {len(issues)}')
    for m in issues:
        print(m)
    if not issues:
        print('OK: All recipes have beginner fields and guardrails/defaults.')


if __name__ == '__main__':
    main()
