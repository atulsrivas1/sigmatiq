from ..base import Indicator
import pandas as pd
import numpy as np


class TRIX(Indicator):
    NAME = "trix"
    CATEGORY = "price"
    SUBCATEGORY = "momentum"

    def __init__(self, column: str = "close", period: int = 15):
        self.column = column
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"trix_{self.period}"] = float('nan')
            return out
        s = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        e1 = s.ewm(span=self.period, adjust=False).mean()
        e2 = e1.ewm(span=self.period, adjust=False).mean()
        e3 = e2.ewm(span=self.period, adjust=False).mean()
        trix = (e3.diff() / e3.shift(1)) * 100.0
        out[f"trix_{self.period}"] = trix
        return out

