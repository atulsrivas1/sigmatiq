from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime
from ...data.sources.polygon import get_polygon_option_chain_snapshot
from ...data.sources.polygon import get_polygon_option_quotes

import math

def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def _bs_price(S, K, T, sigma, r=0.0, q=0.0, option_type='call'):
    if T <= 0 or sigma <= 0:
        return max(0.0, (S - K) if option_type == 'call' else (K - S))
    d1 = (math.log((S+1e-12)/(K+1e-12)) + (r - q + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)
    Nd1 = _norm_cdf(d1)
    Nd2 = _norm_cdf(d2)
    if option_type == 'call':
        return S*math.exp(-q*T)*Nd1 - K*math.exp(-r*T)*Nd2
    else:
        return K*math.exp(-r*T)*(1.0-Nd2) - S*math.exp(-q*T)*(1.0-Nd1)

def implied_vol_newton(S, K, T, price, r=0.0, q=0.0, option_type='call', tol=1e-4, max_iter=50):
    if price <= 0 or S <= 0 or K <= 0 or T <= 0:
        return float('nan')
    sigma = 0.3
    for _ in range(max_iter):
        if sigma <= 1e-8:
            sigma = 1e-4
        # Vega
        d1 = (math.log((S+1e-12)/(K+1e-12)) + (r - q + 0.5*sigma*sigma)*T) / (sigma*math.sqrt(T))
        vega = (S*math.exp(-q*T) * (1.0/math.sqrt(2*math.pi)) * math.exp(-0.5*d1*d1) * math.sqrt(T))
        if vega < 1e-8:
            break
        diff = _bs_price(S, K, T, sigma, r, q, option_type) - price
        sigma_new = sigma - diff/vega
        if abs(sigma_new - sigma) < tol:
            return max(sigma_new, 0.0)
        sigma = sigma_new
    return float('nan')


class IVSkew25Delta(Indicator):
    CATEGORY = "options_volatility"
    SUBCATEGORY = "iv_skew"

    def __init__(self, underlying: str = 'SPY', iv_source: str = 'snapshot', quote_window: str = '10:00-11:00', strike_band: float = 5.0):
        self.underlying = underlying
        self.iv_source = iv_source
        self.quote_window = quote_window
        self.strike_band = float(strike_band)

    def _parse_window(self, w: str):
        try:
            a, b = str(w).split('-')
            ah, am = [int(x) for x in a.split(':')]
            bh, bm = [int(x) for x in b.split(':')]
            return (ah, am), (bh, bm)
        except Exception:
            return (10,0), (11,0)

    def _atm_iv_from_quotes(self, dt, anchor_price: float, side: str) -> float:
        from ...data.sources.polygon import get_polygon_option_quotes
        import pytz
        ET = pytz.timezone('US/Eastern')
        (sh, sm), (eh, em) = self._parse_window(self.quote_window)
        lo = int(np.floor(anchor_price - self.strike_band))
        hi = int(np.ceil(anchor_price + self.strike_band))
        strikes = list(range(lo, hi+1))
        sample_dt = ET.localize(datetime(dt.year, dt.month, dt.day, (sh+eh)//2, (sm+em)//2))
        expiry_dt = ET.localize(datetime(dt.year, dt.month, dt.day, 16, 0))
        T = max((expiry_dt - sample_dt).total_seconds(), 0.0) / (365.0*24*3600.0)
        best_iv, best_dist = float('nan'), float('inf')
        for K in strikes:
            try:
                q = get_polygon_option_quotes(self.underlying, dt, float(K), side, dt, dt)
                if q is None or q.empty:
                    continue
                q['ts'] = pd.to_datetime(q.get('timestamp'))
                q['ts_et'] = q['ts'].dt.tz_convert(ET)
                qq = q[(q['ts_et'].dt.hour*60 + q['ts_et'].dt.minute >= sh*60+sm) & (q['ts_et'].dt.hour*60 + q['ts_et'].dt.minute <= eh*60+em)].copy()
                if qq.empty:
                    qq = q.copy()
                mid = ((qq['bid'].astype(float) + qq['ask'].astype(float)) / 2.0).replace([np.inf,-np.inf], np.nan).dropna()
                if mid.empty or T <= 0:
                    continue
                price = float(mid.median())
                iv = implied_vol_newton(S=float(anchor_price), K=float(K), T=T, price=price, option_type=side)
                if not np.isfinite(iv) or iv <= 0:
                    continue
                dist = abs(float(K) - float(anchor_price))
                if dist < best_dist:
                    best_dist, best_iv = dist, float(iv)
            except Exception:
                continue
        return best_iv

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['iv_skew_25d'] = 0.0
            return out
        dts = pd.to_datetime(df['date']).dt.date
        if 'spy_prev_close' in df.columns:
            anchor_series = pd.to_numeric(df['spy_prev_close'], errors='coerce')
        else:
            anchor_series = pd.to_numeric(df.get('close', pd.Series(0.0, index=df.index)), errors='coerce')
        values = []
        for i, dt in enumerate(dts):
            try:
                if str(self.iv_source).lower() == 'quotes':
                    anchor = float(anchor_series.iloc[i]) if i < len(anchor_series) else float('nan')
                    if not np.isfinite(anchor):
                        values.append(float('nan'))
                        continue
                    ivc = self._atm_iv_from_quotes(dt, anchor, 'call')
                    ivp = self._atm_iv_from_quotes(dt, anchor, 'put')
                    if np.isfinite(ivc) and np.isfinite(ivp):
                        values.append(float(ivc - ivp))
                    else:
                        values.append(float('nan'))
                else:
                    snap = get_polygon_option_chain_snapshot(self.underlying, dt)
                    if snap is None or snap.empty:
                        values.append(float('nan'))
                        continue
                    # nearest to +0.25 for calls and -0.25 for puts
                    calls = snap[snap['contract_type'] == 'call'].copy()
                    puts = snap[snap['contract_type'] == 'put'].copy()
                    for sub in (calls, puts):
                        if 'delta' not in sub.columns and 'greeks.delta' in sub.columns:
                            sub['delta'] = sub['greeks.delta']
                    ivc = np.nan
                    ivp = np.nan
                    if 'delta' in calls.columns and not calls.empty:
                        calls['d2'] = (calls['delta'].astype(float) - 0.25).abs()
                        csel = calls.dropna(subset=['implied_volatility','d2']).sort_values('d2').head(1)
                        if not csel.empty:
                            ivc = float(csel.iloc[0]['implied_volatility'])
                    if 'delta' in puts.columns and not puts.empty:
                        puts['d2'] = (puts['delta'].astype(float) + 0.25).abs()
                        psel = puts.dropna(subset=['implied_volatility','d2']).sort_values('d2').head(1)
                        if not psel.empty:
                            ivp = float(psel.iloc[0]['implied_volatility'])
                    if np.isnan(ivc) or np.isnan(ivp):
                        values.append(float('nan'))
                    else:
                        values.append(ivc - ivp)
            except Exception:
                values.append(float('nan'))
        out['iv_skew_25d'] = pd.Series(values, index=df.index).astype(float)
        return out


class IVTermSlope(Indicator):
    CATEGORY = "options_volatility"
    SUBCATEGORY = "term_structure"

    def __init__(self, underlying: str = 'SPY', days_fwd: int = 30, iv_source: str = 'snapshot', quote_window: str = '10:00-11:00', strike_band: float = 5.0):
        self.underlying = underlying
        self.days_fwd = int(days_fwd)
        self.iv_source = iv_source
        self.quote_window = quote_window
        self.strike_band = float(strike_band)

    def _atm_iv(self, snap, anchor_price: float) -> float:
        try:
            s = snap.copy()
            s = s.dropna(subset=['implied_volatility'])
            s['dist'] = (s['strike'].astype(float) - float(anchor_price))
            s['dist_abs'] = s['dist'].abs()
            sel = s.sort_values('dist_abs').head(1)
            if not sel.empty:
                return float(sel.iloc[0]['implied_volatility'])
        except Exception:
            pass
        return float('nan')

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {'date'}
        if not required.issubset(df.columns):
            out['iv_term_slope'] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        # anchor from prev_close if present else close
        anchor_series = None
        if 'spy_prev_close' in df.columns:
            anchor_series = pd.to_numeric(df['spy_prev_close'], errors='coerce')
        else:
            anchor_series = pd.to_numeric(df.get('close', pd.Series(0.0, index=df.index)), errors='coerce')
        values = []
        for idx, dt in enumerate(dts):
            try:
                anchor = float(anchor_series.iloc[idx] if idx < len(anchor_series) else np.nan)
                if np.isnan(anchor):
                    values.append(float('nan'))
                    continue
                if str(self.iv_source).lower() == 'quotes':
                    # Use quotes on dt for both expiries
                    # Reuse IVSkew25Delta helper to estimate ATM IV via quotes
                    ivc = IVSkew25Delta(self.underlying, iv_source='quotes', quote_window=self.quote_window, strike_band=self.strike_band)
                    iv_near = ivc._atm_iv_from_quotes(dt, anchor, 'call')  # call or put; ATM should be similar
                    far_dt = dt + timedelta(days=self.days_fwd)
                    # For far expiry, reuse quotes fetch with far_dt expiry but sample on dt window
                    # We need a small helper here using the same logic but passing expiry far_dt
                    # Quick inline: loop strikes with get_polygon_option_quotes for far_dt
                    import pytz
                    ET = pytz.timezone('US/Eastern')
                    (sh, sm), (eh, em) = ivc._parse_window(self.quote_window)
                    sample_dt = ET.localize(datetime(dt.year, dt.month, dt.day, (sh+eh)//2, (sm+em)//2))
                    expiry_dt = ET.localize(datetime(far_dt.year, far_dt.month, far_dt.day, 16, 0))
                    T_far = max((expiry_dt - sample_dt).total_seconds(), 0.0) / (365.0*24*3600.0)
                    best_far, best_dist = float('nan'), float('inf')
                    lo = int(np.floor(anchor - self.strike_band)); hi = int(np.ceil(anchor + self.strike_band))
                    for K in range(lo, hi+1):
                        for side in ['call','put']:
                            try:
                                q = get_polygon_option_quotes(self.underlying, far_dt, float(K), side, dt, dt)
                                if q is None or q.empty:
                                    continue
                                q['ts'] = pd.to_datetime(q.get('timestamp'))
                                q['ts_et'] = q['ts'].dt.tz_convert(ET)
                                qq = q[(q['ts_et'].dt.hour*60 + q['ts_et'].dt.minute >= sh*60+sm) & (q['ts_et'].dt.hour*60 + q['ts_et'].dt.minute <= eh*60+em)].copy()
                                if qq.empty:
                                    qq = q.copy()
                                mid = ((qq['bid'].astype(float) + qq['ask'].astype(float))/2.0).replace([np.inf,-np.inf], np.nan).dropna()
                                if mid.empty or T_far <= 0:
                                    continue
                                price = float(mid.median())
                                ivf = implied_vol_newton(S=float(anchor), K=float(K), T=T_far, price=price, option_type=side)
                                if not np.isfinite(ivf) or ivf <= 0:
                                    continue
                                dist = abs(float(K) - float(anchor))
                                if dist < best_dist:
                                    best_dist, best_far = dist, float(ivf)
                            except Exception:
                                continue
                    iv_far = best_far
                else:
                    near = get_polygon_option_chain_snapshot(self.underlying, dt)
                    far_dt = dt + timedelta(days=self.days_fwd)
                    far = get_polygon_option_chain_snapshot(self.underlying, far_dt)
                    if (near is None or near.empty) or (far is None or far.empty):
                        values.append(float('nan'))
                        continue
                    iv_near = self._atm_iv(near, anchor)
                    iv_far = self._atm_iv(far, anchor)
                if np.isnan(iv_near) or np.isnan(iv_far):
                    values.append(float('nan'))
                else:
                    values.append(iv_far - iv_near)
            except Exception:
                values.append(float('nan'))
        out['iv_term_slope'] = pd.Series(values, index=df.index).astype(float)
        return out
