#!/usr/bin/env python3
"""
Lint and validate model registry rows (sc.model_specs).

Checks:
- JSONB configs validate against Pydantic schema (featureset/label_cfg/thresholds/guardrails/artifacts/plan_template).
- Naming convention: model_id starts with 'sq_' (Sigmatiq); brand='sigmatiq'.
- Novice readiness: when novice_ready and status in ('in_review','published'), require beginner_summary and explainer_templates.
- Taxonomy: horizon/style values (DB constraints already guard on publish; linter warns sooner).
- Scope: if present, requires either cohort (allow_presets) or per_ticker (allow_symbols).
- Timeframe hint in model_id (heuristic): if suffix is one of {5m,15m,30m,hourly,daily,weekly}, it should match timeframe.

Exit code non-zero if any issues are found.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv  # type: ignore
    core_env = Path(__file__).resolve().parents[1] / '.env'
    if core_env.exists():
        load_dotenv(dotenv_path=core_env)
except Exception:
    pass

import psycopg2
from psycopg2.extras import RealDictCursor

from model_spec_schema import ModelSpecRow


def get_conn():
    url = os.getenv('DATABASE_URL')
    if url:
        return psycopg2.connect(url)
    host = os.getenv('DB_HOST', 'localhost')
    port = int(os.getenv('DB_PORT', '5432'))
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '')
    dbname = os.getenv('DB_NAME', 'postgres')
    return psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)


TIMEFRAME_HINTS = {
    '5m': '5m', '15m': '15m', '30m': '30m',
    'hourly': 'hour', 'daily': 'day', 'weekly': 'week'
}


def timeframe_from_id(model_id: str) -> Optional[str]:
    parts = model_id.split('_')
    if not parts:
        return None
    last = parts[-1]
    if last in TIMEFRAME_HINTS:
        return TIMEFRAME_HINTS[last]
    return None


def lint_scope(scope: Optional[Dict[str, Any]]) -> Optional[str]:
    if not scope:
        return None
    t = scope.get('type')
    if t == 'cohort':
        presets = scope.get('allow_presets') or []
        if not presets:
            return "scope.type=cohort requires allow_presets[]"
    elif t == 'per_ticker':
        syms = scope.get('allow_symbols') or []
        if not syms:
            return "scope.type=per_ticker requires allow_symbols[]"
    else:
        return "scope.type must be 'cohort' or 'per_ticker'"
    return None


def main() -> int:
    issues: List[str] = []
    with get_conn() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT model_id, version, status, title, description,
                       target_kind, target_id, target_version,
                       timeframe, market, instrument,
                       featureset, label_cfg, thresholds, guardrails, artifacts, plan_template,
                       novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
                       brand, display_name, horizon, style, tags, instrument_profile, suitability, scope
                FROM sc.model_specs ORDER BY model_id, version
                """
            )
            rows = cur.fetchall() or []
    for r in rows:
        mid = r['model_id']
        ver = r['version']
        prefix = f"{mid}@v{ver}"
        # Schema validation
        try:
            row = ModelSpecRow(**r)
            _ = row.validate_embedded()
        except Exception as e:
            issues.append(f"{prefix}: schema invalid: {e}")
            continue
        # Branding
        if not mid.startswith('sq_'):
            issues.append(f"{prefix}: model_id should start with 'sq_' (branding)")
        if (r.get('brand') or '').lower() != 'sigmatiq':
            issues.append(f"{prefix}: brand should be 'sigmatiq'")
        # Novice publish readiness
        status = (r.get('status') or '').lower()
        if r.get('novice_ready') and status in ('in_review', 'published'):
            if not r.get('beginner_summary'):
                issues.append(f"{prefix}: novice_ready requires beginner_summary")
            if not r.get('explainer_templates'):
                issues.append(f"{prefix}: novice_ready requires explainer_templates")
        # Taxonomy warnings (DB enforces on publish; warn earlier)
        hz = r.get('horizon'); st = r.get('style')
        if hz and hz not in ('0dte','intraday','swing','position','long_term'):
            issues.append(f"{prefix}: unknown horizon '{hz}'")
        if st and st not in ('momentum','mean_reversion','trend_follow','breakout','volatility','carry','stat_arb'):
            issues.append(f"{prefix}: unknown style '{st}'")
        # Scope
        msg = lint_scope(r.get('scope'))
        if msg:
            issues.append(f"{prefix}: {msg}")
        # Timeframe hint heuristic
        tf_hint = timeframe_from_id(mid)
        if tf_hint and r.get('timeframe') and r['timeframe'] != tf_hint:
            issues.append(f"{prefix}: timeframe '{r['timeframe']}' does not match id hint '{tf_hint}'")

    if issues:
        print("Model linter found issues:\n" + "\n".join(f" - {msg}" for msg in issues))
        return 1
    print("Model linter: OK (no issues)")
    return 0


if __name__ == '__main__':
    sys.exit(main())

