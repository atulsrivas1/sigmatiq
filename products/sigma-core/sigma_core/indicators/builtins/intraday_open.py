from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import timedelta
from ...data.sources.polygon import get_polygon_daily_bars, get_polygon_agg_bars
import pytz


class OpenGapZ(Indicator):
    NAME = "open_gap_z"
    CATEGORY = "intraday"
    SUBCATEGORY = "open"

    def __init__(self, ticker: str = 'SPY', atr_period: int = 14, norm: str = 'atr'):
        self.ticker = ticker
        self.atr_period = int(atr_period)
        self.norm = norm

    def _daily_atr(self, start: str, end: str) -> pd.DataFrame:
        d = get_polygon_daily_bars(self.ticker, start, end)
        if d.empty:
            return d
        d = d.copy()
        prev_close = d['close'].shift(1)
        tr = pd.concat([
            d['high'] - d['low'],
            (d['high'] - prev_close).abs(),
            (d['low'] - prev_close).abs()
        ], axis=1).max(axis=1)
        d['atr'] = tr.rolling(self.atr_period).mean()
        d['d'] = pd.to_datetime(d['date']).dt.tz_convert('US/Eastern').dt.date
        return d[['d','open','close','atr']]

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['open_gap_z'] = float('nan')
            return out
        d0 = pd.to_datetime(df['date']).dt.date.min()
        d1 = pd.to_datetime(df['date']).dt.date.max()
        start = (pd.Timestamp(d0) - pd.Timedelta(days=40)).strftime('%Y-%m-%d')
        end = pd.Timestamp(d1).strftime('%Y-%m-%d')
        daily = self._daily_atr(start, end)
        if daily.empty:
            out['open_gap_z'] = float('nan')
            return out
        # Map prev close and ATR per session day
        daily = daily.sort_values('d')
        daily['prev_close'] = daily['close'].shift(1)
        m_atr = daily.set_index('d')['atr'].to_dict()
        m_prev = daily.set_index('d')['prev_close'].to_dict()
        m_open = daily.set_index('d')['open'].to_dict()
        dates = pd.to_datetime(df['date']).dt.tz_convert('US/Eastern').dt.date
        open_px = dates.map(lambda d: m_open.get(d, np.nan)).astype(float)
        prev_close = dates.map(lambda d: m_prev.get(d, np.nan)).astype(float)
        gap = open_px - prev_close
        if str(self.norm).lower() == 'stddev5m':
            # approximate using 5m returns std over prior day
            m5 = get_polygon_agg_bars(self.ticker, 5, 'minute', (pd.Timestamp(d0)-pd.Timedelta(days=5)).strftime('%Y-%m-%d'), pd.Timestamp(d1).strftime('%Y-%m-%d'))
            if not m5.empty:
                m5 = m5.copy()
                ET = pytz.timezone('US/Eastern')
                m5['ts_et'] = pd.to_datetime(m5['date']).dt.tz_convert(ET)
                m5['d'] = m5['ts_et'].dt.date
                # prior day stddev up to close
                m5 = m5.sort_values('ts_et')
                m5['ret'] = pd.to_numeric(m5['close'], errors='coerce').astype(float).pct_change()
                std_map = m5.groupby('d')['ret'].apply(lambda s: float(s.rolling(20, min_periods=5).std().iloc[-1]) if len(s.dropna())>=5 else np.nan).to_dict()
                denom = dates.map(lambda d: std_map.get(pd.Timestamp(d)-pd.Timedelta(days=1), np.nan)).astype(float)
            else:
                denom = dates.map(lambda d: m_atr.get(d, np.nan)).astype(float)
        else:
            denom = dates.map(lambda d: m_atr.get(d, np.nan)).astype(float)
        out['open_gap_z'] = gap / denom.replace(0.0, np.nan)
        return out


