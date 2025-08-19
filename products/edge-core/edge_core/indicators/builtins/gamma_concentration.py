from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class GammaConcentration(Indicator):
    NAME = "gamma_concentration"
    CATEGORY = "options_structure"
    SUBCATEGORY = "gamma_peaks"

    def __init__(self, underlying: str = 'SPY', top_n: int = 5):
        self.underlying = underlying
        self.top_n = int(top_n)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"gamma_concentration_{self.top_n}"] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        uniq = sorted(set(dts))
        vals = {}
        for d in uniq:
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, d)
                if snap is None or snap.empty or 'gamma' not in snap.columns:
                    vals[d] = np.nan
                    continue
                s = snap.copy()
                g = pd.to_numeric(s['gamma'], errors='coerce').abs().fillna(0.0)
                oi = pd.to_numeric(s.get('open_interest', 0.0), errors='coerce').fillna(0.0)
                s['_g_oi'] = g * oi
                grp = s.groupby('strike')['_g_oi'].sum().sort_values(ascending=False)
                top = grp.head(self.top_n)
                tot = float(grp.sum())
                if tot <= 0:
                    vals[d] = np.nan
                else:
                    shares = (top / tot).astype(float)
                    vals[d] = float((shares * shares).sum())
            except Exception:
                vals[d] = np.nan
        out[f"gamma_concentration_{self.top_n}"] = dts.map(lambda d: vals.get(d, np.nan)).astype(float)
        return out

