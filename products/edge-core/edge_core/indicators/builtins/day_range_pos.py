from ..base import Indicator
import pandas as pd
import numpy as np


class DayRangePos(Indicator):
    NAME = "day_range_pos"
    CATEGORY = "intraday"
    SUBCATEGORY = "session_range"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close','date'}
        if not req.issubset(df.columns):
            out['day_range_pos'] = float('nan')
            return out
        x = df.copy()
        x['d'] = pd.to_datetime(x['date']).dt.tz_convert('US/Eastern').dt.date
        daily_high = x.groupby('d')['high'].transform('max')
        daily_low = x.groupby('d')['low'].transform('min')
        close = pd.to_numeric(x['close'], errors='coerce').astype(float)
        rng = (pd.to_numeric(daily_high, errors='coerce').astype(float) - pd.to_numeric(daily_low, errors='coerce').astype(float)).replace(0.0, np.nan)
        out['day_range_pos'] = (close - pd.to_numeric(daily_low, errors='coerce').astype(float)) / rng
        return out

