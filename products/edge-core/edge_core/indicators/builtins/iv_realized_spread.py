from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import date, datetime, time as dtime, timedelta
from ...data.sources.polygon import get_polygon_option_chain_snapshot, get_polygon_option_quotes
from .iv_skew import implied_vol_newton
import pytz

class IVRealizedSpread(Indicator):
    CATEGORY = "options_volatility"
    SUBCATEGORY = "iv_rv_spread"
    """IV - Realized Volatility spread.

    Params:
      underlying: str = 'SPY'  # underlying ticker
      window: int = 20         # rolling window for realized vol
      freq: str = 'hour'       # 'hour' or 'day' for annualization
      contract_type: str | None = None  # 'call'|'put' or None for both
      iv_source: str = 'snapshot'  # 'snapshot' (default) or 'quotes'
      quote_window: str = '10:00-11:00'  # ET window for quotes-based IV
      strike_band: float = 5.0  # search +/- band around anchor (dollars)

    Output:
      iv_realized_spread_{window}
    """
    def __init__(self, underlying: str = 'SPY', window: int = 20, freq: str = 'hour', contract_type: str | None = None,
                 iv_source: str = 'snapshot', quote_window: str = '10:00-11:00', strike_band: float = 5.0):
        self.underlying = underlying
        self.window = int(window)
        self.freq = freq
        self.contract_type = contract_type
        self.iv_source = iv_source
        self.quote_window = quote_window
        self.strike_band = float(strike_band)

    def _annualization_factor(self) -> float:
        if self.freq == 'day':
            return float(np.sqrt(252.0))
        # approx trading hours per year for intraday hourly bars
        return float(np.sqrt(252.0 * 6.5))

    def _atm_iv_by_date_snapshot(self, df: pd.DataFrame) -> pd.Series:
        # Expect 'date' and 'spy_prev_close' or 'close' columns
        if 'date' not in df.columns:
            return pd.Series(0.0, index=df.index)
        # Normalize dates to date type (drop tz, time)
        dts = pd.to_datetime(df['date']).dt.date
        # Anchor: prefer spy_prev_close if present, else round close
        if 'spy_prev_close' in df.columns:
            anchors = pd.to_numeric(df['spy_prev_close'], errors='coerce')
        else:
            anchors = pd.to_numeric(df.get('close', pd.Series(0.0, index=df.index)), errors='coerce')
        anchors_rounded = np.round(anchors).astype(float)

        iv_map: dict[date, float] = {}
        for dt in sorted(set(dts)):
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, dt)
                if snap.empty:
                    continue
                # nearest strike to anchor of that date (use first row’s anchor for the date)
                anchor_val = float(np.nanmean(anchors_rounded[dts == dt]))
                snap2 = snap.copy()
                if self.contract_type in ('call','put'):
                    snap2 = snap2[snap2['contract_type'] == self.contract_type]
                snap2['dist'] = np.abs(snap2['strike'] - anchor_val)
                snap2 = snap2.sort_values(['dist']).dropna(subset=['implied_volatility'])
                if len(snap2) == 0:
                    continue
                iv = float(snap2.iloc[0]['implied_volatility'])
                iv_map[dt] = iv
            except Exception:
                continue
        # Map each row to its date’s iv (fallback 0.0)
        iv_series = dts.map(lambda x: iv_map.get(x, 0.0)).astype(float)
        return pd.Series(iv_series, index=df.index)

    def _parse_window(self, w: str):
        try:
            a, b = str(w).split('-')
            ah, am = [int(x) for x in a.split(':')]
            bh, bm = [int(x) for x in b.split(':')]
            return dtime(ah, am), dtime(bh, bm)
        except Exception:
            return dtime(10,0), dtime(11,0)

    def _atm_iv_by_date_quotes(self, df: pd.DataFrame) -> pd.Series:
        if 'date' not in df.columns:
            return pd.Series(float('nan'), index=df.index)
        dts = pd.to_datetime(df['date']).dt.date
        # Anchor: prefer spy_prev_close if present, else round close
        if 'spy_prev_close' in df.columns:
            anchors = pd.to_numeric(df['spy_prev_close'], errors='coerce')
        else:
            anchors = pd.to_numeric(df.get('close', pd.Series(0.0, index=df.index)), errors='coerce')
        anchors_rounded = np.round(anchors).astype(float)

        start_t, end_t = self._parse_window(self.quote_window)
        ET = pytz.timezone('US/Eastern')
        iv_map: dict[date, float] = {}

        for dt in sorted(set(dts)):
            try:
                anchor_val = float(np.nanmean(anchors_rounded[dts == dt]))
                if not np.isfinite(anchor_val):
                    continue
                # strike candidates within +/- band, $1 steps
                lo = int(np.floor(anchor_val - self.strike_band))
                hi = int(np.ceil(anchor_val + self.strike_band))
                strikes = list(range(lo, hi + 1))

                # choose a representative timestamp in window for T calculation (midpoint of window)
                sample_dt = datetime.combine(dt, dtime(
                    (start_t.hour + end_t.hour)//2,
                    (start_t.minute + end_t.minute)//2
                ))
                sample_dt = ET.localize(sample_dt)
                # assume expiry at 16:00 ET same day
                expiry_dt = ET.localize(datetime.combine(dt, dtime(16,0)))
                T = max((expiry_dt - sample_dt).total_seconds(), 0.0) / (365.0*24*3600.0)
                if T <= 0:
                    continue

                best_iv = float('nan')
                best_dist = float('inf')
                for side in ([self.contract_type] if self.contract_type in ('call','put') else ['call','put']):
                    for K in strikes:
                        q = get_polygon_option_quotes(self.underlying, dt, float(K), side, dt, dt)
                        if q is None or q.empty:
                            continue
                        q['ts'] = pd.to_datetime(q.get('timestamp'))
                        # filter to ET window
                        q['ts_et'] = q['ts'].dt.tz_convert(ET)
                        mask = (q['ts_et'].dt.time >= start_t) & (q['ts_et'].dt.time <= end_t)
                        qq = q.loc[mask].copy()
                        if qq.empty:
                            # fallback to whole day median
                            qq = q.copy()
                        # midquote
                        try:
                            mid = (qq['bid'].astype(float) + qq['ask'].astype(float)) / 2.0
                            mid = mid.replace([np.inf, -np.inf], np.nan).dropna()
                            if mid.empty:
                                continue
                            price = float(mid.median())
                        except Exception:
                            continue
                        # Invert Black-Scholes
                        iv = implied_vol_newton(S=anchor_val, K=float(K), T=T, price=price, option_type=side)
                        if not np.isfinite(iv) or iv <= 0:
                            continue
                        dist = abs(float(K) - anchor_val)
                        if dist < best_dist:
                            best_dist = dist
                            best_iv = float(iv)
                if np.isfinite(best_iv):
                    iv_map[dt] = best_iv
            except Exception:
                continue

        iv_series = dts.map(lambda x: iv_map.get(x, float('nan'))).astype(float)
        return pd.Series(iv_series, index=df.index)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'close' not in df.columns or 'date' not in df.columns:
            out[f"iv_realized_spread_{self.window}"] = float('nan')
            return out
        # Realized volatility over window
        ret = pd.to_numeric(df['close'], errors='coerce').astype(float).pct_change().fillna(0.0)
        rv = ret.rolling(self.window).std().fillna(0.0) * self._annualization_factor()
        # Implied vol (ATM) per date
        if str(self.iv_source).lower() == 'quotes':
            iv = self._atm_iv_by_date_quotes(df)
            # if quotes failed entirely, try snapshot as final fallback
            if iv.isna().all():
                iv = self._atm_iv_by_date_snapshot(df)
        else:
            iv = self._atm_iv_by_date_snapshot(df)
        out[f"iv_realized_spread_{self.window}"] = (iv - rv).astype(float)
        return out
