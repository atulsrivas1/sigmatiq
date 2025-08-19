#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import numpy as np

from edge_core.data.stocks import build_stock_matrix as build_stock_matrix_range


def resolve_indicator_set_path(pack_id: str, model_id: str, indicator_set_name: str | None = None) -> Path | None:
    base = ROOT / 'packs' / pack_id / 'indicator_sets'
    cand = base / f"{model_id}.yaml"
    if cand.exists():
        return cand
    if indicator_set_name:
        cand2 = base / f"{indicator_set_name}.yaml"
        if cand2.exists():
            return cand2
    # model config reference
    cfg = ROOT / 'packs' / pack_id / 'model_configs' / f"{model_id}.yaml"
    if cfg.exists():
        import yaml
        data = yaml.safe_load(cfg.read_text()) or {}
        name = data.get('indicator_set')
        if name:
            cand3 = base / f"{name}.yaml"
            if cand3.exists():
                return cand3
    return None


def compute_breakout_momentum_score(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    # Expect latest row per ticker; compute sub-scores and total aligned with the guide
    out = df.copy()
    eps = float(cfg.get('epsilon', 0.002))
    rsi_min = float(cfg.get('rsi_min', 55))
    adx_min = float(cfg.get('adx_min', 18))
    bos_min = float(cfg.get('bos_min', 0.25))
    w = cfg.get('weights', {}) or {}
    w_break = float(w.get('breakout', 40))
    w_momo = float(w.get('momentum', 30))
    w_trendq = float(w.get('trend_quality', 15))
    w_align = float(w.get('alignment', 15))
    w_sum = max(1e-6, w_break + w_momo + w_trendq + w_align)

    # Core columns
    close = pd.to_numeric(out.get('close', pd.Series(index=out.index)), errors='coerce')
    # Bands & Donchian
    upper = pd.to_numeric(out.filter(like='upper_').iloc[:,0] if any(out.columns.str.startswith('upper_')) else pd.Series(np.nan, index=out.index), errors='coerce')
    donch_cols = [c for c in out.columns if c.startswith('donchian_high_')]
    donch_high = pd.to_numeric(out[donch_cols[0]] if donch_cols else pd.Series(np.nan, index=out.index), errors='coerce')
    atr = pd.to_numeric(out.filter(like='atr_').iloc[:,0] if any(out.columns.str.startswith('atr_')) else pd.Series(np.nan, index=out.index), errors='coerce')

    # BoS_N = (close - donchian_high_N) / ATR_14
    bos = (close - donch_high) / atr.replace(0.0, np.nan)
    bos = bos.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    # Breakout pass (epsilon or BoS)
    breakout_pass = ((close > upper * (1.0 + eps)) | (close > donch_high * (1.0 + eps)) | (bos >= bos_min)).astype(float)
    # Breakout score ~ scale BoS to 0..1 via clipping at 0.50 (per doc example)
    score_breakout = np.clip(bos / 0.50, 0.0, 1.0)

    # Momentum: combine momentum_20 and momentum_63 (fallback to returns)
    m20 = pd.to_numeric((out.filter(like='momentum_20').iloc[:,0] if any(out.columns.str.contains('momentum_20')) else out.get('ret_20', pd.Series(np.nan, index=out.index))), errors='coerce')
    m63 = pd.to_numeric((out.filter(like='momentum_63').iloc[:,0] if any(out.columns.str.contains('momentum_63')) else out.get('ret_63', pd.Series(np.nan, index=out.index))), errors='coerce')
    # Normalize via percentile ranks (robust without scipy)
    momentum_score = (m20.rank(pct=True) * 0.5 + m63.rank(pct=True) * 0.5).fillna(0.0)

    # Trend quality: ADX scaled; fallback to lr_r2 if present
    adx = pd.to_numeric((out.filter(like='adx_').iloc[:,0] if any(out.columns.str.startswith('adx_')) else pd.Series(np.nan, index=out.index)), errors='coerce')
    r2 = pd.to_numeric((out.filter(like='lr_r2_').iloc[:,0] if any(out.columns.str.startswith('lr_r2_')) else pd.Series(np.nan, index=out.index)), errors='coerce').fillna(0.0)
    trend_quality = np.clip((adx - 20.0) / 15.0, 0.0, 1.0)
    # If ADX missing, use r2 directly (already ~0..1)
    trend_quality = np.where(adx.notna(), trend_quality, r2)

    # Alignment: ema20 > ema50 and RSI/ADX gates
    ema20 = pd.to_numeric((out.filter(like='ema_20').iloc[:,0] if any(out.columns.str.startswith('ema_20')) else pd.Series(np.nan, index=out.index)), errors='coerce')
    ema50 = pd.to_numeric((out.filter(like='ema_50').iloc[:,0] if any(out.columns.str.startswith('ema_50')) else pd.Series(np.nan, index=out.index)), errors='coerce')
    rsi = pd.to_numeric((out.filter(like='rsi_').iloc[:,0] if any(out.columns.str.startswith('rsi_')) else pd.Series(np.nan, index=out.index)), errors='coerce')
    align_trend = (ema20 > ema50).astype(float)
    align_rsi = (rsi >= rsi_min).astype(float)
    align_adx = (adx >= adx_min).astype(float) if adx.notna().any() else 1.0
    score_alignment = (align_trend + align_rsi + align_adx) / 3.0

    out['bos_derived'] = bos
    out['score_breakout'] = score_breakout
    out['score_momentum'] = momentum_score
    out['score_trend_quality'] = pd.to_numeric(trend_quality, errors='coerce').fillna(0.0)
    out['score_alignment'] = score_alignment
    out['score_total'] = (w_break * out['score_breakout'] + w_momo * out['score_momentum'] + w_trendq * out['score_trend_quality'] + w_align * out['score_alignment']) / w_sum
    # Apply gates: breakout pass + RSI/ADX
    gates = (breakout_pass >= 1.0) & (align_rsi >= 1.0) & (align_adx >= 1.0)
    out['_gates_pass'] = gates.astype(bool)
    return out


def main():
    ap = argparse.ArgumentParser(description='Breakout & Momentum Scanner')
    ap.add_argument('--pack_id', default='swingedge')
    ap.add_argument('--model_id', default='universe_eq_swing_daily_scanner')
    ap.add_argument('--tickers', required=False, help='Comma-separated universe, e.g., AAPL,MSFT,SPY')
    ap.add_argument('--universe_csv', required=False, help='CSV file with a ticker column')
    ap.add_argument('--universe_col', default='ticker', help='Column name in universe CSV (default: ticker)')
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--indicator_set', default='swing_eq_breakout_scanner')
    ap.add_argument('--config', default=str(ROOT / 'docs' / 'Improvements' / 'breakout_momentum_scanner_assets' / 'scanner_config.json'))
    ap.add_argument('--top_n', type=int, default=50)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()

    # Load config
    cfg_path = Path(args.config)
    cfg = json.loads(cfg_path.read_text()) if cfg_path.exists() else {}
    top_n = int(args.top_n or cfg.get('top_n', 50))

    # Resolve indicator set path
    ind_path = resolve_indicator_set_path(args.pack_id, args.model_id, args.indicator_set)

    # Resolve universe
    tickers = []
    if args.universe_csv:
        import pandas as pd
        u = pd.read_csv(args.universe_csv)
        col = args.universe_col
        if col not in u.columns:
            raise SystemExit(f"Universe CSV missing column: {col}")
        tickers = [str(x).strip().upper() for x in u[col].dropna().tolist() if str(x).strip()]
    elif args.tickers:
        tickers = [x.strip().upper() for x in args.tickers.split(',') if x.strip()]
    else:
        raise SystemExit("Provide --tickers or --universe_csv")

    # Build per-ticker matrices and keep latest row per ticker
    rows = []
    for t in tickers:
        out_csv = ROOT / 'matrices' / args.model_id / f"{t}_scan.csv"
        out_csv.parent.mkdir(parents=True, exist_ok=True)
        build_stock_matrix_range(
            start_date=args.start,
            end_date=args.end,
            out_csv=str(out_csv),
            ticker=t,
            indicator_set_path=(str(ind_path) if ind_path else None),
            label_kind='none',
        )
        try:
            df = pd.read_csv(out_csv)
            if len(df) == 0:
                continue
            last = df.iloc[[-1]].copy()
            last['ticker'] = t
            rows.append(last)
        except Exception:
            continue

    if not rows:
        print(json.dumps({'ok': False, 'error': 'No data built for provided tickers'}, indent=2))
        sys.exit(1)

    latest = pd.concat(rows, ignore_index=True)
    scored = compute_breakout_momentum_score(latest, cfg)
    # Keep only rows that pass gates if available
    if '_gates_pass' in scored.columns:
        scored = scored[scored['_gates_pass']].copy()
    scored = scored.sort_values('score_total', ascending=False)
    scored['rank'] = np.arange(1, len(scored) + 1)
    picked = scored.head(top_n).copy()

    # Write outputs
    live_dir = ROOT / 'live_data' / args.model_id
    live_dir.mkdir(parents=True, exist_ok=True)
    out_csv = live_dir / 'signals.csv'
    keep_cols = [c for c in ['ticker', 'date', 'close', 'score_total', 'score_breakout', 'score_momentum', 'score_trend_quality', 'score_alignment', 'rank'] if c in picked.columns]
    picked.to_csv(out_csv, index=False, columns=keep_cols)
    result = {
        'ok': True,
        'model_id': args.model_id,
        'pack_id': args.pack_id,
        'count': int(len(picked)),
        'signals_csv': str(out_csv),
        'top': picked[keep_cols].head(min(5, len(picked))).to_dict(orient='records'),
    }
    print(json.dumps(result, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
