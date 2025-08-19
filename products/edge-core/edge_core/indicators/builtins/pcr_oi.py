from ..base import Indicator
import pandas as pd
import numpy as np
from datetime import date
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class PCROI(Indicator):
    NAME = "pcr_oi"
    CATEGORY = "options_flow"
    SUBCATEGORY = "ratios"

    def __init__(self, underlying: str = 'SPY'):
        self.underlying = underlying

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out['pcr_oi'] = float('nan')
            return out
        dts = pd.to_datetime(df['date']).dt.date
        unique_days = sorted(set(dts))
        ratios = {}
        for d in unique_days:
            try:
                snap = get_polygon_option_chain_snapshot(self.underlying, d)
            except Exception:
                snap = pd.DataFrame()
            if snap is None or snap.empty:
                ratios[d] = np.nan
                continue
            try:
                s = snap.copy()
                s['side'] = s['contract_type'].astype(str).str.lower()
                agg = s.groupby('side')['open_interest'].sum()
                p = float(agg.get('put', 0.0))
                c = float(agg.get('call', 0.0))
                ratios[d] = (p + 1e-9) / (c + 1e-9)
            except Exception:
                ratios[d] = np.nan
        out['pcr_oi'] = dts.map(lambda d: ratios.get(d, np.nan)).astype(float)
        return out

