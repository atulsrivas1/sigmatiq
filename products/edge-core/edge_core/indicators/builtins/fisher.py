from ..base import Indicator
import pandas as pd
import numpy as np

class FisherTransform(Indicator):
    CATEGORY = "oscillator"
    SUBCATEGORY = "fisher"

    def __init__(self, period: int = 9):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"high", "low"}
        if not required.issubset(df.columns):
            out[f"fisher_{self.period}"] = 0.0
            return out
        high = pd.to_numeric(df['high'], errors='coerce').astype(float)
        low = pd.to_numeric(df['low'], errors='coerce').astype(float)
        hl2 = (high + low) / 2.0
        min_l = hl2.rolling(self.period).min()
        max_h = hl2.rolling(self.period).max()
        x = 2.0 * ((hl2 - min_l) / (max_h - min_l + 1e-12)) - 1.0
        x = x.ewm(alpha=0.33, adjust=False).mean()
        x = x.clip(-0.999, 0.999)
        fisher = 0.5 * (np.log((1 + x) / (1 - x + 1e-12)))
        out[f"fisher_{self.period}"] = fisher.fillna(0.0)
        return out

