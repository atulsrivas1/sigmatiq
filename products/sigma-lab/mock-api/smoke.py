#!/usr/bin/env python3
"""
Comprehensive smoke test for Sigmatiq Sigma Mock API.
Checks all documented endpoints with minimal shape assertions.

Usage:
  MOCK_API_URL=http://localhost:8010 python smoke.py
"""
from __future__ import annotations
import os
import sys
import time
from typing import Any, Dict, List

try:
    import requests
except Exception as e:  # pragma: no cover
    print("[ERR] requests not installed. Please: pip install requests", file=sys.stderr)
    sys.exit(2)


BASE_URL = os.environ.get("MOCK_API_URL", "http://localhost:8010").rstrip("/")


def get(path: str, **kwargs):
    url = f"{BASE_URL}{path}"
    r = requests.get(url, timeout=10, **kwargs)
    r.raise_for_status()
    return r.json()


def post(path: str, json: Dict[str, Any]):
    url = f"{BASE_URL}{path}"
    r = requests.post(url, json=json, timeout=15)
    r.raise_for_status()
    return r.json()


class SmokeFailure(Exception):
    pass


def assert_keys(d: Dict[str, Any], keys: List[str], ctx: str):
    for k in keys:
        if k not in d:
            raise SmokeFailure(f"{ctx}: missing key '{k}' in {list(d.keys())}")


def run_smoke() -> int:
    failures: List[str] = []

    def check(name: str, fn):
        try:
            fn()
            print(f"[OK] {name}")
        except Exception as e:
            failures.append(f"{name}: {e}")
            print(f"[FAIL] {name}: {e}")

    # 1) Index
    check("GET /", lambda: (
        (lambda j: (
            assert_keys(j, ["ok", "endpoints"], "/"),
            isinstance(j["endpoints"], list) or (_ for _ in ()).throw(SmokeFailure("endpoints not list"))
        ))(get("/"))
    ))

    # 2) Health
    check("GET /health", lambda: assert_keys(get("/health"), ["ok", "service", "version", "now"], "/health"))

    # 3) Models
    check("GET /models", lambda: (
        (lambda j: (
            assert_keys(j, ["models"], "/models"),
            (len(j["models"]) >= 1) or (_ for _ in ()).throw(SmokeFailure("no models"))
        ))(get("/models"))
    ))

    # 4) Model detail
    check("GET /model_detail", lambda: assert_keys(get("/model_detail", params={"model_id": "spy_opt_0dte_hourly", "pack_id": "zerosigma"}), ["ok", "config", "policy_valid"], "/model_detail"))

    # 5) Indicator sets
    check("GET /indicator_sets", lambda: assert_keys(get("/indicator_sets"), ["ok", "groups"], "/indicator_sets"))

    # 6) Leaderboard (basic + filters + pass_gate)
    def _ld(params=None):
        j = get("/leaderboard", params=params or {"limit": 3, "offset": 0})
        assert_keys(j, ["rows", "limit", "offset", "next_offset"], "/leaderboard")
        if j["rows"]:
            r0 = j["rows"][0]
            assert_keys(r0, ["model_id", "pack_id", "sharpe", "trades", "win_rate", "gate"], "leaderboard.row")
    check("GET /leaderboard", _ld)
    check("GET /leaderboard pass_gate", lambda: _ld({"pass_gate": True}))

    # 7) Signals
    check("GET /signals", lambda: assert_keys(get("/signals", params={"limit": 2}), ["rows", "limit", "offset"], "/signals"))
    check("GET /option_signals", lambda: assert_keys(get("/option_signals", params={"limit": 2}), ["rows", "limit", "offset"], "/option_signals"))

    # 8) Policy explain
    check("GET /policy/explain", lambda: assert_keys(get("/policy/explain", params={"model_id": "spy_opt_0dte_hourly", "pack_id": "zerosigma"}), ["ok", "execution_effective"], "/policy/explain"))

    # 9) Calibrate thresholds
    check("POST /calibrate_thresholds", lambda: assert_keys(post("/calibrate_thresholds", {"model_id": "spy_opt_0dte_hourly", "grid": "0.5,0.55,0.6"}), ["recommended_threshold", "counts"], "/calibrate_thresholds"))

    # 10) Scan
    check("POST /scan", lambda: assert_keys(post("/scan", {"pack_id": "swingsigma", "model_id": "universe_eq_swing_daily_scanner", "indicator_set": "swing_eq_breakout_scanner", "start": "2024-07-01", "end": "2024-07-05", "tickers": "AAPL,MSFT"}), ["ok", "rows"], "/scan"))

    # 11) Build & Preview
    build_body = {"model_id": "spy_opt_0dte_hourly", "pack_id": "zerosigma", "start": "2024-06-01", "end": "2024-06-15"}
    check("POST /build_matrix", lambda: (
        (lambda j: (
            assert_keys(j, ["ok", "path", "matrix_sha", "profile"], "/build_matrix")
        ))(post("/build_matrix", build_body))
    ))
    check("POST /preview_matrix", lambda: assert_keys(post("/preview_matrix", build_body), ["ok", "columns", "rows"], "/preview_matrix"))

    # 12) Train & Backtest
    check("POST /train", lambda: assert_keys(post("/train", {"model_id": "spy_opt_0dte_hourly", "pack_id": "zerosigma"}), ["ok", "model_out"], "/train"))
    check("POST /backtest", lambda: assert_keys(post("/backtest", {"model_id": "spy_opt_0dte_hourly", "pack_id": "zerosigma"}), ["ok", "summary", "artifacts"], "/backtest"))

    # 13) Create Model
    new_name = f"smoke_model_{int(time.time())}"
    check("POST /models", lambda: (
        (lambda j: (
            assert_keys(j, ["ok", "model_id"], "/models:create"),
            (j["model_id"] == new_name) or (_ for _ in ()).throw(SmokeFailure("model_id mismatch"))
        ))(post("/models", {"template_id": "spy_opt_0dte_hourly", "name": new_name, "risk_profile": "Balanced"}))
    ))

    # 14) Backtest Sweep
    check("POST /backtest_sweep", lambda: (
        (lambda j: (
            assert_keys(j, ["ok", "rows"], "/backtest_sweep"),
            isinstance(j["rows"], list) or (_ for _ in ()).throw(SmokeFailure("rows not list"))
        ))(post("/backtest_sweep", {
            "model_id": "spy_opt_0dte_hourly",
            "risk_profile": "Balanced",
            "sweep": {"thresholds_variants": [[0.5, 0.55, 0.6]], "hours_variants": [[13,14], [13,14,15]], "top_pct_variants": [[0.1, 0.15]]},
            "tag": "smoke"
        }))
    ))

    if failures:
        print("\n== FAILURES ==")
        for f in failures:
            print(" - ", f)
        return 1
    print("\nAll endpoints passed smoke checks.")
    return 0


if __name__ == "__main__":
    sys.exit(run_smoke())

