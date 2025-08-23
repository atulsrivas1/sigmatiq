#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
STRAT_DIR = REPO / 'docs' / 'catalog' / 'strategies'


def load_jsons(dir_path: Path) -> list[tuple[Path, dict]]:
    out = []
    if not dir_path.exists():
        return out
    for fp in sorted(dir_path.glob('*.json')):
        try:
            out.append((fp, json.loads(fp.read_text(encoding='utf-8'))))
        except Exception:
            out.append((fp, {'__error__': 'invalid_json'}))
    return out


def lint_strategies() -> list[str]:
    issues: list[str] = []
    for fp, data in load_jsons(STRAT_DIR):
        if '__error__' in data:
            issues.append(f'strategy:{fp.name}: invalid_json')
            continue
        if not data.get('novice_ready'):
            issues.append(f'strategy:{fp.name}: novice_ready missing/false')
        if not data.get('beginner_summary'):
            issues.append(f'strategy:{fp.name}: beginner_summary missing')
        if not data.get('entry_logic') or not data.get('exit_logic'):
            issues.append(f'strategy:{fp.name}: entry_logic/exit_logic missing')
        sd = data.get('simple_defaults') or {}
        if not sd.get('operation') or not sd.get('timeframe'):
            issues.append(f'strategy:{fp.name}: simple_defaults.operation/timeframe missing')
        gr = data.get('guardrails') or {}
        if gr.get('max_positions') is None or gr.get('max_daily_trades') is None or gr.get('loss_cap_bps') is None:
            issues.append(f'strategy:{fp.name}: guardrails max_positions/max_daily_trades/loss_cap_bps missing')
        pre = data.get('pre_reqs') or {}
        if not pre.get('indicator_sets_used'):
            issues.append(f'strategy:{fp.name}: pre_reqs.indicator_sets_used missing')
        if not data.get('assistant_hints'):
            issues.append(f'strategy:{fp.name}: assistant_hints missing')
    return issues


def main():
    issues = lint_strategies()
    print(f'Issues: {len(issues)}')
    for msg in issues:
        print(msg)
    if not issues:
        print('OK: All strategies have required beginner fields and links.')


if __name__ == '__main__':
    main()
