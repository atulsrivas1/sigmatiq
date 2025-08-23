#!/usr/bin/env python3
"""
Lint sc.model_specs.training_cfg for novice-safe defaults.

Checks:
- selection.thresholds within [0.5, 0.9] if present
- selection.top_pct within (0.0, 0.5] if present
- selection.allowed_hours subset of US RTH hours (9..16 inclusive)

Exit non-zero if violations found; prints a short report.
"""
from __future__ import annotations
import sys
from typing import Any, Dict, List
from sigma_core.storage.relational import get_db

RTH_MIN = 9
RTH_MAX = 16


def _err(msg: str) -> None:
    sys.stderr.write(msg + "\n")


def main() -> int:
    violations: List[str] = []
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT model_id, version, training_cfg FROM sc.model_specs WHERE status IN ('draft','in_review','published')")
            rows = cur.fetchall()
    for model_id, version, cfg in rows:
        tc = cfg or {}
        if not isinstance(tc, dict):
            continue
        sel = tc.get('selection') or {}
        if not isinstance(sel, dict):
            continue
        # thresholds
        thr = sel.get('thresholds')
        if thr is not None:
            try:
                vals = [float(x) for x in thr]
                for v in vals:
                    if not (0.5 <= v <= 0.9):
                        violations.append(f"{model_id}@{version}: thresholds contains out-of-range value {v} (expected 0.5..0.9)")
            except Exception:
                violations.append(f"{model_id}@{version}: thresholds not a numeric list")
        # top_pct
        tp = sel.get('top_pct')
        if tp is not None:
            try:
                v = float(tp)
                if not (0.0 < v <= 0.5):
                    violations.append(f"{model_id}@{version}: top_pct={v} out of range (expected 0.0..0.5]")
            except Exception:
                violations.append(f"{model_id}@{version}: top_pct is not numeric")
        # allowed_hours
        hrs = sel.get('allowed_hours')
        if hrs is not None:
            try:
                hs = [int(h) for h in hrs]
                bad = [h for h in hs if h < RTH_MIN or h > RTH_MAX]
                if bad:
                    violations.append(f"{model_id}@{version}: allowed_hours has out-of-RTH hours {bad} (expected between {RTH_MIN} and {RTH_MAX})")
            except Exception:
                violations.append(f"{model_id}@{version}: allowed_hours not an integer list")
    if violations:
        _err("Training cfg linter violations:")
        for v in violations:
            _err("- " + v)
        return 2
    print("lint-training-cfg: OK (no violations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

