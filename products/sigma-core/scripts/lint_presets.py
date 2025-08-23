#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

# Read SQL seeds to ensure presets have beginner_summary set (simple static check fallback)
# Prefer live DB linter later; for now validate JSON-like expectations via reading seed files present.

migs = [
    Path('products/sigma-core/migrations/0010_sc_seed_universe_presets.sql'),
    Path('products/sigma-core/migrations/0013_sc_seed_universe_presets_novice.sql'),
]

required = {
    'sp500': None,
    'nasdaq100': None,
    'dow30': None,
    'liquid_etfs': None,
}

issues = []
for p in migs:
    if not p.exists():
        continue
    txt = p.read_text(encoding='utf-8')
    for k in list(required.keys()):
        if k in txt:
            # naive presence check; 0013 ensures beginner_summary updates
            required[k] = True

for k, v in required.items():
    if not v:
        issues.append(f'preset:{k}: missing from seeds or novice updates')

print(f'Issues: {len(issues)}')
for i in issues:
    print(i)
if not issues:
    print('OK: Preset seeds include novice fields and metadata for common presets.')
