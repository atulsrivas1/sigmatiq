#!/usr/bin/env python3
"""
Generate a CSV with all implemented indicators using live Polygon data and run basic validation checks.

Usage:
  python scripts/test_indicators_full_polygon.py \
    --ticker SPY --start 2024-07-01 --end 2024-07-05 --expiry 2024-07-05 \
    --out_csv reports/indicators_full.csv --out_summary reports/indicators_full_summary.json

Notes:
- Requires POLYGON_API_KEY in env or .env at repo root.
- This script computes indicators that only require underlying bars and Polygon options snapshots.
- Flow-dependent indicators (e.g., sold_flow_ratio) are not included here because they require the full 0DTE flow build.
"""

from __future__ import annotations
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

import pandas as pd

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sigma_core.data.sources.polygon import (
    get_polygon_hourly_bars,
    get_polygon_daily_bars,
)

from sigma_core.indicators.builtins.momentum import Momentum
from sigma_core.indicators.builtins.roll_std import RollingStd
from sigma_core.indicators.builtins.rsi import RSI
from sigma_core.indicators.builtins.ema import EMA
from sigma_core.indicators.builtins.ema_slope import EmaSlope
from sigma_core.indicators.builtins.dist_to_ema import DistToEma
from sigma_core.indicators.builtins.ret import Ret
from sigma_core.indicators.builtins.macd import MACD
from sigma_core.indicators.builtins.bollinger import BollingerBands
from sigma_core.indicators.builtins.adx import ADX
from sigma_core.indicators.builtins.atr import ATR
from sigma_core.indicators.builtins.obv import OBV
from sigma_core.indicators.builtins.daily_rsi import DailyRSI
from sigma_core.indicators.builtins.daily_ema import DailyEMA
from sigma_core.indicators.builtins.daily_ret import DailyRet
from sigma_core.indicators.builtins.daily_dist_to_ema import DailyDistToEma
from sigma_core.indicators.builtins.daily_vwap import DailyVWAP
from sigma_core.indicators.builtins.momentum_score import MomentumScoreTotal
from sigma_core.indicators.builtins.iv_realized_spread import IVRealizedSpread
from sigma_core.indicators.builtins.iv_skew import IVSkew25Delta, IVTermSlope
from sigma_core.data.datasets import fetch_0dte_flow
from sigma_core.features.builder import FeatureBuilder


