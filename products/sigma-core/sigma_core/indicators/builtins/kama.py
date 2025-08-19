from ..base import Indicator
import pandas as pd
import numpy as np


class KAMA(Indicator):
    NAME = "kama"
    CATEGORY = "price"
    SUBCATEGORY = "moving_average"

    def __init__(self, column: str = "close", er_period: int = 10, fast: int = 2, slow: int = 30):
        self.column = column
        self.er_period = int(er_period)
        self.fast = int(fast)
        self.slow = int(slow)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"kama_{self.er_period}_{self.fast}_{self.slow}"] = float('nan')
            return out
        price = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        change = price.diff(self.er_period).abs()
        volatility = price.diff().abs().rolling(self.er_period).sum()
        er = (change / volatility).replace([np.inf, -np.inf], np.nan).fillna(0.0)
        sc_fast = 2.0 / (self.fast + 1.0)
        sc_slow = 2.0 / (self.slow + 1.0)
        sc = (er * (sc_fast - sc_slow) + sc_slow) ** 2
        kama = price.copy()
        # Initialize with first valid price
        first = price.first_valid_index()
        if first is None:
            out[f"kama_{self.er_period}_{self.fast}_{self.slow}"] = float('nan')
            return out
        kama.iloc[: price.index.get_loc(first) + 1] = price.iloc[price.index.get_loc(first)]
        for i in range(price.index.get_loc(first) + 1, len(price)):
            p = price.iloc[i]
            k_prev = kama.iloc[i - 1]
            s = sc.iloc[i] if np.isfinite(sc.iloc[i]) else sc_slow**2
            kama.iloc[i] = k_prev + s * (p - k_prev)
        out[f"kama_{self.er_period}_{self.fast}_{self.slow}"] = kama
        return out

