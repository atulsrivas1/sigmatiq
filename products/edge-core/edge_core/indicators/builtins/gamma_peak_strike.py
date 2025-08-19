from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class GammaPeakStrike(Indicator):
    NAME = "gamma_peak_strike"
    CATEGORY = "options_structure"
    SUBCATEGORY = "gamma_peaks"

    def __init__(self, underlying: str = 'SPY'):
        self.underlying = underlying

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['gamma_peak_strike'] = float('nan')
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
                # proxy: sum |gamma| * OI by strike
                try:
                    g = pd.to_numeric(s['gamma'], errors='coerce').abs()
                except Exception:
                    peak[d] = np.nan; continue
                oi = pd.to_numeric(s.get('open_interest', 0.0), errors='coerce').fillna(0.0)
                s['_g_oi'] = g * oi
                grp = s.groupby('strike')['_g_oi'].sum()
                if grp.empty:
                    peak[d] = np.nan
                else:
                    peak[d] = float(grp.idxmax())
            except Exception:
                peak[d] = np.nan
        out['gamma_peak_strike'] = dts.map(lambda d: peak.get(d, np.nan)).astype(float)
        return out

