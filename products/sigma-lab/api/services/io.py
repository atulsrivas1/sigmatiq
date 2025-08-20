from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Optional
import os
import yaml
import logging

# Establish both repo root and product root to keep packs (shared) at top-level
# while writing product outputs (matrices, artifacts, live_data, reports) under the product folder.
PRODUCT_DIR = Path(__file__).resolve().parents[2]  # products/sigma-lab
# Packs directory is configurable; defaults to product-local packs
PACKS_DIR = Path(os.environ.get('PACKS_DIR', str(PRODUCT_DIR / 'packs')))
ALLOWED_WRITE_ROOTS = [PRODUCT_DIR]

logger = logging.getLogger(__name__)


def workspace_paths(model_id: str, pack_id: str = "zerosigma") -> Dict[str, Path]:
    return {
        # Product-scoped outputs
        "matrices": PRODUCT_DIR / "matrices" / model_id,
        "live": PRODUCT_DIR / "live_data" / model_id,
        "artifacts": PRODUCT_DIR / "artifacts" / model_id,
        "reports": PRODUCT_DIR / "reports",
        "plots": PRODUCT_DIR / "static" / "backtest_plots" / model_id,
        # Packs path (configurable)
        "policy": PACKS_DIR / pack_id / "policy_templates" / f"{model_id}.yaml",
        "config": PACKS_DIR / pack_id / "model_configs" / f"{model_id}.yaml",
    }


def load_config(model_id: str, pack_id: str = "zerosigma") -> Dict[str, Any]:
    p = PACKS_DIR / pack_id / "model_configs" / f"{model_id}.yaml"
    if p.exists():
        try:
            return yaml.safe_load(p.read_text()) or {}
        except Exception:
            return {}
    return {}


def resolve_indicator_set_path(pack_id: str, model_id: str, indicator_set_name: Optional[str] = None) -> Path:
    base = PACKS_DIR / pack_id
    cand = base / 'indicator_sets' / f"{model_id}.yaml"
    if cand.exists():
        return cand
    if indicator_set_name:
        cand2 = base / 'indicator_sets' / f"{indicator_set_name}.yaml"
        if cand2.exists():
            return cand2
    legacy = base / 'indicator_set.yaml'
    return legacy


def _is_within(path: Path, root: Path) -> bool:
    try:
        return root.resolve(strict=False) in path.resolve(strict=False).parents or path.resolve(strict=False) == root.resolve(strict=False)
    except Exception:
        return False


def sanitize_out_path(candidate: Optional[str], default_path: Path) -> Path:
    """Return a safe output path confined to product workspace.

    - If candidate is None/empty, return default_path.
    - If candidate resolves outside allowed roots, raise ValueError.
    - Ensure parent directory exists.
    """
    if not candidate:
        default_path.parent.mkdir(parents=True, exist_ok=True)
        return default_path
    p = Path(candidate)
    # Disallow absolute paths that are not under allowed roots
    resolved = p.resolve(strict=False)
    allowed = any(_is_within(resolved, r) for r in ALLOWED_WRITE_ROOTS)
    if not allowed:
        msg = f"out path not allowed: {resolved} (must be within {ALLOWED_WRITE_ROOTS[0]})"
        logger.warning(msg)
        raise ValueError(msg)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    return resolved
