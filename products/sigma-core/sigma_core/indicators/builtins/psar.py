from ..base import Indicator
import pandas as pd
import numpy as np


class PSAR(Indicator):
    NAME = "psar"
    CATEGORY = "price"
    SUBCATEGORY = "trend"

    def __init__(self, step: float = 0.02, max_step: float = 0.2):
        self.step = float(step)
        self.max_step = float(max_step)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close'}
        if not req.issubset(df.columns):
            out['psar'] = float('nan')
            return out
        high = pd.to_numeric(df['high'], errors='coerce').astype(float).values
        low = pd.to_numeric(df['low'], errors='coerce').astype(float).values
        n = len(high)
        if n == 0:
            out['psar'] = []
            return out

        psar = np.zeros(n)
        bull = True  # start with uptrend by default
        af = self.step
        ep = high[0]
        psar[0] = low[0]

        for i in range(1, n):
            prev_psar = psar[i-1]
            if bull:
                psar[i] = prev_psar + af * (ep - prev_psar)
                psar[i] = min(psar[i], low[i-1])
                if i >= 2:
                    psar[i] = min(psar[i], low[i-2])
                if high[i] > ep:
                    ep = high[i]
                    af = min(af + self.step, self.max_step)
                if low[i] < psar[i]:
                    bull = False
                    psar[i] = ep
                    ep = low[i]
                    af = self.step
            else:
                psar[i] = prev_psar + af * (ep - prev_psar)
                psar[i] = max(psar[i], high[i-1])
                if i >= 2:
                    psar[i] = max(psar[i], high[i-2])
                if low[i] < ep:
                    ep = low[i]
                    af = min(af + self.step, self.max_step)
                if high[i] > psar[i]:
                    bull = True
                    psar[i] = ep
                    ep = high[i]
                    af = self.step

        out['psar'] = pd.Series(psar, index=df.index)
        return out

