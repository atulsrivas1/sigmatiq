#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WF_DIR = REPO / 'docs' / 'workflows' / 'examples'


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
    for fp, w in load_jsons(WF_DIR):
        if '__error__' in w:
            issues.append(f'workflow:{fp.name}: invalid_json'); continue
        wid = w.get('workflow_id') or w.get('id')
        if not wid:
            issues.append(f'workflow:{fp.name}: workflow_id missing')
        if not w.get('title'):
            issues.append(f'workflow:{fp.name}: title missing')
        if not w.get('persona') or not w.get('difficulty'):
            issues.append(f'workflow:{fp.name}: persona/difficulty missing')
        if w.get('time_to_complete') is None:
            issues.append(f'workflow:{fp.name}: time_to_complete missing')
        deps = w.get('dependencies') or {}
        if not (deps.get('indicators') or deps.get('indicator_sets') or deps.get('strategies')):
            issues.append(f'workflow:{fp.name}: dependencies empty')
        steps = w.get('steps') or []
        if not steps:
            issues.append(f'workflow:{fp.name}: steps missing')
        else:
            for i, s in enumerate(steps, 1):
                if not s.get('description'):
                    issues.append(f'workflow:{fp.name}: step#{i} description missing')
                api = s.get('api') or {}
                if not api.get('method') or not api.get('path'):
                    issues.append(f'workflow:{fp.name}: step#{i} api.method/path missing')
        if not w.get('outputs'):
            issues.append(f'workflow:{fp.name}: outputs missing')
        if not w.get('novice_ready'):
            issues.append(f'workflow:{fp.name}: novice_ready missing/false')
        if not w.get('beginner_summary'):
            issues.append(f'workflow:{fp.name}: beginner_summary missing')
    return issues


def main():
    issues = lint()
    print(f'Issues: {len(issues)}')
    for m in issues:
        print(m)
    if not issues:
        print('OK: All workflows have required beginner fields and structure.')


if __name__ == '__main__':
    main()
