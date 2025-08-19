from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import datetime, time as dtime
import pytz
from ...data.sources.polygon import get_polygon_option_quotes
from .iv_skew import implied_vol_newton


class IVSmileWings(Indicator):
    NAME = "iv_smile_wings"
    CATEGORY = "options_volatility"
    SUBCATEGORY = "smile"

    def __init__(self, underlying: str = 'SPY', sampling: str = '10:00-11:00', wing_points: int = 10, strike_band: float = 20.0):
        self.underlying = underlying
        self.sampling = sampling
        self.wing_points = int(wing_points)
        self.strike_band = float(strike_band)

    def _parse_win(self, w: str):
        a,b = w.split('-'); ah,am=[int(x) for x in a.split(':')]; bh,bm=[int(x) for x in b.split(':')]
        return dtime(ah,am), dtime(bh,bm)

    def _atm_iv(self, day: pd.Timestamp, anchor: float, start_t, end_t) -> float:
        return self._wing_iv(day, anchor, 0, start_t, end_t)

    def _wing_iv(self, day: pd.Timestamp, anchor: float, offset: int, start_t, end_t) -> float:
        ET = pytz.timezone('US/Eastern')
        lo = int(np.floor(anchor - self.strike_band)); hi = int(np.ceil(anchor + self.strike_band))
        K_target = float(anchor + offset)
        best_iv, best_dist = float('nan'), float('inf')
        # approx T to 16:00 from mid-window
        mid_h=(start_t.hour+end_t.hour)//2; mid_m=(start_t.minute+end_t.minute)//2
        sample_dt = ET.localize(datetime(day.year, day.month, day.day, mid_h, mid_m))
        expiry_dt = ET.localize(datetime(day.year, day.month, day.day, 16, 0))
        T = max((expiry_dt - sample_dt).total_seconds(), 0.0)/(365.0*24*3600.0)
        for K in range(lo, hi+1):
            for side in ['call','put']:
                try:
                    q = get_polygon_option_quotes(self.underlying, day.date(), float(K), side, day.date(), day.date())
                    if q is None or q.empty: continue
                    q['ts'] = pd.to_datetime(q['timestamp']); q['et'] = q['ts'].dt.tz_convert(ET)
                    m = (q['et'].dt.time >= start_t) & (q['et'].dt.time <= end_t)
                    qq = q[m]
                    if qq.empty: continue
                    mid = ((pd.to_numeric(qq['bid'], errors='coerce') + pd.to_numeric(qq['ask'], errors='coerce'))/2.0).replace([np.inf,-np.inf], np.nan).dropna()
                    if mid.empty or T<=0: continue
                    price = float(mid.median())
                    iv = implied_vol_newton(S=float(anchor), K=float(K), T=T, price=price, option_type=side)
                    if not np.isfinite(iv) or iv<=0: continue
                    dist = abs(float(K) - K_target)
                    if dist < best_dist:
                        best_dist, best_iv = dist, float(iv)
                except Exception:
                    continue
        return best_iv

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['iv_smile_wings'] = float('nan'); return out
        ET = pytz.timezone('US/Eastern')
        dts = pd.to_datetime(df['date']).dt.tz_convert(ET)
        days = sorted(set(dts.dt.date))
        # anchor from prev_close/close
        if 'spy_prev_close' in df.columns:
            anchors = pd.to_numeric(df['spy_prev_close'], errors='coerce')
        else:
            anchors = pd.to_numeric(df.get('close', pd.Series(0.0, index=df.index)), errors='coerce')
        anchors_rounded = np.round(anchors).astype(float)
        start_t, end_t = self._parse_win(self.sampling)
        smile_map = {}
        for d in days:
            try:
                anchor_val = float(np.nanmean(anchors_rounded[dts.dt.date == d]))
                iv_atm = self._atm_iv(ET.localize(datetime(d.year, d.month, d.day)), anchor_val, start_t, end_t)
                iv_left = self._wing_iv(ET.localize(datetime(d.year, d.month, d.day)), anchor_val, -self.wing_points, start_t, end_t)
                iv_right = self._wing_iv(ET.localize(datetime(d.year, d.month, d.day)), anchor_val, self.wing_points, start_t, end_t)
                if np.isfinite(iv_atm) and np.isfinite(iv_left) and np.isfinite(iv_right):
                    smile_map[d] = float(((iv_left + iv_right)/2.0) - iv_atm)
                else:
                    smile_map[d] = np.nan
            except Exception:
                smile_map[d] = np.nan
        out['iv_smile_wings'] = dts.dt.date.map(lambda x: smile_map.get(x, np.nan)).astype(float)
        return out

