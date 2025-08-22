from __future__ import annotations
import json
import hashlib
from pathlib import Path
from typing import Dict, Any
import yaml  # type: ignore


def _hash_indicator_set(data: Dict[str, Any]) -> str:
    try:
        # Normalize structure: keep only stable keys
        if 'indicators' in data and isinstance(data['indicators'], list):
            norm = {'name': data.get('name'), 'version': data.get('version', 1), 'indicators': data['indicators']}
        else:
            norm = data
        s = json.dumps(norm, sort_keys=True, separators=(",", ":"))
    except Exception:
        s = json.dumps(data, default=str, sort_keys=True)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()[:16]


def materialize_indicator_set(base_reports_dir: Path, model_id: str, ind_data: Dict[str, Any]) -> Path:
    """Cache the indicator set to a YAML file based on content hash.

    - Writes to base_reports_dir/indicator_cache/<model_id>_<hash>.yaml
    - If file exists, reuses it.
    - Cleans up older cache files for the same model_id to avoid clutter.
    Returns the Path to the cached YAML.
    """
    cache_dir = base_reports_dir / 'indicator_cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    h = _hash_indicator_set(ind_data)
    target = cache_dir / f'{model_id}_{h}.yaml'
    if not target.exists():
        # Write current
        to_write = ind_data if ('indicators' in ind_data) else {'name': model_id, 'version': 1, 'indicators': ind_data}
        target.write_text(yaml.safe_dump(to_write, sort_keys=False), encoding='utf-8')
        # Cleanup old cache files for this model
        try:
            prefix = f'{model_id}_'
            for f in cache_dir.glob(f'{model_id}_*.yaml'):
                if f.name != target.name:
                    f.unlink(missing_ok=True)
        except Exception:
            pass
    return target

