from __future__ import annotations
import json
from pathlib import Path

def load(p: str) -> dict:
    try:
        return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:
        return {}

def main():
    b = load('.smoke/build.json')
    t = load('.smoke/train.json')
    bk = load('.smoke/backtest.json')
    print('[summary] Build:', b.get('ok'), 'csv=', b.get('out_csv'))
    print('[summary] Train:', t.get('ok'), 'rows=', t.get('rows'), 'model=', (t.get('model_out') or ''))
    best_sharpe = bk.get('best_sharpe_hourly')
    best_cum = bk.get('best_cum_ret')
    folds = None
    total_trades = None
    best_thr = None
    best_trades = None
    res = bk.get('result')
    if isinstance(res, dict):
        th = res.get('threshold_results')
        if isinstance(th, list):
            folds = len(th)
            # total trades across folds
            try:
                total_trades = int(sum(int(r.get('trades') or 0) for r in th))
            except Exception:
                total_trades = None
            # best fold by sharpe
            try:
                br = max(th, key=lambda r: (r.get('sharpe_hourly') or -1e9))
                best_thr = br.get('thr')
                best_trades = br.get('trades')
            except Exception:
                pass
    p = bk.get('parity') if isinstance(bk.get('parity'), dict) else None
    parity_str = 'absent'
    if isinstance(p, dict):
        parity_str = f"hit_rate={p.get('hit_rate')}, avg_rr={p.get('avg_rr')}, avg_ret%={p.get('avg_return_pct')}"
    print('[summary] Backtest:', bk.get('ok'), 'best_sharpe=', best_sharpe, f'(thr={best_thr}, trades={best_trades})', 'best_cum=', best_cum, 'folds=', folds, 'total_trades=', total_trades, 'parity:', parity_str)

if __name__ == '__main__':
    main()
