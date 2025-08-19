from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class OIConcentrationHHI(Indicator):
    NAME = "oi_concentration_hhi"
    CATEGORY = "options_structure"
    SUBCATEGORY = "concentration"

    def __init__(self, underlying: str = 'SPY', top_n: int = 5):
        self.underlying = underlying
        self.top_n = int(top_n)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"oi_concentration_hhi_{self.top_n}"] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        uniq = sorted(set(dts))
        vals = {}
        for d in uniq:
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, d)
                if snap is None or snap.empty:
                    vals[d] = np.nan
                    continue
                s = snap.copy()
                by_strike = s.groupby('strike')['open_interest'].sum().sort_values(ascending=False)
                top = by_strike.head(self.top_n)
                tot = float(by_strike.sum())
                if tot <= 0:
                    vals[d] = np.nan
                else:
                    shares = (top / tot).astype(float)
                    vals[d] = float((shares * shares).sum())
            except Exception:
                vals[d] = np.nan
        out[f"oi_concentration_hhi_{self.top_n}"] = dts.map(lambda d: vals.get(d, np.nan)).astype(float)
        return out

