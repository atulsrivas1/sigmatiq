import os
import time
import logging
from datetime import date, datetime, timedelta
from typing import List
from pathlib import Path

import pandas as pd
import numpy as np
import pytz
from dotenv import load_dotenv

from .sources.polygon import (
    get_polygon_options_aggs,
    get_polygon_option_trades,
    get_polygon_option_quotes,
    get_polygon_hourly_bars,
    get_polygon_oi_snapshot_today,
)
from .data_loader import get_multi_timeframe_data
from ..features.builder import FeatureBuilder
from ..features.loader import load_indicator_set
from ..labels.hourly_direction import label_next_hour_direction
from ..indicators.builtins.momentum import Momentum
from ..indicators.builtins.volatility import Volatility


ET = pytz.timezone("US/Eastern")
UTC = pytz.utc
logger = logging.getLogger(__name__)


def _daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def _ensure_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure a 'date' column exists by resetting index if needed."""
    if 'date' in df.columns:
        return df
    df2 = df.reset_index()
    if 'date' not in df2.columns and 'index' in df2.columns:
        df2 = df2.rename(columns={'index': 'date'})
    if 'date' not in df2.columns:
        # Try common alternatives
        for alt in ('timestamp', 'ts', 'time'):
            if alt in df2.columns:
                df2 = df2.rename(columns={alt: 'date'})
                break
    return df2


def fetch_0dte_flow(start_date: date, end_date: date, *, ticker: str = "SPY", distance_max: int = 7) -> pd.DataFrame:
    """
    Build raw 0DTE flow at per-strike, per-hour granularity:
    Returns columns: date, price_level, spy_prev_close, hour_et, calls_sold, puts_sold
    """
    # Prefer daily bars for prev_close anchor; fallback to previous day's last hourly close
    daily_dict = get_multi_timeframe_data(
        ticker,
        (start_date - timedelta(days=5)).strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d"),
        ["day"],
    )
    daily = daily_dict.get("day", pd.DataFrame())
    prev_close_map: dict[date, float] = {}
    if not daily.empty:
        ddf = _ensure_date_column(daily)
        ddf['date'] = pd.to_datetime(ddf['date']).dt.date
        ddf = ddf.set_index('date')
        ddf['prev_close'] = ddf['close'].shift(1)
        prev_close_map = ddf['prev_close'].dropna().to_dict()
        logger.info("Daily prev_close map size: %s", len(prev_close_map))
    else:
        # Fallback: use last hourly close from prior day
        logger.warning("No day data found for %s. Falling back to previous day's last hourly close for prev_close anchor…", ticker)
        hourly_dict = get_multi_timeframe_data(
            ticker,
            (start_date - timedelta(days=5)).strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            ["hour"],
        )
        hourly_df = hourly_dict.get("hour", pd.DataFrame())
        if hourly_df.empty:
            raise RuntimeError("Failed to fetch SPY hourly bars from Polygon for prev_close fallback")
        hdf = _ensure_date_column(hourly_df)
        # Polygon timestamps are UTC in milliseconds; treat parsed datetimes as UTC
        hdf['date'] = pd.to_datetime(hdf['date'], utc=True)
        hdf['hour_et'] = hdf['date'].dt.tz_convert(ET).dt.hour
        hdf['session_date'] = hdf['date'].dt.tz_convert(ET).dt.date
        # last hourly close per session date
        last_per_day = (
            hdf.sort_values(['session_date', 'date'])
               .groupby('session_date')
               .tail(1)
               .set_index('session_date')['close']
        )
        # prev_close for date d is last close of d-1
        dates_sorted = sorted(last_per_day.index)
        for i in range(1, len(dates_sorted)):
            prev_day = dates_sorted[i-1]
            curr_day = dates_sorted[i]
            prev_close_map[curr_day] = float(last_per_day.loc[prev_day])
        logger.info("Hourly-based prev_close map size: %s", len(prev_close_map))

    # If some dates in the requested range are missing in prev_close_map (common for 'today' intraday
    # because daily bars are not yet available), backfill using hourly data for the whole window.
    missing_dates = [d for d in _daterange(start_date, end_date) if d not in prev_close_map]
    if missing_dates:
        try:
            hourly_dict2 = get_multi_timeframe_data(
                ticker,
                (start_date - timedelta(days=6)).strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                ["hour"],
            )
            hourly_df2 = hourly_dict2.get("hour", pd.DataFrame())
            if not hourly_df2.empty:
                h2 = _ensure_date_column(hourly_df2)
                h2['date'] = pd.to_datetime(h2['date'], utc=True)
                h2['session_date'] = h2['date'].dt.tz_convert(ET).dt.date
                # last hourly close per session
                last_per_day2 = (
                    h2.sort_values(['session_date', 'date'])
                      .groupby('session_date')
                      .tail(1)
                      .set_index('session_date')['close']
                )
                dates_sorted2 = sorted(last_per_day2.index)
                hourly_prev: dict[date, float] = {}
                for i in range(1, len(dates_sorted2)):
                    prev_day = dates_sorted2[i-1]
                    curr_day = dates_sorted2[i]
                    hourly_prev[curr_day] = float(last_per_day2.loc[prev_day])
                filled = 0
                for d in missing_dates:
                    if d in hourly_prev:
                        prev_close_map[d] = hourly_prev[d]
                        filled += 1
                if filled:
                    logger.info("Filled %s missing prev_close anchors from hourly data (range %s..%s)", filled, start_date, end_date)
        except Exception as e:
            # Non-fatal: keep prev_close_map as-is and proceed
            logger.warning("Failed to backfill prev_close from hourly for missing dates: %s", e)

    records: List[dict] = []

    for d in _daterange(start_date, end_date):
        if d not in prev_close_map:
            # If still missing, skip this day (likely holiday or data gap)
            continue
        prev_close = prev_close_map.get(d)
        if prev_close is None:
            continue
        anchor = int(np.round(float(prev_close)))
        # Use configurable +/- distance_max around anchor
        price_levels = [anchor + k for k in range(-abs(distance_max), abs(distance_max) + 1)]

        for lvl in price_levels:
            for opt_type in ["call", "put"]:
                df_min = get_polygon_options_aggs(
                    underlying_ticker=ticker,
                    expiration_date=d,
                    strike_price=float(lvl),
                    option_type=opt_type,
                    from_date=d,
                    to_date=d,
                )
                if df_min.empty:
                    continue

                # Ensure timezone-aware in ET
                ts = pd.to_datetime(df_min["timestamp"], utc=True).dt.tz_convert(ET)
                hours = ts.dt.hour
                minutes = ts.dt.minute
                mins_total = hours * 60 + minutes
                market_open = 9 * 60 + 30
                market_close = 16 * 60
                mask = (mins_total >= market_open) & (mins_total < market_close)
                df_mkt = df_min.loc[mask].copy()
                if df_mkt.empty:
                    continue
                df_mkt["hour_et"] = pd.to_datetime(df_mkt["timestamp"], utc=True).dt.tz_convert(ET).dt.hour
                # Compute minute-level premium ~ vwap * volume * 100 (contract multiplier)
                px = df_mkt.get("vwap")
                if px is None or px.isna().all():
                    px = df_mkt.get("close")
                df_mkt["_premium"] = df_mkt["volume"].astype(float) * px.astype(float).fillna(0.0) * 100.0
                grp = df_mkt.groupby("hour_et").agg(volume=("volume","sum"), premium=("_premium","sum"))

                for hour_et, row in grp.iterrows():
                    vol = float(row.get("volume", 0.0) or 0.0)
                    prem = float(row.get("premium", 0.0) or 0.0)
                    records.append({
                        "date": d,
                        "price_level": lvl,
                        "spy_prev_close": float(prev_close),
                        "hour_et": int(hour_et),
                        "calls_sold": float(vol) if opt_type == "call" else 0.0,
                        "puts_sold": float(vol) if opt_type == "put" else 0.0,
                        "calls_premium": float(prem) if opt_type == "call" else 0.0,
                        "puts_premium": float(prem) if opt_type == "put" else 0.0,
                    })

    if not records:
        return pd.DataFrame(columns=["date", "price_level", "spy_prev_close", "hour_et", "calls_sold", "puts_sold"]) 

    raw = pd.DataFrame(records)
    # Volumes may be split across call vs put rows; combine them
    raw = (
        raw.groupby(["date", "price_level", "spy_prev_close", "hour_et"], as_index=False)
           .agg({"calls_sold": "sum", "puts_sold": "sum", "calls_premium":"sum", "puts_premium":"sum"})
    )
    logger.info("Collected raw 0DTE flow records: %s", len(raw))
    return raw


def fetch_0dte_trades_premium_inferred(
    start_date: date,
    end_date: date,
    *,
    ticker: str = "SPY",
    distance_max: int = 7,
    start_hour_et: int = 9,
    end_hour_et: int = 14,
) -> pd.DataFrame:
    """Compute dealer-sold premium inferred from trades classified via NBBO quotes.
    Returns per-strike, per-hour records with calls_premium_inf_sold, puts_premium_inf_sold.
    """
    records: List[dict] = []
    for d in _daterange(start_date, end_date):
        # Approx anchor from daily/hourly as in fetch_0dte_flow
        daily_dict = get_multi_timeframe_data(ticker, (d - timedelta(days=5)).strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d"), ["day"])
        prev_close = None
        if daily_dict.get('day') is not None and not daily_dict['day'].empty:
            dd = _ensure_date_column(daily_dict['day']).copy()
            dd['date'] = pd.to_datetime(dd['date']).dt.date
            dd = dd.set_index('date')
            if d in dd.index:
                try:
                    prev_close = float(dd.loc[d]['close'])
                except Exception:
                    prev_close = None
        if prev_close is None:
            # fallback: use previous day’s last hourly close
            hourly_dict = get_multi_timeframe_data(ticker, (d - timedelta(days=5)).strftime("%Y-%m-%d"), d.strftime("%Y-%m-%d"), ["hour"])
            hdf = hourly_dict.get('hour', pd.DataFrame())
            if not hdf.empty:
                hdf2 = _ensure_date_column(hdf)
                hdf2['date'] = pd.to_datetime(hdf2['date'], utc=True).dt.tz_convert(ET).dt.date
                last_prev = (
                    hdf2.sort_values(['date'])
                        .groupby('date')
                        .tail(1)
                        .set_index('date')['close']
                )
                prev_days = sorted(last_prev.index)
                for i in range(1, len(prev_days)):
                    if prev_days[i] == d:
                        prev_close = float(last_prev.loc[prev_days[i-1]])
                        break
        if prev_close is None:
            continue
        anchor = int(np.round(prev_close))
        price_levels = [anchor + k for k in range(-abs(distance_max), abs(distance_max) + 1)]
        for lvl in price_levels:
            for opt_type in ["call", "put"]:
                trades = get_polygon_option_trades(ticker, d, float(lvl), opt_type, d, d)
                quotes = get_polygon_option_quotes(ticker, d, float(lvl), opt_type, d, d)
                if trades.empty:
                    continue
                # Align nearest prior quote per trade
                try:
                    tdf = trades.copy()
                    qdf = quotes.copy() if not quotes.empty else pd.DataFrame(columns=['timestamp','bid','ask'])
                    tdf['ts'] = pd.to_datetime(tdf['timestamp'])
                    qdf['ts'] = pd.to_datetime(qdf.get('timestamp', pd.Series([], dtype='datetime64[ns]')))
                    tdf = tdf.sort_values('ts')
                    qdf = qdf.sort_values('ts')
                    merged = pd.merge_asof(tdf, qdf[['ts','bid','ask']], on='ts', direction='backward', tolerance=pd.Timedelta('5min'))
                    # Classify buyer-initiated if price >= ask - tiny eps; seller-initiated if price <= bid + eps
                    eps = 1e-6
                    price = merged['price'].astype(float)
                    bid = merged.get('bid', pd.Series(np.nan))
                    ask = merged.get('ask', pd.Series(np.nan))
                    buyer = price >= (ask.astype(float).fillna(np.inf) - 1e-6)
                    # If ask missing, fallback: price above midpoint by >0 may be buyer, else seller
                    mid = (bid.astype(float).fillna(0.0) + ask.astype(float).fillna(0.0)) / 2.0
                    buyer = buyer | (price > (mid + 1e-6))
                    # Dealers are on the opposite side: buyer-initiated => dealers sold
                    prem = price * merged['size'].astype(float) * 100.0
                    merged['hour_et'] = merged['ts'].dt.tz_convert(ET).dt.hour
                    # Filter to hour window if provided
                    try:
                        sh = int(start_hour_et)
                        eh = int(end_hour_et)
                        if sh <= eh:
                            merged = merged[(merged['hour_et'] >= sh) & (merged['hour_et'] <= eh)]
                    except Exception:
                        pass
                    grp = merged.groupby('hour_et').apply(lambda g: float(prem[g.index][buyer[g.index]].sum()))
                    for hour_et, prem_sold in grp.items():
                        records.append({
                            'date': d,
                            'price_level': lvl,
                            'spy_prev_close': float(prev_close),
                            'hour_et': int(hour_et),
                            'calls_premium_inf_sold': float(prem_sold) if opt_type=='call' else 0.0,
                            'puts_premium_inf_sold': float(prem_sold) if opt_type=='put' else 0.0,
                        })
                except Exception:
                    continue
    if not records:
        return pd.DataFrame(columns=['date','price_level','spy_prev_close','hour_et','calls_premium_inf_sold','puts_premium_inf_sold'])
    df = pd.DataFrame(records)
    df = (
        df.groupby(['date','price_level','spy_prev_close','hour_et'], as_index=False)
          .agg({ 'calls_premium_inf_sold':'sum', 'puts_premium_inf_sold':'sum' })
    )
    return df


def fetch_hourly_ticker(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    data = get_multi_timeframe_data(ticker, start_date, end_date, ["hour"]).get("hour", pd.DataFrame())
    if data.empty:
        raise RuntimeError(f"Failed to fetch {ticker} hourly bars from Polygon")
    df = _ensure_date_column(data)
    if 'ts_utc' not in df.columns:
        df = df.rename(columns={"date": "ts_utc"})
    # Make tz-aware UTC then convert to ET
    df["ts_utc"] = pd.to_datetime(df["ts_utc"], utc=True)
    df["ts_et"] = df["ts_utc"].dt.tz_convert(ET)
    df["date"] = df["ts_et"].dt.date
    df["hour_et"] = df["ts_et"].dt.hour
    for c in ["open","high","low","close","volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors='coerce').astype(float)
    cols = [c for c in ["date","hour_et","open","high","low","close","volume"] if c in df.columns]
    return df[cols]


def build_matrix(
    start_date: str,
    end_date: str,
    out_csv: str,
    make_real_labels: bool = False,
    k_sigma: float = 0.3,
    fixed_bp: float | None = None,
    *,
    distance_max: int = 7,
    dump_raw: bool = False,
    raw_out: str | None = None,
    ticker: str = "SPY",
    features_config: dict | None = None,
    indicator_set_path: str | None = None,
    label_config: dict | None = None,
) -> str:
    sd = datetime.strptime(start_date, "%Y-%m-%d").date()
    ed = datetime.strptime(end_date, "%Y-%m-%d").date()

    logger.info("Fetching 0DTE flow for %s %s -> %s using Polygon keys from .env", ticker, sd, ed)
    raw = fetch_0dte_flow(sd, ed, ticker=ticker, distance_max=distance_max)
    if raw.empty:
        raise RuntimeError(f"No 0DTE flow data collected for {ticker} from {sd} to {ed}. Halting matrix build. Check API key and data availability.")
    if dump_raw:
        raw_path = raw_out or out_csv.replace(".csv", "_raw.csv")
        raw.to_csv(raw_path, index=False)
        logger.info("Saved raw 0DTE flow to %s", raw_path)

    # Load indicator set if provided
    indicator_set = None
    if indicator_set_path:
        try:
            indicator_set = load_indicator_set(indicator_set_path)
        except Exception as e:
            logger.warning("failed to load indicator set from %s: %s", indicator_set_path, e)

    fb = FeatureBuilder(distance_max=distance_max, indicator_set=indicator_set)
    feats = fb.add_base_features(raw)
    # Optional ATM and dealer orientation early (flow-based)
    if features_config:
        if (features_config.get("flow", {}).get("atm", False)):
            feats = fb.add_atm_features(feats)
        if (features_config.get("dealer", {}).get("mm_profit_dir_simple", False)):
            feats = fb.add_dealer_orientation(feats)
    # Optional: trade-level inferred premium (heavy). Only if requested via features_config
    if features_config and (features_config.get('dealer', {}).get('sold_premium_inferred', False)):
        try:
            win = (features_config.get('dealer', {}) or {}).get('sold_premium_inferred_window', {})
            sh = int(win.get('start', 9))
            eh = int(win.get('end', 14))
            inferred = fetch_0dte_trades_premium_inferred(sd, ed, ticker=ticker, distance_max=distance_max, start_hour_et=sh, end_hour_et=eh)
            if not inferred.empty:
                feats = pd.merge(feats, inferred, on=['date','price_level','spy_prev_close','hour_et'], how='left')
        except Exception as e:
            logger.warning("failed to compute trade-level premium inferred: %s", e)

    # Merge hourly underlying ticker close for label and price-derived features
    hourly = fetch_hourly_ticker(ticker, start_date, end_date)
    m = pd.merge(feats, hourly, on=["date", "hour_et"], how="left")

    # Add indicator features (from pack-defined indicator set)
    m = fb.add_indicator_features(m)

    # Aggregate to one row per (date, hour_et): sum per-distance/ATM features across price levels
    try:
        sum_cols = [c for c in m.columns if str(c).startswith("calls_sold_d") or str(c).startswith("puts_sold_d") or str(c).startswith("calls_premium_d") or str(c).startswith("puts_premium_d") or str(c).startswith("calls_premium_inf_sold_d") or str(c).startswith("puts_premium_inf_sold_d")]
        sum_cols += [c for c in ["atm_calls","atm_puts"] if c in m.columns]
        keep_first = [c for c in ["spy_prev_close","close","day_of_week"] if c in m.columns]
        grp = m.groupby(["date","hour_et"], as_index=False)
        m_sum = grp[sum_cols].sum() if sum_cols else grp.size().rename(columns={"size":"rows"})
        if sum_cols:
            m = pd.merge(m_sum, grp[keep_first].first(), on=["date","hour_et"], how="left")
        # Recompute totals and ratios post-aggregation
        calls_d = [c for c in m.columns if str(c).startswith("calls_sold_d")]
        puts_d = [c for c in m.columns if str(c).startswith("puts_sold_d")]
        if calls_d:
            m["calls_sold_total"] = m[calls_d].sum(axis=1)
        if puts_d:
            m["puts_sold_total"] = m[puts_d].sum(axis=1)
        if "calls_sold_total" in m.columns and "puts_sold_total" in m.columns:
            m["pc_ratio"] = (m["puts_sold_total"].fillna(0.0) + 1e-6) / (m["calls_sold_total"].fillna(0.0) + 1e-6)
            m["imbalance"] = m["calls_sold_total"].fillna(0.0) - m["puts_sold_total"].fillna(0.0)
        # Premium totals and dealer premium imbalance (normalized)
        calls_p = [c for c in m.columns if str(c).startswith("calls_premium_d")]
        puts_p = [c for c in m.columns if str(c).startswith("puts_premium_d")]
        if calls_p:
            m["calls_premium_total"] = m[calls_p].sum(axis=1)
        if puts_p:
            m["puts_premium_total"] = m[puts_p].sum(axis=1)
        if "calls_premium_total" in m.columns and "puts_premium_total" in m.columns:
            num = m["puts_premium_total"].fillna(0.0) - m["calls_premium_total"].fillna(0.0)
            den = m["puts_premium_total"].fillna(0.0) + m["calls_premium_total"].fillna(0.0) + 1e-6
            m["dealer_sold_premium_imbalance"] = (num / den).astype(float)
        # Inferred (trade-level) dealer sold premium imbalance
        calls_inf = [c for c in m.columns if str(c).startswith("calls_premium_inf_sold_d")]
        puts_inf = [c for c in m.columns if str(c).startswith("puts_premium_inf_sold_d")]
        if calls_inf:
            m["calls_premium_inf_total"] = m[calls_inf].sum(axis=1)
        if puts_inf:
            m["puts_premium_inf_total"] = m[puts_inf].sum(axis=1)
        if "calls_premium_inf_total" in m.columns and "puts_premium_inf_total" in m.columns:
            num2 = m["puts_premium_inf_total"].fillna(0.0) - m["calls_premium_inf_total"].fillna(0.0)
            den2 = m["puts_premium_inf_total"].fillna(0.0) + m["calls_premium_inf_total"].fillna(0.0) + 1e-6
            m["dealer_sold_premium_inferred"] = (num2 / den2).astype(float)
    except Exception as e:
        logger.warning("aggregation step failed; continuing with partial features: %s", e)
    # Dealer-driven divergence score & orientation (recompute with aggregated totals if available)
    if indicator_set and (indicator_set.name == 'zerosigma_v1'): # This is a hack, will be removed
        try:
            sign_slope = np.sign(m.get("ret_prev_hour", pd.Series(0.0))).astype(float)
            # If not previously set, derive mm_profit_dir_simple from aggregated totals
            if "mm_profit_dir_simple" not in m.columns and {"calls_sold_total","puts_sold_total"}.issubset(m.columns):
                m["mm_profit_dir_simple"] = np.sign(m["puts_sold_total"].fillna(0.0) - m["calls_sold_total"].fillna(0.0)).astype(float)
            sign_mm = np.sign(m.get("mm_profit_dir_simple", pd.Series(0.0))).astype(float)
            m["divergence_score"] = -1.0 * sign_slope * sign_mm
        except Exception:
            m["divergence_score"] = 0.0
    # OI-based features (expiry = session date)
    if indicator_set and (indicator_set.name == 'zerosigma_v1'): # This is a hack, will be removed
        try:
            win = 10
            # Use unique strikes present in raw window around anchor
            strikes = sorted(raw["price_level"].unique().tolist())
            if strikes:
                oi = get_polygon_oi_snapshot_today(ticker, sd, strikes)
                if not oi.empty:
                    oi["oi_total"] = oi.get("oi_total", oi.get("oi_calls", 0)) + oi.get("oi_puts", 0)
                    # Max pain proxy: strike with max total OI
                    max_pain_strike = float(oi.sort_values("oi_total", ascending=False).head(1)["strike"].values[0])
                    m["distance_to_max_pain"] = np.abs(np.round(m["spy_prev_close"].astype(float)) - max_pain_strike)
                    # Concentration: Herfindahl over a window around anchor
                    anchor = int(np.round(float(m.get("spy_prev_close", pd.Series([0])).iloc[0] or 0)))
                    window = [s for s in strikes if abs(s - anchor) <= win]
                    sub = oi[oi["strike"].isin(window)].copy()
                    w = sub["oi_total"].astype(float)
                    total = float(w.sum())
                    if total > 0:
                        hhi = float(((w/total) ** 2).sum())
                    else:
                        hhi = 0.0
                    m["oi_concentration"] = hhi
                else:
                    m["distance_to_max_pain"] = np.nan
                    m["oi_concentration"] = np.nan
            else:
                m["distance_to_max_pain"] = np.nan
                m["oi_concentration"] = np.nan
        except Exception:
            m["distance_to_max_pain"] = np.nan
            m["oi_concentration"] = np.nan
    m = m.sort_values(["date", "hour_et"]).reset_index(drop=True)

    if make_real_labels:
        # Optional pack-specific labels
        if label_config and isinstance(label_config, dict):
            kind = str(label_config.get('kind') or label_config.get('type') or '').lower()
            try:
                if kind == 'headfake_reversal' or kind == 'headfake' or kind == 'reversal_after_window':
                    from ..labels.zerosigma import label_headfake_reversal
                    params = label_config.get('params') or {}
                    m = label_headfake_reversal(m, **params)
                elif kind == 'pin_drift' or kind == 'pin':
                    from ..labels.zerosigma import label_pin_drift
                    params = label_config.get('params') or {}
                    m = label_pin_drift(m, **params)
                else:
                    m = label_next_hour_direction(m, k_sigma=k_sigma, fixed_bp=fixed_bp)
            except Exception:
                m = label_next_hour_direction(m, k_sigma=k_sigma, fixed_bp=fixed_bp)
        else:
            m = label_next_hour_direction(m, k_sigma=k_sigma, fixed_bp=fixed_bp)

    Path(out_csv).parent.mkdir(parents=True, exist_ok=True)
    m.to_csv(out_csv, index=False)
    logger.info("Saved training matrix to %s (%s rows)", out_csv, len(m))
    return out_csv
