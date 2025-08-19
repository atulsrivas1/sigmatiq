from ..base import Indicator
import pandas as pd
import numpy as np
from ...data.sources.polygon import get_polygon_option_chain_snapshot


class OITrend(Indicator):
    NAME = "oi_trend"
    CATEGORY = "options_flow"
    SUBCATEGORY = "open_interest"

    def __init__(self, underlying: str = 'SPY', window: int = 5):
        self.underlying = underlying
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'date' not in df.columns:
            out[f"oi_trend_{self.window}"] = float('nan')
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
        # build series and compute rolling ema trend (slope-like): current - ema(window)
        s = pd.Series({d: totals.get(d, np.nan) for d in uniq}).sort_index()
        ema = s.ewm(span=self.window, adjust=False).mean()
        trend = (s - ema).to_dict()
        out[f"oi_trend_{self.window}"] = dts.map(lambda d: trend.get(d, np.nan)).astype(float)
        return out

