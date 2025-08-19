from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import date, datetime
from pathlib import Path
import pytz, os
from ...data.sources.polygon import get_polygon_option_chain_snapshot


def _today_et() -> date:
    return datetime.now(pytz.timezone('US/Eastern')).date()


def _atm_iv_series(df: pd.DataFrame, underlying: str) -> pd.Series:
    # Build per-date ATM IV by nearest strike to anchor (prev_close if present else close)
    if 'date' not in df.columns:
        return pd.Series([], dtype=float)
    dts = pd.to_datetime(df['date']).dt.date
    if 'spy_prev_close' in df.columns:
        anchors = pd.to_numeric(df['spy_prev_close'], errors='coerce')
    else:
        anchors = pd.to_numeric(df.get('close', pd.Series(0.0, index=df.index)), errors='coerce')
    anchors_rounded = np.round(anchors).astype(float)
    uniq = sorted(set(dts))
    # load cache
    cache_dir = Path('data_cache') / 'atm_iv'
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{underlying}_atm_iv.csv"
    iv_cache = {}
    if cache_path.exists():
        try:
            cdf = pd.read_csv(cache_path)
            cdf['date'] = pd.to_datetime(cdf['date']).dt.date
            iv_cache = {r['date']: float(r['iv']) for _, r in cdf.iterrows()}
        except Exception:
            iv_cache = {}
    iv_map = dict(iv_cache)
    for d in uniq:
        if d in iv_map and np.isfinite(iv_map[d]):
            continue
        try:
            snap = get_polygon_option_chain_snapshot(underlying, d)
            if snap is None or snap.empty:
                iv_map[d] = np.nan; continue
            anchor_val = float(np.nanmean(anchors_rounded[dts == d]))
            s2 = snap.dropna(subset=['implied_volatility']).copy()
            s2['dist'] = (pd.to_numeric(s2['strike'], errors='coerce') - anchor_val).abs()
            s2 = s2.sort_values('dist')
            if s2.empty:
                iv_map[d] = np.nan
            else:
                iv_map[d] = float(pd.to_numeric(s2.iloc[0]['implied_volatility'], errors='coerce'))
        except Exception:
            iv_map[d] = np.nan
    # write cache for historical days (never today)
    try:
        today = _today_et()
        rows = [{'date': d, 'iv': iv_map.get(d, np.nan)} for d in uniq if d != today]
        cdf = pd.DataFrame(rows).dropna()
        if not cdf.empty:
            cdf = cdf.drop_duplicates(subset=['date']).sort_values('date')
            cdf.to_csv(cache_path, index=False)
    except Exception:
        pass
    return pd.Series({d: iv_map.get(d, np.nan) for d in uniq})


class ATMIVRank52W(Indicator):
    NAME = "iv_rank_52w"
    CATEGORY = "options_volatility"
    SUBCATEGORY = "iv_rank"

    def __init__(self, underlying: str = 'SPY', window_days: int = 252):
        self.underlying = underlying
        self.window_days = int(window_days)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        dts = pd.to_datetime(df['date']).dt.date if 'date' in df.columns else None
        if dts is None:
            out['iv_rank_52w'] = float('nan'); return out
        iv_series = _atm_iv_series(df, self.underlying)
        iv_series = iv_series.sort_index()
        # compute rolling rank as (iv - min) / (max - min)
        iv = iv_series.reindex(sorted(set(dts)))
        roll_max = iv.rolling(self.window_days, min_periods=10).max()
        roll_min = iv.rolling(self.window_days, min_periods=10).min()
        rank = (iv - roll_min) / (roll_max - roll_min + 1e-12)
        rank_map = rank.to_dict()
        out['iv_rank_52w'] = [float(rank_map.get(d, np.nan)) for d in dts]
        return out


class ATMIVPercentile52W(Indicator):
    NAME = "iv_percentile_52w"
    CATEGORY = "options_volatility"
    SUBCATEGORY = "iv_rank"

    def __init__(self, underlying: str = 'SPY', window_days: int = 252):
        self.underlying = underlying
        self.window_days = int(window_days)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        dts = pd.to_datetime(df['date']).dt.date if 'date' in df.columns else None
        if dts is None:
            out['iv_percentile_52w'] = float('nan'); return out
        iv_series = _atm_iv_series(df, self.underlying)
        iv_series = iv_series.sort_index()
        iv = iv_series.reindex(sorted(set(dts)))
        # rolling percentile: fraction of past values <= current
        pct = []
        vals = []
        for i, (dt, v) in enumerate(iv.items()):
            window = iv.iloc[max(0, i-self.window_days+1):i+1].dropna()
            if window.empty or not np.isfinite(v):
                pct.append(np.nan)
            else:
                pct.append(float((window <= v).sum()) / float(len(window)))
        pct_map = {d: p for d, p in zip(iv.index, pct)}
        out['iv_percentile_52w'] = [float(pct_map.get(d, np.nan)) for d in dts]
        return out


class ATMIVZScore(Indicator):
    NAME = "atm_iv_zscore"
    CATEGORY = "options_volatility"
    SUBCATEGORY = "iv_zscore"

    def __init__(self, underlying: str = 'SPY', window_days: int = 20):
        self.underlying = underlying
        self.window_days = int(window_days)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        dts = pd.to_datetime(df['date']).dt.date if 'date' in df.columns else None
        if dts is None:
            out['atm_iv_zscore'] = float('nan'); return out
        iv_series = _atm_iv_series(df, self.underlying)
        iv_series = iv_series.sort_index()
        iv = iv_series.reindex(sorted(set(dts)))
        mean = iv.rolling(self.window_days, min_periods=5).mean()
        std = iv.rolling(self.window_days, min_periods=5).std()
        z = (iv - mean) / (std + 1e-12)
        z_map = z.to_dict()
        out['atm_iv_zscore'] = [float(z_map.get(d, np.nan)) for d in dts]
        return out
