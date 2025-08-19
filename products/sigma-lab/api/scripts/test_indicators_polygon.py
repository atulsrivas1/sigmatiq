#!/usr/bin/env python3
"""
Test all implemented indicators against live Polygon data.

Usage:
  python scripts/test_indicators_polygon.py \
    --ticker SPY --start 2024-07-01 --end 2024-07-05 --expiry 2024-07-05 \
    --out reports/test_indicators

Requirements:
  - POLYGON_API_KEY must be set in environment (or .env at repo root)
  - Network access to Polygon API

Outputs:
  - Writes a summary JSON with per-indicator stats under --out
  - Writes optional CSVs with computed columns for manual inspection
"""

from __future__ import annotations
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, date

import pandas as pd

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from sigma_core.data.sources.polygon import (
    get_polygon_hourly_bars,
    get_polygon_daily_bars,
    get_polygon_option_chain_snapshot,
)
from sigma_core.indicators.builtins.momentum import Momentum
from sigma_core.indicators.builtins.volatility import Volatility
from sigma_core.indicators.builtins.roll_std import RollingStd
from sigma_core.indicators.builtins.rsi import RSI
from sigma_core.indicators.builtins.ema import EMA
from sigma_core.indicators.builtins.ema_slope import EmaSlope
from sigma_core.indicators.builtins.dist_to_ema import DistToEma
from sigma_core.indicators.builtins.ret import Ret
from sigma_core.indicators.builtins.sold_flow_ratio import SoldFlowRatio
from sigma_core.indicators.builtins.iv_realized_spread import IVRealizedSpread
from sigma_core.indicators.builtins.daily_rsi import DailyRSI
from sigma_core.indicators.builtins.daily_ema import DailyEMA
from sigma_core.indicators.builtins.daily_ret import DailyRet
from sigma_core.indicators.builtins.daily_dist_to_ema import DailyDistToEma
from sigma_core.indicators.builtins.momentum_score import MomentumScoreTotal


