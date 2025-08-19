from ..base import Indicator
import pandas as pd

class Ret(Indicator):
    CATEGORY = "price_trend"
    SUBCATEGORY = "returns"
    """Return over N periods (pct change).
    Params: column: str='close', window: int=1
    Output: ret_{window}h
    """
    def __init__(self, column: str = "close", window: int = 1):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"ret_{self.window}h"] = 0.0
            return out
        ret = df[self.column].astype(float).pct_change(self.window).fillna(0.0)
        out[f"ret_{self.window}h"] = ret
        return out
