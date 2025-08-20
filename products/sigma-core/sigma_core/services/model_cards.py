from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from datetime import datetime

from .io import PACKS_DIR, resolve_indicator_set_path, load_config
from .policy import load_policy
from .lineage import compute_lineage


def _cards_dir(pack_id: str, model_id: str) -> Path:
    return PACKS_DIR / pack_id / 'model_cards' / model_id


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def write_model_card(
    *,
    pack_id: str,
    model_id: str,
    event: str,
    params: Optional[Dict[str, Any]] = None,
    metrics: Optional[Dict[str, Any]] = None,
    features: Optional[List[str]] = None,
    lineage: Optional[Dict[str, Optional[str]]] = None,
    notes: Optional[str] = None,
) -> Dict[str, str]:
    event = str(event or 'unknown').lower()
    ts = _now_iso()
    pack_dir = PACKS_DIR / pack_id
    try:
        ind_path = resolve_indicator_set_path(pack_id, model_id)
    except Exception:
        ind_path = None
    lineage_vals = lineage or compute_lineage(pack_dir=pack_dir, model_id=model_id, indicator_set_path=ind_path)
    pol = load_policy(model_id, pack_id)
    cfg = load_config(model_id, pack_id)
    exec_pol = pol.get('execution', {}) if isinstance(pol.get('execution', {}), dict) else {}
    pol_summary = {
        'slippage_bps': exec_pol.get('slippage_bps', 1.0),
        'size_by_conf': exec_pol.get('size_by_conf', False),
        'conf_cap': exec_pol.get('conf_cap', 1.0),
        'momentum_gate': exec_pol.get('momentum_gate', False),
        'momentum_min': exec_pol.get('momentum_min', 0.0),
        'momentum_column': exec_pol.get('momentum_column', None),
        'brackets': exec_pol.get('brackets', {}),
        'options': exec_pol.get('options', {}),
    }

    card: Dict[str, Any] = {
        'schema_version': '1.0',
        'pack_id': pack_id,
        'model_id': model_id,
        'created_at': ts,
        'event': event,
        'policy_version': pol.get('version'),
        'lineage': lineage_vals,
        'config': {
            'ticker': cfg.get('ticker'),
            'model': cfg.get('model'),
            'task': cfg.get('task'),
            'train_window': cfg.get('train_window'),
        },
        'policy': pol_summary,
        'params': params or {},
        'metrics': metrics or {},
        'features': list(features) if features else None,
        'notes': notes,
    }

    outdir = _cards_dir(pack_id, model_id)
    outdir.mkdir(parents=True, exist_ok=True)
    safe_event = ''.join(ch for ch in event if ch.isalnum() or ch in ('-', '_')) or 'event'
    fname = f"{ts.replace(':','-')}_{safe_event}"
    json_path = outdir / f"{fname}.json"
    md_path = outdir / f"{fname}.md"
    json_path.write_text(json.dumps(card, indent=2))

    md_lines = []
    md_lines.append(f"# Model Card — {model_id}")
    md_lines.append("")
    md_lines.append(f"- Pack: {pack_id}")
    md_lines.append(f"- Created: {ts}")
    md_lines.append(f"- Event: {event}")
    md_lines.append(f"- Policy Version: {pol.get('version')}")
    md_lines.append("")
    md_lines.append("## Lineage")
    for k in ('pack_sha','indicator_set_sha','model_config_sha','policy_sha'):
        md_lines.append(f"- {k}: {lineage_vals.get(k)}")
    md_lines.append("")
    md_lines.append("## Config")
    md_lines.append(f"- Ticker: {cfg.get('ticker')}")
    md_lines.append(f"- Model: {cfg.get('model')}")
    md_lines.append(f"- Task: {cfg.get('task')}")
    md_lines.append(f"- Train window: {cfg.get('train_window')}")
    md_lines.append("")
    md_lines.append("## Policy (execution)")
    for k, v in pol_summary.items():
        md_lines.append(f"- {k}: {v}")
    md_lines.append("")
    if features:
        md_lines.append("## Features")
        md_lines.append(", ".join(features))
        md_lines.append("")
    if params:
        md_lines.append("## Params")
        for k, v in (params or {}).items():
            if isinstance(v, (dict, list)):
                try:
                    v = json.dumps(v)
                except Exception:
                    v = str(v)
            md_lines.append(f"- {k}: {v}")
        md_lines.append("")
    if metrics:
        md_lines.append("## Metrics")
        for k in ('best_sharpe_hourly','best_cum_ret','rows','n_trades','auc','f1'):
            if k in (metrics or {}):
                md_lines.append(f"- {k}: {(metrics or {}).get(k)}")
        md_lines.append("")
    if notes:
        md_lines.append("## Notes")
        md_lines.append(str(notes))
        md_lines.append("")

    md_path.write_text("\n".join(md_lines))

    return {'json_path': str(json_path), 'md_path': str(md_path)}


def list_model_cards(*, pack_id: str, model_id: str) -> List[Dict[str, Any]]:
    outdir = _cards_dir(pack_id, model_id)
    if not outdir.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for p in sorted(outdir.glob('*.json')):
        try:
            data = json.loads(p.read_text())
            rows.append({'file': p.name, 'created_at': data.get('created_at'), 'event': data.get('event'), 'path': str(p)})
        except Exception:
            rows.append({'file': p.name, 'created_at': None, 'event': None, 'path': str(p)})
    rows.sort(key=lambda r: (r.get('created_at') or r.get('file')), reverse=True)
    return rows


def load_model_card(*, pack_id: str, model_id: str, file: Optional[str] = None) -> Dict[str, Any]:
    outdir = _cards_dir(pack_id, model_id)
    if not outdir.exists():
        raise FileNotFoundError('model cards directory not found')
    target: Optional[Path] = None
    if file:
        cand = outdir / file
        if cand.exists():
            target = cand
        else:
            raise FileNotFoundError(f'card not found: {cand}')
    else:
        cards = list(outdir.glob('*.json'))
        if not cards:
            raise FileNotFoundError('no cards found')
        target = sorted(cards)[-1]
    data = json.loads(target.read_text())
    md_file = target.with_suffix('.md')
    md_text = md_file.read_text() if md_file.exists() else None
    return {'json': data, 'markdown': md_text, 'json_path': str(target), 'md_path': str(md_file)}