def _summary(col: pd.Series) -> dict:
    col = pd.to_numeric(col, errors='coerce')
    return {
        "count": int(col.notna().sum()),
        "min": float(col.min()) if col.notna().any() else None,
        "max": float(col.max()) if col.notna().any() else None,
        "mean": float(col.mean()) if col.notna().any() else None,
        "std": float(col.std()) if col.notna().any() else None,
        "nonzero_pct": float((col.fillna(0.0) != 0.0).mean()) if len(col) else 0.0,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticker", default="SPY")
    ap.add_argument("--start", required=True, help="YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="YYYY-MM-DD")
    ap.add_argument("--expiry", required=False, help="YYYY-MM-DD (options expiry for IV snapshot; default=end)")
    ap.add_argument("--out", default="reports/test_indicators")
    ap.add_argument("--write_csvs", action="store_true")
    args = ap.parse_args()

    polygon_key = os.getenv("POLYGON_API_KEY") or os.getenv("ZE_POLYGON_API_KEY")
    if not polygon_key:
        raise SystemExit("POLYGON_API_KEY not set; please export it or put in .env")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1) Fetch underlying hourly + daily bars
    hourly = get_polygon_hourly_bars(args.ticker, args.start, args.end)
    if hourly.empty:
        raise SystemExit("Failed to fetch hourly bars from Polygon; check dates and entitlements.")
    hourly["hour_et"] = pd.to_datetime(hourly["date"], utc=True).dt.tz_convert("US/Eastern").dt.hour
    hourly["date"] = pd.to_datetime(hourly["date"])  # keep tz-aware
    hourly_df = hourly[["date", "hour_et", "close"]].copy()

    daily = get_polygon_daily_bars(args.ticker, args.start, args.end)
    if daily.empty:
        raise SystemExit("Failed to fetch daily bars from Polygon; check dates and entitlements.")

    # 2) Compute intraday indicators on hourly_df
    intraday = hourly_df.copy()
    ind_defs = [
        ("close_mom_1", Momentum(column="close", window=1)),
        ("close_mom_3", Momentum(column="close", window=3)),
        ("close_vol_3", Volatility(column="close", window=3)),
        ("roll_std_20", RollingStd(column="close", window=20)),
        ("rsi_14", RSI(column="close", period=14)),
        ("ema_10", EMA(column="close", window=10)),
        ("ema_20", EMA(column="close", window=20)),
        ("ema10_slope1h", EmaSlope(column="close", window=10, period=1)),
        ("dist_ema10_norm", DistToEma(column="close", window=10, normalize="price")),
        ("ret_1h", Ret(column="close", window=1)),
        ("ret_3h", Ret(column="close", window=3)),
    ]
    intraday_summaries = {}
    for label, ind in ind_defs:
        got = ind.calculate(intraday)
        intraday = pd.concat([intraday, got], axis=1)
        col = got.columns[-1]
        intraday_summaries[col] = _summary(intraday[col])

    # 3) Daily indicators mapped to hourly timeline (shifted one day)
    daily_defs = [
        ("rsi_14_d", DailyRSI(underlying=args.ticker, period=14)),
        ("ema_20_d", DailyEMA(underlying=args.ticker, window=20)),
        ("ret_1d_d", DailyRet(underlying=args.ticker, window=1)),
        ("ret_5d_d", DailyRet(underlying=args.ticker, window=5)),
        ("dist_ema20_d", DailyDistToEma(underlying=args.ticker, window=20)),
    ]
    daily_summaries = {}
    daily_df = intraday.copy()
    for label, ind in daily_defs:
        got = ind.calculate(daily_df)
        daily_df = pd.concat([daily_df, got], axis=1)
        col = got.columns[-1]
        daily_summaries[col] = _summary(daily_df[col])

    # 4) Momentum score composite
    score = MomentumScoreTotal().calculate(daily_df)
    daily_df = pd.concat([daily_df, score], axis=1)
    score_summary = _summary(daily_df[score.columns[-1]])

    # 5) IV/Greeks snapshot + IV-RV spread
    expiry = args.expiry or args.end
    try:
        exp_dt = datetime.strptime(expiry, "%Y-%m-%d").date()
    except Exception:
        raise SystemExit("--expiry must be YYYY-MM-DD")
    snapshot = get_polygon_option_chain_snapshot(args.ticker, exp_dt)
    snapshot_ok = (not snapshot.empty) and ("implied_volatility" in snapshot.columns)
    iv_summ = {}
    if snapshot_ok:
        iv_summ = {
            "rows": int(len(snapshot)),
            "has_greeks": bool(set(["delta","gamma","theta","vega"]) <= set(snapshot.columns)),
            "iv_nonnull": int(snapshot["implied_volatility"].notna().sum()),
        }
    ivrs = IVRealizedSpread(underlying=args.ticker, window=20, freq='hour').calculate(daily_df)
    ivrs_summary = _summary(ivrs[ivrs.columns[-1]])

    # Optional: sold_flow_ratio requires flow totals; this test focuses on indicators not dependent on heavy options flow aggregation.

    # Write outputs
    if args.write_csvs:
        hourly.to_csv(out_dir / "underlying_hourly.csv", index=False)
        daily.to_csv(out_dir / "underlying_daily.csv", index=False)
        intraday.to_csv(out_dir / "intraday_indicators.csv", index=False)
        daily_df.to_csv(out_dir / "daily_indicators.csv", index=False)
        if snapshot_ok:
            snapshot.to_csv(out_dir / "options_snapshot.csv", index=False)
        ivrs.to_csv(out_dir / "iv_realized_spread.csv", index=False)

    summary = {
        "ticker": args.ticker,
        "start": args.start,
        "end": args.end,
        "expiry": expiry,
        "intraday": intraday_summaries,
        "daily": daily_summaries,
        "momentum_score_total": score_summary,
        "snapshot": iv_summ,
        "iv_realized_spread_20": ivrs_summary,
    }
    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

