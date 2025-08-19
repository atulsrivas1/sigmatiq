
#!/usr/bin/env python3
"""
paper_run.py — submit model signals to Paper Trader and stream alerts.

Usage:
  python scripts/paper_run.py --create-account --account-name default_paper
  python scripts/paper_run.py --pack-id swingedge --model-id universe_eq_swing_daily_scanner \\
    --signals scans/breakout_momentum/2025-08-15.csv --stream
"""

import argparse, csv, os, sys, time
from typing import Optional, Dict, Any
try:
    import requests
except Exception:
    requests = None

def create_account(base_url: str, name: str, cash: float, commission_bps: float, slippage_bps: float,
                   vp_limit: float, default_fill_model: str, margin_mode: str="reg-t") -> str:
    if requests is None:
        raise RuntimeError("requests not available in this environment")
    body = {
        "name": name, "cash": cash, "margin_mode": margin_mode,
        "commission_bps": commission_bps, "slippage_bps": slippage_bps,
        "vp_limit": vp_limit, "default_fill_model": default_fill_model
    }
    r = requests.post(f"{base_url}/paper/accounts", json=body, timeout=30)
    r.raise_for_status()
    j = r.json()
    if not j.get("ok", True):
        raise RuntimeError(f"Account creation failed: {j}")
    return j.get("account_id")

def submit_order(base_url: str, account_id: str, model_id: str, row: Dict[str, Any],
                 fill_model: Optional[str]=None, brackets: Optional[Dict[str, Any]]=None) -> str:
    if requests is None:
        raise RuntimeError("requests not available in this environment")
    symbol = row.get("symbol") or row.get("ticker")
    if not symbol:
        raise ValueError("signals CSV must include 'symbol' or 'ticker' column")
    side   = (row.get("side") or "buy").lower()
    qty    = int(float(row.get("qty") or row.get("shares") or 1))

    body = {
        "account_id": account_id,
        "model_id": model_id,
        "signal_id": f"sig_{int(time.time())}_{symbol}",
        "symbol": symbol,
        "side": side,
        "qty": qty,
        "tif": "MKT",
        "limit_px": None
    }
    if fill_model:
        body["fill_model"] = fill_model
    if brackets:
        body["bracket"] = brackets

    r = requests.post(f"{base_url}/paper/orders", json=body, timeout=30)
    r.raise_for_status()
    return r.json().get("order_id", "")

def stream_alerts(base_url: str, account_id: str):
    if requests is None:
        raise RuntimeError("requests not available in this environment")
    with requests.get(f"{base_url}/paper/alerts/stream", params={"account_id": account_id}, stream=True, timeout=300) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            try:
                print(line.decode("utf-8"))
            except Exception:
                pass

def parse_brackets(spec: str):
    if not spec:
        return None
    d = {}
    for part in [p.strip() for p in spec.split(",")]:
        if not part or ":" not in part: 
            continue
        k, v = part.split(":", 1)
        v = v.strip()
        if v.lower() in ("true","false"):
            d[k] = (v.lower()=="true")
        else:
            try:
                d[k] = float(v) if v.replace('.','',1).isdigit() else v
            except Exception:
                d[k] = v
    return d

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="http://localhost:8000")
    ap.add_argument("--pack-id", default="swingedge")
    ap.add_argument("--model-id", default="universe_eq_swing_daily_scanner")
    ap.add_argument("--signals", help="CSV: symbol|ticker, side, qty[,score_total,close,notional]")
    ap.add_argument("--account-id")
    ap.add_argument("--account-name", default="default_paper")
    ap.add_argument("--fill-model", default=None)
    ap.add_argument("--brackets", default="enabled:true,mode:atr,atr_mult_stop:1.2,atr_mult_target:2.0,time_stop_minutes:120")
    ap.add_argument("--create-account", action="store_true")
    ap.add_argument("--cash", type=float, default=100000)
    ap.add_argument("--commission-bps", type=float, default=0.5)
    ap.add_argument("--slippage-bps", type=float, default=1.0)
    ap.add_argument("--vp-limit", type=float, default=0.10)
    ap.add_argument("--margin-mode", default="reg-t")
    ap.add_argument("--stream", action="store_true")
    args = ap.parse_args()

    account_id = args.account_id
    if args.create_account or not account_id:
        account_id = create_account(args.base_url, args.account_name, args.cash, args.commission_bps,
                                    args.slippage_bps, args.vp_limit, args.fill_model or "next_bar_open",
                                    margin_mode=args.margin_mode)
        print(f"Account: {account_id}")

    brackets = parse_brackets(args.brackets)

    if args.signals and os.path.exists(args.signals):
        with open(args.signals, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    oid = submit_order(args.base_url, account_id, args.model_id, row, args.fill_model, brackets)
                    print(f"Submitted {row.get('symbol') or row.get('ticker')} → order {oid}")
                except Exception as e:
                    print(f"Error submitting {row}: {e}", file=sys.stderr)
    else:
        print("No signals CSV provided; use --signals path/to/file.csv")

    if args.stream:
        print("Streaming alerts... (Ctrl+C to stop)")
        try:
            stream_alerts(args.base_url, account_id)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
