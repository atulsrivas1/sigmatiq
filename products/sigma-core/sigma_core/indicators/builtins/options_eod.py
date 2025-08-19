from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import datetime, time as dtime
import pytz
from ...data.sources.polygon import get_polygon_option_quotes
from .iv_skew import implied_vol_newton


class ATMIVEOD(Indicator):
    NAME = "atm_iv_eod"
    CATEGORY = "options_volatility"
    SUBCATEGORY = "eod"

    def __init__(self, underlying: str = 'SPY', sampling: str = '15:55-16:00', strike_band: float = 5.0):
        self.underlying = underlying
        self.sampling = sampling
        self.strike_band = float(strike_band)

    def _parse_win(self, w: str):
        a,b = w.split('-'); ah,am = [int(x) for x in a.split(':')]; bh,bm = [int(x) for x in b.split(':')]
        return dtime(ah,am), dtime(bh,bm)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['atm_iv_eod'] = float('nan'); return out
        ET = pytz.timezone('US/Eastern')
        dts = pd.to_datetime(df['date']).dt.tz_convert(ET)
        days = sorted(set(dts.dt.date))
        start_t, end_t = self._parse_win(self.sampling)
        iv_map = {}
        # Anchor from prev_close or close
        if 'spy_prev_close' in df.columns:
            anchors = pd.to_numeric(df['spy_prev_close'], errors='coerce')
        else:
            anchors = pd.to_numeric(df.get('close', pd.Series(0.0, index=df.index)), errors='coerce')
        anchors_rounded = np.round(anchors).astype(float)
        for d in days:
            try:
                anchor_val = float(np.nanmean(anchors_rounded[dts.dt.date == d]))
                lo = int(np.floor(anchor_val - self.strike_band)); hi = int(np.ceil(anchor_val + self.strike_band))
                best_iv, best_dist = float('nan'), float('inf')
                # T to 16:00 ET same day from mid of window
                mid_h = (start_t.hour + end_t.hour)//2; mid_m = (start_t.minute + end_t.minute)//2
                sample_dt = ET.localize(datetime(d.year, d.month, d.day, mid_h, mid_m))
                expiry_dt = ET.localize(datetime(d.year, d.month, d.day, 16, 0))
                T = max((expiry_dt - sample_dt).total_seconds(), 0.0)/(365.0*24*3600.0)
                for K in range(lo, hi+1):
                    for side in ['call','put']:
                        q = get_polygon_option_quotes(self.underlying, d, float(K), side, d, d)
                        if q is None or q.empty: continue
                        q['ts'] = pd.to_datetime(q['timestamp']); q['et'] = q['ts'].dt.tz_convert(ET)
                        m = (q['et'].dt.time >= start_t) & (q['et'].dt.time <= end_t)
                        qq = q[m]
                        if qq.empty: continue
                        mid = ((pd.to_numeric(qq['bid'], errors='coerce') + pd.to_numeric(qq['ask'], errors='coerce'))/2.0).replace([np.inf,-np.inf], np.nan).dropna()
                        if mid.empty or T<=0: continue
                        price = float(mid.median())
                        iv = implied_vol_newton(S=float(anchor_val), K=float(K), T=T, price=price, option_type=side)
                        if not np.isfinite(iv) or iv<=0: continue
                        dist = abs(float(K) - float(anchor_val))
                        if dist < best_dist:
                            best_dist, best_iv = dist, float(iv)
                iv_map[d] = best_iv
            except Exception:
                iv_map[d] = np.nan
        out['atm_iv_eod'] = dts.dt.date.map(lambda x: iv_map.get(x, np.nan)).astype(float)
        return out


class PCREOD(Indicator):
    NAME = "pcr_eod"
    CATEGORY = "options_flow"
    SUBCATEGORY = "eod"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        # Approximate EOD PCR using totals across the session from flow columns
        out = pd.DataFrame(index=df.index)
        if not ({'date'}).issubset(df.columns):
            out['pcr_eod'] = float('nan'); return out
        # Try totals: calls_sold_total/puts_sold_total; fallback sum of d-columns
        def row_pcr(g: pd.DataFrame):
            if 'calls_sold_total' in g.columns and 'puts_sold_total' in g.columns:
                c = float(pd.to_numeric(g['calls_sold_total'], errors='coerce').sum())
                p = float(pd.to_numeric(g['puts_sold_total'], errors='coerce').sum())
            else:
                calls = [c for c in g.columns if str(c).startswith('calls_sold_d')]
                puts = [c for c in g.columns if str(c).startswith('puts_sold_d')]
                c = float(pd.to_numeric(g[calls], errors='coerce').sum().sum()) if calls else 0.0
                p = float(pd.to_numeric(g[puts], errors='coerce').sum().sum()) if puts else 0.0
            return (p + 1e-9)/(c + 1e-9)
        dates = pd.to_datetime(df['date']).dt.date
        g = df.copy(); g['d'] = dates
        pcr_map = g.groupby('d').apply(row_pcr).to_dict()
        out['pcr_eod'] = dates.map(lambda d: float(pcr_map.get(d, np.nan))).astype(float)
        return out


class DIVEOD(Indicator):
    NAME = "div_eod"
    CATEGORY = "options_volatility"
    SUBCATEGORY = "eod"

    def __init__(self, underlying: str = 'SPY'):
        self.underlying = underlying

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Day-over-day change in ATM IV at EOD (approx). Uses ATMIVEOD internally.
        div_eod = iv_eod_today - iv_eod_yesterday
        """
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['div_eod'] = float('nan'); return out
        iv_eod = ATMIVEOD(self.underlying).calculate(df)['atm_iv_eod']
        # Map by date to compute delta per day, then expand back to rows
        dates = pd.to_datetime(df['date']).dt.date
        per_day = pd.Series(index=sorted(set(dates)), dtype=float)
        tmp = pd.DataFrame({'d': dates, 'iv': iv_eod}).dropna()
        first = tmp.groupby('d')['iv'].first()
        diff = first.diff().to_dict()
        out['div_eod'] = dates.map(lambda d: diff.get(d, np.nan)).astype(float)
        return out
