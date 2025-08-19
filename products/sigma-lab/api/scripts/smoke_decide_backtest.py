from __future__ import annotations
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', required=True)
    ap.add_argument('--min_trades', type=int, default=1)
    ap.add_argument('--top_pct', type=float, default=0.10)
    args = ap.parse_args()
    try:
        data = json.load(open(args.json, 'r', encoding='utf-8'))
    except Exception:
        data = {}
    total_trades = None
    res = data.get('result')
    if isinstance(res, dict):
        thr = res.get('threshold_results')
        if isinstance(thr, list):
            try:
                total_trades = int(sum(int(r.get('trades') or 0) for r in thr))
            except Exception:
                total_trades = None
    use = 1 if (total_trades is None or total_trades < int(args.min_trades)) else 0
    with open('.smoke/use_top_pct.txt','w',encoding='utf-8') as f:
        f.write(str(use))
    print(f"[smoke] Backtest trades={total_trades}, min_trades={args.min_trades} => use_top_pct={use} (top_pct={args.top_pct})")

if __name__ == '__main__':
    main()

