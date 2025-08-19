from ..base import Indicator
import pandas as pd
import numpy as np


class UltimateOscillator(Indicator):
    NAME = "ultimate_oscillator"
    CATEGORY = "price"
    SUBCATEGORY = "momentum"

    def __init__(self, short: int = 7, mid: int = 14, long: int = 28):
        self.short = int(short)
        self.mid = int(mid)
        self.long = int(long)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close'}
        if not req.issubset(df.columns):
            out['ultimate_osc'] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        c = pd.to_numeric(df['close'], errors='coerce').astype(float)
        prev_c = c.shift(1)
        bp = c - pd.concat([l, prev_c], axis=1).min(axis=1)
        tr = pd.concat([h, prev_c], axis=1).max(axis=1) - pd.concat([l, prev_c], axis=1).min(axis=1)
        def avg_ratio(period: int):
            sum_bp = bp.rolling(period).sum()
            sum_tr = tr.rolling(period).sum().replace(0.0, np.nan)
            return sum_bp / sum_tr
        a1 = avg_ratio(self.short)
        a2 = avg_ratio(self.mid)
        a3 = avg_ratio(self.long)
        uo = 100.0 * (4*a1 + 2*a2 + a3) / 7.0
        out['ultimate_osc'] = uo
        return out

