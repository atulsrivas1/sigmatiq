from ..base import Indicator
import pandas as pd
import numpy as np


class LRR2(Indicator):
    NAME = "lr_r2"
    CATEGORY = "trend"
    SUBCATEGORY = "quality"

    def __init__(self, column: str = 'close', window: int = 126):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"lr_r2_{self.window}"] = float('nan')
            return out
        s = pd.to_numeric(df[self.column], errors='coerce').astype(float)
        # rolling R^2 between time index (0..n-1) and s
        x = pd.Series(range(len(s)), index=s.index).astype(float)
        def r2_win(y):
            xi = np.arange(len(y), dtype=float)
            if len(y) < 2 or np.allclose(y, y[0]):
                return np.nan
            corr = np.corrcoef(xi, y)[0,1]
            return corr*corr
        r2 = s.rolling(self.window).apply(r2_win, raw=False)
        out[f"lr_r2_{self.window}"] = r2
        return out

