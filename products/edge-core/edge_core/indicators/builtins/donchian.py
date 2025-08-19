from ..base import Indicator
import pandas as pd
import numpy as np


class DonchianChannels(Indicator):
    NAME = "donchian"
    CATEGORY = "price"
    SUBCATEGORY = "channels"

    def __init__(self, window: int = 20):
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low'}
        if not req.issubset(df.columns):
            out[f"donchian_upper_{self.window}"] = float('nan')
            out[f"donchian_lower_{self.window}"] = float('nan')
            out[f"donchian_mid_{self.window}"] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        upper = h.rolling(self.window, min_periods=max(1, self.window//2)).max()
        lower = l.rolling(self.window, min_periods=max(1, self.window//2)).min()
        mid = (upper + lower) / 2.0
        out[f"donchian_upper_{self.window}"] = upper
        out[f"donchian_lower_{self.window}"] = lower
        out[f"donchian_mid_{self.window}"] = mid
        return out

