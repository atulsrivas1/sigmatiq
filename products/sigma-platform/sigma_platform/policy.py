from __future__ import annotations
from typing import Any, Dict, List, Optional
from pathlib import Path as _Path
import yaml

from .io import PACKS_DIR


def load_policy(model_id: str, pack_id: str) -> Dict[str, Any]:
    pol_path = PACKS_DIR / pack_id / 'policy_templates' / f'{model_id}.yaml'
    data: Dict[str, Any] = {}
    try:
        raw = yaml.safe_load(pol_path.read_text()) if pol_path.exists() else {}
        if isinstance(raw, dict):
            data = raw.get('policy', raw)
    except Exception:
        data = {}
    return data or {}


def validate_policy_file(path: _Path) -> (bool, List[str]):
    errs: List[str] = []
    try:
        data = yaml.safe_load(path.read_text())
    except Exception as e:
        return False, [f'failed to parse YAML: {e}']
    if not isinstance(data, dict):
        return False, ['policy root must be a mapping']
    pol = data.get('policy') if 'policy' in data else data
    if not isinstance(pol, dict):
        errs.append("'policy' must be a mapping if present; otherwise provide keys at root")
        return False, errs
    for sec in ('risk','execution','alerting'):
        if sec not in pol or not isinstance(pol.get(sec), dict):
            errs.append(f'missing or invalid section: {sec}')
    execd = pol.get('execution', {}) if isinstance(pol.get('execution', {}), dict) else {}
    if 'slippage_bps' in execd and not isinstance(execd.get('slippage_bps'), (int,float)):
        errs.append('execution.slippage_bps must be a number')
    if 'size_by_conf' in execd and not isinstance(execd.get('size_by_conf'), bool):
        errs.append('execution.size_by_conf must be a boolean')
    if 'conf_cap' in execd and not isinstance(execd.get('conf_cap'), (int,float)):
        errs.append('execution.conf_cap must be a number')
    alert = pol.get('alerting', {}) if isinstance(pol.get('alerting', {}), dict) else {}
    if 'cooldown_minutes' in alert and not isinstance(alert.get('cooldown_minutes'), (int,float)):
        errs.append('alerting.cooldown_minutes must be a number')
    risk = pol.get('risk', {}) if isinstance(pol.get('risk', {}), dict) else {}
    for k in ('max_drawdown','max_exposure'):
        if k in risk and not isinstance(risk.get(k), (int,float)):
            errs.append(f'risk.{k} must be a number')
    br = execd.get('brackets', {}) if isinstance(execd.get('brackets', {}), dict) else {}
    if br:
        for key in ('atr_mult_stop','atr_mult_target','time_stop_minutes','atr_period','min_rr'):
            if key in br and not isinstance(br.get(key), (int,float)):
                errs.append(f'execution.brackets.{key} must be a number')
        for key in ('enabled','regime_adjust'):
            if key in br and not isinstance(br.get(key), bool):
                errs.append(f'execution.brackets.{key} must be a boolean')
        if 'entry_mode' in br and not isinstance(br.get('entry_mode'), str):
            errs.append('execution.brackets.entry_mode must be a string')
        if 'mode' in br and not isinstance(br.get('mode'), str):
            errs.append('execution.brackets.mode must be a string')
    opt = execd.get('options', {}) if isinstance(execd.get('options', {}), dict) else {}
    if opt:
        sel = opt.get('selection', {}) if isinstance(opt.get('selection', {}), dict) else {}
        if sel:
            for key in ('dte_target','min_oi','min_vol','spread_width','target_delta'):
                if key in sel and not isinstance(sel.get(key), (int,float)):
                    errs.append(f'execution.options.selection.{key} must be a number')
            for key in ('weekly_ok',):
                if key in sel and not isinstance(sel.get(key), bool):
                    errs.append(f'execution.options.selection.{key} must be a boolean')
    return (len(errs) == 0), errs


def ensure_policy_exists(model_id: str, pack_id: str) -> Optional[str]:
    pol = PACKS_DIR / pack_id / 'policy_templates' / f'{model_id}.yaml'
    if not pol.exists():
        return f"Policy file missing for model '{model_id}'. Please create: {pol}"
    ok, errs = validate_policy_file(pol)
    if not ok:
        return f"Policy file invalid for model '{model_id}': {', '.join(errs)} (path: {pol})"
    return None
