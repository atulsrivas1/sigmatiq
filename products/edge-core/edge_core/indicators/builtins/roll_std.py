from ..base import Indicator
import pandas as pd

class RollingStd(Indicator):
    CATEGORY = "volatility"
    SUBCATEGORY = "rolling_std"
    """Rolling standard deviation of returns.
    Params: column: str='close', window: int=20
    Output: roll_std_{window}
    """
    def __init__(self, column: str = "close", window: int = 20):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"roll_std_{self.window}"] = 0.0
            return out
        ret = df[self.column].astype(float).pct_change().fillna(0.0)
        rs = ret.rolling(self.window).std().fillna(0.0)
        out[f"roll_std_{self.window}"] = rs
        return out
