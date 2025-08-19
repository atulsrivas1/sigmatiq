from ..base import Indicator
import pandas as pd
import numpy as np


class Aroon(Indicator):
    NAME = "aroon"
    CATEGORY = "price"
    SUBCATEGORY = "trend"

    def __init__(self, period: int = 25):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low'}
        if not req.issubset(df.columns):
            out[f"aroon_up_{self.period}"] = float('nan')
            out[f"aroon_down_{self.period}"] = float('nan')
            out[f"aroon_osc_{self.period}"] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        period = self.period

        # Index of most recent max/min within rolling window
        roll_high_idx = h.rolling(period).apply(lambda s: period - 1 - int(s.values[::-1].argmax()), raw=False)
        roll_low_idx = l.rolling(period).apply(lambda s: period - 1 - int(s.values[::-1].argmin()), raw=False)
        aroon_up = 100.0 * (period - roll_high_idx) / period
        aroon_down = 100.0 * (period - roll_low_idx) / period
        out[f"aroon_up_{period}"] = aroon_up
        out[f"aroon_down_{period}"] = aroon_down
        out[f"aroon_osc_{period}"] = (aroon_up - aroon_down)
        return out

