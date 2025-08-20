from __future__ import annotations
from pathlib import Path
import hashlib
from typing import Dict, Optional


def _sha1_path(p: Path) -> Optional[str]:
    try:
        data = p.read_bytes()
        return hashlib.sha1(data).hexdigest()
    except Exception:
        return None


def compute_lineage(*, pack_dir: Path, model_id: str, indicator_set_path: Optional[Path] = None) -> Dict[str, Optional[str]]:
    ind = None
    if indicator_set_path is not None:
        ind = _sha1_path(indicator_set_path)
    cfg = _sha1_path(pack_dir / 'model_configs' / f'{model_id}.yaml')
    pol = _sha1_path(pack_dir / 'policy_templates' / f'{model_id}.yaml')
    packsha = _sha1_path(pack_dir / 'pack.yaml')
    return {
        'pack_sha': packsha,
        'indicator_set_sha': ind,
        'model_config_sha': cfg,
        'policy_sha': pol,
    }
