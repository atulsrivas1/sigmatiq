from ..base import Indicator
import pandas as pd
import numpy as np


class ROC(Indicator):
    NAME = "roc"
    CATEGORY = "price"
    SUBCATEGORY = "momentum"

    def __init__(self, column: str = "close", window: int = 10):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"roc_{self.window}"] = float('nan')
            return out
        s = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        out[f"roc_{self.window}"] = (s / s.shift(self.window) - 1.0) * 100.0
        return out

