from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import datetime, time as dtime
import pytz
from ...data.sources.polygon import get_polygon_option_quotes
from .iv_skew import implied_vol_newton
from ...data.sources.polygon import get_polygon_daily_bars


class ATMIVOpenDelta(Indicator):
    NAME = "atm_iv_open_delta"
    CATEGORY = "options_volatility"
    SUBCATEGORY = "iv_open"

    def __init__(self, underlying: str = 'SPY', open_sampling: str = '09:30-09:35', close_sampling_prev: str = '15:55-16:00', strike_band: float = 5.0):
        self.underlying = underlying
        self.open_sampling = open_sampling
        self.close_sampling_prev = close_sampling_prev
        self.strike_band = float(strike_band)

    def _parse_win(self, w: str):
        a,b = w.split('-')
        ah,am = [int(x) for x in a.split(':')]
        bh,bm = [int(x) for x in b.split(':')]
        return dtime(ah,am), dtime(bh,bm)

    def _prev_close_anchor(self, d: pd.Timestamp) -> float:
        # fetch daily bars around d-2..d to get prev close
        start = (d - pd.Timedelta(days=5)).strftime('%Y-%m-%d')
        end = d.strftime('%Y-%m-%d')
        daily = get_polygon_daily_bars(self.underlying, start, end)
        if daily.empty:
            return float('nan')
        daily = daily.copy()
        daily['dd'] = pd.to_datetime(daily['date']).dt.tz_convert('US/Eastern').dt.date
        dd = sorted(daily['dd'].unique())
        if len(dd) < 2:
            return float('nan')
        # prev close is close of last day before d
        try:
            d_date = d.tz_convert('US/Eastern').date()
        except Exception:
            d_date = d.date()
        try:
            idx = dd.index(d_date)
        except Exception:
            idx = len(dd)-1
        if idx == 0:
            return float('nan')
        prev_day = dd[idx-1]
        row = daily[daily['dd']==prev_day].tail(1)
        return float(pd.to_numeric(row['close'], errors='coerce').iloc[-1])

    def _atm_iv_quotes(self, day: pd.Timestamp, expiry_date: pd.Timestamp, win: str, anchor: float) -> float:
        ET = pytz.timezone('US/Eastern')
        start_t, end_t = self._parse_win(win)
        lo = int(np.floor(anchor - self.strike_band))
        hi = int(np.ceil(anchor + self.strike_band))
        best_iv, best_dist = float('nan'), float('inf')
        # Mid time for T
        mid_h = (start_t.hour + end_t.hour)//2
        mid_m = (start_t.minute + end_t.minute)//2
        sample_dt = ET.localize(datetime(day.year, day.month, day.day, mid_h, mid_m))
        expiry_dt = ET.localize(datetime(expiry_date.year, expiry_date.month, expiry_date.day, 16, 0))
        T = max((expiry_dt - sample_dt).total_seconds(), 0.0) / (365.0*24*3600.0)
        if T <= 0:
            return float('nan')
        for K in range(lo, hi+1):
            for side in ['call','put']:
                try:
                    q = get_polygon_option_quotes(self.underlying, expiry_date.date(), float(K), side, day.date(), day.date())
                    if q is None or q.empty:
                        continue
                    q['ts'] = pd.to_datetime(q['timestamp'])
                    q['et'] = q['ts'].dt.tz_convert(ET)
                    m = (q['et'].dt.time >= start_t) & (q['et'].dt.time <= end_t)
                    qq = q[m]
                    if qq.empty:
                        continue
                    mid = ((pd.to_numeric(qq['bid'], errors='coerce') + pd.to_numeric(qq['ask'], errors='coerce'))/2.0).replace([np.inf,-np.inf], np.nan).dropna()
                    if mid.empty:
                        continue
                    price = float(mid.median())
                    iv = implied_vol_newton(S=float(anchor), K=float(K), T=T, price=price, option_type=side)
                    if not np.isfinite(iv) or iv <= 0:
                        continue
                    dist = abs(float(K) - float(anchor))
                    if dist < best_dist:
                        best_dist, best_iv = dist, float(iv)
                except Exception:
                    continue
        return best_iv

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['atm_iv_open_delta'] = float('nan')
            return out
        ET = pytz.timezone('US/Eastern')
        dts = pd.to_datetime(df['date']).dt.tz_convert(ET)
        unique_days = sorted(set(dts.dt.date))
        ivdelta = {}
        for d in unique_days:
            day_ts = ET.localize(datetime(d.year, d.month, d.day))
            # same-day expiry assumed for 0DTE
            expiry = day_ts
            anchor_prev = self._prev_close_anchor(day_ts)
            if not np.isfinite(anchor_prev):
                ivdelta[d] = np.nan
                continue
            iv_prev = self._atm_iv_quotes(day_ts - pd.Timedelta(days=1), expiry, self.close_sampling_prev, anchor_prev)
            anchor_open = anchor_prev  # approximate using prev close; could update using first prints if available
            iv_open = self._atm_iv_quotes(day_ts, expiry, self.open_sampling, anchor_open)
            if not np.isfinite(iv_prev) or not np.isfinite(iv_open):
                ivdelta[d] = np.nan
            else:
                ivdelta[d] = float(iv_open - iv_prev)
        out['atm_iv_open_delta'] = dts.dt.date.map(lambda x: ivdelta.get(x, np.nan)).astype(float)
        return out