def _summary_checks(df: pd.DataFrame) -> dict:
    checks = {}
    def range_ok(series, lo=None, hi=None):
        s = pd.to_numeric(series, errors='coerce')
        if lo is not None and (s < lo).any():
            return False
        if hi is not None and (s > hi).any():
            return False
        return True

    if {'bb_mid_20','bb_upper_20','bb_lower_20'}.issubset(df.columns):
        checks['bollinger_order_ok'] = bool(((df['bb_upper_20'] >= df['bb_mid_20']) & (df['bb_mid_20'] >= df['bb_lower_20'])).all())
    if 'rsi_14' in df.columns:
        checks['rsi_14_in_0_100'] = range_ok(df['rsi_14'], 0.0, 100.0)
    if 'adx_14' in df.columns:
        checks['adx_14_in_0_100'] = range_ok(df['adx_14'], 0.0, 100.0)
    if 'atr_14' in df.columns:
        checks['atr_14_non_negative'] = bool((pd.to_numeric(df['atr_14'], errors='coerce') >= 0.0).all())
    if 'iv_realized_spread_20' in df.columns:
        s = pd.to_numeric(df['iv_realized_spread_20'], errors='coerce')
        checks['iv_realized_spread_20_any_non_nan'] = bool(s.notna().any())
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ticker', required=True)
    ap.add_argument('--start', required=True, help='YYYY-MM-DD')
    ap.add_argument('--end', required=True, help='YYYY-MM-DD')
    ap.add_argument('--expiry', required=False, help='YYYY-MM-DD (options expiry for IV-based indicators; default=end)')
    ap.add_argument('--out_csv', default=str(ROOT / 'reports' / 'indicators_full.csv'))
    ap.add_argument('--out_summary', default=str(ROOT / 'reports' / 'indicators_full_summary.json'))
    ap.add_argument('--skip_iv', action='store_true', help='Skip IV-based indicators if snapshots not available')
    ap.add_argument('--iv_source', default='snapshot', choices=['snapshot','quotes'], help='Source for IV indicators')
    ap.add_argument('--iv_window', default='10:00-11:00', help='ET window for quotes-based IV, e.g., 10:00-11:00')
    ap.add_argument('--iv_days_fwd', type=int, default=30, help='Days forward for iv_term_slope when using quotes/snapshot')
    args = ap.parse_args()

    if not (os.getenv('POLYGON_API_KEY') or os.getenv('ZE_POLYGON_API_KEY')):
        raise SystemExit('POLYGON_API_KEY not set; export it or put it in .env')

    out_dir = Path(args.out_csv).parent
    out_dir.mkdir(parents=True, exist_ok=True)

    # Base hourly frame with OHLCV
    hourly = get_polygon_hourly_bars(args.ticker, args.start, args.end)
    if hourly.empty:
        raise SystemExit('Failed to fetch hourly bars from Polygon')
    df = hourly.copy()
    df['date'] = pd.to_datetime(df['date'])  # tz-aware UTC

    # Intraday indicators
    intraday_inds = [
        Momentum('close', 1), Momentum('close', 3),
        RollingStd('close', 20), RSI('close', 14),
        EMA('close', 10), EMA('close', 20),
        EmaSlope('close', 10, 1), DistToEma('close', 10),
        Ret('close', 1), Ret('close', 3),
        MACD('close', 12, 26, 9), BollingerBands('close', 20, 2.0),
        ADX(14), ATR(14), OBV('close','volume'),
    ]
    for ind in intraday_inds:
        df = pd.concat([df, ind.calculate(df)], axis=1)

    # Daily indicators mapped to hourly timeline
    daily_inds = [
        DailyRSI(args.ticker, 14), DailyEMA(args.ticker, 20),
        DailyRet(args.ticker, 1), DailyRet(args.ticker, 5),
        DailyDistToEma(args.ticker, 20), DailyVWAP(args.ticker, 1),
    ]
    for ind in daily_inds:
        df = pd.concat([df, ind.calculate(df)], axis=1)

    # Composite
    df = pd.concat([df, MomentumScoreTotal().calculate(df)], axis=1)

    # Options IV-based
    expiry = args.expiry or args.end
    if not args.skip_iv:
        df = pd.concat([df, IVRealizedSpread(args.ticker, 20, 'hour', iv_source=args.iv_source, quote_window=args.iv_window).calculate(df)], axis=1)
        df = pd.concat([df, IVSkew25Delta(args.ticker, iv_source=args.iv_source, quote_window=args.iv_window).calculate(df)], axis=1)
        df = pd.concat([df, IVTermSlope(args.ticker, args.iv_days_fwd, iv_source=args.iv_source, quote_window=args.iv_window).calculate(df)], axis=1)

    # Flow-based per-distance features (0DTE): build and aggregate to (date,hour_et)
    try:
        raw_flow = fetch_0dte_flow(pd.to_datetime(args.start).date(), pd.to_datetime(args.end).date(), ticker=args.ticker, distance_max=7)
        if not raw_flow.empty:
            fb = FeatureBuilder(distance_max=7)
            flow_feats = fb.add_base_features(raw_flow)
            # Aggregate per (date, hour_et)
            sum_cols = [c for c in flow_feats.columns if any(c.startswith(p) for p in ["calls_sold_d","puts_sold_d","calls_premium_d","puts_premium_d"]) ]
            grp = flow_feats.groupby(['date','hour_et'], as_index=False)
            agg = grp[sum_cols].sum()
            # Totals & ratios post-aggregation
            calls_d = [c for c in agg.columns if c.startswith('calls_sold_d')]
            puts_d = [c for c in agg.columns if c.startswith('puts_sold_d')]
            if calls_d:
                agg['calls_sold_total'] = agg[calls_d].sum(axis=1)
            if puts_d:
                agg['puts_sold_total'] = agg[puts_d].sum(axis=1)
            if {'calls_sold_total','puts_sold_total'}.issubset(agg.columns):
                agg['pc_ratio'] = (agg['puts_sold_total']+1e-6)/(agg['calls_sold_total']+1e-6)
                agg['imbalance'] = agg['calls_sold_total'] - agg['puts_sold_total']
            prem_calls = [c for c in agg.columns if c.startswith('calls_premium_d')]
            prem_puts = [c for c in agg.columns if c.startswith('puts_premium_d')]
            if prem_calls:
                agg['calls_premium_total'] = agg[prem_calls].sum(axis=1)
            if prem_puts:
                agg['puts_premium_total'] = agg[prem_puts].sum(axis=1)
            if {'calls_premium_total','puts_premium_total'}.issubset(agg.columns):
                num = agg['puts_premium_total'].fillna(0.0) - agg['calls_premium_total'].fillna(0.0)
                den = agg['puts_premium_total'].fillna(0.0) + agg['calls_premium_total'].fillna(0.0) + 1e-6
                agg['dealer_sold_premium_imbalance'] = (num/den)
            # Merge into hourly df (by date,hour_et)
            df_merge = df.copy()
            df_merge['date_key'] = df_merge['date'].dt.date
            agg['date_key'] = pd.to_datetime(agg['date']).dt.date
            df = pd.merge(df_merge, agg.drop(columns=['date']), left_on=['date_key','hour_et'], right_on=['date_key','hour_et'], how='left').drop(columns=['date_key'])
    except Exception as e:
        # Non-fatal: flow features may not be present
        pass

    # Write CSV
    df.to_csv(args.out_csv, index=False)

    # Summaries + basic checks
    checks = _summary_checks(df)
    summary = {
        'ticker': args.ticker,
        'start': args.start,
        'end': args.end,
        'rows': int(len(df)),
        'columns': sorted(df.columns.tolist()),
        'checks': checks,
        'iv_source': (None if args.skip_iv else args.iv_source),
        'iv_nan_counts': {
            k: int(pd.to_numeric(df[k], errors='coerce').isna().sum())
            for k in ['iv_realized_spread_20','iv_skew_25d','iv_term_slope']
            if k in df.columns
        },
        'generated_at': datetime.utcnow().isoformat(),
    }
    Path(args.out_summary).write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
