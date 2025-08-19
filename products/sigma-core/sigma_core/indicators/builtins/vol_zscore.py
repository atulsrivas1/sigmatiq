from ..base import Indicator
import pandas as pd
import numpy as np


class VolumeZScore(Indicator):
    NAME = "vol_zscore"
    CATEGORY = "volume"
    SUBCATEGORY = "zscore"

    def __init__(self, window: int = 20):
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if 'volume' not in df.columns:
            out[f"vol_zscore_{self.window}"] = float('nan')
            return out
        v = pd.to_numeric(df['volume'], errors='coerce').astype(float)
        mean = v.rolling(self.window, min_periods=max(1, self.window//2)).mean()
        std = v.rolling(self.window, min_periods=max(1, self.window//2)).std()
        z = (v - mean) / std.replace(0.0, np.nan)
        out[f"vol_zscore_{self.window}"] = z
        return out

