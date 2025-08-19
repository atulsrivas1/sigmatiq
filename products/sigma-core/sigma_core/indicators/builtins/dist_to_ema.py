from ..base import Indicator
import pandas as pd

class DistToEma(Indicator):
    CATEGORY = "moving_average"
    SUBCATEGORY = "distance"
    """Normalized distance of price to EMA.
    Params: column: str='close', window: int=10, normalize: str='price' (price|ema)
    Output: dist_ema{window}_norm
    """
    def __init__(self, column: str = "close", window: int = 10, normalize: str = "price"):
        self.column = column
        self.window = int(window)
        self.normalize = normalize

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.column not in df.columns:
            out[f"dist_ema{self.window}_norm"] = 0.0
            return out
        price = df[self.column].astype(float)
        ema = price.ewm(span=self.window, adjust=False).mean()
        denom = price.abs() if self.normalize == "price" else ema.abs()
        dist = (price - ema) / (denom + 1e-12)
        out[f"dist_ema{self.window}_norm"] = dist.fillna(0.0)
        return out
