from __future__ import annotations
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', required=True)
    ap.add_argument('--min', type=float, default=0.5)
    args = ap.parse_args()
    try:
        data = json.load(open(args.json, 'r', encoding='utf-8'))
    except Exception:
        data = {}
    best = data.get('best_sharpe_hourly')
    # Fallback: compute from threshold_results
    if best is None:
        res = data.get('result')
        if isinstance(res, dict):
            thr = res.get('threshold_results')
            if isinstance(thr, list) and thr:
                try:
                    best = max((r.get('sharpe_hourly') or 0.0) for r in thr)
                except Exception:
                    best = None
    should = int((best is not None) and (float(best) >= float(args.min)))
    with open('.smoke/should_train.txt','w',encoding='utf-8') as f:
        f.write(str(should))
    print(f"[smoke] Decision: should_train={should} (best_sharpe={best}, min={args.min})")

if __name__ == '__main__':
    main()

