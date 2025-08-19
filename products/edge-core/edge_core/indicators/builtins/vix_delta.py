from ..base import Indicator
import pandas as pd
import numpy as np
from ...indicators.builtins.vix_level import VIXLevel


class VIXDelta(Indicator):
    NAME = "vix_delta"
    CATEGORY = "regime"
    SUBCATEGORY = "vix"

    def __init__(self):
        pass

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        lvl = VIXLevel().calculate(df)
        s = pd.to_numeric(lvl.get('vix_level', pd.Series(index=df.index)), errors='coerce')
        # Map by date; compute daily diff then align back to rows by date
        if 'date' not in df.columns:
            out['vix_delta'] = float('nan')
            return out
        dates = pd.to_datetime(df['date']).dt.tz_convert('US/Eastern').dt.date
        # build per-day series
        per_day = pd.Series(index=pd.Index(sorted(set(dates)), name='d'), dtype=float)
        # use first non-nan value per day
        tmp = pd.DataFrame({'d': dates, 'v': s}).dropna()
        first = tmp.groupby('d')['v'].first()
        diff = first.diff().to_dict()
        out['vix_delta'] = dates.map(lambda d: diff.get(d, np.nan)).astype(float)
        return out

