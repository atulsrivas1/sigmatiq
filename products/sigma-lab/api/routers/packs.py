from __future__ import annotations
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query
from pathlib import Path
import yaml

router = APIRouter()


ROOT = Path(__file__).resolve().parents[2]
PACKS_DIR = ROOT / "packs"


def _safe_yaml(path: Path) -> Dict[str, Any]:
    try:
        return yaml.safe_load(path.read_text()) or {}
    except Exception:
        return {}


@router.get("/packs")
def list_packs() -> Dict[str, Any]:
    packs: List[Dict[str, Any]] = []
    if PACKS_DIR.exists():
        for d in sorted(p for p in PACKS_DIR.iterdir() if p.is_dir()):
            meta = {}
            pack_yaml = d / "pack.yaml"
            if pack_yaml.exists():
                meta = _safe_yaml(pack_yaml)
            packs.append({"id": d.name, "meta": meta})
    return {"ok": True, "packs": packs}


@router.get("/packs/{pack_id}")
def pack_detail(pack_id: str) -> Dict[str, Any]:
    p = PACKS_DIR / pack_id
    if not p.exists():
        return {"ok": False, "error": f"pack not found: {pack_id}"}
    meta = _safe_yaml(p / "pack.yaml") if (p / "pack.yaml").exists() else {}
    # list indicator sets
    sets = []
    ind_dir = p / "indicator_sets"
    if ind_dir.exists():
        for f in sorted(ind_dir.glob("*.yaml")):
            sets.append({"name": f.stem})
    # list templates
    templates = []
    tpl_dir = p / "model_templates"
    if tpl_dir.exists():
        for f in sorted(tpl_dir.glob("*.yaml")):
            try:
                y = _safe_yaml(f)
                templates.append({
                    "template_id": y.get("template_id") or f.stem,
                    "name": y.get("name") or f.stem,
                    "template_version": y.get("template_version"),
                })
            except Exception:
                templates.append({"template_id": f.stem, "name": f.stem})
    # recent models
    models = []
    cfg_dir = p / "model_configs"
    if cfg_dir.exists():
        for f in sorted(cfg_dir.glob("*.yaml")):
            models.append(f.stem)
    return {"ok": True, "pack": {"id": pack_id, "meta": meta, "indicator_sets": sets, "templates": templates, "models": models}}


@router.get("/packs/{pack_id}/templates")
def pack_templates(pack_id: str) -> Dict[str, Any]:
    p = PACKS_DIR / pack_id / "model_templates"
    out: List[Dict[str, Any]] = []
    if p.exists():
        for f in sorted(p.glob("*.yaml")):
            y = _safe_yaml(f)
            out.append({
                "template_id": y.get("template_id") or f.stem,
                "name": y.get("name") or f.stem,
                "pack": pack_id,
                "horizon": y.get("horizon"),
                "cadence": y.get("cadence"),
                "template_version": y.get("template_version"),
            })
    return {"ok": True, "templates": out}


@router.get("/packs/{pack_id}/indicator_sets")
def pack_indicator_sets(pack_id: str) -> Dict[str, Any]:
    p = PACKS_DIR / pack_id / "indicator_sets"
    out: List[Dict[str, Any]] = []
    if p.exists():
        for f in sorted(p.glob("*.yaml")):
            out.append({"name": f.stem})
    return {"ok": True, "indicator_sets": out}

