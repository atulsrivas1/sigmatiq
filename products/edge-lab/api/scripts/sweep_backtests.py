from __future__ import annotations
import argparse, json, time
from pathlib import Path
import requests as req

def split_variants(s: str) -> list[str]:
    s = (s or '').strip()
    if not s:
        return []
    return [part.strip() for part in s.split(';') if part.strip()]

def main():
    ap = argparse.ArgumentParser(description='Sweep backtests across parameter combos')
    ap.add_argument('--base-url', default='http://localhost:8001')
    ap.add_argument('--model-id', required=True)
    ap.add_argument('--pack-id', default='zeroedge')
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--thresholds', default='')  # semicolon-separated variants, each is comma list
    ap.add_argument('--allowed-hours', default='')  # semicolon-separated variants (e.g., "13,14,15;13,14")
    ap.add_argument('--top-pcts', default='')  # semicolon-separated (e.g., "0.10;0.15"), used when thresholds blank or as additional axis
    ap.add_argument('--splits', type=int, default=5)
    ap.add_argument('--embargo', type=float, default=0.0)
    ap.add_argument('--tag', default='sweep')
    ap.add_argument('--limit', type=int, default=20)
    args = ap.parse_args()

    base = args.base_url.rstrip('/')
    tvars = split_variants(args.thresholds)
    avars = split_variants(args.allowed_hours)
    pvars = split_variants(args.top_pcts)
    if not tvars and not pvars:
        # sensible defaults if nothing provided
        tvars = ['0.50,0.52,0.54','0.55,0.60,0.65']
    if not avars:
        avars = ['13,14,15']

    results: list[dict] = []
    out_dir = Path('products/edge-lab/reports')
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S')
    out_json = out_dir / f'sweep_{args.model_id}_{ts}.json'

    def do_post(payload: dict) -> dict:
        try:
            r = req.post(f'{base}/backtest', json=payload, timeout=300)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    # thresholds-based sweeps
    for th in tvars:
        for ah in avars:
            payload = {
                'model_id': args.model_id,
                'pack_id': args.pack_id,
                'thresholds': th,
                'splits': int(args.splits),
                'embargo': float(args.embargo),
                'allowed_hours': ah,
                'tag': args.tag,
            }
            res = do_post(payload)
            results.append({'kind': 'thresholds', 'thresholds': th, 'allowed_hours': ah, 'res': res})

    # top-pct sweeps
    for tp in pvars:
        for ah in avars:
            try:
                topv = float(tp)
            except Exception:
                continue
            payload = {
                'model_id': args.model_id,
                'pack_id': args.pack_id,
                'top_pct': topv,
                'splits': int(args.splits),
                'embargo': float(args.embargo),
                'allowed_hours': ah,
                'tag': args.tag,
            }
            res = do_post(payload)
            results.append({'kind': 'top_pct', 'top_pct': topv, 'allowed_hours': ah, 'res': res})

    # Persist raw sweep results
    try:
        out_json.write_text(json.dumps({'runs': results}, indent=2), encoding='utf-8')
        print(f'[sweep] Wrote {out_json}')
    except Exception:
        pass

    # Print a tidy summary and show leaderboard top-N
    def best_of(r: dict) -> float:
        if not isinstance(r, dict):
            return -1e9
        v = r.get('best_sharpe_hourly')
        if v is not None:
            try:
                return float(v)
            except Exception:
                return -1e9
        res = r.get('res', {}) if 'res' in r else r
        if isinstance(res, dict):
            v = res.get('best_sharpe_hourly')
            if v is not None:
                try:
                    return float(v)
                except Exception:
                    return -1e9
        return -1e9

    ranked = sorted(results, key=lambda x: best_of(x['res']), reverse=True)
    print('[sweep] Top combos (by best_sharpe_hourly):')
    for i, row in enumerate(ranked[:10]):
        r = row['res']
        print(f"  {i+1}. kind={row.get('kind')}, thr={row.get('thresholds')}, top_pct={row.get('top_pct')}, hours={row.get('allowed_hours')}, best_sharpe={r.get('best_sharpe_hourly')}, best_cum={r.get('best_cum_ret')}")

    # Leaderboard fetch
    try:
        lb = req.get(f"{base}/leaderboard", params={'pack_id': args.pack_id, 'model_id': args.model_id, 'limit': int(args.limit)}).json()
        rows = lb.get('rows', []) if isinstance(lb, dict) else []
        print(f"[sweep] Leaderboard top {args.limit}:")
        for i, row in enumerate(rows):
            print(f"  {i+1}. sharpe={row.get('best_sharpe_hourly')}, cum={row.get('best_cum_ret')}, tag={row.get('tag')}")
    except Exception as e:
        print('[sweep] Could not fetch leaderboard:', e)

if __name__ == '__main__':
    main()

