from ..base import Indicator
import pandas as pd
import numpy as np


class MFI(Indicator):
    NAME = "mfi"
    CATEGORY = "volume"
    SUBCATEGORY = "money_flow"

    def __init__(self, period: int = 14):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close','volume'}
        if not req.issubset(df.columns):
            out[f"mfi_{self.period}"] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        c = pd.to_numeric(df['close'], errors='coerce').astype(float)
        v = pd.to_numeric(df['volume'], errors='coerce').astype(float)
        tp = (h + l + c) / 3.0
        rmf = tp * v
        prev_tp = tp.shift(1)
        pos_flow = rmf.where(tp > prev_tp, 0.0)
        neg_flow = rmf.where(tp < prev_tp, 0.0)
        pos_sum = pos_flow.rolling(self.period, min_periods=max(1, self.period//2)).sum()
        neg_sum = neg_flow.rolling(self.period, min_periods=max(1, self.period//2)).sum()
        neg_sum = neg_sum.replace(0.0, np.nan)
        mr = pos_sum / neg_sum
        mfi = 100.0 - (100.0 / (1.0 + mr))
        out[f"mfi_{self.period}"] = mfi.fillna(method='bfill')
        return out

