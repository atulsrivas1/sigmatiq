#!/usr/bin/env python3

"""
scanner_breakout_momentum.py — nightly breakout + momentum scanner (swing, daily)

Usage:
  python scripts/scanner_breakout_momentum.py --universe data/universe.csv --out scans/breakout_momentum --config scanner_config.json
"""
import argparse, os, sys, json, datetime as dt
from typing import List, Dict

# ---- If you call your own REST API ----
# import requests

# ---- Or, if you have local builders in sigma_core ----
# from sigma_core.build import build_matrix_for_ticker

def load_universe(path: str) -> List[str]:
    with open(path, "r") as f:
        return [line.strip().split(",")[0] for line in f if line.strip() and not line.lower().startswith("ticker")]

def score_row(row, w):
    # Expect row dict to contain computed fields
    bos20 = row.get("bos_20", 0.0)
    zret20 = row.get("zret_20", 0.0)
    zret63 = row.get("zret_63", 0.0)
    adx14  = row.get("adx_14", 0.0)
    ema20  = row.get("ema_20", 0.0)
    ema50  = row.get("ema_50", 0.0)
    close  = row.get("close", 0.0)

    def clip01(x): return max(0.0, min(1.0, x))

    breakout_score = clip01(bos20 / 0.50) * w["breakout"]
    momentum_score = clip01(0.5*zret20 + 0.5*zret63) * w["momentum"]
    trend_quality  = clip01((adx14 - 20.0) / 15.0) * w["trend_quality"]
    alignment      = w["alignment"] if (close > ema20 > ema50) else 0.0
    total          = breakout_score + momentum_score + trend_quality + alignment
    return total

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--universe", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", default="scanner_config.json")
    args = ap.parse_args()

    with open(args.config, "r") as f:
        cfg = json.load(f)

    os.makedirs(args.out, exist_ok=True)
    tickers = load_universe(args.universe)
    today = dt.date.today().isoformat()
    out_csv = os.path.join(args.out, f"{today}.csv")

    # ---- Example loop (pseudo): replace the feature acquisition with your pipeline ----
    rows = []
    for tkr in tickers:
        # Option A: REST call to your API that builds a daily matrix for the last 300 days
        # resp = requests.post("http://localhost:8000/build_matrix", json={...})
        # df = pd.DataFrame(resp.json()["rows"])
        # Option B: local builder function
        # df = build_matrix_for_ticker(tkr, indicator_set="swing_eq_breakout_scanner", cadence="daily")

        # PSEUDO: replace with real data; below is a placeholder row
        row = {
            "ticker": tkr,
            "close": 100.0,
            "ema_20": 99.0,
            "ema_50": 95.0,
            "adx_14": 22.0,
            "rsi_14": 58.0,
            "bos_20": 0.30,   # (close - roll_max_20) / atr_14
            "zret_20": 0.6,
            "zret_63": 0.4,
            "donchian_20": 1,
            "adv_20": 1_000_000,
            "price": 25.0,
        }

        # Gates
        gates = (
            (row["price"] >= 5.0) and
            (row["adv_20"] >= 500_000) and
            ((row["donchian_20"] == 1) or (row["bos_20"] >= cfg["bos_min"])) and
            (row["rsi_14"] >= cfg["rsi_min"]) and
            (row["adx_14"] >= cfg["adx_min"])
        )
        if not gates:
            continue

        score = score_row(row, cfg["weights"])
        row["score_total"] = round(score, 2)
        rows.append(row)

    # Rank & write
    rows.sort(key=lambda r: r["score_total"], reverse=True)
    rows = rows[: cfg["top_n"]]
    cols = ["ticker", "score_total", "donchian_20", "bos_20", "rsi_14", "adx_14", "close", "ema_20", "ema_50"]
    with open(out_csv, "w") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join(str(r.get(c, "")) for c in cols) + "\n")

    print(f"Wrote {len(rows)} rows to {out_csv}")

if __name__ == "__main__":
    main()
