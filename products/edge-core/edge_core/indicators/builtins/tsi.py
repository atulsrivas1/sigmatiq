from ..base import Indicator
import pandas as pd
import numpy as np


class TSI(Indicator):
    NAME = "tsi"
    CATEGORY = "price"
    SUBCATEGORY = "momentum"

    def __init__(self, column: str = "close", r: int = 25, s: int = 13):
        self.column = column
        self.r = int(r)
        self.s = int(s)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"tsi_{self.r}_{self.s}"] = float('nan')
            return out
        p = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        m = p.diff()
        ema1 = m.ewm(span=self.r, adjust=False).mean()
        ema2 = ema1.ewm(span=self.s, adjust=False).mean()
        absm = m.abs()
        ema1d = absm.ewm(span=self.r, adjust=False).mean()
        ema2d = ema1d.ewm(span=self.s, adjust=False).mean()
        tsi = 100.0 * (ema2 / ema2d.replace(0.0, np.nan))
        out[f"tsi_{self.r}_{self.s}"] = tsi
        return out

