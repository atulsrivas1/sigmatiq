from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class OIPeakStrike(Indicator):
    NAME = "oi_peak_strike"
    CATEGORY = "options_structure"
    SUBCATEGORY = "oi_peaks"

    def __init__(self, underlying: str = 'SPY'):
        self.underlying = underlying

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['oi_peak_strike'] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        uniq = sorted(set(dts))
        peak = {}
        for d in uniq:
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, d)
                if snap is None or snap.empty:
                    peak[d] = np.nan
                    continue
                s = snap.copy()
                grp = s.groupby('strike')['open_interest'].sum()
                if grp.empty:
                    peak[d] = np.nan
                else:
                    peak[d] = float(grp.idxmax())
            except Exception:
                peak[d] = np.nan
        out['oi_peak_strike'] = dts.map(lambda d: peak.get(d, np.nan)).astype(float)
        return out

