from ..base import Indicator
import pandas as pd
import numpy as np


class SuperTrend(Indicator):
    NAME = "supertrend"
    CATEGORY = "price"
    SUBCATEGORY = "trend"

    def __init__(self, period: int = 10, multiplier: float = 3.0):
        self.period = int(period)
        self.multiplier = float(multiplier)

    def _atr(self, h: pd.Series, l: pd.Series, c: pd.Series, period: int) -> pd.Series:
        prev_c = c.shift(1)
        tr1 = h - l
        tr2 = (h - prev_c).abs()
        tr3 = (l - prev_c).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(period, min_periods=max(1, period//2)).mean()

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        req = {'high','low','close'}
        if not req.issubset(df.columns):
            out['supertrend'] = float('nan')
            out['supertrend_dir'] = float('nan')
            return out
        h = pd.to_numeric(df['high'], errors='coerce').astype(float)
        l = pd.to_numeric(df['low'], errors='coerce').astype(float)
        c = pd.to_numeric(df['close'], errors='coerce').astype(float)
        atr = self._atr(h, l, c, self.period)
        hl2 = (h + l) / 2.0
        upper_basic = hl2 + self.multiplier * atr
        lower_basic = hl2 - self.multiplier * atr

        upper = upper_basic.copy()
        lower = lower_basic.copy()
        n = len(c)
        for i in range(1, n):
            upper.iloc[i] = min(upper_basic.iloc[i], upper.iloc[i-1]) if c.iloc[i-1] > upper.iloc[i-1] else upper_basic.iloc[i]
            lower.iloc[i] = max(lower_basic.iloc[i], lower.iloc[i-1]) if c.iloc[i-1] < lower.iloc[i-1] else lower_basic.iloc[i]

        st = pd.Series(index=df.index, dtype=float)
        direction = pd.Series(index=df.index, dtype=float)
        # Initialize
        st.iloc[0] = upper.iloc[0]
        direction.iloc[0] = 1.0
        for i in range(1, n):
            if st.iloc[i-1] == upper.iloc[i-1]:
                st.iloc[i] = lower.iloc[i] if c.iloc[i] > upper.iloc[i] else upper.iloc[i]
            else:
                st.iloc[i] = upper.iloc[i] if c.iloc[i] < lower.iloc[i] else lower.iloc[i]
            direction.iloc[i] = 1.0 if c.iloc[i] >= st.iloc[i] else -1.0

        out['supertrend'] = st
        out['supertrend_dir'] = direction
        return out

