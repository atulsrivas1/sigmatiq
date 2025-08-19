from ..base import Indicator
import pandas as pd
import numpy as np


class DPO(Indicator):
    NAME = "dpo"
    CATEGORY = "price"
    SUBCATEGORY = "detrended"

    def __init__(self, column: str = "close", period: int = 20):
        self.column = column
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"dpo_{self.period}"] = float('nan')
            return out
        s = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        sma = s.rolling(self.period, min_periods=max(1, self.period//2)).mean()
        shift = int(np.floor(self.period / 2.0) + 1)
        dpo = s - sma.shift(shift)
        out[f"dpo_{self.period}"] = dpo
        return out

