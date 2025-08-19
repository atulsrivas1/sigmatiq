from ..base import Indicator
import pandas as pd

class Qstick(Indicator):
    CATEGORY = "price_trend"
    SUBCATEGORY = "qstick"

    def __init__(self, period: int = 10):
        self.period = int(period)

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        required = {"open", "close"}
        if not required.issubset(df.columns):
            out[f"qstick_{self.period}"] = 0.0
            return out
        oc = pd.to_numeric(df['close'], errors='coerce').astype(float) - pd.to_numeric(df['open'], errors='coerce').astype(float)
        q = oc.rolling(self.period).mean()
        out[f"qstick_{self.period}"] = q.fillna(0.0)
        return out

