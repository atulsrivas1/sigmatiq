from ..base import Indicator
import pandas as pd

class Momentum(Indicator):
    CATEGORY = "price_trend"
    SUBCATEGORY = "momentum"
    def __init__(self, column: str = "close", window: int = 1):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame()
        if self.column in df.columns:
            out[f"close_mom_{self.window}"] = df[self.column].astype(float).pct_change(self.window).fillna(0.0)
        else:
            out[f"close_mom_{self.window}"] = 0.0
        return out
