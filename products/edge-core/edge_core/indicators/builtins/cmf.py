from ..base import Indicator
import pandas as pd
import numpy as np


class CMF(Indicator):
    NAME = "cmf"
    CATEGORY = "volume"
    SUBCATEGORY = "money_flow"

    def __init__(self, period: int = 20):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close','volume'}
        if not req.issubset(df.columns):
            out[f"cmf_{self.period}"] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        c = pd.to_numeric(df['close'], errors='coerce').astype(float)
        v = pd.to_numeric(df['volume'], errors='coerce').astype(float)
        denom = (h - l).replace(0.0, np.nan)
        mfm = ((c - l) - (h - c)) / denom
        mfv = mfm.fillna(0.0) * v
        mfv_sum = mfv.rolling(self.period, min_periods=max(1, self.period//2)).sum()
        vol_sum = v.rolling(self.period, min_periods=max(1, self.period//2)).sum().replace(0.0, np.nan)
        cmf = (mfv_sum / vol_sum).fillna(0.0)
        out[f"cmf_{self.period}"] = cmf
        return out

