
#!/usr/bin/env python3
"""
scanner_breakout_momentum.py — nightly breakout + momentum scanner (swing, daily)

Usage:
  python scripts/scanner_breakout_momentum.py --universe data/universe.csv --out scans/breakout_momentum --config scanner_config.json
"""
import argparse, os, json, datetime as dt

def load_universe(path: str):
    with open(path, "r") as f:
        return [line.strip().split(",")[0] for line in f if line.strip() and not line.lower().startswith("ticker")]

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

    # Placeholder scoring: replace with real feature matrix + logic
    rows = []
    for t in tickers:
        rows.append({
          "ticker": t, "score_total": 80.0, "donchian_20": 1,
          "bos_20": 0.30, "rsi_14": 58, "adx_14": 22, "close": 100.0, "ema_20": 99.0, "ema_50": 95.0
        })

    rows = sorted(rows, key=lambda r: r["score_total"], reverse=True)[: cfg["top_n"]]
    cols = ["ticker","score_total","donchian_20","bos_20","rsi_14","adx_14","close","ema_20","ema_50"]
    with open(out_csv, "w") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join(str(r.get(c, "")) for c in cols) + "\n")

    print(f"Wrote {len(rows)} rows to {out_csv}")

if __name__ == "__main__":
    main()