class FirstNMinRangeZ(Indicator):
    NAME = "first15m_range_z"
    CATEGORY = "intraday"
    SUBCATEGORY = "open"

    def __init__(self, ticker: str = 'SPY', window_mins: int = 15, norm: str = 'atr'):
        self.ticker = ticker
        self.window_mins = int(window_mins)
        self.norm = norm

    def _daily_atr_map(self, start: str, end: str) -> dict:
        d = get_polygon_daily_bars(self.ticker, start, end)
        if d.empty:
            return {}
        prev_close = d['close'].shift(1)
        tr = pd.concat([
            d['high'] - d['low'],
            (d['high'] - prev_close).abs(),
            (d['low'] - prev_close).abs()
        ], axis=1).max(axis=1)
        atr = tr.rolling(14).mean()
        dd = pd.to_datetime(d['date']).dt.tz_convert('US/Eastern').dt.date
        return dict(zip(dd, atr))

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"first15m_range_z_{self.window_mins}"] = float('nan')
            return out
        d0 = pd.to_datetime(df['date']).dt.date.min()
        d1 = pd.to_datetime(df['date']).dt.date.max()
        start = pd.Timestamp(d0).strftime('%Y-%m-%d')
        end = pd.Timestamp(d1).strftime('%Y-%m-%d')
        # Fetch 5m bars to compute first N minutes range
        m5 = get_polygon_agg_bars(self.ticker, 5, 'minute', start, end)
        if m5.empty:
            out[f"first15m_range_z_{self.window_mins}"] = float('nan')
            return out
        m5 = m5.copy()
        ET = pytz.timezone('US/Eastern')
        m5['ts_et'] = pd.to_datetime(m5['date']).dt.tz_convert(ET)
        m5['d'] = m5['ts_et'].dt.date
        m5['t'] = m5['ts_et'].dt.time
        # Window: 09:30 to 09:30+window_mins
        start_h, start_m = 9, 30
        start_t = pd.Timestamp(0).replace(hour=start_h, minute=start_m).time()
        end_dt = (pd.Timestamp(0).replace(hour=start_h, minute=start_m) + pd.Timedelta(minutes=self.window_mins)).time()
        mask = (m5['t'] >= start_t) & (m5['t'] < end_dt)
        seg = m5[mask]
        if seg.empty:
            out[f"first15m_range_z_{self.window_mins}"] = float('nan')
            return out
        rng = seg.groupby('d').apply(lambda g: float(pd.to_numeric(g['high'], errors='coerce').max() - pd.to_numeric(g['low'], errors='coerce').min()))
        if str(self.norm).lower() == 'stddev5m':
            # Use prior day 5m std of returns as denom
            m5_all = get_polygon_agg_bars(self.ticker, 5, 'minute', (pd.Timestamp(d0)-pd.Timedelta(days=5)).strftime('%Y-%m-%d'), end)
            std_map = {}
            if not m5_all.empty:
                m = m5_all.copy(); ET = pytz.timezone('US/Eastern')
                m['ts_et'] = pd.to_datetime(m['date']).dt.tz_convert(ET)
                m['d'] = m['ts_et'].dt.date
                m = m.sort_values('ts_et')
                m['ret'] = pd.to_numeric(m['close'], errors='coerce').astype(float).pct_change()
                std_map = m.groupby('d')['ret'].apply(lambda s: float(s.rolling(20, min_periods=5).std().iloc[-1]) if len(s.dropna())>=5 else np.nan).to_dict()
            atr_map = std_map
        else:
            atr_map = self._daily_atr_map(start, end)
        # Map to df rows by date
        dates = pd.to_datetime(df['date']).dt.tz_convert('US/Eastern').dt.date
        denom = dates.map(lambda d: atr_map.get(d, np.nan)).astype(float)
        range_map = rng.to_dict()
        range_val = dates.map(lambda d: range_map.get(d, np.nan)).astype(float)
        out[f"first15m_range_z_{self.window_mins}"] = range_val / denom.replace(0.0, np.nan)
        return out
