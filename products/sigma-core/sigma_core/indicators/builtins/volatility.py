from ..base import Indicator
import pandas as pd

class Volatility(Indicator):
    CATEGORY = "volatility"
    SUBCATEGORY = "realized"
    def __init__(self, column: str = "close", window: int = 3):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        if self.column in df.columns:
            ret = df[self.column].astype(float).pct_change().fillna(0.0)
            out[f"close_vol_{self.window}"] = ret.rolling(self.window).std().fillna(0.0)
        else:
            out[f"close_vol_{self.window}"] = 0.0
        return out
