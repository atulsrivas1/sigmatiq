#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
IND_OVR = REPO / 'docs' / 'catalog' / 'overrides' / 'indicators'
SET_OVR = REPO / 'docs' / 'catalog' / 'overrides' / 'indicator_sets'


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


def lint_indicators() -> list[str]:
    issues: list[str] = []
    for fp, data in load_jsons(IND_OVR):
        if '__error__' in data:
            issues.append(f'indicator:{fp.name}: invalid_json')
            continue
        if not data.get('novice_ready'):
            issues.append(f'indicator:{fp.name}: novice_ready missing/false')
        if not data.get('beginner_summary'):
            issues.append(f'indicator:{fp.name}: beginner_summary missing')
        measures = data.get('measures') or {}
        if not measures.get('what_it_measures') or not measures.get('how_to_read'):
            issues.append(f'indicator:{fp.name}: measures.what_it_measures/how_to_read incomplete')
        usage = data.get('usage') or {}
        if not usage.get('example_conditions'):
            issues.append(f'indicator:{fp.name}: usage.example_conditions missing')
        if not data.get('assistant_hints'):
            issues.append(f'indicator:{fp.name}: assistant_hints missing')
    return issues


def lint_sets() -> list[str]:
    issues: list[str] = []
    for fp, data in load_jsons(SET_OVR):
        if '__error__' in data:
            issues.append(f'set:{fp.name}: invalid_json')
            continue
        if not data.get('novice_ready'):
            issues.append(f'set:{fp.name}: novice_ready missing/false')
        if not data.get('beginner_summary'):
            issues.append(f'set:{fp.name}: beginner_summary missing')
        comps = data.get('components') or []
        if not comps:
            issues.append(f'set:{fp.name}: components empty')
        rg = data.get('reading_guide') or {}
        if not rg.get('signal_logic') or not rg.get('timeframe_alignment'):
            issues.append(f'set:{fp.name}: reading_guide.signal_logic/timeframe_alignment incomplete')
        sd = data.get('simple_defaults') or {}
        if not sd.get('timeframe'):
            issues.append(f'set:{fp.name}: simple_defaults.timeframe missing')
        gr = data.get('guardrails') or {}
        if gr.get('universe_cap') is None or gr.get('throttle_per_min') is None:
            issues.append(f'set:{fp.name}: guardrails.universe_cap/throttle_per_min missing')
        if not data.get('assistant_hints'):
            issues.append(f'set:{fp.name}: assistant_hints missing')
    return issues


def main():
    ind_issues = lint_indicators()
    set_issues = lint_sets()
    total = len(ind_issues) + len(set_issues)
    print(f'Issues: {total}')
    for msg in ind_issues + set_issues:
        print(msg)
    if total == 0:
        print('OK: All indicators and sets have required beginner fields.')


if __name__ == '__main__':
    main()
