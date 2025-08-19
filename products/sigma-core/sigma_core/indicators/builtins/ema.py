from ..base import Indicator
import pandas as pd

class EMA(Indicator):
    CATEGORY = "moving_average"
    SUBCATEGORY = "ema"
    """Exponential moving average.
    Params: column: str = 'close', window: int = 10
    Output: ema_{window}
    """
    def __init__(self, column: str = "close", window: int = 10):
        self.column = column
        self.window = int(window)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"ema_{self.window}"] = 0.0
            return out
        ema = df[self.column].astype(float).ewm(span=self.window, adjust=False).mean()
        out[f"ema_{self.window}"] = ema.fillna(0.0)
        return out
