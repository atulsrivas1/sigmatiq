from ..base import Indicator
import pandas as pd

class EmaSlope(Indicator):
    CATEGORY = "moving_average"
    SUBCATEGORY = "slope"
    """Slope (first difference over period) of EMA.
    Params: column: str='close', window: int=10, period: int=1
    Output: ema{window}_slope{period}h
    """
    def __init__(self, column: str = "close", window: int = 10, period: int = 1):
        self.column = column
        self.window = int(window)
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        colname = f"ema_{self.window}"
        if colname in df.columns:
            ema = df[colname].astype(float)
        elif self.column in df.columns:
            ema = df[self.column].astype(float).ewm(span=self.window, adjust=False).mean()
        else:
            out[f"ema{self.window}_slope{self.period}h"] = 0.0
            return out
        slope = ema.diff(self.period)
        out[f"ema{self.window}_slope{self.period}h"] = slope.fillna(0.0)
        return out
