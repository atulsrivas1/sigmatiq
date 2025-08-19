#!/usr/bin/env python3
from __future__ import annotations
import argparse
import sys
from pathlib import Path

import pandas as pd


def main():
    ap = argparse.ArgumentParser(description='Resolve a ticker universe from CSV with optional filters')
    ap.add_argument('--csv', required=True, help='Universe CSV path')
    ap.add_argument('--col', default='ticker', help='Ticker column name (default: ticker)')
    ap.add_argument('--min_price', type=float, default=None)
    ap.add_argument('--min_adv', type=float, default=None, help='Minimum average daily volume (shares) if ADV column exists')
    ap.add_argument('--adv_col', default='adv_20', help='ADV column name if present (default: adv_20)')
    ap.add_argument('--out', default='-')
    args = ap.parse_args()

    p = Path(args.csv)
    if not p.exists():
        raise SystemExit(f"CSV not found: {p}")
    df = pd.read_csv(p)
    if args.col not in df.columns:
        raise SystemExit(f"Ticker column '{args.col}' not found in CSV")
    tickers = df.copy()
    # Optional filters
    if args.min_price is not None and 'price' in tickers.columns:
        tickers = tickers[tickers['price'] >= args.min_price]
    if args.min_adv is not None and args.adv_col in tickers.columns:
        tickers = tickers[tickers[args.adv_col] >= args.min_adv]

    syms = [str(x).upper() for x in tickers[args.col].dropna().tolist() if str(x).strip()]
    if args.out == '-' or not args.out:
        print(','.join(syms))
    else:
        Path(args.out).write_text('\n'.join(syms))
        print(f"Wrote {len(syms)} tickers to {args.out}")


if __name__ == '__main__':
    main()

