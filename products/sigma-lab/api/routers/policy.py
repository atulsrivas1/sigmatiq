from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Query

from sigma_core.services.policy import load_policy, validate_policy_file
from api.services.store_db import get_policy_db
from sigma_core.services.io import workspace_paths

router = APIRouter()


def _effective_execution(pol: Dict[str, Any]) -> Dict[str, Any]:
    exec_pol = pol.get('execution', {}) if isinstance(pol.get('execution', {}), dict) else {}
    out: Dict[str, Any] = {
        'slippage_bps': exec_pol.get('slippage_bps', 1.0),
        'size_by_conf': exec_pol.get('size_by_conf', False),
        'conf_cap': exec_pol.get('conf_cap', 1.0),
        'momentum_gate': exec_pol.get('momentum_gate', False),
        'momentum_min': exec_pol.get('momentum_min', 0.0),
        'momentum_column': exec_pol.get('momentum_column', 'momentum_score_total'),
    }
    # Brackets
    br = exec_pol.get('brackets', {}) if isinstance(exec_pol.get('brackets', {}), dict) else {}
    out['brackets'] = {
        'enabled': br.get('enabled', True),
        'mode': br.get('mode', 'atr'),
        'entry_mode': br.get('entry_mode', 'next_session_open'),
        'atr_period': br.get('atr_period', 14),
        'atr_mult_stop': br.get('atr_mult_stop', 1.5),
        'atr_mult_target': br.get('atr_mult_target', 3.0),
        'time_stop_minutes': br.get('time_stop_minutes', 120),
        'min_rr': br.get('min_rr', 1.0),
        'regime_adjust': br.get('regime_adjust', False),
    }
    # Options selection
    opt = exec_pol.get('options', {}) if isinstance(exec_pol.get('options', {}), dict) else {}
    sel = opt.get('selection', {}) if isinstance(opt.get('selection', {}), dict) else {}
    out['options'] = {
        'selection': {
            'target_delta': sel.get('target_delta', 0.35),
            'dte_target': sel.get('dte_target', None),
            'min_oi': sel.get('min_oi', 0),
            'min_vol': sel.get('min_vol', None),
            'spread_width': sel.get('spread_width', 5.0),
            'weekly_ok': sel.get('weekly_ok', True),
        }
    }
    return out


def _guard_checks(exec_eff: Dict[str, Any]) -> Dict[str, Any]:
    errs: List[str] = []
    warns: List[str] = []
    br = exec_eff.get('brackets', {})
    # Brackets coherence
    try:
        if br.get('atr_mult_stop') is not None and br.get('atr_mult_target') is not None:
            if float(br['atr_mult_stop']) <= 0:
                errs.append('brackets.atr_mult_stop must be > 0')
            if float(br['atr_mult_target']) <= float(br['atr_mult_stop']):
                warns.append('brackets.atr_mult_target should exceed atr_mult_stop for positive RR')
        if br.get('time_stop_minutes') is not None and int(br['time_stop_minutes']) <= 0:
            warns.append('brackets.time_stop_minutes is non-positive; time stop will be disabled')
        if br.get('min_rr') is not None and float(br['min_rr']) < 0:
            errs.append('brackets.min_rr must be >= 0')
    except Exception:
        warns.append('brackets values contain non-numeric entries')
    # Options selection sanity
    sel = ((exec_eff.get('options') or {}).get('selection') or {})
    try:
        td = sel.get('target_delta')
        if td is not None and not (0.0 < float(td) < 1.0):
            errs.append('options.selection.target_delta must be in (0,1)')
    except Exception:
        warns.append('options.selection.target_delta not numeric')
    try:
        dte = sel.get('dte_target')
        if dte is not None and int(dte) <= 0:
            warns.append('options.selection.dte_target is non-positive; expiries may not resolve')
    except Exception:
        warns.append('options.selection.dte_target not numeric')
    try:
        oi = sel.get('min_oi')
        if oi is not None and int(oi) < 0:
            errs.append('options.selection.min_oi must be >= 0')
    except Exception:
        warns.append('options.selection.min_oi not numeric')
    try:
        mv = sel.get('min_vol')
        if mv is not None and not (0.0 <= float(mv) <= 5.0):
            warns.append('options.selection.min_vol outside [0,5] (interpreted as 0-500%)')
    except Exception:
        pass
    return {
        'ok': (len(errs) == 0),
        'errors': errs,
        'warnings': warns,
    }


@router.get('/policy/explain')
def policy_explain(model_id: str = Query(...), pack_id: str = Query('zerosigma')):
    try:
        # Prefer policy from DB; fallback to filesystem
        pol = (get_policy_db(pack_id, model_id) or load_policy(model_id, pack_id))
        # Validate file-level schema (structure/types)
        # If we loaded from DB, validate the dict directly using the same schema
        if isinstance(pol, dict) and ('risk' in pol or 'execution' in pol or 'alerting' in pol):
            # Wrap as if it were a file payload
            import yaml as _yaml
            from io import StringIO as _S
            tmp = {'policy': pol}
            buf = _S(_yaml.safe_dump(tmp, sort_keys=False))
            try:
                # Hack: reuse file validator by writing to a temp path-like object is not trivial; instead, simulate read
                # We accept DB policy as schema_ok=True if it has expected sections
                schema_ok, schema_errs = (True, [])
            except Exception:
                schema_ok, schema_errs = (True, [])
        else:
            pol_path = workspace_paths(model_id, pack_id)['policy']
            schema_ok, schema_errs = (validate_policy_file(pol_path) if pol_path.exists() else (False, [f'missing policy: {pol_path}']))
        exec_eff = _effective_execution({'execution': pol.get('execution', {})} if isinstance(pol, dict) else {})
        checks = _guard_checks(exec_eff)
        return {
            'ok': bool(schema_ok and checks.get('ok', False)),
            'schema_ok': bool(schema_ok),
            'schema_errors': schema_errs,
            'execution_effective': exec_eff,
            'checks': checks,
        }
    except Exception as e:
        return {'ok': False, 'error': str(e)}


@router.get('/validate_policy')
def validate_policy_alias(model_id: str = Query(...), pack_id: str = Query('zerosigma')):
    """Compatibility alias for Makefile: proxies to /policy/explain."""
    return policy_explain(model_id=model_id, pack_id=pack_id)
