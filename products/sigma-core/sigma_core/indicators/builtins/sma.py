from ..base import Indicator
import pandas as pd
import numpy as np


class SMA(Indicator):
    NAME = "sma"
    CATEGORY = "price"
    SUBCATEGORY = "moving_average"

    def __init__(self, column: str = "close", window: int = 20):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"sma_{self.window}"] = float('nan')
            return out
        s = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        out[f"sma_{self.window}"] = s.rolling(self.window, min_periods=max(1, self.window//2)).mean()
        return out

