from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class GammaDensityPeakStrike(Indicator):
    NAME = "gamma_density_peak_strike"
    CATEGORY = "options_structure"
    SUBCATEGORY = "gamma_density"

    def __init__(self, underlying: str = 'SPY'):
        self.underlying = underlying

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['gamma_density_peak_strike'] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        uniq = sorted(set(dts))
        peak = {}
        for d in uniq:
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, d)
                if snap is None or snap.empty or 'gamma' not in snap.columns:
                    peak[d] = np.nan
                    continue
                s = snap.copy()
                g = pd.to_numeric(s['gamma'], errors='coerce').abs().fillna(0.0)
                oi = pd.to_numeric(s.get('open_interest', 0.0), errors='coerce').fillna(0.0)
                s['_g_oi'] = g * oi
                grp = s.groupby('strike')['_g_oi'].sum()
                peak[d] = (float(grp.idxmax()) if not grp.empty else np.nan)
            except Exception:
                peak[d] = np.nan
        out['gamma_density_peak_strike'] = dts.map(lambda d: peak.get(d, np.nan)).astype(float)
        return out


class GammaSkewLeftRight(Indicator):
    NAME = "gamma_skew_left_right"
    CATEGORY = "options_structure"
    SUBCATEGORY = "gamma_density"

    def __init__(self, underlying: str = 'SPY', spot_col: str = 'close'):
        self.underlying = underlying
        self.spot_col = spot_col

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns or self.spot_col not in df.columns:
            out['gamma_skew_left_right'] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        uniq = sorted(set(dts))
        # create a map of density per day by strike for efficiency
        density = {}
        for d in uniq:
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, d)
                if snap is None or snap.empty or 'gamma' not in snap.columns:
                    density[d] = None
                    continue
                s = snap.copy()
                g = pd.to_numeric(s['gamma'], errors='coerce').abs().fillna(0.0)
                oi = pd.to_numeric(s.get('open_interest', 0.0), errors='coerce').fillna(0.0)
                s['_g_oi'] = g * oi
                grp = s.groupby('strike')['_g_oi'].sum()
                density[d] = grp
            except Exception:
                density[d] = None
        spot = pd.to_numeric(df[self.spot_col], errors='coerce').astype(float)
        vals = []
        for idx in df.index:
            d = pd.to_datetime(df.loc[idx, 'date']).date()
            grp = density.get(d)
            if grp is None or grp.empty:
                vals.append(np.nan); continue
            spt = float(spot.loc[idx]) if np.isfinite(spot.loc[idx]) else np.nan
            if not np.isfinite(spt):
                vals.append(np.nan); continue
            left = float(grp[grp.index.astype(float) < spt].sum())
            right = float(grp[grp.index.astype(float) > spt].sum())
            denom = right + left + 1e-9
            vals.append((right - left) / denom)
        out['gamma_skew_left_right'] = pd.Series(vals, index=df.index).astype(float)
        return out

