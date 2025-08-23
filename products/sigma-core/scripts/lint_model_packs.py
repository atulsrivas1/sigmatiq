#!/usr/bin/env python3
from __future__ import annotations
"""
Lint and validate model pack registry rows (sc.model_packs) and components.

Checks:
- Branding: pack_id starts with 'sq_', brand='sigmatiq'.
- Novice readiness: when novice_ready and status in ('in_review','published'), require beginner_summary, explainer_templates, and consensus.
- Consensus JSON: policy in {'majority','weighted','all'}, min_quorum sane, buy/sell thresholds in [0,1], tie_breaker in {'hold','buy','sell'}.
- Weighted policy requires weights on components (warn if missing).
- Components: referenced models must exist (sc.model_specs), min_score in [0,1] if provided, no duplicates.
- Timeframe compatibility: pack.timeframe should match component model timeframe (warn on mismatch).

Exit non-zero if any issues are found.
"""
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


def load_models(conn) -> Dict[Tuple[str,int], Dict[str, Any]]:
    out: Dict[Tuple[str,int], Dict[str, Any]] = {}
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT model_id, version, timeframe FROM sc.model_specs")
        for r in cur.fetchall() or []:
            out[(r['model_id'], r['version'])] = r
    return out


def main() -> int:
    issues: List[str] = []
    try:
        conn = get_conn()
    except Exception as e:
        print(f"Failed to connect to DB: {e}", file=sys.stderr)
        return 2
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT pack_id, version, status, brand, display_name, title, description,
                       timeframe, market, instrument,
                       novice_ready, beginner_summary, simple_defaults, explainer_templates, risk_notes,
                       horizon, style, tags, instrument_profile, suitability,
                       consensus
                FROM sc.model_packs
                ORDER BY pack_id, version
                """
            )
            packs = cur.fetchall() or []
            cur.execute(
                """
                SELECT pack_id, pack_version, ord, model_id, model_version, weight, required, min_score
                FROM sc.model_pack_components
                ORDER BY pack_id, pack_version, ord
                """
            )
            comps_all = cur.fetchall() or []
    comps_by_pack: Dict[Tuple[str,int], List[Dict[str, Any]]] = {}
    for c in comps_all:
        comps_by_pack.setdefault((c['pack_id'], c['pack_version']), []).append(c)

    models = load_models(conn)

    for p in packs:
        pid = p['pack_id']; ver = p['version']
        prefix = f"{pid}@v{ver}"
        # Branding
        if not (pid or '').startswith('sq_'):
            issues.append(f"{prefix}: pack_id should start with 'sq_' (branding)")
        if (p.get('brand') or '').lower() != 'sigmatiq':
            issues.append(f"{prefix}: brand should be 'sigmatiq'")
        # Novice publish readiness
        status = (p.get('status') or '').lower()
        if p.get('novice_ready') and status in ('in_review','published'):
            if not p.get('beginner_summary'):
                issues.append(f"{prefix}: novice_ready requires beginner_summary")
            if not p.get('explainer_templates'):
                issues.append(f"{prefix}: novice_ready requires explainer_templates")
            if not p.get('consensus'):
                issues.append(f"{prefix}: novice_ready requires consensus policy")
        # Consensus
        consensus = p.get('consensus') or {}
        if not consensus:
            issues.append(f"{prefix}: missing consensus policy")
        else:
            policy = (consensus.get('policy') or '').lower()
            if policy not in ('majority','weighted','all'):
                issues.append(f"{prefix}: consensus.policy must be majority|weighted|all")
            min_quorum = consensus.get('min_quorum')
            if not isinstance(min_quorum, int) or min_quorum < 1:
                issues.append(f"{prefix}: consensus.min_quorum must be integer >=1")
            for k in ('buy_score','sell_score'):
                v = consensus.get(k)
                if not (isinstance(v, (int,float)) and 0.0 <= float(v) <= 1.0):
                    issues.append(f"{prefix}: consensus.{k} must be in [0,1]")
            tb = (consensus.get('tie_breaker') or '').lower()
            if tb and tb not in ('hold','buy','sell'):
                issues.append(f"{prefix}: consensus.tie_breaker must be hold|buy|sell if provided")

        # Components
        pack_comps = comps_by_pack.get((pid, ver), [])
        if not pack_comps:
            issues.append(f"{prefix}: has no components")
            continue
        if consensus:
            if consensus.get('min_quorum', 0) > len(pack_comps):
                issues.append(f"{prefix}: consensus.min_quorum exceeds component count")
        seen: set[Tuple[str,int]] = set()
        weights_present = False
        for c in pack_comps:
            key = (c['model_id'], c['model_version'])
            if key in seen:
                issues.append(f"{prefix}: duplicate component {key}")
            seen.add(key)
            # referenced model exists
            if key not in models:
                issues.append(f"{prefix}: component model not found {key}")
            # min_score
            if c.get('min_score') is not None:
                try:
                    ms = float(c['min_score'])
                    if not (0.0 <= ms <= 1.0):
                        issues.append(f"{prefix}: component min_score must be in [0,1]")
                except Exception:
                    issues.append(f"{prefix}: component min_score invalid")
            # weights
            if c.get('weight') is not None:
                weights_present = True
        if consensus and (consensus.get('policy') == 'weighted') and not weights_present:
            issues.append(f"{prefix}: weighted policy requires component weights")
        # timeframe compatibility
        pack_tf = p.get('timeframe')
        if pack_tf:
            for c in pack_comps:
                key = (c['model_id'], c['model_version'])
                m = models.get(key)
                if m and m.get('timeframe') and m['timeframe'] != pack_tf:
                    issues.append(f"{prefix}: component {key} timeframe {m['timeframe']} != pack timeframe {pack_tf}")

    if issues:
        print("Model pack linter found issues:\n" + "\n".join(f" - {msg}" for msg in issues))
        return 1
    print("Model pack linter: OK (no issues)")
    return 0


if __name__ == '__main__':
    sys.exit(main())

