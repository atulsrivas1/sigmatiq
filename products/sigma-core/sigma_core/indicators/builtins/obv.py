from ..base import Indicator
import pandas as pd

class OBV(Indicator):
    CATEGORY = "volume"
    SUBCATEGORY = "obv"

    def __init__(self, price_col: str = 'close', volume_col: str = 'volume'):
        self.price_col = price_col
        self.volume_col = volume_col

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        if self.price_col not in df.columns or self.volume_col not in df.columns:
            out['obv'] = 0.0
            return out
        price = pd.to_numeric(df[self.price_col], errors='coerce').astype(float)
        vol = pd.to_numeric(df[self.volume_col], errors='coerce').astype(float).fillna(0.0)
        sign = (price.diff().fillna(0.0)).apply(lambda x: 1.0 if x > 0 else (-1.0 if x < 0 else 0.0))
        obv = (vol * sign).cumsum()
        out['obv'] = obv.fillna(0.0)
        return out

