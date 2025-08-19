from __future__ import annotations
from typing import Dict
from fastapi import APIRouter, Query
import os
import time
import inspect

from edge_core.indicators.registry import registry as indicator_registry

router = APIRouter()

# Simple in-memory TTL cache for indicators response
_CACHE_TTL = float(os.getenv('INDICATORS_CACHE_TTL', '300'))  # seconds
_cache_data = {
    'flat': {'ts': 0.0, 'value': None},
    'grouped': {'ts': 0.0, 'value': None},
}

@router.get('/indicators')
def indicators_api(group: bool = Query(False), bypass_cache: bool = Query(False)):
    now = time.time()
    key = 'grouped' if group else 'flat'
    if not bypass_cache:
        cached = _cache_data.get(key)
        if cached and cached['value'] is not None and (now - float(cached['ts'])) < _CACHE_TTL:
            return cached['value']
    out = []
    for name, cls in indicator_registry.indicators.items():
        try:
            sig = inspect.signature(cls.__init__)
            params = [p.name for p in sig.parameters.values() if p.name != 'self']
        except Exception:
            params = []
        out.append({
            'name': name,
            'category': getattr(cls, 'CATEGORY', 'uncategorized'),
            'subcategory': getattr(cls, 'SUBCATEGORY', 'general'),
            'params': params,
            'doc': (cls.__doc__ or '').strip(),
        })
    if not group:
        resp = {'ok': True, 'indicators': sorted(out, key=lambda x: (x['category'], x['subcategory'], x['name']))}
        _cache_data['flat'] = {'ts': now, 'value': resp}
        return resp
    grouped: Dict[str, Dict[str, list]] = {}
    for it in out:
        grouped.setdefault(it['category'], {}).setdefault(it['subcategory'], []).append(it['name'])
    for cat in grouped:
        for sub in grouped[cat]:
            grouped[cat][sub] = sorted(grouped[cat][sub])
    resp = {'ok': True, 'groups': grouped}
    _cache_data['grouped'] = {'ts': now, 'value': resp}
    return resp
