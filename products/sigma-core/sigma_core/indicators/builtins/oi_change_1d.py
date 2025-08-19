from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class OIChange1D(Indicator):
    NAME = "oi_change_1d"
    CATEGORY = "options_flow"
    SUBCATEGORY = "open_interest"

    def __init__(self, underlying: str = 'SPY'):
        self.underlying = underlying

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['oi_change_1d'] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        uniq = sorted(set(dts))
        totals = {}
        for d in uniq:
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, d)
                if snap is None or snap.empty:
                    totals[d] = np.nan
                    continue
                tot = float(pd.to_numeric(snap.get('open_interest', pd.Series(0.0)), errors='coerce').sum())
                totals[d] = tot
            except Exception:
                totals[d] = np.nan
        # compute change vs prior day
        prev = {}
        last = None
        for d in uniq:
            prev[d] = (None if last is None else totals.get(last, np.nan))
            last = d
        changes = {d: (totals.get(d, np.nan) - (prev[d] if prev[d] is not None else np.nan)) for d in uniq}
        out['oi_change_1d'] = dts.map(lambda d: changes.get(d, np.nan)).astype(float)
        return out

